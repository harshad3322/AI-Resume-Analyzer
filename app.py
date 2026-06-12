import re

from dotenv import load_dotenv

load_dotenv()

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from db import (
    Base,
    engine,
    SessionLocal
)

from ai import analyze_resume

import models
from pypdf import PdfReader
import docx
import json
import os
import re

from flask_wtf.csrf import CSRFProtect








app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")



if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not configured."
    )

app.config["SECRET_KEY"] = SECRET_KEY

csrf = CSRFProtect(app)

app.config[
    "MAX_CONTENT_LENGTH"
] = 10 * 1024 * 1024

Base.metadata.create_all(bind=engine)

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}

EMAIL_REGEX = (
    r"^[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+"
    r"\.[A-Za-z]{2,}$"
)


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():

    if "user_id" in session:
        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


@app.route(
    "/signup",
    methods=["GET", "POST"]
)
def signup():

    if request.method == "POST":

        email = (
            request.form.get(
                "email",
                ""
            )
            .strip()
            .lower()
        )

        password = request.form.get(
            "password",
            ""
        )

        if not re.match(
            EMAIL_REGEX,
            email
        ):
            flash(
                "Invalid email address."
            )
            return redirect(
                url_for("signup")
            )

        if len(password) < 8:
            flash("Password must be at least 8 characters long.")
            return redirect(url_for("signup"))

        if not re.search(r"[A-Z]", password):
            flash("Password must contain at least one uppercase letter.")
            return redirect(url_for("signup"))

        if not re.search(r"[a-z]", password):
            flash("Password must contain at least one lowercase letter.")
            return redirect(url_for("signup"))

        if not re.search(r"\d", password):
            flash("Password must contain at least one number.")
            return redirect(url_for("signup"))

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            flash("Password must contain at least one special character.")
            return redirect(url_for("signup"))

        db = SessionLocal()

        try:

            existing_user = (
                db.query(
                    models.User
                )
                .filter_by(
                    email=email
                )
                .first()
            )

            if existing_user:
                flash(
                    "Account already exists."
                )
                return redirect(
                    url_for("signup")
                )

            user = models.User(
                email=email,
                password=generate_password_hash(
                    password
                )
            )

            db.add(user)
            db.commit()

            flash(
                "Account created successfully."
            )

            return redirect(
                url_for("login")
            )

        finally:
            db.close()

    return render_template(
        "signup.html"
    )


@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = (
            request.form.get(
                "email",
                ""
            )
            .strip()
            .lower()
        )

        password = request.form.get(
            "password",
            ""
        )

        db = SessionLocal()

        try:

            user = (
                db.query(
                    models.User
                )
                .filter_by(
                    email=email
                )
                .first()
            )

            if (
                user
                and check_password_hash(
                    user.password,
                    password
                )
            ):

                session["user_id"] = user.id
                session["email"] = user.email

                return redirect(
                    url_for(
                        "dashboard"
                    )
                )

            flash(
                "Invalid credentials."
            )

            return redirect(
                url_for("login")
            )

        finally:
            db.close()

    return render_template(
        "login.html"
    )


@app.route(
    "/dashboard",
    methods=["GET", "POST"]
)
def dashboard():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    result = None

    if request.method == "POST":

        user_goal = (
            request.form.get(
                "role",
                ""
            )
            .strip()
        )

        resume_text = (
            request.form.get(
                "resume",
                ""
            )
            .strip()
        )

        file = request.files.get(
            "file"
        )

        if file and file.filename:

            filename = secure_filename(
                file.filename
            )

            if not allowed_file(
                filename
            ):
                result = {
                    "error":
                    "Only PDF and DOCX files are allowed."
                }

            elif filename.lower().endswith(
                ".pdf"
            ):

                try:

                    reader = PdfReader(file)

                    text = ""

                    for page in reader.pages:

                        text += (
                            page.extract_text()
                            or ""
                        )

                    if not text.strip():

                        result = {
                            "error":
                            "No readable text found in PDF."
                        }

                    else:
                        resume_text = text

                except Exception as e:

                    result = {
                        "error":
                        f"PDF error: {str(e)}"
                    }

            elif filename.lower().endswith(
                ".docx"
            ):

                try:

                    document = (
                        docx.Document(
                            file
                        )
                    )

                    text = "\n".join(
                        para.text
                        for para in document.paragraphs
                    )

                    if not text.strip():

                        result = {
                            "error":
                            "No readable text found in DOCX."
                        }

                    else:
                        resume_text = text

                except Exception as e:

                    result = {
                        "error":
                        f"DOCX error: {str(e)}"
                    }

        if (
            not resume_text
            and not result
        ):

            result = {
                "error":
                "Please paste a resume or upload a file."
            }

        if (
            resume_text
            and user_goal
            and not result
        ):

            try:

                result = analyze_resume(
                    resume_text,
                    user_goal
                )

                db = SessionLocal()

                try:

                    report = (
                        models.Report(
                            user_id=session[
                                "user_id"
                            ],
                            target_role=user_goal,
                            ats_score=result.get(
                                "ats_score",
                                0
                            ),
                            resume_text=resume_text,
                            result=json.dumps(
                                result
                            )
                        )
                    )

                    db.add(report)
                    db.commit()

                finally:
                    db.close()

            except Exception as e:

                result = {
                    "error":
                    f"AI error: {str(e)}"
                }

    return render_template(
        "dashboard.html",
        user=session.get(
            "email"
        ),
        result=result
    )


@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    db = SessionLocal()

    try:

        reports = (
            db.query(
                models.Report
            )
            .filter_by(
                user_id=session[
                    "user_id"
                ]
            )
            .order_by(
                models.Report.id.desc()
            )
            .all()
        )

        parsed_reports = []

        for report in reports:

            try:

                parsed_result = (
                    json.loads(
                        report.result
                    )
                )

            except Exception:

                parsed_result = {}

            parsed_reports.append({
                "id": report.id,
                "resume": report.resume_text,
                "target_role":
                report.target_role,
                "ats_score":
                report.ats_score,
                "created_at":
                report.created_at,
                "result":
                parsed_result
            })

        return render_template(
            "history.html",
            reports=parsed_reports
        )

    finally:
        db.close()


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


if __name__ == "__main__":
    app.run()