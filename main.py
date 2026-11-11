import json

DATA_FILE = "state.json"


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


def save_state(quizzes, best_score):
    data = {
        "quizzes": [quiz.to_dict() for quiz in quizzes],
        "best_score": best_score
    }

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except OSError:
        print("데이터 저장 중 오류가 발생했습니다.")


def load_state():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        quizzes = []
        for quiz_data in data["quizzes"]:
            quizzes.append(Quiz.from_dict(quiz_data))

        best_score = data.get("best_score", 0)

        print(f"저장된 데이터를 불러왔습니다. 퀴즈 {len(quizzes)}개, 최고 점수 {best_score}점")
        return quizzes, best_score

    except FileNotFoundError:
        print("저장 파일이 없어 기본 퀴즈를 불러옵니다.")
        quizzes = get_default_quizzes()
        best_score = 0
        save_state(quizzes, best_score)
        return quizzes, best_score

    except (json.JSONDecodeError, KeyError, TypeError):
        print("저장 파일이 손상되어 기본 데이터로 초기화합니다.")
        quizzes = get_default_quizzes()
        best_score = 0
        save_state(quizzes, best_score)
        return quizzes, best_score


def input_number(message, min_value, max_value):
    while True:
        try:
            user_input = input(message).strip()

            if user_input == "":
                print("입력이 비어 있습니다. 다시 입력하세요.")
                continue

            number = int(user_input)

            if number < min_value or number > max_value:
                print(f"{min_value}~{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

        except ValueError:
            print("숫자를 입력하세요.")

        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되었습니다.")
            return None


class QuizGame:
    def __init__(self, quizzes, best_score):
        self.quizzes = quizzes
        self.best_score = best_score

    def show_menu(self):
        print()
        print("=" * 40)
        print("        나만의 퀴즈 게임")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def run(self):
        while True:
            self.show_menu()
            choice = input_number("선택: ", 1, 5)

            if choice is None:
                self.save()
                print("프로그램을 안전하게 종료합니다.")
                break

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                self.save()
                print("프로그램을 종료합니다.")
                break

    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0

        print()
        print(f"퀴즈를 시작합니다. 총 {len(self.quizzes)}문제입니다.")

        for index, quiz in enumerate(self.quizzes, start=1):
            print()
            print("-" * 40)
            print(f"[문제 {index}]")
            quiz.display()

            user_answer = input_number("정답 입력: ", 1, 4)

            if user_answer is None:
                print("퀴즈를 중단합니다.")
                self.save()
                return

            if quiz.check_answer(user_answer):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        print()
        print("=" * 40)
        print(f"결과: {len(self.quizzes)}문제 중 {score}문제 정답")

        if score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
            self.save()

        print("=" * 40)

    def add_quiz(self):
        print()
        print("새로운 퀴즈를 추가합니다.")

        try:
            question = input("문제를 입력하세요: ").strip()

            if question == "":
                print("문제가 비어 있어 추가를 취소합니다.")
                return

            choices = []

            for i in range(1, 5):
                choice = input(f"선택지 {i}: ").strip()

                if choice == "":
                    print("선택지가 비어 있어 추가를 취소합니다.")
                    return

                choices.append(choice)

            answer = input_number("정답 번호 (1~4): ", 1, 4)

            if answer is None:
                print("퀴즈 추가를 취소합니다.")
                return

            new_quiz = Quiz(question, choices, answer)
            self.quizzes.append(new_quiz)
            self.save()

            print("퀴즈가 추가되었습니다.")

        except (KeyboardInterrupt, EOFError):
            print("\n퀴즈 추가가 중단되었습니다.")
            self.save()

    def show_quiz_list(self):
        print()

        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"등록된 퀴즈 목록: 총 {len(self.quizzes)}개")
        print("-" * 40)

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")

    def show_score(self):
        print()
        print(f"최고 점수: {self.best_score}점")

        if self.best_score == 0:
            print("아직 최고 점수가 없거나, 정답을 맞힌 기록이 없습니다.")

    def save(self):
        save_state(self.quizzes, self.best_score)


def main():
    quizzes, best_score = load_state()
    game = QuizGame(quizzes, best_score)
    game.run()


main()