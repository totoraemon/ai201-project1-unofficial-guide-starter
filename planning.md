# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

Domain of Choice: Campus Dining

Official campus dining portals usually offer nothing more than menus, operating hours, and polished marketing photos. This domain captures the reality of campus eating: which dining halls to avoid at peak hours, the best value-for-money meal plan hacks, and more. This knowledge is hard to find because it lives in fragmented Reddit threads, casual Discord chats, and word-of-mouth advice that disappears as seniors graduate.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Miss Tam Chiak | Website | https://www.misstamchiak.com/ntu/ |
| 2 | Catharctic Life | Short Review | https://catharticstudent.wordpress.com/2017/05/18/ntu-life-top-16-best-campus-food-at-ntu/ |
| 3 | Happy Cow | Dietary Options | https://www.happycow.net/reviews/national-taiwan-university-taipei-61065 |
| 4 | Home Sweet Home | Local Guide | https://en.hshsharehouse.com/top-eats-and-fun-spots-guide-for-ntu-international-students/ |
| 5 | The Smart Local | Blog Guide | https://thesmartlocal.com/read/ntu-food/ |
| 6 | Reddit | Recommendations | https://www.reddit.com/r/taiwan/comments/1fbqzg9/what_do_college_students_eat_on_a_daily_basis/ |
| 7 | Reddit | Recommendations | https://www.reddit.com/r/NTU/comments/15ktgd7/best_eateries_on_campus/ |
| 8 | Reddit | Food Reviews | https://www.reddit.com/r/NTU/comments/1b17qxm/food_reviews_and_reccomendations/ |
| 9 | Reddit | Recommendations | https://www.reddit.com/r/NTU/comments/w0wi4b/list_of_places_to_eat_at_ntu_food/ |
| 10 | Reddit | Recommendations | https://www.reddit.com/r/taiwan/comments/snpsqo/budgetfriendly_dim_sum_restaurant_attracts_fans/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
700 characters (approximately 80–120 tokens).

**Overlap:**
150 characters (approximately 20 tokens).

**Reasoning:**
Campus dining data is uniquely fragmented. Subreddit comment threads and reviews contain high-density, localized advice (e.g., a single sentence warning about a food stall's peak queue times or a specific dietary allergen). A large chunk size (like 2,000 characters) would dilute these tips with surrounding, unrelated noise.

The 400-character chunk size isolates individual stall recommendations perfectly. The 100-character overlap acts as an informational safety net, ensuring that critical context—such as a food court name mentioned at the end of a sentence isn't severed from the stall's review in the subsequent chunk. This was updated from the initial 500-character chunk size as there were enough chunks being produced.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
text-embedding-3-small

**Top-k:**
K=5 chunks per query.

**Production tradeoff reflection:**
If deploying this system to real users with an unlimited budget, the core tradeoff to weigh is colloquial text accuracy versus operational latency. Campus dining data is highly conversational and packed with localized university shorthand (like "North Spine" or "Can 2") and regional food slang (like "Xiang Guo"). While text-embedding-3-small is efficient, upgrading to an enterprise-grade model with higher dimensional resolution, such as text-embedding-3-large, would better map these highly specific student terms to formal locations without losing semantic nuance. Furthermore, rather than relying on an external API that introduces network latency and risks during peak campus traffic times, a premium alternative would involve hosting a powerful open-weights model.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Where can I find vegetarian options on campus and are they clean? | Di San Xiao Chi Bu has dedicated vegetarian options; cross-contamination is actively monitored by staff.	You can eat at Di San Xiao Chi Bu. Reviews confirm staff monitor cross-contamination. |
| 2 | How much should a student budget daily for food court meals? | Around $50 to $80 NTD per baseline bento meal; student IDs yield an extra 10-15% off at select chains. |
| 3 | Which food stalls stay open past 8:00 PM for late-night studying? | Specific locations in the North Spine cluster reliably stay open until 10:00 PM. |
| 4 | Is the local night market a viable alternative for daily student budgets? | Yes, boundary zones like Gongguan/Shuiyuan serve as affordable transitions when halls close. |
| 5 | What is the best dish to order at the North Spine food court? | Document 7 highlights the Dim Sum and Western options, but warns of massive peak-hour lines. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Campus dining reviews on forums like Reddit are highly conversational and unstructured. A student might mention a specific venue ("The basement food court in the Student Union") at the beginning of a post, but list their specific stall warnings and pricing details multiple paragraphs later. If the chunking boundary cuts down the middle, the vector store will hold a highly descriptive chunk about a dish (e.g., "The $60 bento box is a lifesaver...") that completely lacks the location. This risk leads to off-target retrieval.

2. Because standard embedding models like text-embedding-3-small are trained on generalized global web data, they can struggle with the local terminology unique to a single campus community. Students frequently use abbreviations (e.g., "North Spine", "Can 2", "The Hive") or regional food terms. The system risks encountering semantic drift where the embedding model fails to group a review mentioning a nickname with a user query using the official building name, resulting in the retrieval system completely missing the advice.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

==========================================================================================
                         UNOFFICIAL CAMPUS DINING GUIDE: RAG PIPELINE
==========================================================================================

 [STAGE 1: DOCUMENT INGESTION]
   │
   ├─► Raw Sources: Student Blogs, Reddit Threads, Yelp Reviews, Video Transcripts
   │
   └─► Tool: Python Preprocessing Script
        │   (Strips raw HTML/JSON boilerplates, isolates student text body)
        ▼
 [STAGE 2: CHUNKING]
   │
   └─► Tool: Custom Regex Segmenter (Python)
        │   ┌────────────────────────────────────────────────────────────────────────┐
        │   │  • Strategy: Splits text on structural markdown headers (### Stall)   │
        │   │  • Hyperparameters: Chunk Size = 500 Chars  |  Overlap = 100 Chars      │
        │   │  • Metadata Injection: Prepends parent location/canteen info to chunk  │
        │   └────────────────────────────────────────────────────────────────────────┘
        ▼
 [STAGE 3: EMBEDDING & VECTOR STORE]
   │
   ├─► Embedding Model: openai.embeddings (text-embedding-3-small) -> 1,536 Dimensions
   │
   └─► Vector Database Store: ChromaDB / FAISS
        │   (Stores dense vectors mapped to student context strings + source URLs)
        ▼
 [STAGE 4: RETRIEVAL]
   │
   ├─► User Input Query ──► [ Vector Similarity Search ] ──► Compares against Vector DB
   │
   └─► Hyperparameters: Top-K = 5 Chunks
        │   (Extracts the 5 most semantically relevant text fragments)
        ▼
 [STAGE 5: GENERATION]
   │
   ├─► Context Assembly: Wraps the 5 retrieved student chunks inside XML security tags
   │
   ├─► Prompt Blueprint: Grounded System Prompt
   │    │   (Enforces zero outside extrapolation; demands exact inline markdown URLs)
   │    ▼
   ├─► Generation Model: OpenAI API (gpt-4o-mini)
   │
   └─► Final Output: Grounded, slang-aware student guide response with direct source links
        │
        └─► e.g., "...the bento box costs $65 NTD ([Source 3](https://...)) but lines peak at 12 PM."

==========================================================================================

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->



**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
