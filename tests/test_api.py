from app.services.scoring import (
    score_multi_choice,
    score_number,
    score_single_choice,
    score_text,
)

SAMPLE_JOB = {
    "title": "Backend Engineer",
    "location": "Berlin",
    "customer": "Acme",
    "job_name": "Python Dev",
    "description": "Build APIs",
    "questions": [
        {
            "text": "Main language?",
            "type": "single_choice",
            "scoring": {"correctOption": "Python", "points": 10},
        },
        {
            "text": "Years of experience?",
            "type": "number",
            "scoring": {"min": 1, "max": 5, "points": 10},
        },
    ],
}


def create_test_job(client):
    return client.post("/jobs/", json=SAMPLE_JOB)


# ── API tests ──────────────────────────────────────────────


def test_apply_to_nonexistent_job(client):
    response = client.post(
        "/jobs/9999/apply",
        json={
            "candidate_name": "John Doe",
            "candidate_email": "john@test.com",
            "answers": [{"question_id": 1, "response": "Python"}],
        },
    )
    assert response.status_code == 404


def test_job_can_have_multiple_questions(client):
    response = create_test_job(client)
    assert response.status_code == 201
    assert len(response.json()["questions"]) == 2


def test_correct_answer_scores_full(client):
    job = create_test_job(client)
    job_id = job.json()["id"]
    question_id = job.json()["questions"][0]["id"]

    response = client.post(
        f"/jobs/{job_id}/apply",
        json={
            "candidate_name": "John Doe",
            "candidate_email": "john@test.com",
            "answers": [{"question_id": question_id, "response": "Python"}],
        },
    )
    assert response.status_code == 201
    assert response.json()["score"] == 100.0


def test_wrong_answer_scores_zero(client):
    job = create_test_job(client)
    job_id = job.json()["id"]
    question_id = job.json()["questions"][0]["id"]

    response = client.post(
        f"/jobs/{job_id}/apply",
        json={
            "candidate_name": "John Doe",
            "candidate_email": "john@test.com",
            "answers": [{"question_id": question_id, "response": "Java"}],
        },
    )
    assert response.status_code == 201
    assert response.json()["score"] == 0.0


# ── Scoring unit tests ─────────────────────────────────────


def test_single_choice_correct():
    assert score_single_choice("Python", "Python", 10) == 10


def test_number_in_range():
    assert score_number("3", 1, 5, 10) == 10


def test_multi_choice_partial():
    assert score_multi_choice(["Python"], ["Python", "SQL"], 10) == 5.0


def test_text_partial_keywords():
    assert score_text("I love agile work", ["agile", "teamwork"], 10) == 5.0
