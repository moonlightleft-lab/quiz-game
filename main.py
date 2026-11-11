class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print()
        print(self.question)
        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, user_answer):
        return self.answer == user_answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question"],
            data["choices"],
            data["answer"]
        )


def get_default_quizzes():
    return [
        Quiz(
            "Python에서 화면에 글자를 출력할 때 사용하는 함수는?",
            ["input()", "print()", "len()", "type()"],
            2
        ),
        Quiz(
            "Python에서 리스트를 만들 때 사용하는 기호는?",
            ["{}", "()", "[]", "<>"],
            3
        ),
        Quiz(
            "Git에서 변경사항을 저장하는 명령어는?",
            ["git save", "git commit", "git upload", "git store"],
            2
        ),
        Quiz(
            "JSON 파일에서 주로 사용하는 데이터 구조와 가까운 것은?",
            ["딕셔너리", "반복문", "함수", "클래스"],
            1
        ),
        Quiz(
            "Python에서 조건문을 작성할 때 사용하는 키워드는?",
            ["for", "while", "if", "class"],
            3
        )
    ]


def input_number(message, min_value, max_value):
    while True:
        user_input = input(message).strip()

        if user_input == "":
            print("입력이 비어 있습니다. 다시 입력하세요.")
            continue

        try:
            number = int(user_input)

            if number < min_value or number > max_value:
                print(f"{min_value}~{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

        except ValueError:
            print("숫자를 입력하세요.")


def main():
    quizzes = get_default_quizzes()
    score = 0

    print("===== Quiz Game =====")

    for index, quiz in enumerate(quizzes, start=1):
        print(f"\nQuestion {index}")
        quiz.display()

        user_answer = input_number("Answer: ", 1, 4)

        if quiz.check_answer(user_answer):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. The correct answer is {quiz.answer}.")

    print()
    print("===== Quiz Finished =====")
    print(f"Your final score is {score}/{len(quizzes)}")

    if score == len(quizzes):
        print("Excellent! Perfect score!")
    elif score >= len(quizzes) // 2:
        print("Good job!")
    else:
        print("Keep practicing!")


main()