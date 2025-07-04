# ASIF_Agent  Admission Support Intelligence Framework
#📘 Tamil Nadu Engineering Admissions (TNEA) AI Agent
An intelligent multi-turn assistant powered by Mistral, LangChain, LangGraph, and Chroma for guiding students through TNEA counseling. This agent leverages retrieval-augmented generation (RAG), tool-injection, and session-aware Django integration.

# 🚀 Features
# 🔍 Tool calling with LangChain

searchy: Internet-backed college search via Google Search API

cutoff_calc: Computes student cutoff from 12th marks

# 🧠 Mistral Chat Model (ChatMistralAI)

Handles contextual multi-turn conversations

Bound to tools for deterministic reasoning

# 📚 Semantic Search with Chroma Vector DB

Uses MistralAIEmbeddings for document retrieval

Supports cutoff lookups by college and department

# 🧩 LangGraph Workflow

Conditional routing based on tool calls

Stateful agent flow: rag → tool → rag → end

#🕵️‍♂️ Django Session Integration

Stores chat history across requests

#Uses request.session to persist interaction context

# 🏗️ Architecture Overview

graph TD
  START --> rag
  rag -->|Tool Call| tool
  tool --> rag
  rag -->|No Tool| END
rag: Agent node invoking Mistral with system prompt + RAG context

tool: Node executing tools like searchy, cutoff_calc

Conditional edge: Decides whether tools are needed before responding

# 📦 Installation
Clone repository

bash
git clone (https://github.com/Yasar26951/ASIF_aiAgent)
cd ASIF
Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

\n
bash
pip install -r requirements.txt
Set environment variables Create a .env file:

env
mistral_api=your_mistral_api_key
google_api_key=your_google_api_key
google_cse_id=your_google_cse_id
Run Django migrations

bash
python manage.py migrate
Start the server

bash
python manage.py runserver
🧮 Cutoff Calculator
Tool computes cutoff score as:

math
Cutoff = Maths + (Physics / 2) + (Chemistry / 2)
Invoked directly via tool node for accurate college recommendations.

🧠 RAG Workflow
Embedding model: mistral-embed

Vector DB: Chroma (stored in chroma_db)

Retriever fetches top 10 documents for user question

Result injected into prompt for grounded responses

📝 Example Prompt Template
jinja
You are a RAG-based agent assisting with Tamil Nadu Engineering Admissions.

Context from documents:
{context}

Web data from search tool:
{search}

Question:
{question}

Based on the above, provide a precise, factual answer. If information is missing, invoke the searchy tool.
# 💬 Django View Example

# 📁 File Structure
plaintext
├── chroma_db/              # Persisted vector store
├── templates/
│   └── chat.html           # Django template for chat interface
├── forms.py                # Django form definition
├── views.py                # Main chat view logic
├── agent.py                # LangGraph flow and tools
├── .env                    # API keys      
└── README.md               # You're reading this
# 🛠️ Tech Stack
Component	Usage
MistralAI	LLM & embeddings (Chat + RAG)
LangGraph	Stateful multi-node workflow
LangChain	Tool binding, vector search
Chroma	Semantic storage & retrieval
Django	Web framework with session support
Google Search	Real-time college info lookups
🙌 Future Extensions
🔑 Authenticated user sessions

🎓 Category-aware cutoff filtering

🗄️ PostgreSQL-backed session persistence

🧠 Persistent memory with LangGraph checkpoints
this agent is loaded with least amount of data  because it is prototype if we finetune and promt instruction properly mean it defenetly use for student real world students who want to become engineer
BY-
Data collection,Django and process -Nithish
model init ,prompt and workflow design -mohamed yasar arafath
