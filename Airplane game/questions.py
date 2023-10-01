combined_questions = []


questions1 = [
    {
        "question": "What is a correct syntax to output 'Hello World' in Python?",
        "answer": "print('Hello World')",
    },
    {
        "question": "How do you insert COMMENTS in Python code?",
        "answer": "#",
    },
    {
        "question": "How do you create a variable named 'x' with the numeric value 5?",
        "answer": "x = 5",
    },
]

questions2 = [
    {
        "question": "What is the correct file extension for Python files?",
        "answer": ".py",
    },
    {
        "question": "How many standard datatypes are in Python?(Answer in digits)",
        "answer": "6",
    },
    {
        "question": "Which character returns the remainder of the division between two numbers.",
        "answer": "%",
    },
]

questions3 = [
    {
        "question": "Which method can be used to return a string in upper case letters?",
        "answer": "upper()",
    },
    {
        "question": "How do you write an if statement in Python?(if x is bigger than y)",
        "answer": "if x > y:",
    },
    {
        "question": """What is the output of the following code?
x = 5
y = 3
if x > y:
    print(x)
else:
    print(m)
""",
        "answer": "5",
    },
]

questions4 = [
    {
        "question": "Which one of these loops can iterate through a list? (While or For)",
        "answer": "for",
    },
    {
        "question": "Which statement is used to stop a loop?",
        "answer": "break",
    },
    {
        "question": "How many loops are in Python?(Answer in digits)",
        "answer": "3",
    },
]
questions5 = [
    {
        "question": """Which of these collections defines a set?(Answer in 1, 2 or 3)
1: {'apple, 'banana', 'cherry'}
2: ('apple', 'banana', 'cherry')
3: ['apple', 'banana', 'cherry']
        """,
        "answer": "1",
    },
    {
        "question": """Which collection is ordered, changeable, and allows duplicate members?(Answer in 1, 2, 3 or 4)
1: set
2: list
3: dictionary
4: tuple
        """,
        "answer": "2",
    },
    {
        "question": "What method adds a list to another list?",
        "answer": "extend()",
    },
]

questions6 = [
    {
        "question": "What is the correct way to create a function in Python?(function name is 'myFunc')",
        "answer": "def myFunc()",
    },
    {
        "question": "Which method can be used to replace parts of a string?",
        "answer": "replace()",
    },
    {
        "question": "How many parameters does this functions have: def muFunc(this, that)? (Answer in digits)",
        "answer": "2",
    },
]

questions7 = [
    {
        "question": """
        What is a correct syntax to return the first character in a string?(Answer in digits)
1: x = sub("Hello", 0, 1)
2: x = "Hello"[0]
3: x = "Hello".sub(0, 1)
        """,
        "answer": "2",
    },
    {
        "question": """
        What is the correct syntax to output the type of a variable or object in Python? (Answer in digits)
1: print(type(x)) 
2: print(typeof(x))
3: print(typeof x)
        """,
        "answer": "1",
    },
    {
        "question": "Can a function call an another function? (Yes/No)",
        "answer": "Yes",
    },
]

questions8 = [
    {
        "question": "",
        "answer": "",
    },
    {
        "question": "",
        "answer": "",
    },
    {
        "question": "",
        "answer": "",
    },
]

questions9 = [
    {
        "question": "",
        "answer": "",
    },
    {
        "question": "",
        "answer": "",
    },
    {
        "question": "",
        "answer": "",
    },
]

questions10 = [
    {
        "question": "",
        "answer": "",
    },
    {
        "question": "",
        "answer": "",
    },
    {
        "question": "",
        "answer": "",
    },
]

# Add questions from each list to the combined_questions list
combined_questions.extend(questions1)
combined_questions.extend(questions2)
combined_questions.extend(questions3)
combined_questions.extend(questions4)
combined_questions.extend(questions5)
combined_questions.extend(questions6)
combined_questions.extend(questions7)
combined_questions.extend(questions8)
combined_questions.extend(questions9)
combined_questions.extend(questions10)