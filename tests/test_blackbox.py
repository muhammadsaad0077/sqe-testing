import pytest
from registration import (Student,Course,check_credit_limit,prerequisites_satisfied,registration_decision,register_course,withdraw_course)



# A1: EQUIVALENCE CLASS PARTITIONING

# EC01: Valid credit hours
@pytest.mark.parametrize("current, new, expected", [
    (10, 3, True),
    (0, 1, True),
    (16, 3, False)
])
def test_valid_credit_classes(current, new, expected):
    assert check_credit_limit(current, new) == expected

# EC02 and EC03: Invalid current credits
@pytest.mark.parametrize("current", [-1, 19])
def test_invalid_current_credits(current):
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(current, 2)



# EC04 and EC05: Invalid course credits
@pytest.mark.parametrize("new", [0, 5])
def test_invalid_course_credits(new):
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(10, new)


# EC12: No prerequisites
def test_empty_prerequisites():
    assert prerequisites_satisfied(set(), set()) is True


# EC13: All prerequisites completed
def test_all_prerequisites_completed():
    completed = {"CS101", "MATH101"}
    required = {"CS101", "MATH101"}

    assert prerequisites_satisfied(completed, required) is True


# EC14: Some prerequisites completed
def test_some_prerequisites_completed():
    completed = {"CS101"}
    required = {"CS101", "MATH101"}

    assert prerequisites_satisfied(completed, required) is False


# EC15: No prerequisites completed
def test_no_prerequisites_completed():
    completed = set()
    required = {"CS101", "MATH101"}

    assert prerequisites_satisfied(completed, required) is False


# EC09: Zero dues
def test_zero_dues():
    student = Student("S01", outstanding_dues=0)
    course = Course("CS201", 3, 30, enrolled=10)

    assert registration_decision(student, course) == "REGISTERED"


# EC10: Positive dues
def test_positive_dues():
    student = Student("S01", outstanding_dues=1)
    course = Course("CS201", 3, 30, enrolled=10)

    assert registration_decision(student, course) == "DUES_BLOCK"


# EC11: Negative dues
def test_negative_dues():
    student = Student("S01", outstanding_dues=-1)
    course = Course("CS201", 3, 30)

    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(student, course)


# EC16: Seats available
def test_available_seats():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=29)

    assert registration_decision(student, course) == "REGISTERED"


# EC17: Course is full
def test_course_full():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=30)

    assert registration_decision(student, course) == "WAITLISTED"


# EC18 and EC19: Invalid capacity and enrollment
@pytest.mark.parametrize("capacity, enrolled", [
    (0, 0),
    (30, 31),
    (30, -1)
])
def test_invalid_capacity(capacity, enrolled):
    student = Student("S01")
    course = Course("CS201", 3, capacity, enrolled=enrolled)

    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(student, course)
