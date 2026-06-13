# The Unofficial Guide — Project 1

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This system covers student-generated knowledge about the Computer Science department at Brooklyn College (CUNY). It includes professor reviews, course advice, program requirements, and informal student opinions that are difficult to find through official channels. Official sources like course catalogs and department websites describe what courses exist, but don't reflect teaching style, exam difficulty, workload, or which professors are worth taking. This system makes that informal knowledge searchable and answerable.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | RateMyProfessors| Review Site |https://www.ratemyprofessors.com/|
| 2 | BC CS Department Website| Official website| https://www.brooklyn.edu/academics/programs/computer-science-bs/|
| 3 | Graduate Course Syllabi| Offical website|https://www.brooklyn.cuny.edu/cis/graduate/ |
| 4 | Undergraduate Course Syllabi| Official website |https://www.brooklyn.cuny.edu/cis/undergraduate/ |
| 5 |Graduate Advice Brochure | PDF | docs/graduate.pdf |
| 6 | Undergraduate Advice Brochure| PDF | docs/undergraduate.pdf |
| 7 |r/CUNY | Subreddit| https://www.reddit.com/r/CUNY/|
| 8 | r/BrooklynCollege| Subreddit | https://www.reddit.com/r/BrooklynCollege/|
| 9 | Brooklyn College CS Club Website| Club website | https://www.reddit.com/r/BrooklynCollege/|
| 10 | Brooklyn College CS Discord| Discord export | docs/bc_csclub_discord.html|


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 200 tokens

**Overlap:** 30 tokens

**Why these choices fit your documents:** The corpus is dominated by short-form review and opinion content from RateMyProfessors, Reddit, and Discord, where individual posts are naturally self-contained units of meaning. A smaller chunk size of 200 tokens preserves these atomic opinions without merging unrelated reviews together. The longer structured documents like syllabi and PDFs are also well-served by this size since their key information tends to appear in discrete paragraphs. A 30-token overlap ensures that sentences split across chunk boundaries don't lose context without introducing excessive redundancy. Before chunking, documents were cleaned to remove URLs, email addresses, phone numbers, and PDF table of contents formatting using regex preprocessing.

**Final chunk count:** 980 chunks across 10 documents

---

## Sample Chunks
| # | ChunkID | Source | Text |
|---|--------|------|-----------------|
|1 | graduate.pdf_5 | graduate.pdf | "The Computation track is designed for students interested in computer science research, system development, or advanced applications. This program is focused on teaching the student advanced techniques and methodology, in addition to applying standard computer tools. The program is also recommended for students who wish to pursue doctoral studies in computer science." |
| 2 | bc_csclub_discord.html_1 | bc_csclub_discord.html | "katychuang He's one of the few who are more hands on than most other professors so he gives feedback along the way. Also, when you get stuck on a problem, as long as you show you're making effort to find solutions, he'll give some hints/corrections on the path forward. The key is to show you're being proactive with the learning process" |
| 3 | ratemyprofessor.txt_1 | ratemyprofessor.txt | "not a terrible professor, but there are better options available. If you have the chance to choose a different instructor I recommend doing so. However if he's your only option you'll manage just fine. At times he seems a bit unfit for teaching but if you read the textbook, practice on your own and attend class you'll be fine."|
|4 | undergraduate.pdf_4 | undergraduate.pdf | "knowledge of a high-level computer language (preferably Java or C++), knowledge of assembly language and computer architecture, a course in discrete structures, a course in data structures, and a course in calculus."|
|5| reddit_bc.txt_0 | reddit_bc.txt | "Even if the professors suck at BC, computer science is mostly self-taught anyway. You get taught a little bit from the professors and guided, but a lot of the coding and work is done on your own. You kinda teach yourself through YouTube, Stack Overflow, etc." |

---

## Retrieval Test Examples
**Query 1:** "What programming languages are CS undergrad students required to learn?"
1. undergraduate.pdf — "The Department of Computer and Information Science (CIS) offers a very rich undergraduate program in computer science..." (distance: 0.703)
2. undergraduate.pdf — "knowledge of a high-level computer language (preferably Java or C++), knowledge of assembly language..." (distance: 0.761)
3. reddit_bc.txt — "Even if the professors suck at BC, computer science is mostly self-taught anyway..." (distance: 0.798)
**Why these chunks are relevant:** The top two chunks are from the undergraduate PDF and directly mention Java and C++ as required languages. The Reddit chunk is partially relevant — it discusses CS education at BC generally but doesn't name specific languages. Retrieval correctly prioritized the official document over the informal source.

**Query 2:** "What negative feedback do students give about Professor Ziegler?"
1. bc_csclub_discord.html — "Ziegler is a miserable man bro. The dude is always condescending and in a bad mood..." (distance: 0.953)
2. bc_csclub_discord.html — "as someone who's taken Ziegler for 3115, he's so much worse...Oral assignments with vague instructions, lectures that are only vaguely related to the course's description..." (distance: 1.001)
3. bc_csclub_discord.html — "Class so stressful it made me get a psych eval...for long assignments like Ziegler's, they require several hours of tutoring if you're starting from zero..." (distance: 1.034)
**Why these chunks are relevant:**  All top results came from the Discord export and directly mention Professor Ziegler by name with specific negative feedback. This is the strongest retrieval result in the evaluation.

**Query 3:** If I take the expedited masters, does taking the graduate level computer theory course fulfill both undergrad and grad requirements at the same time?"
1. bc_csclub_discord.html — "they're capstone courses. Can vary on an individual case basis, but is rare..." (distance: 0.953)
2. graduate.pdf — "advanced area test. Students whose first language is not English are required to take the TOEFL..." (distance: 0.976)
3. graduate.pdf — "undergraduate or graduate courses in health and nutrition sciences..." (distance: 0.987)
**Why these chunks struggled:** Only the first chunk is partially relevant. The query uses specific phrasing ("expedited masters", "fulfill both requirements") that doesn't semantically match the language in the documents ("capstone courses", "24 credits of advanced courses"). This is the documented failure case.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers.

**Production tradeoff reflection:** In a production deployment, several tradeoffs would need to be weighed. A larger API-hosted model like OpenAI's text-embedding-3-large would likely produce more accurate embeddings, especially for nuanced queries, but introduces per-request cost and latency. Context length is another consideration, all-MiniLM-L6-v2 has a 256-token limit, which means longer chunks get truncated silently. A model with a longer context window would handle the PDF chunks more accurately. For this project, the local model was the right choice given the scale and constraints.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** "You are a helpful assistant for students at Brooklyn College's CS department. Answer the question using ONLY the information provided in the documents below. If the documents don't contain enough information to answer, say exactly: 'I don't have enough information on that.' Do not use any outside knowledge. Do not make anything up."

**How source attribution is surfaced in the response:** Source filenames are extracted programmatically from ChromaDB metadata for every retrieved chunk and appended to every response, regardless of what the LLM generates. This means attribution is structurally guaranteed rather than left to the model to include on its own.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What programming languages are CS undergrad students required to learn?|Java and C++ (from undergraduate.pdf) | Correctly identified Java and C++ as required languages| Partially relevant| Accurate|
| 2 |What specialization does the CS department recommend for a graduate student that wishes to pursue a PhD? | Computation track (from graduate.pdf)| Correctly identified the Computation track as recommended for doctoral studies|Partially relevant | Accurate|
| 3 | Are Professor Ziegler's exams pen and paper? Short answers or multiple choice? And are they allowed a cheat sheet?| Pulled from Discord|Found partial information — noted that some professors allow cheat sheets but couldn't confirm for Ziegler specifically. Correctly said it didn't have enough information rather than guessing | Partially relevant|Partially accurate |
| 4 |What negative feedback do students give about Professor Ziegler? |Pulled from Discord |Returned 5 specific complaints grounded entirely in Discord content: poor lecture skills, vague instructions, stressful assignments, reads from slides | Relevant| Accurate|
| 5 |If I take the expedited masters, does taking the graduate level computer theory course fulfill both undergrad and grad requirements at the same time? | Pulled from department website|Returned "I don't have enough information on that" despite relevant content existing in the Discord export | Off-target| Inaccurate|

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

**Question that failed:** "If I take the expedited masters, does taking the graduate level computer theory course fulfill both undergrad and grad requirements at the same time?"

**What the system returned:** "I don't have enough information on that." even though the Discord export contained a message from Professor Chuang discussing how courses count toward graduation requirements in the expedited masters program.

**Root cause (tied to a specific pipeline stage):** This is a retrieval failure. The relevant Discord chunk existed in the corpus but was not ranked in the top 5 results because the query language ("expedited masters", "fulfill both requirements") didn't semantically match the language used in the Discord message ("capstone courses", "24 credits of advanced courses"). The embedding model couldn't bridge the gap between the query phrasing and the document phrasing, so the relevant chunk was never passed to the LLM.

**What you would change to fix it:**  Query expansion or rephrasing before retrieval would help, either automatically generating alternative phrasings of the query or using a hybrid search approach that combines semantic search with keyword matching to catch exact term matches like "expedited masters."

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The spec's advice to test retrieval before adding generation was critical. Early retrieval tests revealed that distance scores were consistently above 0.7, which led to debugging the chunking strategy and reducing chunk size from 350 to 200 tokens. Without that intermediate checkpoint, those retrieval failures would have been much harder to diagnose after the LLM was already wired in.

**One way your implementation diverged from the spec, and why:** The spec suggested using LangChain for chunking and pipeline management, but the implementation used manual chunking instead. After reviewing a prior project that used a similar sliding window approach, it was clear that LangChain added abstraction without adding value for a corpus this size. Writing the chunking function manually made it easier to debug chunk boundaries and understand exactly what was being embedded.

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

- *What I gave the AI:* The Chunking Strategy section of planning.md, the document list, and the pipeline diagram
- *What it produced:* A chunk_text() function using a sliding window with configurable chunk size and overlap, and separate loader functions for PDFs, txt files, and HTML exports
- *What I changed or overrode:* The initial chunk size was 350 tokens, which was later reduced to 200 after retrieval testing showed that chunks were too large and mixing multiple topics together, causing retrieval to return off target results



**Instance 2**

- *What I gave the AI:* The Retrieval Approach section of planning.md, the ChromaDB setup, and the Groq model choice
- *What it produced:* The embed.py and query.py files including the grounding prompt, retrieval function, and Gradio interface skeleton
- *What I changed or overrode:* The initial implementation re-embedded all chunks every time the app was launched. This was changed to check collection.count() first and skip embedding if the database already existed, reducing startup time from ~30 seconds to instant

---

## Query Interface
The interface is built with Gradio and runs locally at http://localhost:7860. It has two input/output fields:

- Input: A text box labeled "Your question" where the user types a natural language query
- Output 1: A text box labeled "Answer" showing the LLM-generated response grounded in retrieved chunks
- Output 2: A text box labeled "Retrieved from" listing the source documents the answer drew from

To run the interface:
```bash
python embed.py   # only needed once to build the database
python app.py     # launches the interface
```

**Sample interaction transcript:**

**Question:** What negative feedback do students give about Professor Ziegler?

**Answer:** Students give the following negative feedback about Professor Ziegler:

1. He is a disagreeable and not very lenient professor.
2. He has poor lecture skills, with one student observing that he just reads straight from the slides.
3. His assignments can be stressful and require several hours of work, with some students finding it difficult to parse what he expects them to do based on the instructions.
4. His class is considered hard, with big homework assignments.
5. wo hours of his lecture twice a week for 15 weeks can be overwhelming for some students.

Retrieved from:
- bc_csclub_discord.html

---

## Out of scope query example
**Question:** What is the best pizza place near campus?

**Answer:** I don't have enough information on that.
Retrieved from:
- undergraduate.pdf
- graduate.pdf
- bc_csclub_discord.html
- cs_department.txt
