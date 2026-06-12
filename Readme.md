# AI Resume Analyzer

An AI-powered Resume Analyzer built with Flask and Python that evaluates resumes, generates ATS scores, identifies skill gaps, suggests improvements, creates interview questions, and provides personalized career recommendations.

## Features

* User Authentication (Sign Up / Login)
* Resume Upload (PDF & DOCX)
* ATS Score Analysis
* Skill Gap Identification
* Resume Strengths & Weaknesses Analysis
* AI-Generated Interview Questions
* Career Roadmap Recommendations
* Analysis History Tracking
* Secure Password Hashing
* Database Integration with SQLAlchemy

## Tech Stack

### Backend

* Python
* Flask
* SQLAlchemy
* Werkzeug

### AI & NLP

* Backboard AI API

### File Processing

* PyPDF2
* python-docx

### Frontend

* HTML5
* CSS3
* Jinja2 Templates

### Database

* SQLite (Development)

## Project Structure

```text
resume-analyzer/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   └── history.html
│
├── ai.py
├── app.py
├── db.py
├── models.py
├── reset_db.py
├── requirements.txt
├── .env
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git

cd ai-resume-analyzer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///resume_analyzer.db
BACKBOARD_API_KEY=your_api_key
```

## Run Application

```bash
python app.py
```

Application will start at:

```text
http://127.0.0.1:5000
```

## How It Works

1. User uploads a PDF or DOCX resume.
2. Resume text is extracted and processed.
3. AI analyzes resume content against the selected role.
4. ATS score and recommendations are generated.
5. Analysis results are stored in the database.
6. Users can view previous reports from their dashboard.

## Future Improvements

* Resume Keyword Matching
* Multiple Resume Templates
* LinkedIn Profile Analysis
* Resume PDF Report Export
* Email Notifications
* Admin Dashboard
* Job Recommendation Engine

## Security Features

* Password Hashing
* Session-Based Authentication
* Environment Variable Protection
* Secure Database Queries using SQLAlchemy ORM

## Author

Your Name

## License

This project is intended for educational and portfolio purposes.
