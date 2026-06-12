import asyncio
import json
import os
import re

from dotenv import load_dotenv
import requests

load_dotenv()


async def run_analysis(prompt):

    api_key = os.getenv("BACKBOARD_API_KEY")

    if not api_key:
        raise RuntimeError(
            "BACKBOARD_API_KEY is not configured."
        )

    response = requests.post(
        "https://app.backboard.io/api/threads/messages",
        headers={
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        },
        json={
            "content": prompt
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "content",
        ""
    )




def analyze_resume(resume_text, user_goal):

    try:

        resume_text = (resume_text or "").strip()
        user_goal = (user_goal or "").strip()

        if not resume_text:
            return {
                "error": "Resume is empty",
                "ats_score": 0,
                "skills": [],
                "missing_skills": [],
                "strengths": [],
                "weaknesses": [],
                "roadmap": [],
                "interview_questions": []
            }

        if not user_goal:
            return {
                "error": "Career goal required",
                "ats_score": 0,
                "skills": [],
                "missing_skills": [],
                "strengths": [],
                "weaknesses": [],
                "roadmap": [],
                "interview_questions": []
            }

        prompt = f"""
You are a professional resume analyzer and hiring manager.

Analyze the resume for the target role below.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Do NOT add explanations.
3. Do NOT add markdown.
4. Do NOT add text before JSON.
5. Do NOT add text after JSON.

JSON FORMAT:

{{
    "ats_score": 0,
    "skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "roadmap": [],
    "interview_questions": []
}}

RULES:

- ats_score must be an integer from 0 to 100.
- skills must be an array.
- missing_skills must be an array.
- strengths must be an array.
- weaknesses must be an array.
- roadmap must be an array.
- interview_questions must be an array.

TARGET ROLE:
{user_goal}

RESUME:
{resume_text[:12000]}
"""

        content = asyncio.run(
            run_analysis(prompt)
        )

        if not content:
            raise ValueError(
                "Empty response from AI"
            )

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        match = re.search(
            r"\{.*\}",
            content,
            re.DOTALL
        )

        if not match:
            raise ValueError(
                "JSON not found in AI response"
            )

        result = json.loads(
            match.group(0)
        )

        result.setdefault(
            "ats_score",
            0
        )

        result.setdefault(
            "skills",
            []
        )

        result.setdefault(
            "missing_skills",
            []
        )

        result.setdefault(
            "strengths",
            []
        )

        result.setdefault(
            "weaknesses",
            []
        )

        result.setdefault(
            "roadmap",
            []
        )

        result.setdefault(
            "interview_questions",
            []
        )

        try:
            score = int(
                result.get(
                    "ats_score",
                    0
                )
            )
        except Exception:
            score = 0

        result["ats_score"] = max(
            0,
            min(100, score)
        )

        for key in [
            "skills",
            "missing_skills",
            "strengths",
            "weaknesses",
            "roadmap",
            "interview_questions"
        ]:

            if not isinstance(
                result[key],
                list
            ):
                result[key] = []

        return result

    except Exception as e:

        return {
            "error": str(e),
            "ats_score": 0,
            "skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "roadmap": [],
            "interview_questions": []
        }