import unittest
from unittest.mock import patch
from io import StringIO
from main import *
from event_management import admin_login, create_event, register_user, register_for_event, provide_feedback

# Mocked data for testing
users = {"admin": "admin123"}
events = {}
event_registrations = {}
feedbacks = {}

class TestEventManagementSystem(unittest.TestCase):

    def test_admin_login_success(self):
        with patch('builtins.input', side_effect=["admin"]), \
             patch('getpass.getpass', return_value="admin123"), \
             patch('sys.stdout', new_callable=StringIO) as output:
            admin_login()
            self.assertIn("Admin login successful!", output.getvalue())
    
    def test_admin_login_failure(self):
        with patch('builtins.input', side_effect=["admin"]), \
             patch('getpass.getpass', return_value="wrongpassword"), \
             patch('sys.stdout', new_callable=StringIO) as output:
            admin_login()
            self.assertIn("Invalid admin credentials.", output.getvalue())

    def test_create_event_success(self):
        global events, event_registrations, feedbacks
        events, event_registrations, feedbacks = {}, {}, {}
        with patch('builtins.input', side_effect=["E001", "Tech Workshop", "2024-12-15", "Hall A", "50"]), \
             patch('sys.stdout', new_callable=StringIO) as output:
            create_event()
            self.assertIn("Event 'Tech Workshop' created successfully!", output.getvalue())
            self.assertIn("E001", events)
    
    def test_create_event_duplicate_id(self):
        global events
        events = {"E001": {"name": "Existing Event", "date": "2024-12-10", "venue": "Hall A", "max_participants": 100}}
        with patch('builtins.input', side_effect=["E001"]), \
             patch('sys.stdout', new_callable=StringIO) as output:
            create_event()
            self.assertIn("Event ID already exists. Please try again.", output.getvalue())

    def test_register_user_success(self):
        global users
        users = {"admin": "admin123"}
        with patch('builtins.input', side_effect=["new_user"]), \
             patch('getpass.getpass', return_value="newpassword"), \
             patch('sys.stdout', new_callable=StringIO) as output:
            register_user()
            self.assertIn("User registration successful!", output.getvalue())
            self.assertIn("new_user", users)

    def test_register_user_duplicate(self):
        global users
        users = {"admin": "admin123", "existing_user": "password"}
        with patch('builtins.input', side_effect=["existing_user"]), \
             patch('sys.stdout', new_callable=StringIO) as output:
            register_user()
            self.assertIn("Username already exists. Please try another.", output.getvalue())

    def test_register_for_event_success(self):
        global events, event_registrations
        events = {"E001": {"name": "Tech Workshop", "date": "2024-12-15", "venue": "Hall A", "max_participants": 50}}
        event_registrations = {"E001": []}
        with patch('builtins.input', side_effect=["E001"]), \
             patch('sys.stdout', new_callable=StringIO) as output:
            register_for_event("test_user")
            self.assertIn("Successfully registered for 'Tech Workshop'.", output.getvalue())
            self.assertIn("test_user", event_registrations["E001"])

    def test_register_for_event_full(self):
        global events, event_registrations
        events = {"E001": {"name": "Tech Workshop", "date": "2024-12-15", "venue": "Hall A", "max_participants": 1}}
        event_registrations = {"E001": ["already_registered"]}
        with patch('builtins.input', side_effect=["E001"]), \
             patch('sys.stdout', new_callable=StringIO) as output:
            register_for_event("test_user")
            self.assertIn("Event is full. Registration closed.", output.getvalue())

    def test_provide_feedback_success(self):
        global feedbacks, event_registrations
        feedbacks = {"E001": []}
        event_registrations = {"E001": ["test_user"]}
        with patch('builtins.input', side_effect=["E001", "Great workshop!"]), \
             patch('sys.stdout', new_callable=StringIO) as output:
            provide_feedback("test_user")
            self.assertIn("Feedback submitted successfully!", output.getvalue())
            self.assertIn("Great workshop!", feedbacks["E001"])

    def test_provide_feedback_not_registered(self):
        global feedbacks, event_registrations
        feedbacks = {"E001": []}
        event_registrations = {"E001": []}  # test_user not registered
        with patch('builtins.input', side_effect=["E001"]), \
             patch('sys.stdout', new_callable=StringIO) as output:
            provide_feedback("test_user")
            self.assertIn("You are not registered for this event.", output.getvalue())


if __name__ == '__main__':
    unittest.main()
