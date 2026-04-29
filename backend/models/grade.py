from dataclasses import dataclass


@dataclass
class Grade:
    course_id: str
    course_name: str
    credit: float
    course_nature: str
    academic_year: str
    semester: str
    score: float
    grade_point: float
    status: str
