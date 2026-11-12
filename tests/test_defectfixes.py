import pytest
import registration

from registration import (
    Student,
    Course,
    check_credit_limit,
    prerequisites_satisfied,
    registration_decision,
    register_course,
    withdraw_course
)

#Issue-1
def test_positive_dues():
    student = Student("S01", outstanding_dues=1)
    course = Course("CS301", 3, 30)

    result = registration_decision(student, course)

    assert result == "DUES_BLOCK"

#Issue-2
def test_combined_credits_exactly_18():
    result = check_credit_limit(15, 3)

    assert result == True

#Issue-3 - Course enrollment count is not decreased after student withdrawal
def test_successful_withdrawal():
    student = Student(
        "S05",
        registered_courses={"CS301"},
        current_credits=3
    )

    course = Course("CS301", 3, 30, enrolled=5)

    result = withdraw_course(student, course)

    assert result == True
    assert "CS301" not in student.registered_courses
    assert student.current_credits == 0
    assert course.enrolled == 4