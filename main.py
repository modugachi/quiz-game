

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


def main():
    """메뉴를 반복해서 보여주고, 선택에 따라 기능을 실행한다."""
    try:
        while True:
            show_menu()
            choice = get_number("선택: ", 1, 5)

            if choice == 1:
                print("퀴즈 풀기 (준비 중)")
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