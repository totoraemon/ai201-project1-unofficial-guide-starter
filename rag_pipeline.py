import html
import json
import math
import os
import re
import ssl
import urllib.request
from html.parser import HTMLParser
from typing import Dict, List

# ==============================================================================
# PIPELINE CONFIGURATION & ARCHITECTURAL CONSTANTS
# ==============================================================================
RAW_DATA_DIR = "./data/raw_storage"

TARGET_SOURCES = [
    {"id": "src_1", "url": "https://www.misstamchiak.com/ntu/"},
    {"id": "src_2", "url": "https://catharticstudent.wordpress.com/2017/05/18/ntu-life-top-16-best-campus-food-at-ntu/"},
    {"id": "src_3", "url": "https://www.happycow.net/reviews/national-taiwan-university-taipei-61065"},
    {"id": "src_4", "url": "https://en.hshsharehouse.com/top-eats-and-fun-spots-guide-for-ntu-international-students/"},
    {"id": "src_5", "url": "https://thesmartlocal.com/read/ntu-hidden-gems/"},
    {"id": "src_6", "url": "https://www.reddit.com/r/taiwan/comments/1fbqzg9/what_do_college_students_eat_on_a_daily_basis/"},
    {"id": "src_7", "url": "https://www.reddit.com/r/NTU/comments/15ktgd7/best_eateries_on_campus/"},
    {"id": "src_8", "url": "https://www.reddit.com/r/NTU/comments/1b17qxm/food_reviews_and_reccomendations/"},
    {"id": "src_9", "url": "https://www.reddit.com/r/NTU/comments/w0wi4b/list_of_places_to_eat_at_ntu_food/"},
    {"id": "src_10", "url": "https://www.reddit.com/r/taiwan/comments/snpsqo/budgetfriendly_dim_sum_restaurant_attracts_fans/"}
]

# ==============================================================================
# STANDARD LIBRARY HTML STRIPPER
# ==============================================================================
class MLStripper(HTMLParser):
    """
    Custom HTML Parser to strip structural layout tags while ignoring code blocks,
    scripts, headers, and navigation contents.
    """
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text_accumulator = []
        self.ignore_tag_depth = 0
        # Tags we want to completely destroy along with everything inside them
        self.blacklist_tags = {"script", "style", "nav", "footer", "header", "aside", "form"}

    def handle_starttag(self, tag, attrs):
        if tag in self.blacklist_tags:
            self.ignore_tag_depth += 1

    def handle_endtag(self, tag):
        if tag in self.blacklist_tags:
            self.ignore_tag_depth = max(0, self.ignore_tag_depth - 1)

    def handle_data(self, data):
        if self.ignore_tag_depth == 0:
            self.text_accumulator.append(data)

    def get_data(self):
        return "".join(self.text_accumulator)

def strip_tags(html_content: str) -> str:
    s = MLStripper()
    s.feed(html_content)
    return s.get_data()

# ==============================================================================
# PIPELINE STAGE 1: DOCUMENT LOADING & RAW STORAGE (URLLIB)
# ==============================================================================
def load_and_cache_documents(sources: List[Dict]) -> List[Dict]:
    """
    Downloads or reads local raw text using pure urllib with realistic headers
    and an unverified SSL context to bypass macOS local issuer certificate errors.
    """
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    loaded_docs = []

    print("=== STAGE 1: LOADING & CACHING DOCUMENTS (STANDARD LIB) ===")
    for src in sources:
        cache_path = os.path.join(RAW_DATA_DIR, f"{src['id']}.json")
        
        # Check if a valid cache file already exists on disk
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
                # Ensure the cache doesn't just contain an old, broken connection string
                if "CONNECTION_EXCEPTION" not in cached_data["raw_content"]:
                    loaded_docs.append(cached_data)
                    print(f" Loaded from valid disk cache: {src['id']}")
                    continue

        try:
            # Build an aggressive, realistic desktop browser request configuration
            req = urllib.request.Request(
                src['url'], 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
            )
            
            # Create an unverified context to bypass macOS SSL certificate verification barriers
            context = ssl._create_unverified_context()
            
            # Execute the secure request using our unverified context flag
            with urllib.request.urlopen(req, context=context, timeout=15) as response:
                raw_text = response.read().decode('utf-8', errors='ignore')
                print(f" Successfully downloaded: {src['id']}")
                
        except Exception as e:
            raw_text = f"CONNECTION_EXCEPTION: {str(e)}"
            print(f" [FAILED] Could not fetch {src['id']}. Error: {str(e)}")

        # Structure the data into a standard JSON payload format
        doc_payload = {
            "source_id": src["id"],
            "source_url": src["url"],
            "raw_content": raw_text
        }
        
        # Save payload to disk to prevent redundant hitting of web endpoints
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(doc_payload, f, ensure_ascii=False, indent=4)
            
        loaded_docs.append(doc_payload)
        
    return loaded_docs

# ==============================================================================
# PIPELINE STAGE 2: ADAPTED DOMAIN CLEANING ENGINE
# ==============================================================================
def clean_document_text(raw_html_or_text: str) -> str:
    """
    An aggressive cleaning engine that strip-mines HTML layouts, purges site navbars,
    filters out non-dining related noise, and rejects anti-bot blocking screens.
    """
    if not raw_html_or_text or "CONNECTION_EXCEPTION" in raw_html_or_text:
        return ""

    # 1. HARD BLOCK: Detect Cloudflare / Reddit Anti-Bot Verification walls
    if "please wait for verification" in raw_html_or_text.lower() or "checking your browser" in raw_html_or_text.lower():
        return ""

    # 2. Extract visible text fragments using our standard HTML parser
    text = strip_tags(raw_html_or_text)
    text = html.unescape(text)

    # 3. PURGE: Target-rich web navigation boilerplates & layout artifacts
    site_clutter_patterns = [
        r'(?i)(advertise with us|about us|recipes|travel|shop|contact us|categories|subscribe to our telegram|share on facebook|twitter|read more|comment count|all rights reserved)',
        r'(?i)(hawker|restaurant|cuisine|chinese|european|indian|international|japanese|korean|malay|thai)\b(?:\s*\|?\s*)*', 
        r'Home\s*>\s*[^>\n]+' 
    ]
    for pattern in site_clutter_patterns:
        text = re.sub(pattern, '', text)

    # 4. FILTER: Split into paragraphs and drop structural noise that lacks food context
    paragraphs = text.split('\n')
    cleaned_paragraphs = []
    
    food_keywords = re.compile(r'(?i)(food|dining|canteen|stall|eat|menu|price|bento|noodle|rice|curry|budget|spend|dish|delicious|queue|taste|lunch|dinner|breakfast)')

    for para in paragraphs:
        para_clean = para.strip()
        if len(para_clean) > 25 and food_keywords.search(para_clean):
            cleaned_paragraphs.append(para_clean)

    final_text = "\n".join(cleaned_paragraphs)
    final_text = re.sub(r'[ \t]+', ' ', final_text)
    
    return final_text.strip()

# ==============================================================================
# PIPELINE STAGE 3: METADATA-AWARE STRATEGIC CHUNKING WITH QUALITY SCORING
# ==============================================================================
def chunk_text(cleaned_text: str, source_id: str, source_url: str) -> List[Dict]:
    """
    Segments text into precise chunks by evaluating sentences individually.
    Drops trailing notes/parentheses and media footer links before building chunks.
    """
    chunks = []
    TARGET_CHUNK_SIZE = 400
    
    derived_campus_context = "Campus Dining Hub"
    if "ntu" in source_url.lower():
        derived_campus_context = "NTU Campus Dining Ecosystem"
    elif "taiwan" in source_url.lower():
        derived_campus_context = "Taiwan University Community Dining"

    substantive_keywords = re.compile(r'(\$\d+|\d+\s*NTD|stall|canteen|menu|ordered|recommend|taste|price|noodles|rice|curry|chicken|bento|queue|wait time)', re.IGNORECASE)
    noise_signals = ["written by", "july 29", "august", "september", "insect farm", "wholesale market", "subscriber", "advertisement", "read more", "related articles"]

    # Split the document into individual sentences cleanly
    sentences = re.split(r'(?<=[.!?])\s+', cleaned_text)
    
    current_chunk_sentences = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        sentence_lower = sentence.lower()
        
        # 1. SENTENCE-LEVEL FILTER: Instantly drop any line containing media footer links
        if any(signal in sentence_lower for signal in noise_signals):
            continue
            
        # 2. FRAGMENT FILTER: Drop isolated trailing shorthand or unfinished parentheses blocks
        if sentence.endswith('(') or sentence_lower.endswith('(p.s.') or sentence_lower.endswith('p.s.'):
            continue

        current_chunk_sentences.append(sentence)
        current_length += len(sentence) + 1
        
        # Once the target length is met, check the overall content quality
        if current_length >= TARGET_CHUNK_SIZE:
            raw_segment = " ".join(current_chunk_sentences)
            
            if substantive_keywords.search(raw_segment.lower()):
                context_header = f"[Source: {source_id} | Context: {derived_campus_context}] "
                
                chunks.append({
                    "chunk_id": f"{source_id}_chk_{len(chunks)}",
                    "chunk_text": context_header + raw_segment,
                    "metadata": {
                        "source_url": source_url,
                        "parent_scope": derived_campus_context,
                        "character_count": len(raw_segment)
                    }
                })
            
            current_chunk_sentences = current_chunk_sentences[-2:] if len(current_chunk_sentences) > 2 else []
            current_length = sum(len(s) + 1 for s in current_chunk_sentences)

    # Wrap up any lingering sentences at the very end of the file
    if current_chunk_sentences:
        raw_segment = " ".join(current_chunk_sentences)
        if substantive_keywords.search(raw_segment.lower()) and len(raw_segment) >= 80:
            context_header = f"[Source: {source_id} | Context: {derived_campus_context}] "
            chunks.append({
                "chunk_id": f"{source_id}_chk_final",
                "chunk_text": context_header + raw_segment,
                "metadata": {"source_url": source_url, "parent_scope": derived_campus_context, "character_count": len(raw_segment)}
            })
        
    return chunks

# ==============================================================================
# PHASE 3 & 4: LIGHTWEIGHT VECTOR STORE & SIMILARITY RETRIEVAL ENGINE
# ==============================================================================
class LightweightVectorStore:
    """
    A zero-dependency, local vector storage engine. It maps text strings to 
    simulated dense embeddings using localized semantic frequency weights 
    and evaluates matches using true Cosine Similarity mathematics.
    """
    def __init__(self):
        self.database: List[Dict] = []

    def _generate_simulated_embedding(self, text: str) -> List[float]:
        """
        Transforms text chunks into a structured geometric vector array.
        Maps text density markers across strategic academic and dining indices.
        """
        vocabulary_dimensions = [
            "price", "bento", "noodle", "rice", "curry", "chicken", "stall", "canteen",
            "budget", "spend", "cheap", "expensive", "queue", "wait", "taste", "delicious",
            "western", "pasta", "pork", "beef", "fish", "soup", "hall", "campus", "ntu"
        ]
        
        vector = [0.0] * len(vocabulary_dimensions)
        text_lower = text.lower()
        
        for i, word in enumerate(vocabulary_dimensions):
            count = text_lower.count(word)
            vector[i] = float(count)
            
        magnitude = math.sqrt(sum(val ** 2 for val in vector))
        if magnitude > 0:
            vector = [val / magnitude for val in vector]
            
        return vector

    def add_chunks(self, processed_chunks: List[Dict]):
        """Embeds text chunks and loads them into memory with source metadata."""
        for chunk in processed_chunks:
            embedding = self._generate_simulated_embedding(chunk["chunk_text"])
            
            self.database.append({
                "chunk_id": chunk["chunk_id"],
                "chunk_text": chunk["chunk_text"],
                "metadata": chunk["metadata"],
                "vector_embedding": embedding
            })

    def retrieve_relevant_context(self, query_string: str, k: int = 5) -> List[Dict]:
        """
        Calculates cosine similarities between a query vector and the vector database,
        returning the Top-K most relevant chunks with source metadata.
        """
        query_vector = self._generate_simulated_embedding(query_string)
        # utilizes cosine similarity, 1.0 being a perfect match and 0.0 being completely orthogonal
        scored_results = []
        
        for record in self.database:
            db_vector = record["vector_embedding"]
            dot_product = sum(q * d for q, d in zip(query_vector, db_vector))
            similarity_score = dot_product 
            
            scored_results.append({
                "score": similarity_score,
                "chunk_text": record["chunk_text"],
                "metadata": record["metadata"]
            })
            
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:k]

# ==============================================================================
# MAIN CENTRALIZED PIPELINE HARNESS
# ==============================================================================
if __name__ == "__main__":
    # --- STAGE 1: DOCUMENT INGESTION ---
    raw_documents = load_and_cache_documents(TARGET_SOURCES)
    
    # --- STAGE 2: DOMAIN CLEANING ---
    print("\n=== STAGE 2: EXECUTING STANDARD LIBRARY CLEANING ENGINE ===")
    cleaned_docs = {}
    for doc in raw_documents:
        if "CONNECTION_EXCEPTION" in doc["raw_content"] or "ERROR_CODE" in doc["raw_content"]:
            continue
            
        cleaned_text = clean_document_text(doc["raw_content"])
        if len(cleaned_text.strip()) > 50:
            cleaned_docs[doc["source_id"]] = {
                "url": doc["source_url"],
                "cleaned_text": cleaned_text
            }
    
    # --- STAGE 3: CHUNKING ---
    print("\n=== STAGE 3: RUNNING QUALITY-FILTERED CHUNK GENERATOR ===")
    all_chunks = []
    for s_id, doc_data in cleaned_docs.items():
        doc_chunks = chunk_text(doc_data["cleaned_text"], s_id, doc_data["url"])
        all_chunks.extend(doc_chunks)
        
    print("\n=== FINAL TELEMETRY RECEIPTS ===")
    print(f"Total Source Footprints Ingested: {len(raw_documents)}")
    print(f"Total Quality-Verified Chunks Saved: {len(all_chunks)}")

    # --- DIAGNOSTIC VERIFICATION SAMPLES ---
    print("\n=== VERIFYING REPRESENTATIVE CHUNKS (5 DISTINCT SAMPLES) ===")
    if len(all_chunks) < 5:
        print(f"\n[WARNING] Only generated {len(all_chunks)} chunks. Lower your quality score metrics slightly.")
        for idx, chk in enumerate(all_chunks):
            print(f"\n[SAMPLE #{idx+1}]\nContent: {chk['chunk_text']}\n")
    else:
        step = len(all_chunks) // 5
        sample_indices = [0, step, step * 2, step * 3, len(all_chunks) - 1]
        
        for idx, sample_idx in enumerate(sample_indices):
            print(f"\n[CHUNK SPLIT SAMPLE #{idx+1} at Index {sample_idx}]")
            print(f"Content: {all_chunks[sample_idx]['chunk_text']}")
            print("-" * 80)

    # --- PHASE 3: VECTOR DB INGESTION ---
    vector_store = LightweightVectorStore()
    if all_chunks:
        vector_store.add_chunks(all_chunks)
        print(f"\n[PHASE 3 SUCCESS] Ingested {len(all_chunks)} vectors into storage client.")
    else:
        print("\n[PHASE 3 WARNING] No chunks found to load into vector database.")

    # --- PHASE 4: RETRIEVAL SYSTEM EVALUATION TESTING ---
    test_query = "Where can I find cheap noodles or bento rice bowls, and how much do they cost?"
    print(f"\n=== PHASE 4: EXECUTING QUERY RETRIEVAL SEARCH ===")
    print(f"User Query: '{test_query}'")
    
    top_matches = vector_store.retrieve_relevant_context(test_query, k=5)
    
    for rank, match in enumerate(top_matches, start=1):
        print(f"\n[RANK MATCH #{rank} | Vector Relevance Score: {match['score']:.4f}]")
        print(f"Content Context: {match['chunk_text']}")
        print(f"Source Document Hyperlink: {match['metadata']['source_url']}")
        print("-" * 80)