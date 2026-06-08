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

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Miss Tam Chiak | Website | https://www.misstamchiak.com/ntu/ |
| 2 | Catharctic Life | Short Review | https://catharticstudent.wordpress.com/2017/05/18/ntu-life-top-16-best-campus-food-at-ntu/ |
| 3 | Happy Cow | Dietary Options | https://www.happycow.net/reviews/national-taiwan-university-taipei-61065 |
| 4 | Home Sweet Home | Local Guide | https://en.hshsharehouse.com/top-eats-and-fun-spots-guide-for-ntu-international-students/ |
| 5 | Sweet Potato Island | Video Guide | https://www.youtube.com/watch?v=KwoJw9QZfH0 |
| 6 | Reddit | Recommendations | https://www.reddit.com/r/taiwan/comments/1fbqzg9/what_do_college_students_eat_on_a_daily_basis/ |
| 7 | Reddit | Recommendations | https://www.reddit.com/r/NTU/comments/15ktgd7/best_eateries_on_campus/ |
| 8 | Reddit | Food Reviews | https://www.reddit.com/r/NTU/comments/1b17qxm/food_reviews_and_reccomendations/ |
| 9 | Reddit | Recommendations | https://www.reddit.com/r/NTU/comments/w0wi4b/list_of_places_to_eat_at_ntu_food/ |
| 10 | Reddit | Recommendations | https://www.reddit.com/r/taiwan/comments/snpsqo/budgetfriendly_dim_sum_restaurant_attracts_fans/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
500 characters (approximately 80–120 tokens).

**Overlap:**
100 characters (approximately 20 tokens).

**Why these choices fit your documents:**
Campus dining data is uniquely fragmented. Subreddit comment threads and reviews contain high-density, localized advice (e.g., a single sentence warning about a food stall's peak queue times or a specific dietary allergen). A large chunk size (like 2,000 characters) would dilute these tips with surrounding, unrelated noise.

The 500-character chunk size isolates individual stall recommendations perfectly. The 100-character overlap acts as an informational safety net, ensuring that critical context—such as a food court name mentioned at the end of a sentence isn't severed from the stall's review in the subsequent chunk.

**Final chunk count:**
142 chunks (across all 10 scraped source documents).

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
text-embedding-3-small (OpenAI) configured to 1533 dimensions.

**Production tradeoff reflection:**
The primary trade-off to weigh is multilingual and colloquial text handling versus latency. Campus dining data is heavily identity-driven; students frequently mix official campus building codes (e.g., "North Spine", "Canteen 2") with regional food slang ("Xiang Guo", "Bento"). text-embedding-3-small handles standard English well but can struggle with localized slang syntax.

A model like Cohere natively supports content quality scoring, ensuring that short, slang-heavy, highly accurate Reddit comments score higher in vector similarity searches than long, generic blog posts. While hosting a heavy local model increases operational latency, it eliminates unpredictable upstream API outages during critical university periods.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
You are the Unofficial Campus Dining Guide Assistant. Your sole task is to answer user queries using ONLY the verified student review fragments provided in the context block below. 

Strict Rules:
1. If the context does not explicitly mention the food stall, pricing, dietary status, or hours asked about, state clearly: "I cannot find reliable student documentation for that specific option."
2. Do not extrapolate, assume, or use any outside knowledge about generic restaurant chains or global cuisines.
3. Every factual claim must be explicitly tied to a source URL from the context.

**How source attribution is surfaced in the response:**
The system forces the LLM to use markdown hyperlinks matching the original document source array. Instead of a generic bibliography block at the bottom of the response, source attribution is injected inline immediately following the specific claim, formatted exactly like this: "...the vegetarian bento box at Canteen 1 costs $65 NTD, but the line gets unmanageable after 12:15 PM ([Source 3](https://www.happycow.net/...))."

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

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

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
