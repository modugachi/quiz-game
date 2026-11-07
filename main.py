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


def get_text(prompt):
    """빈 문자열이 아닌 글자를 입력받을 때까지 묻는다."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("⚠️ 입력이 비어 있습니다. 내용을 입력하세요.")


class QuizGame:
    """게임 전체(메뉴, 풀기, 추가, 목록, 점수)를 관리하는 클래스."""

    def __init__(self):
        self.quizzes = create_default_quizzes()  # 퀴즈 목록
        self.best_score = None  # 최고 점수 (아직 풀지 않았으면 None)

    def show_menu(self):
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

    def play_quiz(self):
        """등록된 퀴즈를 모두 출제하고, 결과에 따라 최고 점수를 갱신한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.\n")
            return

        total = len(self.quizzes)
        correct_count = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for number, quiz in enumerate(self.quizzes, start=1):
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
        self.update_best_score(score)

    def update_best_score(self, score):
        """새 점수가 최고 점수보다 높으면 갱신한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!\n")

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 퀴즈 목록에 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = get_text("문제를 입력하세요: ")

        choices = []
        for number in range(1, 5):
            choices.append(get_text(f"선택지 {number}: "))

        answer = get_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        print("\n✅ 퀴즈가 추가되었습니다!\n")

    def show_quiz_list(self):
        """등록된 퀴즈의 번호와 문제를 보여준다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.\n")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40 + "\n")

    def show_score(self):
        """최고 점수를 보여준다."""
        if self.best_score is None:
            print("\n⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어보세요.\n")
        else:
            print(f"\n🏆 최고 점수: {self.best_score}점\n")

    def run(self):
        """메뉴를 반복해서 보여주고, 선택에 따라 기능을 실행한다."""
        try:
            while True:
                self.show_menu()
                choice = get_number("선택: ", 1, 5)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quiz_list()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("프로그램을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 프로그램을 안전하게 종료합니다.")


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()