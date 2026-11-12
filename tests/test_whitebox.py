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


# 1. Tests for check_credit_limit()

def test_credit_limit_valid():
    assert check_credit_limit(10, 3) == True


def test_credit_limit_exceeded():
    assert check_credit_limit(17, 2) == False


def test_credit_limit_invalid_current():
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(-1, 2)


def test_credit_limit_invalid_course():
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(10, 0)


# 2. Tests for prerequisites_satisfied()

def test_empty_prerequisites():
    assert prerequisites_satisfied(set(), set()) == True


def test_all_prerequisites_completed():
    assert prerequisites_satisfied({"CS101", "CS102"}, {"CS101", "CS102"}) == True


def test_prerequisites_missing():
    assert prerequisites_satisfied({"CS101"}, {"CS101", "CS102"}) == False


# 3. Tests for registration_decision()

def test_negative_dues():
    student = Student("S01", outstanding_dues=-1)
    course = Course("CS301", 3, 30)

    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(student, course)


def test_invalid_capacity():
    student = Student("S01")
    course = Course("CS301", 3, 0)

    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(student, course)


def test_dues_block():
    student = Student("S01", outstanding_dues=1001)
    course = Course("CS301", 3, 30)

    assert registration_decision(student, course) == "DUES_BLOCK"


def test_already_registered():
    student = Student("S01", registered_courses={"CS301"})
    course = Course("CS301", 3, 30)

    assert registration_decision(student, course) == "ALREADY_REGISTERED"


def test_prerequisites_missing_decision():
    student = Student("S01", completed_courses={"CS101"})
    course = Course("CS301", 3, 30, prerequisites={"CS101", "CS102"})

    assert registration_decision(student, course) == "PREREQUISITES_MISSING"


def test_credit_limit_decision():
    student = Student("S01", current_credits=17)
    course = Course("CS301", 2, 30)

    assert registration_decision(student, course) == "CREDIT_LIMIT"


def test_registered_decision():
    student = Student("S01")
    course = Course("CS301", 3, 30)

    assert registration_decision(student, course) == "REGISTERED"


def test_full_course_waitlisted():
    student = Student("S01")
    course = Course("CS301", 3, 30, enrolled=30)

    assert registration_decision(student, course) == "WAITLISTED"


# 4. Tests for register_course()

def test_successful_registration():
    student = Student("S01")
    course = Course("CS301", 3, 30)

    result = register_course(student, course)

    assert result == "REGISTERED"
    assert "CS301" in student.registered_courses
    assert student.current_credits == 3
    assert course.enrolled == 1


def test_waitlist_adds_student(monkeypatch):
    student = Student("S02")
    course = Course("CS301", 3, 30, enrolled=30)

    monkeypatch.setattr(
        registration,
        "registration_decision",
        lambda student, course: "WAITLISTED"
    )

    result = register_course(student, course)

    assert result == "WAITLISTED"
    assert "S02" in course.waitlist
    assert student.current_credits == 0
    assert student.registered_courses == set()
    assert course.enrolled == 30


def test_waitlist_does_not_add_duplicate(monkeypatch):
    student = Student("S03")
    course = Course("CS301", 3, 30, waitlist=["S03"])

    monkeypatch.setattr(
        registration,
        "registration_decision",
        lambda student, course: "WAITLISTED"
    )

    result = register_course(student, course)

    assert result == "WAITLISTED"
    assert course.waitlist == ["S03"]


def test_unsuccessful_registration_no_mutation():
    student = Student("S04", outstanding_dues=1001)
    course = Course("CS301", 3, 30)

    old_credits = student.current_credits
    old_enrolled = course.enrolled
    old_registered = student.registered_courses.copy()

    register_course(student, course)

    assert student.current_credits == old_credits
    assert course.enrolled == old_enrolled
    assert student.registered_courses == old_registered


# 5. Tests for withdraw_course()

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


def test_unsuccessful_withdrawal():
    student = Student("S06")
    course = Course("CS301", 3, 30, enrolled=5)

    result = withdraw_course(student, course)

    assert result == False
    assert student.current_credits == 0
    assert course.enrolled == 5


