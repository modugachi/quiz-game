

class Quiz:
    """퀴즈 1개를 표현하는 클래스 (문제, 선택지 4개, 정답 번호 1~4)."""

    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer  # 1~4 중 하나의 번호

    def show(self):
        """문제와 선택지를 화면에 출력한다."""
        print(self.question)
        print()
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 입력한 번호가 정답이면 True, 아니면 False."""
        return user_answer == self.answer


def create_default_quizzes():
    """기본 퀴즈 5개를 만들어 리스트로 돌려준다."""
    return [
        Quiz('x = "3" 일 때 type(x)의 결과는?',
             ["int", "str", "bool", "list"], 2),
        Quiz('fruits = ["사과", "배", "귤", "감"] 일 때 fruits[2]는?',
             ["배", "사과", "귤", "감"], 3),
        Quiz("파이썬에서 '같은지 비교'하는 기호는?",
             ["==", "=", "!=", "=>"], 1),
        Quiz("조건이 끝날 때까지 몇 번 돌지 모를 때 쓰는 반복문은?",
             ["for", "if", "def", "while"], 4),
        Quiz("원격 저장소를 처음 통째로 내려받는 Git 명령은?",
             ["push", "pull", "clone", "checkout"], 3),
    ]


def get_number(prompt, min_value, max_value):
    """min_value~max_value 사이의 정수를 올바르게 입력받을 때까지 묻는다."""
    while True:
        text = input(prompt).strip()

        if text == "":
            print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        if number < min_value or number > max_value:
            print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        return number


def show_menu():
    """메뉴를 화면에 출력한다."""
    print("=" * 40)
    print("      🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def play_quiz(quizzes):
    """등록된 퀴즈를 모두 출제하고 점수(0~100)를 돌려준다. 퀴즈가 없으면 None."""
    if not quizzes:
        print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.\n")
        return None

    total = len(quizzes)
    correct_count = 0
    print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

    for number, quiz in enumerate(quizzes, start=1):
        print("-" * 40)
        print(f"[문제 {number}]")
        quiz.show()
        print()
        user_answer = get_number("정답 입력: ", 1, 4)
        if quiz.is_correct(user_answer):
            correct_count += 1
            print("✅ 정답입니다!\n")
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

    score = round(correct_count / total * 100)
    print("=" * 40)
    print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
    print("=" * 40 + "\n")
    return score

    
def main():
    """메뉴를 반복해서 보여주고, 선택에 따라 기능을 실행한다."""
    quizzes = create_default_quizzes()
    
    try:
        while True:
            show_menu()
            choice = get_number("선택: ", 1, 5)

            if choice == 1:
                play_quiz(quizzes)
            elif choice == 2:
                print("퀴즈 추가 (준비 중)")
            elif choice == 3:
                print("퀴즈 목록 (준비 중)")
            elif choice == 4:
                print("점수 확인 (준비 중)")
            elif choice == 5:
                print("프로그램을 종료합니다.")
                break
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()