import unittest
from unittest.mock import patch
from io import StringIO

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
  

    def register():
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input("Enter role (admin/seller/buyer): ").lower()
    
        with open('users.json', 'r+') as file:
            users = json.load(file)
            if username in users:
                print("Username already exists.")
            else:
                users[username] = {'password': password, 'role': role} 
                file.seek(0)
                json.dump(users, file, indent=4)
                print("Registration successful!")
    
    def login():
        username = input("Enter username: ")
        password = input("Enter password: ")
    
        with open('users.json', 'r') as file:
            users = json.load(file)
            if username in users and users[username]['password'] == password:
                print("Login successful!")
                return {'username': username, 'role': users[username]['role']}
            else:
                print("Invalid username or password.")
                return None


    def manage_cars():
        print("\n1. Add Car\n2. Update Car\n3. Remove Car")
        choice = input("Choose an option: ")
        if choice == '1':
            add_car()
        elif choice == '2':
            update_car()
        elif choice == '3':
            remove_car()
        else:
            print("Invalid choice.")
    
    def add_car(user):
        car_id = input("Enter Car ID: ")
        make = input("Enter Make: ")
        model = input("Enter Model: ")
        year = input("Enter Year: ")
        price = float(input("Enter Starting Price: "))
        
        with open('cars.json', 'r+') as file:
            cars = json.load(file)
            cars[car_id] = {'make': make, 'model': model, 'year': year, 'price': price, 'seller': user['username']}
            file.seek(0)
            json.dump(cars, file, indent=4)
            print("Car added successfully!")
    
    def view_cars():
        with open('cars.json', 'r') as file:
            cars = json.load(file)
            for car_id, car in cars.items():
                print(f"\nID: {car_id}, Make: {car['make']}, Model: {car['model']}, Year: {car['year']}, Price: {car['price']}")



if __name__ == '__main__':
    unittest.main()
