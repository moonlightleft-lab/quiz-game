print("===== Python Quiz Game =====")
print("Read the question and type your answer.")
print()

questions = [
    {
        "question": "Which function is used to print text in Python?",
        "answer": "print"
    },
    {
        "question": "Which keyword is used for conditional statements in Python?",
        "answer": "if"
    },
    {
        "question": "Which function is used to get user input in Python?",
        "answer": "input"
    }
]

score = 0

for index, quiz in enumerate(questions, start=1):
    print(f"Question {index}: {quiz['question']}")
    user_answer = input("Answer: ")

    if user_answer.strip().lower() == quiz["answer"]:
        print("Correct!")
        score += 1
    else:
        print(f"Wrong. The correct answer is {quiz['answer']}.")

    print()

print("===== Quiz Finished =====")
print(f"Your final score is {score}/{len(questions)}")