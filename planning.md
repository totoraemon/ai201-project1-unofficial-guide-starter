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
500 characters (100 words).

**Overlap:**
100 characters (20 words).

**Reasoning:**
My sources consist heavily of highly structured campus directory links, store operational matrices, and short student reviews/menu items. A smaller, precise chunk size of 500 characters guarantees that specific details (such as a single dining hall’s hours or a specific menu item profile like "Fitbites salad bowls") stay contained within a tight semantic window without being diluted by unrelated campus locations. The 100-character overlap balances this constraint by preserving necessary context across structural shifts or markdown tables, ensuring that location tags or parent headers are not cut off mid-sentence during splitting.

---

## Retrieval Approach

**Embedding model:**
`all-MiniLM-L6-v2`

**Top-k:**
5 chunks

**Production tradeoff reflection:**
The transformer model eliminates the manual maintenance of vocabulary checklists. While initally completing this project, I utilized a different embedding model and had to specify multiple keywords of different categories. Even with the list, the model still failed to properly respond to user queries. With the `all-MiniLM-L6-v2` embedding model, the system can parse through synonyms, structural changes, and potentially misspelled inputs. The main difference is that it requires Python dependencies (`torch`, `sentence-transformers`, `numpy`).

Additionally, my program utilizes a native database with `LightweightVectorStore`, keeping query latency beneath 5 milliseconds. However, restarting the script forces the pipeline to crawl, parse, clean, and re-embed all 14 target web nodes from scratch. If any source URL experiences downtime or anti-bot blocks during startup, those locations vanish from memory. This was evident through my multiple runs of my program as I could oneasily say an hour was lost on ending the program as I had to fix the line of code that was wrong, delete the created data files, and re-run the program (which loaded all of the sources, ran the test chunks, and ran the retrieval chunks before loading the webpage).

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Where can I find healthy or vegetarian-friendly options? | Fitbites offers salad bowls of multiple varieties. |
| 2 | What is Goomo? | Goomo is a nearby boba shop that provides cheap snacks and drinks. |
| 3 | What foods are offered at Vista Market? | Vista Market provides a wide assortment of snacks and meals, from fresh to frozen. |
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
     - e.g., "...the bowl costs $12 (source) but lines peak at 12 PM."

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
* **Verification Strategy:** Execute a quick collection count assert query to verify that the final database record count perfectly mirrors the total chunk count generated by our ingestion script and print 3 test cases.

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

## Milestone 4 — Embedding and retrieval:
TEST CASE #1: Querying vector space for:
   'Where are the vending machines located inside the BSC?'
   SUCCESS | Top Match Score: 0.9071
   Top Chunk Text: [Source: src_9 | Context: CPP Campus Dining Hub] Vending MachinesThe BSC has vending machines positioned on the first floor, providing additional snack and drink options during BSC operational hours. Whether you’re studying or simply passing through, satisfy your cravings with ease. | In case you encounter any issues, a dedicated support team is just a phone call away. Find the support team information listed on the vending machines for prompt assistance. | New Furniture & Charging StationsThe BSC has various lounge spaces and charging stations available on a first come, first served basis.
   
TEST CASE #2: Querying vector space for:
   'Are there any vegan or vegetarian options at Centerpointe?'
   SUCCESS | Top Match Score: 0.8220
   Top Chunk Text: [Source: src_4 | Context: CPP Campus Dining Hub] Campus Map | Building 72: Residence Halls - Centerpointe DiningLocated in the core of the Cal Poly Pomona campus, Centerpointe Dining Commons is a state of the art all-you-care-to-eat dining facility. Centerpointe offers delicious and nutritious food stations with items such as handmade tortillas, a sushi bar, a salad bar featuring Cal Poly Pomona grown produce, a carving station, plenty of vegan and vegetarian options and so much more!

TEST CASE #3: Querying vector space for:
   'Can I use my Bronco Bucks or meal plan swipes at Vista Market?'
   SUCCESS | Top Match Score: 0.6530
   Top Chunk Text: [Source: src_2 | Context: CPP Campus Dining Hub] Bronco Bucks | Learn about our Bronco Bucks program: just deposit money into your Bronco Bucks Account, and you can use your Bronco One Card to make purchases on campus. Even better - it's easy for you (or others) to add more money.

---

## Milestone 5 — Generation and interface:
Question 1: Where can I find healthy or vegetarian-friendly options?
- Expected answer: Fitbites offers salad bowls of multiple varieties.
- Actual answer: You can find healthy options at the Farm Store, which sells fresh produce grown and sold from the campus farm, orchards, and greenhouses. Additionally, the Poly Fresh Market and the Student-staffed store at Kellogg Ranch (FitbitesCampus) offer fresh produce. Vegetarian-friendly options may include items like canned vegetables, fruits, and grains available in Poly Pantry bags, such as bell peppers, potatoes, tomatoes, onions, cucumbers, zucchini, apples, bananas, kiwis, pears, and oranges, as well as non-dairy milk alternatives like almond milk, coconut milk, soy milk, and oat milk.
- Source(s): https://asi.cpp.edu/services/poly-pantry/, https://cppdining.com/dining-locations/, https://www.cpp.edu/campus-life/housing-dining.shtml

Question 2: What is Goomo?
- Expected answer: Goomo is a nearby boba shop that provides cheap snacks and drinks.
- Actual answer: Goomo Tea Shop is a local bubble tea destination in Walnut, CA, dedicated to serving fresh, handcrafted tea and drinks with natural ingredients.
- Source(s): https://asi.cpp.edu/services/poly-pantry/, https://cppdining.com/dining-locations/https://www.goomoteashop.com/

Question 3: What foods are offered at Vista Market?
- Expected answer: Vista Market provides a wide assortment of snacks and meals, from fresh to frozen.
- Actual answer: Vista Market offers a mix of essentials for home-cooked meals, personal items, grab-and-go options like sushi and parfaits, and other grocery staples.
- Sources: https://asi.cpp.edu/services/poly-pantry/, https://cppdining.com/dining-locations/, https://www.cpp.edu/maps/text-map.php?id=27142&list=cat, https://www.cpp.edu/openhouse/dining.shtml

Question 4: What are meal points?
- Expected answer: Meal points are plans that students can purchase to spend on food.
- Actual answer: I do not possess sufficient reference documentation to answer this question accurately.
- Sources: https://cppdining.com/dining-locations/, https://www.cpp.edu/campus-life/housing-dining.shtml, https://www.cpp.edu/maps/text-map.php?id=458829&list=loc

Question 5: What type of food does Fitbites serve?
- Expected answer: Fitbites (located near the Residence Suites) serves warm bowls, salads, hot subs, and paninis.
- Actual answer: Fitbites serves a fusion of diverse cuisines, including warm bowls, salads, hot subs, and paninis. They also offer savory bites such as mozzarella sticks and fried zucchini to add to meals.
- Sources: https://asi.cpp.edu/services/poly-pantry/, https://cppdining.com/dining-locations/