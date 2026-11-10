import json
import os
import shutil

# 데이터 파일은 main.py 가 있는 폴더(프로젝트 루트)의 state.json 에 저장한다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "state.json")
BACKUP_FILE = STATE_FILE + ".bak"      # 직전 정상 데이터의 백업
CORRUPT_FILE = STATE_FILE + ".corrupt"  # 손상된 파일을 원인 분석용으로 보관
TMP_FILE = STATE_FILE + ".tmp"          # 저장 도중에만 잠깐 쓰는 임시 파일

# 저장 파일을 읽다가 발생할 수 있는 오류 모음 (파일 문제, JSON 문법, 형식 오류)
LOAD_ERRORS = (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError,
               AttributeError)


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

    def to_dict(self):
        """JSON 으로 저장하기 위해 딕셔너리로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """저장된 딕셔너리를 Quiz 객체로 되돌린다. 형식이 틀리면 ValueError."""
        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question 형식 오류")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("choices 는 4개여야 합니다")
        if type(answer) is not int or not 1 <= answer <= 4:  # bool(True) 제외
            raise ValueError("answer 는 1~4 여야 합니다")
        return cls(question, choices, answer)


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

    def save(self):
        """퀴즈 목록과 최고 점수를 state.json 에 안전하게 저장한다.

        1) 임시 파일(state.json.tmp)에 먼저 쓴다.
        2) 기존 state.json 이 정상이면 state.json.bak 으로 백업한다.
        3) 임시 파일을 state.json 으로 교체한다. (저장 도중 꺼져도 원본이 깨지지 않는다)
        """
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(TMP_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            self.backup_current_file()
            os.replace(TMP_FILE, STATE_FILE)
        except OSError:
            print("⚠️ 저장 중 오류가 발생했습니다. 파일 권한과 디스크 공간을 확인하세요.")

    def backup_current_file(self):
        """현재 state.json 이 정상일 때만 state.json.bak 으로 복사해 둔다."""
        if not os.path.exists(STATE_FILE):
            return
        try:
            self.read_state(STATE_FILE)  # 손상된 파일이 정상 백업을 덮어쓰지 않게 검사
            shutil.copy2(STATE_FILE, BACKUP_FILE)
        except LOAD_ERRORS:
            pass

    def read_state(self, path):
        """path 의 JSON 을 읽어 (퀴즈 목록, 최고 점수)를 돌려준다. 형식이 틀리면 예외."""
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
        best_score = data.get("best_score")
        # 최고 점수는 None 이거나 0~100 사이의 정수여야 한다.
        if best_score is not None and (type(best_score) is not int
                                       or not 0 <= best_score <= 100):
            raise ValueError("best_score 형식 오류")
        return quizzes, best_score

    def load(self):
        """state.json 을 읽어 온다. 파일이 없거나 손상돼도 실행 가능해야 한다."""
        if not os.path.exists(STATE_FILE):
            return "🆕 저장된 데이터가 없어 기본 퀴즈로 시작합니다."

        try:
            self.quizzes, self.best_score = self.read_state(STATE_FILE)
        except LOAD_ERRORS:
            return self.recover()

        score_text = "없음" if self.best_score is None else f"{self.best_score}점"
        return f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})"

    def recover(self):
        """손상된 state.json 을 처리한다: 백업으로 복구, 안 되면 기본 퀴즈로 초기화."""
        # 1) 손상된 파일은 지우지 않고 .corrupt 로 옮겨 둔다. (원인 분석용)
        try:
            os.replace(STATE_FILE, CORRUPT_FILE)
        except OSError:
            pass

        # 2) 백업이 정상이면 백업으로 복구한다.
        if os.path.exists(BACKUP_FILE):
            try:
                self.quizzes, self.best_score = self.read_state(BACKUP_FILE)
                self.save()
                return "⚠️ 저장 파일이 손상되어 백업(state.json.bak)으로 복구했습니다."
            except LOAD_ERRORS:
                pass

        # 3) 백업도 없거나 손상됐으면 기본 퀴즈로 초기화한다.
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.save()
        return "⚠️ 저장 파일이 손상되어 기본 퀴즈로 복구했습니다."

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
        """새 점수가 최고 점수보다 높으면 갱신하고 저장한다."""
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!\n")
            self.save()

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 퀴즈 목록에 추가하고 저장한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = get_text("문제를 입력하세요: ")

        choices = []
        for number in range(1, 5):
            choices.append(get_text(f"선택지 {number}: "))

        answer = get_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save()
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
        """저장된 데이터를 불러온 뒤, 메뉴를 반복하며 기능을 실행한다."""
        print(self.load())

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

        self.save()  # 종료 전에 한 번 더 저장


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
