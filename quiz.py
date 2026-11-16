quizzes = [
    {
        "question": "파이썬에서 출력할 때 사용하는 함수는?",
        "answer": "print"
    },
    {
        "question": "조건이 참일 동안 반복하는 반복문은?",
        "answer": "while"
    }
]


def show_menu():
    print("\n=== 퀴즈 게임 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록 보기")
    print("0. 종료")


def play_quiz():
    score = 0

    for quiz in quizzes:
        print("\n문제:", quiz["question"])
        user_answer = input("정답: ")

        if user_answer == quiz["answer"]:
            print("정답입니다!")
            score += 1
        else:
            print("틀렸습니다.")
            print("정답은", quiz["answer"], "입니다.")

    print("\n최종 점수:", score, "/", len(quizzes))


def add_quiz():
    question = input("추가할 문제를 입력하세요: ")
    answer = input("정답을 입력하세요: ")

    new_quiz = {
        "question": question,
        "answer": answer
    }

    quizzes.append(new_quiz)
    print("퀴즈가 추가되었습니다.")


def show_quiz_list():
    print("\n=== 퀴즈 목록 ===")

    for index, quiz in enumerate(quizzes, start=1):
        print(index, ".", quiz["question"])


while True:
    show_menu()

    choice = input("메뉴 선택: ")

    if choice == "1":
        play_quiz()
    elif choice == "2":
        add_quiz()
    elif choice == "3":
        show_quiz_list()
    elif choice == "0":
        print("게임을 종료합니다.")
        break
    else:
        print("잘못된 입력입니다.")
        