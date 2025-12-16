# 🎓 Campus Companion

**AI-Powered Campus Information Assistant for NIT Durgapur**

# Tech-Stacks used:

# Backend API : FastAPI + Uvicorn
# Database : SQLite3
# Vector Storage : ChromaDB(internally using SQLite3)
# Embeddings : Sentence Transformers -> 384-dim vectors
# Frontend : StreamLit
# PDF Loading : PyPDF Loader
# Classification : Keyword -> Logistic Regression(ML) -> LLM
# LLM : OpenSource Model from HuggingFace : Mistral-7B-Instruct

# Project FlowChart

```
┌──────────────────────────────────────────────────────────────────┐
│                     CAMPUS COMPANION SYSTEM                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  USER QUERY → FastAPI Backend → 3-Level Classification           │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  INTENT CLASSIFIER (core/classifier.py)                     │ │
│  │                                                              │ │
│  │  Level 1: Keyword Matching (⚡ 0.001s) - 70% queries        │ │
│  │  Level 2: ML Classifier (⚡⚡ 0.01s) - 25% queries          │ │
│  │  Level 3: LLM (Mistral-7B) (⚡⚡⚡ 1-2s) - 5% queries       │ │
│  └──────────────────────┬───────────────────────────────────────┘ │
│                         │                                          │
│         ┌───────────────┼───────────────┐                         │
│         ▼               ▼               ▼                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                 │
│  │ DATABASE   │  │ RAG SYSTEM │  │ AI FALLBACK│                 │
│  │            │  │            │  │            │                 │
│  │ • Canteen  │  │ • ChromaDB │  │ Mistral-7B │                 │
│  │ • Faculty  │  │ • 384-dim  │  │ Generates  │                 │
│  │ • Rooms    │  │   Vectors  │  │ Responses  │                 │
│  │ • Wardens  │  │ • Cosine   │  │            │                 │
│  │ (SQLite)   │  │   Search   │  │            │                 │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘                 │
│        │               │               │                         │
│        └───────────────┼───────────────┘                         │
│                        ▼                                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  AI RESPONSE FORMATTER (core/response.py)                   │ │
│  │  Raw Data → Natural Language (Mistral-7B, Temp: 0.5)       │ │
│  └────────────────────┬───────────────────────────────────────┘ │
│                       ▼                                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  JSON RESPONSE                                              │ │
│  │  {"answer": "...", "intent": "...", "confidence": 0.85}    │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

# Project Structure
```
## 📁 Project Structure

```
CAMPUS_COMPANION/
├── api/
│   ├── main.py                    # FastAPI app initialization
│   └── routers/
│       └── chat.py                # ⭐ Main chat endpoint (600+ lines)
├── core/
│   ├── classifier.py              # ⭐ 3-level intent classification (800+ lines)
│   ├── rag.py                     # ⭐ RAG system with ChromaDB (190+ lines)
│   ├── response.py                # 🤖 AI response formatter
│   ├── fallback_message.py        # 🛡️ AI fallback handler
│   ├── embeddings.py              # Document chunking & embeddings
│   └── ocr_utils.py               # PDF/OCR processing
├── db/
│   ├── models.py                  # ⭐ Database schema (10 tables)
│   └── session.py                 # DB connection
├── scripts/
│   ├── ingest_pdfs.py             # PDF → ChromaDB pipeline
│   ├── pdf_processor.py           # Text extraction (PyPDF2 + Tesseract)
│   └── chunking.py                # Text chunking logic
├── data/
│   ├── pdfs/                      # Source PDF documents
│   └── rag_docs/                  # ChromaDB storage
├── frontend.py                    # Streamlit chat UI
├── app.py                         # Database initializer
├── testdb.py                      # Sample data loader
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables
└── campus_companion.db            # SQLite database
```
```

# ========================================================================
# DAY 0 : Setup
# ========================================================================

# Verify installations
python3 --version    
pip --version
git --version

# Clone and Navigate
git clone <your-repo-url>
cd CAMPUS_COMPANION

# Create virtual environment
python3 -m venv .venv
# Activate (Linux/Mac)
source .venv/bin/activate
# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Get HuggingFace Token
1. Visit: https://huggingface.co/settings/tokens
2.  Create token (Read access)
3. Copy token
# Create .env file
echo "HUGGINGFACEHUB_API_TOKEN=hf_paste_your_token_here" > .env

# Initialise Database
python3 app.py
python3 testdb.py

# Create data folder
mkdir -p data/pdfs
# Add a sample PDF (students can use any PDF)
# Then run:
python3 scripts/ingest_pdfs.py

# Start backend
uvicorn api.main:app --reload

# Test chat (in new terminal)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text":"hello"}'

# Start frontend (on another terminal with .venv activated)
streamlit run frontend.py



# ========================================================================
# DAY 1 : DB Setup & AI Fallback
# ========================================================================

Show how to use SQLite3 extension and view db tables

# DB 
The Problem: How does the system know what type of question was asked?

Solution: Progressive complexity with fallback

# Level 1: Keyword Matching (Fast - 0.001s)
Handles: 70% of queries
Method: Simple word detection
Example: "phone" + "canteen" = contact query
Function: classify_keyword() in classifier.py
When it works:

"Roy canteen phone" → Keywords found → db_contact
"Where is AB-301?" → Keywords found → db_location
When it fails:

"I need to contact the mess" → No exact keywords → Move to Level 2

# Level 2: Machine Learning (Medium - 0.01s)
Handles: 25% of queries
Method: TF-IDF + Logistic Regression
Training: Pre-trained on 200+ example queries
Function: ml_classify() in classifier.py

How it works:

Converts text to numerical features (word importance)
Trained model predicts intent
Example: "mess contact" → ML recognizes as contact query
When it works:

Variations of known patterns
Synonyms and paraphrases
When it fails:

Completely novel phrasing
Ambiguous questions
Move to Level 3

# Level 3: LLM Classification (Slow ~ 1-2s)
# Allot HW

Hints:
Sends query to Mistral-7B with instructions
"Classify this as: contact/location/rag/small_talk/fallback"
Returns intent with reasoning
When it's used:

"Can you help me reach the person in charge of food services?" → LLM understands context → db_contact

# What's in the Database?
8-10 tables in SQLite: Faculty, Canteen, Warden, Room, Building, etc.
Fixed schema (columns known in advance)
Fast exact matches

# Key functions
try_get_contact(text, session) - Search people/places
try_get_location(text, session) - Search rooms/buildings
extract_entity_names() - Parse query for names


# AI Fallback
Concept: Graceful handling of out-of-scope queries

When Fallback Triggers:
Intent classified as "ai_fallback"
Database search returns nothing
RAG(which we will be covering tomorrow) search finds no relevant documents
Confidence too low (< 0.3)

# Generate response
Send query + system prompt to Mistral-7B
Temperature: 0.7 (more creative for deflection)
Explain temperature
AI generates polite refusal + redirection + organised

# Key function
fallback_ai_response(query) in fallback_message.py

# Hands-on Exercise
Edit testdb.py
add and populate data of your choice

# Functions Involved:
session.add() - Add to database
session.commit() - Save changes
try_get_contact() - Search function

AI Fallback System
Purpose: Handle queries outside campus scope gracefully





# ========================================================================
# DAY 2 : RAG
# ========================================================================

Understand RAG (Retrieval Augmented Generation) concept
Learn PDF processing pipeline (extraction → chunking → embedding)
Understand semantic search and cosine similarity

# Sample Example
The Problem: Student asks "How to calculate CGPA?"

Why Database Won't Work:
CGPA calculation is a multi-step explanation (not a single data point)
Rules are in PDF documents (Academic Handbook, 50+ pages)
Manual data entry = tedious + error-prone
Rules change → Need to update database every time (data scraping cover if your choice)

# Why not raw AI ? 
LLMs hallucinate
No existing knowledge of the campus rules 
CGPA varies from campus to campus

# Functioning of RAG:
PDFs → Extract Text → Split into Chunks → Convert to Vectors → Store in Database
User Question → Convert to Vector → Find Similar Vectors → Get Text Chunks
Question + Context Chunks → LLM → Natural Answer

# PDF Processing Pipeline
Functioning of PDF Loader:
1. Open PDF file
2. Iterate through each page
3. Extract text layer (embedded text data)
4. Concatenate all pages

# Key Functions:
extract_text_pypdf2() in pdf_processor.py

Function of Text Cleaning: 
Removes Noise : page numbers, urls, headers/footers, whitespaces

# Key Functions:
clean_text() in pdf_processor.py

Quality Check: check the length of answer and whether it is in readable format

# Key Function:
validate_extracted_text() in pdf_processor.py


# Concept and need of Chunking
Embedding models have token limits for each query
Semantic search less accurate and more tokens -> higher API cost

Solution: Split into smaller, semantically meaningful pieces

Chunking parameters : chunk_size, chunk_overlap, min_chunk_size

# Key Function:
chunk_text() in chunking.py

# Concept of embedding
# Embedding Model Used: all-MiniLM-L6-v2 (Sentence Transformers)
Concept: Convert text into numbers that capture meaning

Example:
Text: "How to calculate CGPA?"
Embedding: [0.234, -0.112, 0.567, ..., 0.891]  (384 numbers)

"CGPA calculation" → [0.12, 0.45, -0.23, ...]
"Grade point average" → [0.15, 0.43, -0.20, ...]  (CLOSE! ✅)
"Pizza recipe" → [0.87, -0.32, 0.61, ...]  (FAR! ❌)

# Key Function:
get_embeddings() in embeddings.py

Generate embeddings:
# Func : 
generate_embeddings() in embeddings.py

# VectorDB -> ChromaDB
Stores all the embeddings for semantic search


# Hands-on Exercise
# 1. Add PDF to data folder
cp ~/hostel_rules.pdf data/pdfs/

# 2. Run ingestion
python3 scripts/ingest_pdfs.py

# 3. Check ChromaDB
python3 -c "from core.rag import collection; print(f'{collection.count()} documents')"

# 4. Test query
curl -X POST http://localhost:8000/api/chat \
  -d '{"text":"What are hostel visiting hours?"}'




# ========================================================================
# DAY 3 : Classifier
# ========================================================================

Problem: When a user asks "Roy canteen phone", how does the system know they want contact information and not location or rules?

Solution: Intent Classification - categorizing user queries into predefined intents.

# Intent Types in Campus Companion:
db_contact - Contact information (phone, email)
db_location - Location queries (rooms, buildings)
rag - Document-based questions (CGPA rules, policies)
ai_fallback - General questions / greetings
small_talk [HW]

# Three_Level Classification:
Keyword matching (Fast) -> Machine Learning (Accurate) -> LLM (Slow but most Accurate) [HW]

# Key Functions to discuss:
classify_keywords(text: str) -> IntentResult

Purpose: Fast rule-based classification using keyword matching

# Priority order matters!!!!!!
1. Check for RAG keywords → "CGPA", "rules", "policy"
2. Check for contact keywords → "phone", "email", "canteen"
3. Check for location keywords → "where", "room", "building"
4. Default → ai_fallback

# Why?
RAG first because academic queries are most specific
Contact/Location second because they have clear entities
Fallback last as catch-all


# Concept of ML
# Key Function:
MLClassifier Class

Purpose: Learn patterns from training examples using Machine Learning
Understand in brief:
1. TF-IDF Vectorizer
2. Logistic Regression

# The Orchestrator
UnifiedClassifier.classify()
Purpose: Combine all three classifiers and make final decision

# Classification Pipeline: 
Step 1: Run keyword classifier (always)
  ↓
Step 2: Run ML classifier (if trained)
  ↓
Step 3: Run LLM classifier (if requested AND confidence < 0.7)
  ↓
Step 4: Aggregate results by taking MAX confidence per intent
  ↓
Step 5: Detect multi-intent queries
  ↓
Step 6: Determine if AI fallback needed
  ↓
Return ClassificationResult

# Result Aggregation Strategy: 
Why MAX (not AVG)?

If one classifier is very confident, it likely found a strong signal
Average would dilute strong predictions
Example: Keyword (0.90) + ML (0.60) → MAX=0.90 (better than AVG=0.75)

[HW] Multi-intent Discussion




# ========================================================================
# DAY 4 : Response Generation + Frontend
# ========================================================================





