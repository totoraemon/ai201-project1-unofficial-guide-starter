# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Domain of Choice: Campus Dining

Official campus dining portals usually offer nothing more than menus, operating hours, and polished marketing photos. This domain captures the reality of campus eating: which dining halls to avoid at peak hours, the best value-for-money meal plan hacks, and more. This knowledge is hard to find because it lives in fragmented Reddit threads, casual Discord chats, and word-of-mouth advice that disappears as seniors graduate.

---

## Documents

| # | Source | Type | URL or file path |
| --- | --- | --- | --- |
| 1 | CPP Foundation Dining Hub | Campus Portal Website | [https://cppdining.com/dining-locations/](https://cppdining.com/dining-locations/) |
| 2 | CPP Housing & Residential Dining Portal | Campus Portal Website | [https://www.cpp.edu/campus-life/housing-dining.shtml](https://www.cpp.edu/campus-life/housing-dining.shtml) |
| 3 | Open House Special Operation Matrix | Campus Informational Directory | [https://www.cpp.edu/openhouse/dining.shtml](https://www.google.com/search?q=https%3A%2F%2Fwww.cpp.edu%2Fopenhouse%2Fdining.shtml) |
| 4 | Building 72 Mapping Data (Centerpointe & Lollicup) | Campus Informational Directory | [https://www.cpp.edu/maps/text-map.php?id=458829&list=loc](https://www.google.com/search?q=https%3A%2F%2Fwww.cpp.edu%2Fmaps%2Ftext-map.php%3Fid%3D458829%26list%3Dloc) |
| 5 | Building 52 & 35 Operations Node | Campus Informational Directory | [https://www.cpp.edu/maps/text-map.php?id=27142&list=cat](https://www.google.com/search?q=https%3A%2F%2Fwww.cpp.edu%2Fmaps%2Ftext-map.php%3Fid%3D27142%26list%3Dcat) |
| 6 | Building 1070574 Geolocation Map (Fitbites) | Campus Informational Directory | [https://www.cpp.edu/maps/text-map.php?id=1070574&list=loc](https://www.google.com/search?q=https%3A%2F%2Fwww.cpp.edu%2Fmaps%2Ftext-map.php%3Fid%3D1070574%26list%3Dloc) |
| 7 | Housing Staff Administration Records | Campus Informational Directory | [https://www.cpp.edu/housing/about/staff-directory.shtml](https://www.google.com/search?q=https%3A%2F%2Fwww.cpp.edu%2Fhousing%2Fabout%2Fstaff-directory.shtml) |
| 8 | ASI Poly Pantry Portal | Campus Portal Website | [https://asi.cpp.edu/services/poly-pantry/](https://www.google.com/search?q=https%3A%2F%2Fasi.cpp.edu%2Fservices%2Fpoly-pantry%2F) |
| 9 | ASI BSC Amenities Index (Qdoba, Saddles, Vending) | Campus Informational Directory | [https://asi.cpp.edu/facilities/bsc/bsc-amenities/](https://www.google.com/search?q=https%3A%2F%2Fasi.cpp.edu%2Ffacilities%2Fbsc%2Fbsc-amenities%2F) |
| 10 | ASI Bronco Student Center General Info | Campus Informational Directory | [https://asi.cpp.edu/facilities/bsc/bsc-info/](https://www.google.com/search?q=https%3A%2F%2Fasi.cpp.edu%2Ffacilities%2Fbsc%2Fbsc-info%2F) |
| 11 | CPP PolyCentric University News | Campus News Article | [https://www.cpp.edu/polycentric/index.shtml](https://www.google.com/search?q=https%3A%2F%2Fwww.cpp.edu%2Fpolycentric%2Findex.shtml) |
| 12 | CPP Student Services Gateway | Campus Portal Website | [https://www.cpp.edu/student-gateway/](https://www.google.com/search?q=https%3A%2F%2Fwww.cpp.edu%2Fstudent-gateway%2F) |
| 13 | Goomo Tea Shop Homepage | Company Website | [https://www.goomoteashop.com/](https://www.google.com/search?q=https%3A%2F%2Fwww.goomoteashop.com%2F) |
| 14 | The Habit Burger & Grill Tracker | Company Website | [https://www.habitburger.com/locations/claremont/](https://www.google.com/search?q=https%3A%2F%2Fwww.habitburger.com%2Flocations%2Fclaremont%2F) |

---

## Chunking Strategy

**Chunk size:**
500 characters.

**Overlap:**
100 characters.

**Reasoning:**
My sources consist heavily of highly structured campus directory links, store operational matrices, and short student reviews/menu items. A smaller, precise chunk size of 500 characters guarantees that specific details (such as a single dining hall’s hours or a specific menu item profile like "Fitbites salad bowls") stay contained within a tight semantic window without being diluted by unrelated campus locations. The 100-character overlap balances this constraint by preserving necessary context across structural shifts or markdown tables, ensuring that location tags or parent headers are not cut off mid-sentence during splitting.

---

## Retrieval Approach

**Embedding model:**
`llama-3.3-70b-versatile`

**Top-k:**
5 chunks

**Production tradeoff reflection:**
If deploying this to real users at scale, running a massive 70-billion parameter model like `llama-3.3-70b-versatile` purely for extracting dense vector representations presents massive latency challenges. While its parameter scale grants it a deep semantic understanding of complex student slang, messy context fragments, and campus abbreviations (e.g., "BSC", "CPP"), the hosting overhead is extremely heavy compared to lightweight, dedicated embedding endpoints.

If cost and infrastructure constraints were entirely removed in production, the primary trade-off we would evaluate is latency vs. contextual depth. Because campus dining is entirely localized and English-centric, we would gladly trade away broad multilingual capabilities and massive context windows in exchange for lightning-fast search latency and a vocabulary index highly fine-tuned for high-density, short text student discourse.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Where can I find healthy or vegetarian-friendly options? | Fitbites offers salad bowls of multiple varieties. |
| 2 | What is Goomo? | Goomo is a nearby boba shop that provides cheap snacks and drinks. |
| 3 | What are some of the popular foods at Goomo? | Their fruit teas and popcorn chicken are some of their most purchased items. |
| 4 | What are meal points? | Meal points are plans that students can purchase to spend on food. |
| 5 | What type of food does Fitbites serve? | Fitbites (located near the Residence Suites) serves warm bowls, salads, hot subs, and paninis. |

---

## Anticipated Challenges

1. Because much of the campus directory info (like hours, location numbers, and menus) lives within dense markdown structures and HTML matrices, standard text chunking could easily shear a dining hall's name away from its operating hours. This would result in completely unanchored data fragments inside the vector store.

2. Since open-source student commentary and unofficial websites update infrequently, the Generation model (`gemini-2.5-flash` / `gemini-2.5-pro`) might rely on its pre-trained global knowledge to invent generic pricing or menu options when the local vector store context is sparse. This directly undermines our goal of delivering an accurate campus-specific guide.

---

## Architecture

                         UNOFFICIAL CAMPUS DINING GUIDE: RAG PIPELINE

[STAGE 1: DOCUMENT INGESTION]
- Raw Sources: Student Blogs, Reddit Threads, Yelp Reviews, Video Transcripts
- Tool: Python Preprocessing Script
     - (Strips raw HTML/JSON boilerplates, isolates student text body)

[STAGE 2: CHUNKING]
- Tool: Custom Regex Segmenter (Python)
     - Strategy: Splits text on structural markdown headers (### Stall)
     - Hyperparameters: Chunk Size = 500 Chars  |  Overlap = 100 Chars
     - Metadata Injection: Prepends parent location/canteen info to chunk

[STAGE 3: EMBEDDING & VECTOR STORE]
- Embedding Model: llama-3.3-70b-versatile
- Vector Database Store: LightweightVectorStore
     - (Stores dense vectors mapped to student context strings + source URLs)

[STAGE 4: RETRIEVAL]
- User Input Query ──► [ Vector Similarity Search ] ──► Compares against Vector DB
- Hyperparameters: Top-K = 5 Chunks
     - (Extracts the 5 most semantically relevant text fragments)

[STAGE 5: GENERATION]
- Context Assembly: Wraps the 5 retrieved student chunks inside XML security tags
- Prompt Blueprint: Grounded System Prompt
     - (Enforces zero outside extrapolation; demands exact inline markdown URLs)
- Generation Model: Gemini API (gemini-2.5-flash)
- Final Output: Grounded, slang-aware student guide response with direct source links
     - e.g., "...the bowl costs $12 ([Source 3](https://...)) but lines peak at 12 PM."

---

## AI Tool Plan

### 1. Data Ingestion & Chunking
* **AI Tool:** Gemini
* **Inputs:** *Chunking Strategy* section, sample markdown text from our document matrix, and the target specifications (500 chars size, 100 chars overlap).
* **Expected Output:** A clean Python script (`rag_pipeline.py`) utilizing standard string tools or regex to split files securely into overlapping windows, passing forward parent source metadata strings attached to each block.
* **Verification Strategy:** Run the code locally on sources and print out 5 test cases, checking lengths and boundary fragments of three consecutive chunks to ensure characters uniformly sit around 500 characters with correct context preservation.

### 2. Embedding & Vector DB Storage
* **AI Tool:** Gemini
* **Inputs:** *Architecture Stage 3* parameters
* **Expected Output:** Modular Python code initializing the local storage, connecting to the API, mapping text chunks into dense embeddings, and persisting them cleanly to local disk storage.
* **Verification Strategy:** Execute a quick collection count assert query to verify that the final database record count perfectly mirrors the total chunk count generated by our ingestion script.

### 3. Retrieval & Generation Interface
* **AI Tool:** Gemini
* **Inputs:** *Retrieval Approach*, *Evaluation Plan*, and *Architecture Stages 4 & 5* specifications.
* **Expected Output:** An execution pipeline function `query_guide(user_prompt: str)` that fetches the top 5 chunks, frames them inside an XML block, triggers a `gemini-2.5-flash` generation request, and streams back responses.
* **Verification Strategy:** Fire all 5 evaluation test questions through the query pipeline sequentially. Compare system outputs manually against our hardcoded *Expected answers* to check for accuracy, and look out for structural markdown links to verify strict source grounding.

---

## Milestone 3 — Ingestion and chunking:
CHUNK SAMPLE #1
ID: src_1_chk_0
Full Text:
[Source: src_1 | Context: CPP Campus Dining Hub] Dining Locations - CPPE Dining Services | Skip to content | Dining Hours | AboutAbout Us Awards Management Our Chefs Jobs Contact Hours LocationsDining Locations GrubHub Food Truck Vending & ATMs Catering Robot Delivery Interactive Map Centerpointe Meal PlansMeal Plan Options Meal Plans Finder Meal Plan Account Access News | View AllDining HallQuick BitesHealthy EatsConvenience StoresResidentialBeveragesLate NightFood Trucks | BRIC Break | BRIC (Building 42) | Monday (Summer Break) Closed
Metadata Source: https://cppdining.com/dining-locations/

CHUNK SAMPLE #2
ID: src_1_chk_1
Full Text:
[Source: src_1 | Context: CPP Campus Dining Hub] Monday (Summer Break) Closed | View DetailsA healthy food stand, located inside the Bronco Recreational and Intramural Complex (BRIC), that serves customizable acai bowls, smoothies, and other healthy snacks like protein bars to students and visitors. It provides a convenient and affordable option for a healthy pick-me-up, with service windows both inside the BRIC and outside at the front and on the pool deck | Centerpointe Dining | Building 72 | Summer hours: Monday 11 AM - 6 PM
Metadata Source: https://cppdining.com/dining-locations/

CHUNK SAMPLE #3
ID: src_1_chk_2
Full Text:
[Source: src_1 | Context: CPP Campus Dining Hub] Summer hours: Monday 11 AM - 6 PM | View DetailsCenterpointe Dining Commons at Cal Poly Pomona is a 35,000-square-foot all-you-care-to-eat dining hall offering diverse food stations, campus-grown produce, and sustainable dining options for students, faculty, staff, and the public. | Element Cafe | College of Business Administration (Building 164) | View DetailsThe Element Coffee & Food menu offers a variety of sandwiches and bowls consisting of fresh ingredients to deliver a delicious flavor! | ENV Cafe | College of Environmental Design (Building 7)
Metadata Source: https://cppdining.com/dining-locations/

CHUNK SAMPLE #4
ID: src_1_chk_3
Full Text:
[Source: src_1 | Context: CPP Campus Dining Hub] College of Environmental Design (Building 7) | View DetailsLocated at the College of Environmental Design (Building 7), ENV Cafe offers trendy drinks from lattes to lemonades, shakes, frappes, teas, smoothies, boba drinks, pastries, and breakfast and lunch burritos. | Farm Store at Kellogg Ranch | AGRIscapes (Building 211) | Monday 10 AM - 6 PM
Metadata Source: https://cppdining.com/dining-locations/

CHUNK SAMPLE #5
ID: src_1_chk_4
Full Text:
[Source: src_1 | Context: CPP Campus Dining Hub] Monday 10 AM - 6 PM | View DetailsStudent-staffed store at Kellogg Ranch featuring fresh produce, meats, and other food products from the campus farm, orchards, and greenhouses, alongside locally sourced and specialty items like CPP-made wines, beers, and honeys. It also sells ornamental and edible plants from the campus nursery and offers student-designed apparel and unique gift baskets. | FitbitesCampus | Residence Suites (Building 52)
Metadata Source: https://cppdining.com/dining-locations/

---

