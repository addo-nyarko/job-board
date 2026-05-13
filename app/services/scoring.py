import logging

from app.enums import QuestionType

logger = logging.getLogger(__name__)


def score_single_choice(answer: str, correct_option: str, points: float) -> float:
    if answer.strip().lower() == correct_option.strip().lower():
        return points
    return 0.0


def score_number(answer: str, min_val: float, max_val: float, points: float) -> float:
    try:
        value = float(answer)
        if min_val <= value <= max_val:
            return points
        return 0.0
    except (ValueError, TypeError):
        return 0.0


def score_multi_choice(answers: list[str], correct_options: list[str], points: float) -> float:
    if not correct_options:
        return 0.0
    answers_set = {a.strip().lower() for a in answers}
    correct_set = {c.strip().lower() for c in correct_options}
    overlap = answers_set & correct_set
    return (len(overlap) / len(correct_set)) * points


def score_text(answer: str, keywords: list[str], points: float) -> float:
    if not keywords:
        return 0.0
    answer_lower = answer.lower()
    matched = [kw for kw in keywords if kw.lower() in answer_lower]
    return (len(matched) / len(keywords)) * points


def calculate_score(answers: list[dict], questions) -> float:
    total_possible = 0.0
    total_earned = 0.0

    question_map = {q.id: q for q in questions}

    for answer in answers:
        question = question_map.get(answer["question_id"])
        if not question:
            continue

        scoring = question.scoring
        points = scoring.get("points", 1.0)
        total_possible += points

        q_type = question.type

        if q_type == QuestionType.SINGLE_CHOICE:
            earned = score_single_choice(answer["response"], scoring["correctOption"], points)
        elif q_type == QuestionType.NUMBER:
            earned = score_number(answer["response"], scoring["min"], scoring["max"], points)
        elif q_type == QuestionType.MULTI_CHOICE:
            earned = score_multi_choice(answer["response"], scoring["correctOptions"], points)
        elif q_type == QuestionType.TEXT:
            earned = score_text(answer["response"], scoring["keywords"], points)
        else:
            logger.warning("Unknown question type: %s", q_type)
            earned = 0.0

        total_earned += earned

    if total_possible == 0:
        return 0.0

    return round((total_earned / total_possible) * 100, 1)
