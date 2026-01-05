class ListEmptyError(Exception):
    """Custom exception raised when a list is empty."""
    pass

class PositionValidator:
    """
    Validator class for Position attributes.
    """
    def __init__(self):
        self.max_team_size = 100

    def validate_team_size(self, size):
        """
        Validates the team size.
        Must be an integer between 1 and self.max_team_size.
        """
        if size is None:
            raise ValueError("Team size cannot be None")
        if not isinstance(size, int):
            raise TypeError("Team size must be an integer")
        if size < 1:
            raise ValueError("Team size must be at least 1")
        if size > self.max_team_size:
            raise ValueError(f"Team size cannot exceed {self.max_team_size}")
        return True

    def validate_gpa(self, gpa):
        """
        Validates the GPA.
        Must be a float between 0.0 and 4.0.
        """
        if gpa is None:
            raise ValueError("GPA cannot be None")
        if not isinstance(gpa, (float, int)):
             raise TypeError("GPA must be a number")
        if not (0.0 <= gpa <= 4.0):
            raise ValueError("GPA must be between 0.0 and 4.0")
        return True

    def validate_majors(self, majors):
        """
        Validates the list of majors.
        Must not be None or empty.
        """
        if majors is None:
            raise ValueError("Majors list cannot be None")
        if not isinstance(majors, list):
            raise TypeError("Majors must be a list")
        if len(majors) == 0:
            raise ListEmptyError("Majors list cannot be empty")
        return True

    def check_aliasing(self, list1, list2):
        """
        Checks if two lists are the same object (aliasing).
        Returns True if they are the same object, False otherwise.
        """
        return list1 is list2
