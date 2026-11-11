
import pytest
from registration import (
    Student,
    Course,
    check_credit_limit,
    prerequisites_satisfied,
    registration_decision,
    register_course,
    withdraw_course
)


# ST-01: Dues exceed the allowed threshold
def test_high_dues_block():
    student = Student("S01", outstanding_dues=1001)
    course = Course("CS201", 3, 30)

    assert registration_decision(student, course) == "DUES_BLOCK"


# ST-02: Dues exactly at the threshold
def test_dues_at_threshold():
    student = Student("S01", outstanding_dues=1000)
    course = Course("CS201", 3, 30)

    assert registration_decision(student, course) == "REGISTERED"


# ST-03: All prerequisites must be completed
def test_prerequisites_superset():
    completed = {"CS101", "MATH101", "PHY101"}
    required = {"CS101", "MATH101"}

    assert prerequisites_satisfied(completed, required) is True


# ST-04: Missing even one prerequisite
def test_prerequisites_missing_one():
    completed = {"CS101"}
    required = {"CS101", "MATH101"}

    assert prerequisites_satisfied(completed, required) is False


# ST-05: Exact credit boundary
def test_credit_limit_exact_boundary():
    assert check_credit_limit(17, 1) is True


# ST-06: Duplicate registration must not modify state
def test_duplicate_registration_no_state_change():
    student = Student(
        "S01",
        current_credits=6,
        registered_courses={"CS201"}
    )
    course = Course("CS201", 3, 30, enrolled=10)

    result = register_course(student, course)

    assert result == "ALREADY_REGISTERED"
    assert student.current_credits == 6
    assert course.enrolled == 10


# ST-07: Withdrawal without registration
def test_withdraw_non_registered_course():
    student = Student("S01", current_credits=6)
    course = Course("CS201", 3, 30, enrolled=10)

    assert withdraw_course(student, course) is False
    assert student.current_credits == 6
    assert course.enrolled == 10


# ST-08: Invalid enrollment must raise an exception
def test_enrollment_exceeds_capacity():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=31)

    with pytest.raises(ValueError):
        registration_decision(student, course)
