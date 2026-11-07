# 나만의 퀴즈 게임 (파이썬·Git 코드 읽기 퀴즈)

터미널에서 동작하는 파이썬 콘솔 퀴즈 게임입니다. (코디세이 입학연수 미션 2)
퀴즈를 풀고, 추가하고, 목록과 최고 점수를 확인할 수 있으며, 프로그램을 종료해도 데이터가 `state.json`에 남습니다.

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [퀴즈 주제 선정 이유](#2-퀴즈-주제-선정-이유)
3. [개발 환경](#3-개발-환경)
4. [실행 방법](#4-실행-방법)
5. [기능 목록](#5-기능-목록)
6. [파일 구조](#6-파일-구조)
7. [데이터 파일 설명 (state.json)](#7-데이터-파일-설명-statejson)
8. [입력·예외 처리 기준](#8-입력예외-처리-기준)
9. [main.py 전체 코드](#9-mainpy-전체-코드)
10. [코드로 배우는 Python (과제 목표 정리)](#10-코드로-배우는-python-과제-목표-정리)
11. [Git 정리](#11-git-정리)
12. [실행 화면](#12-실행-화면)
13. [제출물 체크리스트](#13-제출물-체크리스트)

---

## 1. 프로젝트 개요

- **목표:** 입력 → 처리 → 출력 흐름을 가진 파이썬 콘솔 프로그램을 처음부터 끝까지 직접 만들고, 그 과정을 Git으로 기록한다.
- **구성:** `Quiz`(퀴즈 1개)와 `QuizGame`(게임 전체) 두 개의 클래스로 역할을 나눴다.
- **데이터 영속성:** 퀴즈 목록과 최고 점수를 JSON 파일(`state.json`)에 저장해서, 프로그램을 껐다 켜도 유지된다.
- **Git 기록:** 기능 단위로 커밋하고, 브랜치를 나눠 작업한 뒤 병합하며, GitHub에 저장소를 공개했다.
- **외부 라이브러리 없이** 파이썬 표준 라이브러리(`json`, `os`)만 사용한다.

## 2. 퀴즈 주제 선정 이유

**주제: 파이썬·Git 코드 읽기**

초보 개발자인 내가 미션을 먼저 완료한 뒤, **내가 만든 코드와 미션에서 배운 용어로 복습**하기 위해 이 주제를 골랐다. 퀴즈를 만들고 푸는 과정이 곧 시험 대비가 된다.

| # | 문제 | 정답 | 확인하는 개념 |
|---|---|---|---|
| 1 | `x = "3"` 일 때 `type(x)`의 결과는? | 2. `str` | 입력은 항상 문자열 |
| 2 | `fruits = ["사과", "배", "귤", "감"]` 일 때 `fruits[2]`는? | 3. 귤 | 리스트 번호는 0부터 |
| 3 | 파이썬에서 "같은지 비교"하는 기호는? | 1. `==` | `=`(담기)와 `==`(비교)의 차이 |
| 4 | 조건이 끝날 때까지 몇 번 돌지 모를 때 쓰는 반복문은? | 4. `while` | `for`와 `while`의 차이 |
| 5 | 원격 저장소를 처음 통째로 내려받는 Git 명령은? | 3. `clone` | `clone`과 `pull`의 차이 |

## 3. 개발 환경

| 항목 | 내용 |
|---|---|
| OS | Ubuntu on WSL (버전: `<lsb_release -d 결과>`) |
| 에디터 | VS Code (WSL 연결) |
| Python | 3.14.4 |
| Git | 2.53.0 |
| 외부 라이브러리 | 없음 (`json`, `os` 표준 라이브러리만 사용) |

환경 확인 명령:

```bash
python3 --version
git --version
git config --list
```

## 4. 실행 방법

**처음 받을 때 (clone)**

```bash
git clone https://github.com/<GitHub아이디>/quiz-game.git
cd quiz-game
python3 main.py
```

**이미 받은 뒤 (최신 변경 가져오기)**

```bash
cd quiz-game
git pull
python3 main.py
```

- 첫 실행에서는 `state.json`이 없어서 기본 퀴즈 5개로 시작하고, 퀴즈를 풀거나 추가하면 파일이 만들어진다.
- 메뉴에서 번호(1~5)를 입력해 기능을 선택한다.

## 5. 기능 목록

- [x] 메뉴 출력과 종료
- [x] 퀴즈 풀기 (전체 출제, 정답/오답 표시, 결과 점수)
- [x] 퀴즈 추가 (문제, 선택지 4개, 정답 번호)
- [x] 퀴즈 목록
- [x] 점수 확인 (최고 점수)
- [x] 잘못된 입력 처리 (공백, 문자, 범위 밖, 빈 입력)
- [x] 종료 후에도 데이터 유지 (`state.json`)
- [x] 파일이 없거나 손상돼도 실행 가능 (기본 데이터로 복구)

## 6. 파일 구조

```
quiz-game/
├── main.py              # 프로그램 전체 (실행 파일)
├── state.json           # 퀴즈 목록과 최고 점수 (실행하면 생성, Git에는 올리지 않음)
├── README.md            # 이 문서
├── .gitignore           # Git이 추적하지 않을 파일 목록
└── docs/
    └── screenshots/     # 실행 화면 캡처
```

**main.py 안의 구성**

| 이름 | 종류 | 역할 |
|---|---|---|
| `Quiz` | 클래스 | 퀴즈 1개(문제, 선택지 4개, 정답)를 표현. `show`, `is_correct`, `to_dict`, `from_dict` |
| `QuizGame` | 클래스 | 게임 전체를 관리. 메뉴, 풀기, 추가, 목록, 점수, 저장, 불러오기 |
| `create_default_quizzes()` | 함수 | 기본 퀴즈 5개를 만들어 리스트로 돌려줌 |
| `get_number()` | 함수 | 범위 안의 정수를 올바르게 입력받을 때까지 묻는 공통 입력 함수 |
| `get_text()` | 함수 | 빈 글자가 아닌 입력을 받을 때까지 묻는 함수 |
| `main()` | 함수 | `QuizGame`을 만들어 실행 |

## 7. 데이터 파일 설명 (state.json)

| 항목 | 내용 |
|---|---|
| 경로 | 프로젝트 루트의 `state.json` (`main.py`와 같은 폴더) |
| 역할 | 퀴즈 목록과 최고 점수를 저장해서 프로그램을 종료해도 유지 |
| 인코딩 | UTF-8 (`ensure_ascii=False`라서 한글이 그대로 저장됨) |
| 저장 시점 | 퀴즈 추가 직후, 최고 점수 갱신 직후, 프로그램 종료 직전 |
| 불러오는 시점 | 프로그램 시작 시 |

**필드 구조**

| 필드 | 자료형 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list(str) | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int 또는 null | 최고 점수(0~100). 아직 풀지 않았으면 `null` |

**예시**

```json
{
    "quizzes": [
        {
            "question": "x = \"3\" 일 때 type(x)의 결과는?",
            "choices": ["int", "str", "bool", "list"],
            "answer": 2
        }
    ],
    "best_score": 80
}
```

**`state.json`을 Git에 올리지 않는 이유:** 실행할 때마다 바뀌는 데이터라서 커밋 이력이 지저분해지기 때문이다. 대신 이 문서에 구조를 적어 두었고, 처음 실행하면 기본 퀴즈로 자동 생성된다.

## 8. 입력·예외 처리 기준

| 상황 | 처리 방식 | 담당 코드 |
|---|---|---|
| 앞뒤 공백 (`" 1 "`) | `.strip()`으로 제거 후 처리 | `get_number`, `get_text` |
| 빈 입력 (그냥 Enter) | 안내 문구 출력 후 다시 입력받음 | `get_number`, `get_text` |
| 숫자가 아닌 입력 (`abc`) | `ValueError`를 잡아 안내 후 다시 입력받음 | `get_number` |
| 범위 밖 숫자 (`9`, `0`) | 안내 문구 출력 후 다시 입력받음 | `get_number` |
| `Ctrl+C` (`KeyboardInterrupt`) | 안내 문구 출력 후 안전 종료 | `QuizGame.run` |
| 입력 스트림 종료 (`Ctrl+D`, `EOFError`) | 안내 문구 출력 후 안전 종료 | `QuizGame.run` |
| `state.json`이 없음 | 기본 퀴즈 5개로 시작 | `QuizGame.load` |
| `state.json`이 손상됨 | 안내 후 기본 퀴즈로 복구하고 다시 저장 | `QuizGame.load` |
| 퀴즈가 하나도 없음 | 안내 문구 출력 후 메뉴로 복귀 | `play_quiz`, `show_quiz_list` |
| 아직 퀴즈를 풀지 않음 | 안내 문구 출력 후 메뉴로 복귀 | `show_score` |

## 9. main.py 전체 코드

```python
{{MAIN_PY}}
```

## 10. 코드로 배우는 Python (과제 목표 정리)

### 10-0. 과제 목표와 코드의 연결

| 과제 목표 | 이 프로젝트에서 쓰인 곳 |
|---|---|
| 변수가 무엇이고 왜 사용하는지 | `score`, `correct_count`, `self.best_score` |
| `int`, `str`, `bool`, `list`, `dict`의 차이 | 점수(`int`), 문제(`str`), 정답 여부(`bool`), 선택지(`list`), 저장 데이터(`dict`) |
| `if/elif/else` | 메뉴 분기 (`QuizGame.run`), 입력 검사 (`get_number`) |
| `for`와 `while`의 차이 | `for`: 퀴즈 출제, 목록 출력 / `while`: 메뉴 반복, 입력 재요청 |
| 함수, 매개변수, 반환값 | `get_number(prompt, min_value, max_value)` → 정수를 `return` |
| 클래스가 무엇이고 왜 사용하는지 | `Quiz`, `QuizGame` |
| `__init__`와 `self`의 역할 | `Quiz.__init__`, `self.question` 등 |
| 속성(attribute)과 메서드(method) | 속성: `question`, `choices`, `answer`, `quizzes`, `best_score` / 메서드: `show`, `is_correct`, `save`, `load` |
| 파일 열기, 읽기, 쓰기 | `QuizGame.save`, `QuizGame.load` |
| JSON 형식과 사용 이유 | `json.dump`, `json.load`로 `state.json` 저장·불러오기 |
| `try/except` | `get_number`(`ValueError`), `load`(파일 손상), `run`(`Ctrl+C`) |
| Git 7종, 브랜치 병합, `clone`/`pull` | [11장](#11-git-정리) |

### 10-1. 변수와 자료형

**변수**는 값을 저장해 두고 이름으로 다시 꺼내 쓰는 공간이다. 입력값을 기억해야 정답 비교와 점수 계산을 할 수 있어서 쓴다.

```python
correct_count = 0               # 정답 개수를 담는 변수
correct_count += 1              # 꺼내서 1을 더한 뒤 다시 담는다
```

| 자료형 | 뜻 | 이 프로젝트의 예 |
|---|---|---|
| `int` | 정수 | 점수 `80`, 정답 번호 `2` |
| `str` | 문자열 | 문제 `"파이썬에서 ..."` |
| `bool` | 참/거짓 | `is_correct()`의 결과 `True` / `False` |
| `list` | 순서 있는 묶음 `[ ]` | 선택지 `["int", "str", "bool", "list"]` |
| `dict` | 이름표:값 쌍 `{ }` | `{"question": ..., "choices": ..., "answer": ...}` |

- `list`는 **번호**(0부터)로, `dict`는 **이름표**로 꺼낸다. `fruits[2]`는 세 번째 값이다.
- `input()`의 결과는 **항상 `str`**이다. 숫자로 쓰려면 `int()`로 바꿔야 한다.
- `=`는 값을 **담는** 기호이고, `==`는 **같은지 비교**하는 기호이다.

**스스로 점검:** 변수를 왜 쓰는가? `list`와 `dict`는 값을 꺼내는 방법이 어떻게 다른가? 키보드로 `3`을 입력하면 어떤 자료형으로 받는가?

### 10-2. 조건문 `if / elif / else`

조건이 참일 때만 그 아래 코드를 실행한다. 위에서부터 차례로 검사해서 **처음 참인 곳 하나만** 실행한다.

```python
if choice == 1:
    self.play_quiz()
elif choice == 2:
    self.add_quiz()
else:
    ...
```

**스스로 점검:** `elif`와 `else`는 언제 실행되는가? `if`를 여러 번 쓰는 것과 `elif`로 잇는 것은 무엇이 다른가?

### 10-3. 반복문 `for`와 `while`

| | `for` | `while` |
|---|---|---|
| 쓰는 때 | 횟수나 대상이 정해졌을 때 | 조건이 끝날 때까지 몇 번인지 모를 때 |
| 이 프로젝트의 예 | 퀴즈를 하나씩 출제 | 메뉴를 종료 선택 전까지 반복, 올바른 입력이 나올 때까지 재요청 |

```python
for number, quiz in enumerate(self.quizzes, start=1):   # 퀴즈를 번호와 함께 하나씩
    ...

while True:                                              # break가 나올 때까지 반복
    ...
```

- `break`는 반복을 **완전히 끝낸다**. `continue`는 이번 반복을 건너뛰고 **처음으로 돌아간다**.
- `enumerate(목록, start=1)`은 번호와 값을 한 쌍씩 꺼낸다. 번호를 1부터 시작하게 했다.

**스스로 점검:** 퀴즈를 하나씩 출제할 때 왜 `for`를 썼는가? 메뉴 반복에 왜 `while`을 썼는가?

### 10-4. 함수, 매개변수, 반환값

함수는 여러 줄의 코드를 묶어 이름을 붙이고 필요할 때 불러 쓰는 것이다.

```python
def get_number(prompt, min_value, max_value):   # 매개변수 3개 = 함수에 넣는 재료
    ...
    return number                                # 반환값 = 함수가 돌려주는 결과

choice = get_number("선택: ", 1, 5)              # 부르면 결과가 choice에 담긴다
```

- **왜 쓰는가:** 같은 입력 검사를 메뉴, 정답 입력, 정답 번호 입력에서 모두 재사용하기 위해서다.
- `def`는 "이런 함수를 만들어 두겠다"는 **등록**이고, 이름 뒤에 `()`를 붙여야 **실행**된다.

**스스로 점검:** 매개변수와 반환값은 각각 무엇인가? `get_number`를 함수로 만든 이유는?

### 10-5. 클래스와 객체

클래스는 객체를 만드는 **설계도**(붕어빵 틀)이고, 객체는 그 설계도로 만든 **실물**(붕어빵)이다.

```python
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question     # 속성
        self.choices = choices
        self.answer = answer

    def is_correct(self, user_answer):   # 메서드
        return user_answer == self.answer

q1 = Quiz("파이썬에서 '같은지 비교'하는 기호는?", ["==", "=", "!=", "=>"], 1)
```

| 용어 | 뜻 |
|---|---|
| `__init__` | 객체를 만들 때 **자동으로 실행**되는 초기 설정 메서드(생성자) |
| `self` | 지금 만들어지는 **객체 자기 자신**. 메서드의 첫 번째 자리에 쓴다 |
| 속성(attribute) | 객체가 가진 데이터 (`self.question`) |
| 메서드(method) | 클래스 안에 정의된 함수 (`is_correct`) |

- **왜 쓰는가:** 퀴즈 1개는 문제, 선택지, 정답이 항상 한 세트라서 하나로 묶어야 관리하기 쉽다.
- **역할 분리:** `Quiz`는 퀴즈 1개를, `QuizGame`은 게임 전체(메뉴, 목록, 점수, 저장)를 맡는다.

**스스로 점검:** `__init__`는 언제 실행되는가? `self`는 무엇을 가리키는가? 속성과 메서드의 차이는?

### 10-6. 파일 입출력과 JSON

데이터를 파일에 저장하면 프로그램을 꺼도 남는다(**데이터 영속성**). 파일을 다루는 기본 과정은 **열기 → 읽기/쓰기 → 닫기**이다.

```python
with open(STATE_FILE, "w", encoding="utf-8") as file:     # 열기 (쓰기 모드)
    json.dump(data, file, ensure_ascii=False, indent=4)   # 쓰기

with open(STATE_FILE, "r", encoding="utf-8") as file:     # 열기 (읽기 모드)
    data = json.load(file)                                # 읽기
```

| 코드 | 의미 |
|---|---|
| `"r"` / `"w"` / `"a"` | 읽기 / 쓰기(덮어씀) / 이어쓰기 |
| `with ... as` | 블록이 끝나면 파일을 **자동으로 닫음** |
| `encoding="utf-8"` | 한글이 깨지지 않게 하는 설정 |
| `json.dump` / `json.load` | 파이썬 데이터 → 파일 / 파일 → 파이썬 데이터 |
| `ensure_ascii=False` | 한글을 `\uc548...`이 아닌 글자 그대로 저장 |

**JSON**은 데이터를 글자 형태로 저장하는 표준 형식이다. 파이썬의 `dict`, `list`와 모양이 거의 같고, 구조가 있는 데이터를 그대로 저장하고 불러올 수 있으며, 다른 프로그램과 언어도 읽을 수 있어서 데이터 저장에 쓴다.

- `Quiz` 객체는 JSON으로 바로 저장되지 않아서 `to_dict()`로 딕셔너리로 바꿔 저장하고, 읽을 때 `from_dict()`로 객체로 되돌린다.

**스스로 점검:** 파일을 열고 읽고 쓰는 기본 과정을 말해 보라. JSON을 왜 쓰는가? `with`를 쓰면 무엇이 좋은가?

### 10-7. 예외 처리 `try / except`

오류가 날 수 있는 코드를 **시도**(`try`)하고, 오류가 나면 프로그램이 죽지 않고 대신 **처리**(`except`)한다.

```python
try:
    number = int(text)            # "abc"는 숫자로 못 바꿔서 오류가 난다
except ValueError:
    print("⚠️ 잘못된 입력입니다.")
    continue                      # 다시 입력받는다
```

| 예외 | 언제 발생하나 |
|---|---|
| `ValueError` | 형태가 틀린 값을 변환할 때 (`int("abc")`) |
| `json.JSONDecodeError` | JSON 문법이 틀린 파일을 읽을 때 |
| `KeyboardInterrupt` | `Ctrl+C`를 눌렀을 때 |
| `EOFError` | 입력 스트림이 끝났을 때 (`Ctrl+D`) |

**스스로 점검:** `try/except`가 없으면 `abc`를 입력했을 때 어떻게 되는가? 파일이 손상됐을 때 프로그램이 멈추지 않게 어디서 처리했는가?

## 11. Git 정리

### 11-1. Git이란

Git은 파일의 변경 이력을 기록하고 관리하는 도구다. 잘못 고쳐도 이전 상태로 돌아갈 수 있고, 언제 무엇을 바꿨는지 알 수 있으며, 여러 사람이 함께 작업할 수 있어서 필요하다.
**Git**은 내 PC의 버전 관리 도구이고, **GitHub**는 그 이력을 올려 두고 협업하는 원격 플랫폼이다.

### 11-2. 기초 명령어 7종

| 명령어 | 뜻 | 하는 일 |
|---|---|---|
| `git init` | initialize | 폴더를 Git 저장소로 만든다 |
| `git add` | 스테이징 | 커밋에 포함할 변경을 고른다 |
| `git commit -m "메시지"` | 커밋 | 변경을 이력으로 저장한다 |
| `git push` | 밀어올리기 | 내 커밋을 GitHub로 보낸다 |
| `git pull` | 끌어오기 | GitHub의 변경을 내 PC로 가져온다 |
| `git checkout` | 전환 | 브랜치를 바꾼다 (`-b`는 새로 만들며 이동) |
| `git clone` | 복제 | 원격 저장소를 처음 통째로 내려받는다 |

**`clone`과 `pull`의 차이:** `clone`은 처음 한 번 저장소 전체를 받고, `pull`은 이미 가진 저장소에 새로 바뀐 내용만 가져온다.

### 11-3. 브랜치와 병합

브랜치는 `main`을 건드리지 않고 복사본에서 따로 작업하는 가지이고, 병합(merge)은 그 작업을 `main`에 합치는 것이다. 이 프로젝트에서는 퀴즈 풀기 기능을 별도 브랜치에서 개발한 뒤 병합했다.

```bash
git checkout -b <브랜치이름>        # 새 브랜치를 만들며 이동
# 작업 → git add → git commit
git checkout main                   # main으로 돌아가기
git merge <브랜치이름>              # 작업을 main에 합치기
```

### 11-4. 커밋 메시지 규칙

작업 내용을 드러내는 형식으로 쓴다.

| 접두어 | 의미 | 예 |
|---|---|---|
| `Feat:` | 기능 추가 | `Feat: 퀴즈 출제 기능 구현` |
| `Fix:` | 오류 수정 | `Fix: 점수 계산 오류 수정` |
| `Docs:` | 문서 | `Docs: README 실행 방법 추가` |
| `Refactor:` | 구조 개선 | `Refactor: QuizGame 클래스로 책임 분리` |
| `Merge:` | 병합 | `Merge: 퀴즈 풀기 기능 병합` |

### 11-5. 커밋 이력

```bash
git log --oneline --graph
```

```text
{{GIT_LOG}}
```

### 11-6. clone / pull 실습

- [ ] 저장소를 `git clone`으로 별도 폴더에 복제했다.
- [ ] 복제본에서 간단한 변경(README에 한 줄 추가)을 하고 `commit` → `push` 했다.
- [ ] 기존 작업 폴더에서 `git pull`로 변경을 가져왔다.
- [ ] `pull` 받은 내용이 정상적으로 반영된 것을 확인했다.

## 12. 실행 화면

| 화면 | 파일 |
|---|---|
| 개발 환경(버전, Git 설정) | `docs/screenshots/env.png` |
| 메뉴 | `docs/screenshots/menu.png` |
| 퀴즈 풀기와 결과(점수) | `docs/screenshots/play.png` |
| 퀴즈 추가 | `docs/screenshots/add_quiz.png` |
| 퀴즈 목록 | `docs/screenshots/list.png` |
| 점수 확인 | `docs/screenshots/score.png` |
| 잘못된 입력 처리 | `docs/screenshots/invalid_input.png` |
| 재시작 후 데이터 유지 | `docs/screenshots/persist.png` |
| `git log --oneline --graph` | `docs/screenshots/git_log.png` |

## 13. 제출물 체크리스트

- [ ] GitHub 저장소 URL: `https://github.com/<GitHub아이디>/quiz-game`
- [ ] 개발 환경 설정 스크린샷
- [ ] 프로그램 실행 결과 스크린샷 (퀴즈 추가, 목록, 플레이, 점수)
- [ ] `git log --oneline --graph` 결과 스크린샷
- [x] 퀴즈 5개 이상, 클래스 2개 이상, 커밋 10개 이상
- [x] 브랜치 생성과 병합 1회 이상
- [ ] `clone`과 `pull` 각 1회 이상
- [ ] README의 `<...>` 자리표시를 모두 실제 값으로 교체
