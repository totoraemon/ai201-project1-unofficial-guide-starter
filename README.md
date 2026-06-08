# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Domain of Choice: Campus Dining

Official campus dining portals usually offer nothing more than menus, operating hours, and polished marketing photos. This domain captures the reality of campus eating: which dining halls to avoid at peak hours, the best value-for-money meal plan hacks, and more. This knowledge is hard to find because it lives in fragmented Reddit threads, casual Discord chats, and word-of-mouth advice that disappears as seniors graduate.

---

## Document Sources

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
500 characters (approximately 100 tokens / 100 words).

**Overlap:**
100 characters (approximately 20 tokens / 20 words).

**Why these choices fit your documents:**
My sources consist heavily of highly structured campus directory links, store operational matrices, and short student reviews/menu items. A smaller, precise chunk size of 500 characters guarantees that specific details (such as a single dining hall’s hours or a specific menu item profile like "Fitbites salad bowls") stay contained within a tight semantic window without being diluted by unrelated campus locations. The 100-character overlap balances this constraint by preserving necessary context across structural shifts or markdown tables, ensuring that location tags or parent headers are not cut off mid-sentence during splitting.

**Preprocessing:**
I begin by creating a set of keywords that are common across dining locations (such as am/pm for time, open/closed for availability, menu, price, etc.). Then, each cleaned text is split at a newline to ensure that there are no breaks in a chunk.

**Final chunk count:**
82 chunks (across all 14 scraped source documents).

---

## Embedding Model

**Model used:**
`all-MiniLM-L6-v2`

**Production tradeoff reflection:**
The transformer model eliminates the manual maintenance of vocabulary checklists. While initally completing this project, I utilized a different embedding model and had to specify multiple keywords of different categories. Even with the list, the model still failed to properly respond to user queries. With the `all-MiniLM-L6-v2` embedding model, the system can parse through synonyms, structural changes, and potentially misspelled inputs. The main difference is that it requires Python dependencies (`torch`, `sentence-transformers`, `numpy`).

Additionally, my program utilizes a native database with `LightweightVectorStore`, keeping query latency beneath 5 milliseconds. However, restarting the script forces the pipeline to crawl, parse, clean, and re-embed all 14 target web nodes from scratch. If any source URL experiences downtime or anti-bot blocks during startup, those locations vanish from memory. This was evident through my multiple runs of my program as I could oneasily say an hour was lost on ending the program as I had to fix the line of code that was wrong, delete the created data files, and re-run the program (which loaded all of the sources, ran the test chunks, and ran the retrieval chunks before loading the webpage).

---

## Grounded Generation

**System prompt grounding instruction:**
You are the Unofficial Campus Dining Guide Assistant. Your sole task is to answer user queries using ONLY the verified student review fragments provided in the context block below. 

Strict Rules:
1. If the context does not explicitly mention the food location, pricing, dietary status, or hours asked about, state clearly: "I do not possess sufficient reference documentation to answer this question accurately."
2. Do not extrapolate, assume, or use any outside knowledge about generic restaurant chains or global cuisines.
3. Every factual claim must be explicitly tied to a source URL from the context.

**How source attribution is surfaced in the response:**
The system forces the LLM to use markdown hyperlinks matching the original document source array. Instead of a generic bibliography block at the bottom of the response, source attribution is injected inline immediately following the specific claim, formatted exactly like this: "...the salad bowl at Fitbites cost $12, but the line gets unmanageable after 9:00 PM (source)."

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Where can I find healthy or vegetarian-friendly options? | Fitbites offers salad bowls of multiple varieties. | You can find healthy options at the Farm Store, which sells fresh produce grown and sold from the campus farm, orchards, and greenhouses. Additionally, the Poly Fresh Market and the Student-staffed store at Kellogg Ranch (FitbitesCampus) offer fresh produce. | Partially relevant | Partially accurate |
| 2 | What is Goomo? | Goomo is a nearby boba shop that provides cheap snacks and drinks. | Goomo Tea Shop is a local bubble tea destination in Walnut, CA, dedicated to serving fresh, handcrafted tea and drinks with natural ingredients. | Relevant | Accurate |
| 3 | What foods are offered at Vista Market? | Vista Market provides a wide assortment of snacks and meals, from fresh to frozen. | Vista Market offers a mix of essentials for home-cooked meals, personal items, grab-and-go options like sushi and parfaits, and other grocery staples. | Relevant | Partially accurate |
| 4 | What are meal points? | Meal points are plans that students can purchase to spend on food. | I do not possess sufficient reference documentation to answer this question accurately. | Off-target | Inaccurate |
| 5 | What type of food does Fitbites serve? | Fitbites (located near the Residence Suites) serves warm bowls, salads, hot subs, and paninis. | Fitbites serves a fusion of diverse cuisines, including warm bowls, salads, hot subs, and paninis. They also offer savory bites such as mozzarella sticks and fried zucchini to add to meals. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

For responses I deemed as relevant, they provided information that related to the user's query. For responses I deemed as accurate, they provided infromation that answered the user's query correctly. For example, with the second test question, the model gave the location (which is relevant) of Goomo and a short description of what it sells (which is accurate.)

---

## Failure Case Analysis

**Question that failed:**
What are meal points?

**What the system returned:**
I do not possess sufficient reference documentation to answer this question accurately.

**Root cause (tied to a specific pipeline stage):**
In my Architecture diagram (located in `planning.md`), I specify that Stage 1 is 'Document Ingestion', where all the sources that the model will build chunks from are cleaned for the future stages. Within this stage, there was no specific source that explained what meal points are or how they work. This causes the model to reach the "grounded" answer of not being able to produce a proper response as it has not been provided sufficient information to do so.

**What you would change to fix it:**
To fix this issue, I would add more sources to my source list in `rag_pipeline.py`.

---

## Spec Reflection

**One way the spec helped you during implementation:**
`planning.md` helped me draft out each step and pathway I would need to take to complete this project. Initially, when I was confused about which part of the program was tackling what, I could easily determine the stage because of the ASCII drawing that `planning.md` specified was required. This helped my comprehension of the program's timeline: take in documents, pre-process documents to prepare for chunking, chunk documents into ~500 characters, test queries against chunks, and implement user interface.

**One way your implementation diverged from the spec, and why:**
With my first few iterations of `planning.md`, I was utilizing a different embedding model with a fairly strict vocabulary list. However, this was extremely inefficient as I had to specify dozens of words ranging from type of building to food options. After re-reading the guides from Codepath, I realized I could use the `all-MiniLM-L6-v2` embedding model, which completely eliminated my need for the extensive vocabulary list.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* I provided Gemini my Chunking Strategy section from `planning.md` and requested it to implement the chunk_text() method.
- *What it produced:* It recommended cleaning the sources beforehand, resulting in preceding method clean_document_text(). It returned a function that utilized a limit of 120 words and splits at newlines.
- *What I changed or overrode:* I overrode the chunk size from 120 to 100 as many of my sources are webpages with short descriptions rather than long, extensive guides about the food locations.

**Instance 2**

- *What I gave the AI:* I provided Gemini my Architecture diagram from `planning.md` and requested it to implement the embeddings while storing them in a database.
- *What it produced:* It returned a function that generated the embeddings, added the chunks from chunk_text(), and retrieved context from the user's query to match against the chunks.
- *What I changed or overrode:* I noticed that the initial output utilized a database and re-read the guides from Codepath to see if they were necessary. Since this is a small collection of sources, I requested a modification to store the files locally.
