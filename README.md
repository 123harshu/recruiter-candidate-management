# Recruiter Candidate Management

A FastAPI-based web application for managing candidates throughout the recruitment process. The system provides candidate management, recruitment stage tracking, search functionality, and a simple web interface for recruiters.

## 🚀 Features

* Candidate management
* Add and view candidate details
* Recruitment stage tracking
* Candidate search
* Dashboard with recruitment statistics
* Stage transition management
* REST API using FastAPI
* Server-side HTML rendering with Jinja2
* SQLAlchemy database integration
* Automated tests with Pytest
* Seed data support
* Windows setup and run scripts

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **Jinja2**
* **SQLite**
* **Pytest**
* **HTML / CSS / JavaScript**

## 📁 Project Structure

```text
recruiter-candidate-management/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── candidate_service.py
│   │   ├── stage_service.py
│   │   └── search_service.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── candidates.py
│   │   └── pages.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── candidate_detail.html
│   │   └── candidate_form.html
│   │
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── tests/
│   ├── __init__.py
│   ├── test_candidates.py
│   ├── test_stage_transitions.py
│   └── test_search.py
│
├── docs/
│   ├── AI_CHAT_LOG.md
│   ├── ARCHITECTURE.md
│   └── DEMO_SCRIPT.md
│
├── data/
│   └── .gitkeep
│
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── README.md
├── setup.bat
├── run.bat
└── seed.py
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/123harshu/recruiter-candidate-management.git
cd recruiter-candidate-management
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For development and testing:

```bash
pip install -r requirements-dev.txt
```

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`.

```bash
copy .env.example .env
```

Do not commit `.env` to GitHub because it may contain sensitive configuration.

## 🌱 Seed Data

To populate the application with sample candidate data:

```bash
python seed.py
```

## ▶️ Run the Application

You can run the application using:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

You can also use the provided Windows script:

```bash
run.bat
```

## 🧪 Run Tests

Run the complete test suite:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_candidates.py
```

## 🔌 API Documentation

When the FastAPI application is running, API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## 📊 Recruitment Stages

The application supports the following candidate stages:

```text
Applied
   ↓
Screening
   ↓
Interview
   ↓
Offer
   ↓
Hired
```

Stage transitions can be managed through the application services and APIs.

## 🏗️ Architecture

The application follows a layered structure:

```text
Frontend / Jinja2 Templates
            ↓
         Routes
            ↓
        Services
            ↓
      CRUD / Database
            ↓
        SQLAlchemy
            ↓
         SQLite
```

* **Routes** handle HTTP requests.
* **Services** contain business logic.
* **CRUD** handles database operations.
* **Models** define database entities.
* **Schemas** define request/response validation.
* **Templates** provide the web interface.
* **Tests** validate application functionality.

## 🧪 Testing

The project includes tests covering:

* Candidate creation and retrieval
* Candidate stage transitions
* Candidate search functionality

Testing is implemented using Pytest.

## 📌 Future Improvements

Potential enhancements include:

* Authentication and role-based access
* Recruiter accounts
* Resume upload and parsing
* Email notifications
* Advanced candidate filtering
* Interview scheduling
* Analytics and reporting
* PostgreSQL support
* Docker deployment
* CI/CD pipeline

## 👩‍💻 Author

**Harshita Verma**

GitHub: [123harshu](https://github.com/123harshu)

---

⭐ If you find this project useful, feel free to star the repository.
