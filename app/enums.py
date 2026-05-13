from enum import Enum


class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"
    NUMBER = "number"
    TEXT = "text"
