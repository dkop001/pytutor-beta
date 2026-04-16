import copy
# Lessons database
mock_lessons = {
    0: {
        "id": 0,
        "title": "Welcome to Python",
        "questions": [
            {
                "prompt": "Which of these is a Python data type?",
                "options": ["Elephant", "Integer", "Car", "House"],
                "correct_option_idx": 1,
                "explanation": "Integer is a numeric data type in Python."
            },
            {
                "prompt": "What does print() do?",
                "options": ["Calculates math", "Outputs to console", "Gets user input", "Imports modules"],
                "correct_option_idx": 1,
                "explanation": "print() outputs text to the console."
            }
        ]
    },
    1: {
        "id": 1,
        "title": "Printing Strings",
        "questions": [
            {
                "prompt": "How do you output 'Hello World' in Python?",
                "options": [
                    "echo 'Hello World'",
                    "System.out.println('Hello World')",
                    "print('Hello World')",
                    "console.log('Hello World')"
                ],
                "correct_option_idx": 2,
                "explanation": "print() is the built-in function to output to console."
            },
            {
                "prompt": "What is the correct syntax to print a string literal?",
                "options": ["print(Hello)", "print 'Hello'", "print(\"Hello\")", "print: Hello"],
                "correct_option_idx": 2,
                "explanation": "Strings must be enclosed in quotes."
            }
        ]
    },
    2: {
        "id": 2,
        "title": "Variables",
        "questions": [
            {
                "prompt": "Which is a valid variable name in Python?",
                "options": ["1st_name", "first-name", "first_name", "first name"],
                "correct_option_idx": 2,
                "explanation": "Variable names can contain letters, numbers, and underscores, but cannot start with a number."
            },
            {
                "prompt": "How do you assign the value 5 to a variable named x?",
                "options": ["x = 5", "int x = 5", "x == 5", "assign x 5"],
                "correct_option_idx": 0,
                "explanation": "Python uses the '=' operator for assignment. No type declaration is needed."
            }
        ]
    },
    3: {
        "id": 3,
        "title": "Math Operations",
        "questions": [
            {
                "prompt": "What is the output of 3 ** 2?",
                "options": ["6", "9", "5", "1"],
                "correct_option_idx": 1,
                "explanation": "The ** operator is used for exponentiation, so 3 squared is 9."
            },
            {
                "prompt": "Which operator is used for true division in Python 3?",
                "options": ["//", "%", "/", "#"],
                "correct_option_idx": 2,
                "explanation": "The / operator returns a float representing true division."
            }
        ]
    },
    # --- New levels ---
    4: {
        "id": 4,
        "title": "Booleans & Conditionals",
        "questions": [
            {
                "prompt": "Which of the following represents a Boolean value?",
                "options": ["\"True\"", "True", "1", "T"],
                "correct_option_idx": 1,
                "explanation": "True (without quotes) is a boolean keyword in Python."
            },
            {
                "prompt": "If x = 10 and y = 5, what does (x > y) evaluate to?",
                "options": ["True", "False", "None", "Error"],
                "correct_option_idx": 0,
                "explanation": "10 is greater than 5, so the expression is True."
            }
        ]
    },
    5: {
        "id": 5,
        "title": "Lists",
        "questions": [
            {
                "prompt": "How do you create an empty list in Python?",
                "options": ["list = {}", "list = ()", "list = []", "list = empty()"],
                "correct_option_idx": 2,
                "explanation": "Square brackets [] are used to create lists in Python."
            },
            {
                "prompt": "How do you access the first element of a list named 'my_list'?",
                "options": ["my_list[1]", "my_list[0]", "my_list.first()", "my_list(0)"],
                "correct_option_idx": 1,
                "explanation": "Python lists are 0-indexed, meaning the first element is at index 0."
            }
        ]
    },
    6: {
        "id": 6,
        "title": "Loops",
        "questions": [
            {
                "prompt": "Which keyword is used to iterate over a sequence (like a list, a tuple, a dictionary, a set, or a string)?",
                "options": ["loop", "while", "for", "iterate"],
                "correct_option_idx": 2,
                "explanation": "A 'for' loop is used for iterating over a sequence."
            },
            {
                "prompt": "How do you write a while loop that stops when x is no longer less than 5?",
                "options": ["while x < 5:", "while x < 5", "while (x < 5):", "until x < 5:"],
                "correct_option_idx": 0,
                "explanation": "In Python, a while statement requires a colon (:) at the end."
            }
        ]
    },
    7: {
        "id": 7,
        "title": "Functions",
        "questions": [
            {
                "prompt": "How do you create a function in Python?",
                "options": ["function myFunc()", "def myFunc():", "create myFunc()", "func myFunc():"],
                "correct_option_idx": 1,
                "explanation": "The 'def' keyword is used to define functions in Python."
            },
            {
                "prompt": "Which statement is used inside a function to send a result back to the caller?",
                "options": ["output", "return", "send", "yield value"],
                "correct_option_idx": 1,
                "explanation": "The 'return' statement exits a function and passes back a value."
            }
        ]
    },
    8: {
        "id": 8,
        "title": "Dictionaries",
        "questions": [
            {
                "prompt": "How do you define a dictionary?",
                "options": ["['key', 'val']", "('key': 'val')", "{'key': 'val'}", "<'key': 'val'>"],
                "correct_option_idx": 2,
                "explanation": "Dictionaries are defined with curly braces containing key-value pairs."
            },
            {
                "prompt": "How do you access the value associated with the key 'name' in dictionary 'd'?",
                "options": ["d.name", "d{'name'}", "d('name')", "d['name']"],
                "correct_option_idx": 3,
                "explanation": "You access values by providing the key inside square brackets."
            }
        ]
    }
}

# Units containing lessons
mock_units = [
    {
        "id": 1,
        "title": "Python Basics",
        "description": "Form the foundation of your Python journey.",
        "lessons": [
            {"id": 0, "status": "active"},
            {"id": 1, "status": "locked"},
            {"id": 2, "status": "locked"},
            {"id": 3, "status": "locked"},
            {"id": 4, "status": "locked"},
            {"id": 5, "status": "locked"},
            {"id": 6, "status": "locked"},
            {"id": 7, "status": "locked"},
            {"id": 8, "status": "locked"}
        ]
    }
]

def get_user_units(user):
    """Helper to return a localized visual status of map based on specific user progress"""
    user_units = copy.deepcopy(mock_units)
    for unit in user_units:
        for lesson in unit["lessons"]:
            if lesson["id"] in user["completed_lessons"]:
                lesson["status"] = "completed"
            elif lesson["id"] == user["current_lesson_id"]:
                lesson["status"] = "active"
            else:
                lesson["status"] = "locked"
    return user_units
