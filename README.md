# 🔍 JobMatchAI - Resume Job Matcher Using Vector Database

This project demonstrates the use of a **vector database** for **semantic search**.
Users can paste their skills/experience or upload a PDF resume, and the app finds the **top 5 most
relevant jobs** from the database using AI embeddings and cosine similarity, not simple keyword matching.

---

## 🛠️ Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Backend         | Django 4.x (Python)                 |
| Vector Database | ChromaDB (local, persistent)        |
| Embeddings      | sentence-transformers (`all-MiniLM-L6-v2`) |
| PDF Parsing     | pdfplumber                          |
| Frontend        | Django HTML Templates + Vanilla CSS |

---

## 📁 Project Structure

```
VectorDB/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── chroma_db/                         # ChromaDB persistent storage (auto-created)
├── media/                             # Uploaded PDF files (auto-created)
│
├── core/                              # Django project settings
│   ├── settings.py
│   └── urls.py
│
└── matcher/                           # Main Django app
    ├── views.py                       # Page views (index, results, how it works)
    ├── urls.py                        # URL routing
    ├── vector_db.py                   # ChromaDB helpers (embed + search)
    │
    ├── management/
    │   └── commands/
    │       └── seed_jobs.py           # Command to populate ChromaDB with 55+ jobs
    │
    ├── templatetags/
    │   └── matcher_filters.py         # Custom template filter (trim whitespace)
    │
    ├── templates/matcher/
    │   ├── base.html                  # Layout (navbar + footer)
    │   ├── index.html                 # Home page (input form)
    │   ├── results.html               # Top 5 results page
    │   └── how_it_works.html          # Explanation page
    │
    └── static/matcher/
        └── style.css                  # Stylesheet
```

---

## ⚙️ Setup Instructions

### 1. Prerequisites

Make sure you have:
- **Python 3.9+** installed
- `pip` available

### 2. Clone / Navigate to the Project

```bash
cd /path/to/VectorDB
```

### 3. (Optional) Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/Mac
# venv\Scripts\activate        # Windows
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ **Note:** `sentence-transformers` is a large package (~500MB) and will also download the
> AI model (`all-MiniLM-L6-v2`, ~90MB) on first run. This is a one-time download.

### 5. Run Django Migrations

```bash
python3 manage.py migrate
```

### 6. Seed the Database

This command embeds 55+ job listings into ChromaDB. **Run this once** before using the app.

```bash
python3 manage.py seed_jobs
```

Expected output:
```
Connecting to ChromaDB...
Embedding and inserting 55 jobs into ChromaDB...
  [1/55] Embedded: Software Engineer
  [2/55] Embedded: Frontend Developer
  ...
✓ Successfully seeded 55 jobs into ChromaDB!
```

### 7. Run the Development Server

```bash
python3 manage.py runserver
```

Open your browser and go to: **http://127.0.0.1:8000/**

---

## 🚀 How to Use

1. Open **http://127.0.0.1:8000/**
2. Choose one of two input methods:
   - **Type Skills** - paste a description of your experience and skills
   - **Upload PDF Resume** - upload a `.pdf` file (text will be extracted automatically)
3. Click **"Find Matching Jobs"**
4. View your **Top 5 Matching Jobs** with similarity scores

---

## 📖 How Semantic Search Works

Unlike keyword search (which requires exact word matches), semantic search understands **meaning**.

### Step-by-step:

1. **Seeding**: Each job description is converted into a 384-dimensional vector (embedding) by the
   `all-MiniLM-L6-v2` model and stored in ChromaDB.

2. **User Input**: Your text/resume is also converted to a vector using the same model.

3. **Search**: ChromaDB computes the **cosine similarity** between your vector and every job vector.
   This measures how "close" the two meanings are in mathematical space.

4. **Results**: The top 5 jobs with the highest similarity scores are returned.

### Why is it better than keyword search?

| Input | Keyword Match | Semantic Match |
|---|---|---|
| "ICU nurse experience" | Only finds exact matches | Also finds "critical care professional", "healthcare worker" |
| "Python developer" | Only finds "Python" | Also finds "software engineer", "data scientist" |

---

## 🗂️ Job Categories Included

The database covers **55+ jobs** across 20+ fields:

- Software Engineering (Frontend, Backend, Mobile, DevOps)
- Data Science & AI (Data Scientist, ML Engineer, BI Developer)
- Healthcare (Nurse, Doctor, Pharmacist, Physical Therapist)
- Education (Teacher, Lecturer, Online Instructor)
- Finance & Accounting (Accountant, Analyst, Investment Banker)
- Marketing & Sales
- Design (Graphic Design, UI/UX, Interior Design)
- Engineering (Mechanical, Civil, Electrical, Chemical)
- Legal & HR
- Culinary Arts & Hospitality
- Architecture & Construction
- Journalism & Communications
- Supply Chain & Logistics
- Psychology & Social Work
- Agriculture & Environmental Science

---

## 🧪 Testing the Search

Try these inputs to see how semantic search works:

| Input | Expected Top Results |
|---|---|
| "I am a nurse with ICU experience" | Registered Nurse, ICU Nurse, Physical Therapist |
| "Python machine learning data analysis" | Data Scientist, ML Engineer, Data Analyst |
| "I design logos and marketing materials in Photoshop" | Graphic Designer, UI/UX Designer, Brand Manager |
| "I build roads and bridges, structural analysis" | Civil Engineer, Construction Manager, Architect |
| "cooking, menu planning, kitchen management" | Executive Chef, Pastry Chef, Hotel Manager |

---

## 📝 Notes

- The `chroma_db/` folder stores all vector data persistently - you only need to run `seed_jobs` once.
- To re-seed (e.g., after adding more jobs), run `python3 manage.py seed_jobs` again.
- No login or authentication is required - the app is open to all users.
- The AI model is downloaded automatically on first run.

---

## 👨‍🎓 Project Info

- **Course**: Advance Database Management Systems
- **Objective**: Demonstrate the use of a vector database and embeddings for semantic search
- **Stack**: Django + ChromaDB + sentence-transformers
