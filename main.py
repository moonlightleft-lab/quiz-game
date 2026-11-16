import json
import shutil  # 파일 복사를 위해 추가
import os      # 파일 존재 확인을 위해 추가

DB_FILE = 'state.json'
BACKUP_FILE = 'state.json.bak'


quizzes = [
    {
        "question": "파이썬에서 출력할 때 사용하는 함수는?",
        "answer": "print"
    },
    {
        "question": "반복문 중 조건이 참일 동안 반복하는 문법은?",
        "answer": "while"
    }
]
def save_state(data):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        shutil.copy(DB_FILE, BACKUP_FILE)
    except Exception as e:
        print(f"저장 오류: {e}")

def load_state():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            print("메인 파일 손상, 백업 확인 중...")
    
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                shutil.copy(BACKUP_FILE, DB_FILE)
                return data
        except:
            pass
    return {"score": 0, "level": 1} # 기본 데이터


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
        