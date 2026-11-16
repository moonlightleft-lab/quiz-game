import json
import shutil
import os

DB_FILE = 'state.json'
BACKUP_FILE = 'state.json.bak'


# 기본 퀴즈 데이터
# 평가 항목 #4 보완: 기본 퀴즈를 5개 이상 제공한다.
DEFAULT_QUIZZES = [
    {
        "question": "파이썬에서 출력할 때 사용하는 함수는?",
        "answer": "print"
    },
    {
        "question": "반복문 중 조건이 참일 동안 반복하는 문법은?",
        "answer": "while"
    },
    {
        "question": "조건에 따라 코드를 실행할 때 사용하는 문법은?",
        "answer": "if"
    },
    {
        "question": "여러 값을 순서대로 저장하는 파이썬 자료형은?",
        "answer": "list"
    },
    {
        "question": "키와 값으로 데이터를 저장하는 파이썬 자료형은?",
        "answer": "dict"
    }
]


# 전역 상태 변수
quizzes = []
best_score = 0


def get_non_empty_input(prompt):
    """
    빈 입력을 막기 위한 입력 검증 함수
    사용자가 엔터만 누르거나 공백만 입력하면 다시 입력하게 한다.
    """
    while True:
        user_input = input(prompt).strip()

        if user_input:
            return user_input

        print("입력값이 비어 있습니다. 다시 입력해 주세요.")


def get_menu_choice():
    """
    메뉴 입력 검증 함수
    0, 1, 2, 3 이외의 입력은 다시 입력하게 한다.
    """
    while True:
        choice = get_non_empty_input("메뉴 선택: ")

        if choice in ["1", "2", "3", "0"]:
            return choice

        print("잘못된 입력입니다. 메뉴 번호 0, 1, 2, 3 중에서 선택해 주세요.")


def make_default_state():
    """
    state.json이 없거나 손상되었을 때 사용할 기본 데이터
    """
    return {
        "quizzes": DEFAULT_QUIZZES.copy(),
        "best_score": 0
    }


def add_default_quizzes_if_needed(valid_quizzes):
    """
    저장된 퀴즈가 5개 미만이면 기본 퀴즈를 보충한다.
    기존 퀴즈는 유지하고, 부족한 개수만 기본 퀴즈에서 추가한다.
    """
    existing_questions = []

    for quiz in valid_quizzes:
        existing_questions.append(quiz["question"])

    for default_quiz in DEFAULT_QUIZZES:
        if len(valid_quizzes) >= 5:
            break

        if default_quiz["question"] not in existing_questions:
            valid_quizzes.append(default_quiz)
            existing_questions.append(default_quiz["question"])

    return valid_quizzes


def normalize_state(data):
    """
    불러온 데이터가 올바른 형태인지 확인하고 정리하는 함수
    """
    if not isinstance(data, dict):
        return make_default_state()

    loaded_quizzes = data.get("quizzes", DEFAULT_QUIZZES)
    loaded_best_score = data.get("best_score", 0)

    # 퀴즈 목록 검증
    if not isinstance(loaded_quizzes, list):
        loaded_quizzes = DEFAULT_QUIZZES

    valid_quizzes = []

    for quiz in loaded_quizzes:
        if (
            isinstance(quiz, dict)
            and isinstance(quiz.get("question"), str)
            and isinstance(quiz.get("answer"), str)
            and quiz.get("question").strip()
            and quiz.get("answer").strip()
        ):
            valid_quizzes.append({
                "question": quiz["question"].strip(),
                "answer": quiz["answer"].strip()
            })

    # 평가 항목 #4 보완:
    # 저장된 퀴즈가 없거나 5개 미만이면 기본 퀴즈를 추가하여 최소 5개 이상 유지한다.
    valid_quizzes = add_default_quizzes_if_needed(valid_quizzes)

    if not valid_quizzes:
        valid_quizzes = DEFAULT_QUIZZES.copy()

    # 최고점 검증
    if not isinstance(loaded_best_score, int):
        loaded_best_score = 0

    return {
        "quizzes": valid_quizzes,
        "best_score": loaded_best_score
    }


def save_state(data):
    """
    현재 퀴즈 목록과 최고점을 state.json에 저장한다.
    저장 후 백업 파일도 생성한다.

    호출 시점:
    1. 새 퀴즈가 추가되어 데이터가 변경된 직후
    2. 퀴즈 풀이 후 최고점이 변경된 직후
    3. 프로그램 종료 직전 최종 저장 시
    """
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        shutil.copy(DB_FILE, BACKUP_FILE)

    except Exception as e:
        print(f"저장 오류: {e}")


def load_state():
    """
    프로그램 시작 직후 1회 호출된다.
    state.json에서 저장된 퀴즈 목록과 최고점을 불러온다.
    state.json이 없거나 손상된 경우 기본 데이터를 사용한다.

    호출 시점:
    - main() 함수 시작 부분에서 메뉴 실행 전에 호출된다.
    """
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return normalize_state(data)
        except Exception:
            print("메인 파일 손상, 백업 확인 중...")

    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            shutil.copy(BACKUP_FILE, DB_FILE)
            print("백업 파일에서 데이터를 복구했습니다.")
            return normalize_state(data)

        except Exception:
            print("백업 파일도 사용할 수 없습니다.")

    print("기본 데이터로 시작합니다.")
    return make_default_state()


def get_current_state():
    """
    현재 프로그램 상태를 저장 가능한 딕셔너리 형태로 만든다.
    """
    return {
        "quizzes": quizzes,
        "best_score": best_score
    }


def show_menu():
    print("\n=== 퀴즈 게임 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록 보기")
    print("0. 종료")
    print(f"현재 최고점: {best_score}")


def play_quiz():
    global best_score

    score = 0

    for quiz in quizzes:
        print("\n문제:", quiz["question"])
        user_answer = get_non_empty_input("정답: ")

        if user_answer.lower() == quiz["answer"].lower():
            print("정답입니다!")
            score += 1
        else:
            print(f"오답입니다. 정답은 {quiz['answer']}입니다.")

    print(f"\n이번 점수: {score} / {len(quizzes)}")

    if score > best_score:
        best_score = score
        print("최고점이 갱신되었습니다!")

        # [저장 시점]
        # 퀴즈 풀이 후 최고점이 변경되었으므로 변경된 점수를 즉시 저장한다.
        save_state(get_current_state())
    else:
        print("최고점은 변경되지 않았습니다.")


def add_quiz():
    """
    새 퀴즈를 추가하는 함수
    """
    question = get_non_empty_input("추가할 문제를 입력하세요: ")
    answer = get_non_empty_input("정답을 입력하세요: ")

    new_quiz = {
        "question": question,
        "answer": answer
    }

    quizzes.append(new_quiz)

    # [저장 시점]
    # 새 퀴즈가 추가되어 퀴즈 목록 데이터가 변경되었으므로 즉시 저장한다.
    save_state(get_current_state())

    print("퀴즈가 추가되었습니다.")


def show_quizzes():
    """
    현재 퀴즈 목록을 보여주는 함수
    """
    print("\n=== 퀴즈 목록 ===")

    for index, quiz in enumerate(quizzes, start=1):
        print(f"{index}. {quiz['question']} / 정답: {quiz['answer']}")


def main():
    global quizzes
    global best_score

    # [로드 시점]
    # 프로그램 시작 직후, 메뉴를 실행하기 전에 저장된 퀴즈 목록과 최고점을 불러온다.
    data = load_state()

    quizzes = data["quizzes"]
    best_score = data["best_score"]

    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == "1":
            play_quiz()

        elif choice == "2":
            add_quiz()

        elif choice == "3":
            show_quizzes()

        elif choice == "0":
            # [저장 시점]
            # 프로그램 종료 직전에 현재 퀴즈 목록과 최고점을 최종 저장한다.
            save_state(get_current_state())

            print("프로그램을 종료합니다.")
            break


if __name__ == "__main__":
    main()