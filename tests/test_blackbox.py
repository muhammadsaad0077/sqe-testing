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

# A2: BOUNDARY VALUE ANALYSIS

# Current credits: minimum and maximum
def test_current_credits_minimum():
    assert check_credit_limit(0, 1) is True


def test_current_credits_maximum():
    assert check_credit_limit(18, 1) is False

# Course credits: minimum and maximum
def test_course_credits_minimum():
    assert check_credit_limit(0, 1) is True


def test_course_credits_maximum():
    assert check_credit_limit(0, 4) is True



# Combined credits: exactly 18 and just above 18
def test_combined_credits_exactly_18():
    assert check_credit_limit(15, 3) is True


def test_combined_credits_just_above_18():
    assert check_credit_limit(16, 3) is False



# Course capacity boundary
def test_enrollment_just_below_capacity():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=29)

    assert registration_decision(student, course) == "REGISTERED"



def test_enrollment_at_capacity():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=30)

    assert registration_decision(student, course) == "WAITLISTED"


# Outstanding dues boundary
def test_dues_at_zero():
    student = Student("S01", outstanding_dues=0)
    course = Course("CS201", 3, 30)

    assert registration_decision(student, course) == "REGISTERED"

def test_dues_at_one():
    student = Student("S01", outstanding_dues=1)
    course = Course("CS201", 3, 30)

    assert registration_decision(student, course) == "DUES_BLOCK"


# A3: DECISION TABLE TESTING

# R1: Dues have highest priority
def test_dues_priority():
    student = Student(
        "S01",
        outstanding_dues=1,
        registered_courses={"CS201"}
    )
    course = Course(
        "CS201",
        3,
        30,
        prerequisites={"CS101"}
    )

    assert registration_decision(student, course) == "DUES_BLOCK"



# R2: Duplicate registration has second priority
def test_duplicate_registration_priority():
    student = Student(
        "S01",
        registered_courses={"CS201"}
    )
    course = Course(
        "CS201",
        3,
        30,
        prerequisites={"CS101"}
    )

    assert registration_decision(student, course) == "ALREADY_REGISTERED"

# R3: Missing prerequisites
def test_missing_prerequisites_priority():
    student = Student("S01", current_credits=18)
    course = Course(
        "CS201",
        3,
        30,
        enrolled=30,
        prerequisites={"CS101"}
    )

    assert registration_decision(student, course) == "PREREQUISITES_MISSING"


# R4: Credit limit
def test_credit_limit_priority():
    student = Student(
        "S01",
        completed_courses={"CS101"},
        current_credits=16
    )
    course = Course(
        "CS201",
        3,
        30,
        enrolled=30,
        prerequisites={"CS101"}
    )

    assert registration_decision(student, course) == "CREDIT_LIMIT"


# R5: Successful registration decision
def test_registered_decision():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=10)

    assert registration_decision(student, course) == "REGISTERED"



# R6: Waiting list decision
def test_waitlisted_decision():
    student = Student("S01")
    course = Course("CS201", 3, 30, enrolled=30)

    assert registration_decision(student, course) == "WAITLISTED"