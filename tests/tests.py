import unittest
import sys
import os

# Ensure the app module can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from tests.utils import PositionValidator, ListEmptyError
except (ImportError, ModuleNotFoundError):
    from utils import PositionValidator, ListEmptyError

class TestPositionValidator(unittest.TestCase):
    """
    Test suite for PositionValidator class covering boundary analysis,
    exception handling, and various assertions.
    """

    def setUp(self):
        """
        Fixture: Initialize the System Under Test (SUT) before each test.
        """
        self.validator = PositionValidator()
        self.valid_majors = ["Computer Science", "Data Science"]

    def tearDown(self):
        """
        Fixture: Clean up after each test.
        """
        self.validator = None

    def test_default_max_team_size(self):
        """Test default configuration using assertEqual."""
        self.assertEqual(self.validator.max_team_size, 100, "Default max team size should be 100")

    def test_validate_team_size_valid(self):
        """Test valid team sizes."""
        self.assertTrue(self.validator.validate_team_size(1), "Team size of 1 should be valid")
        self.assertTrue(self.validator.validate_team_size(50), "Team size of 50 should be valid")
        self.assertTrue(self.validator.validate_team_size(100), "Team size of 100 should be valid")

    def test_validate_team_size_boundary(self):
        """
        Boundary Analysis: Test edge cases for team size.
        """
        # Minimum boundary
        self.assertTrue(self.validator.validate_team_size(1), "Minimum boundary team size (1) should be valid")
        # Maximum boundary
        self.assertTrue(self.validator.validate_team_size(100), "Maximum boundary team size (100) should be valid")
        
        # Just below minimum
        with self.assertRaises(ValueError, msg="Team size of 0 should raise ValueError"):
            self.validator.validate_team_size(0)
            
        # Just above maximum
        with self.assertRaises(ValueError, msg="Team size of 101 should raise ValueError"):
            self.validator.validate_team_size(101)

    def test_validate_team_size_invalid_types(self):
        """Test invalid types for team size (None, float, string)."""
        with self.assertRaises(ValueError, msg="None team size should raise ValueError"):
            self.validator.validate_team_size(None)
        with self.assertRaises(TypeError, msg="Float team size should raise TypeError"):
            self.validator.validate_team_size(5.5)
        with self.assertRaises(TypeError, msg="String team size should raise TypeError"):
            self.validator.validate_team_size("10")

    def test_validate_gpa_boundary(self):
        """
        Boundary Analysis: Test edge cases for GPA.
        """
        # Min and Max valid
        self.assertTrue(self.validator.validate_gpa(0.0), "GPA of 0.0 should be valid")
        self.assertTrue(self.validator.validate_gpa(4.0), "GPA of 4.0 should be valid")
        
        # Invalid boundaries
        with self.assertRaises(ValueError, msg="GPA of -0.01 should raise ValueError"):
            self.validator.validate_gpa(-0.01)
        with self.assertRaises(ValueError, msg="GPA of 4.01 should raise ValueError"):
            self.validator.validate_gpa(4.01)

    def test_validate_gpa_none(self):
        """Test None input for GPA."""
        with self.assertRaises(ValueError, msg="None GPA should raise ValueError"):
            self.validator.validate_gpa(None)

    def test_validate_majors_valid(self):
        """Test valid majors list."""
        self.assertTrue(self.validator.validate_majors(self.valid_majors), "Valid majors list should pass validation")

    def test_validate_majors_empty(self):
        """
        Exception Handling: Verify ListEmptyError is raised for empty list.
        """
        empty_list = []
        with self.assertRaises(ListEmptyError, msg="Empty majors list should raise ListEmptyError"):
            self.validator.validate_majors(empty_list)

    def test_validate_majors_none(self):
        """Test None input for majors."""
        with self.assertRaises(ValueError, msg="None majors list should raise ValueError"):
            self.validator.validate_majors(None)

    def test_object_aliasing(self):
        """
        Boundary Analysis: Test object aliasing.
        """
        list1 = ["CS", "DS"]
        list2 = list1 # Aliasing: list2 refers to the same object as list1
        list3 = ["CS", "DS"] # Different object, same content

        # Verify aliasing using assertIs (checks identity)
        self.assertIs(list1, list2, "list1 and list2 should be the same object")
        self.assertTrue(self.validator.check_aliasing(list1, list2), "check_aliasing should return True for same object")

        # Verify equality but not identity
        self.assertIsNot(list1, list3, "list1 and list3 should not be the same object")
        self.assertListEqual(list1, list3, "list1 and list3 should have the same content")
        self.assertFalse(self.validator.check_aliasing(list1, list3), "check_aliasing should return False for different objects")

if __name__ == '__main__':
    unittest.main()
