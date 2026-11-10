"""퀴즈 수가 많아질 때(1,000개 이상) 저장·불러오기·목록 출력의 시간과 메모리를 측정한다.

사용법: python3 benchmark.py
- 실제 state.json 은 건드리지 않고, 임시 폴더에서만 측정한다.
- 표준 라이브러리만 사용한다.
"""
import contextlib
import io
import os
import statistics
import tempfile
import time
import tracemalloc

import main

SIZES = [1000, 5000, 10000]   # 측정할 퀴즈 개수
REPEAT = 5                    # 각 측정을 반복할 횟수 (중앙값 사용)


def make_game(count):
    """퀴즈 count 개를 가진 QuizGame 을 만든다."""
    game = main.QuizGame()
    game.quizzes = [
        main.Quiz(f"퀴즈 {i}번 문제입니다.", ["선택지 A", "선택지 B", "선택지 C", "선택지 D"], i % 4 + 1)
        for i in range(count)
    ]
    game.best_score = 80
    return game


def median_ms(func):
    """func 를 REPEAT 번 실행해 걸린 시간(ms)의 중앙값을 돌려준다."""
    times = []
    for _ in range(REPEAT):
        start = time.perf_counter()
        func()
        times.append((time.perf_counter() - start) * 1000)
    return statistics.median(times)


def silent(func):
    """func 가 출력하는 글자를 화면에 내보내지 않고 버린다."""
    def wrapper():
        with contextlib.redirect_stdout(io.StringIO()):
            func()
    return wrapper


def measure(count, folder):
    main.STATE_FILE = os.path.join(folder, "state.json")
    main.BACKUP_FILE = main.STATE_FILE + ".bak"
    main.CORRUPT_FILE = main.STATE_FILE + ".corrupt"
    main.TMP_FILE = main.STATE_FILE + ".tmp"

    game = make_game(count)
    game.save()  # 파일을 먼저 만들어 두면 이후 save 는 백업 단계까지 포함해 측정된다.

    save_ms = median_ms(game.save)
    load_ms = median_ms(lambda: main.QuizGame().load())
    list_ms = median_ms(silent(game.show_quiz_list))
    size_kb = os.path.getsize(main.STATE_FILE) / 1024

    # 메모리: 불러오는 동안의 최대 사용량 (tracemalloc 은 느려서 시간 측정과 따로 실행)
    tracemalloc.start()
    main.QuizGame().load()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {"count": count, "save": save_ms, "load": load_ms, "list": list_ms,
            "size": size_kb, "peak": peak / 1024 / 1024}


def main_benchmark():
    with tempfile.TemporaryDirectory() as folder:
        rows = [measure(count, folder) for count in SIZES]

    print("| 퀴즈 수 | 저장 (ms) | 불러오기 (ms) | 목록 출력 (ms) | 파일 크기 (KB) | 불러올 때 최대 메모리 (MB) |")
    print("|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        print(f"| {r['count']:,} | {r['save']:.1f} | {r['load']:.1f} | {r['list']:.1f} "
              f"| {r['size']:.0f} | {r['peak']:.2f} |")

    first, last = rows[0], rows[-1]
    ratio_n = last["count"] / first["count"]
    print()
    print(f"퀴즈 수가 {ratio_n:.0f}배(1,000 → {last['count']:,}개)가 될 때: "
          f"저장 {last['save'] / first['save']:.1f}배, 불러오기 {last['load'] / first['load']:.1f}배, "
          f"목록 출력 {last['list'] / first['list']:.1f}배, 메모리 {last['peak'] / first['peak']:.1f}배 증가")


if __name__ == "__main__":
    main_benchmark()
