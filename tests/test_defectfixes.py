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

