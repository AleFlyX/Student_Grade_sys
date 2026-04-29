from dataclasses import dataclass


@dataclass
class User:
    student_id: str
    name: str
    major: str | None = None
    grade: str | None = None
