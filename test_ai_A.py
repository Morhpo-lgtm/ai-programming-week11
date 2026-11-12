'''아래 함수의 단위 테스트를 pytest로 작성해 주세요.
정상 · 예외 · 경계값을 모두 포함해 주세요.'''
import csv

MIN_SCORE = 0
MAX_SCORE = 100


def load_scores(path):
    """성적 CSV를 읽어 (유효한 목록, 건너뛴 줄 기록) 을 돌려준다."""
    kept = []
    skipped = []

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for line_no, row in enumerate(reader, start=1):
            if line_no == 1:              # 헤더
                continue
            if not row:                   # 빈 줄 — 기록하지 않는다
                continue

            원본 = ",".join(row)

            if len(row) != 2:
                skipped.append((line_no, 원본, "열 개수가 2가 아님"))
                continue

            name = row[0].strip()
            raw = row[1].strip()

            if name == "":
                skipped.append((line_no, 원본, "이름이 비어 있음"))
                continue
            if raw == "":
                skipped.append((line_no, 원본, "점수가 비어 있음"))
                continue

            try:
                score = int(raw)
            except ValueError:
                skipped.append((line_no, 원본, "점수가 정수가 아님"))
                continue

            if score < MIN_SCORE or score > MAX_SCORE:
                skipped.append((line_no, 원본, "점수가 0~100 밖"))
                continue

            kept.append((name, score))

    return kept, skipped


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "scores.csv"
    kept, skipped = load_scores(path)
    print(f"읽은 줄 : {len(kept)}개")
    for name, score in kept:
        print(f"  {name} {score}")
    print(f"건너뛴 줄 : {len(skipped)}개")
    for line_no, 원본, 이유 in skipped:
        print(f"  {line_no}행  {원본}   ← {이유}")


import pytest

from load_scores import load_scores


def test_정상적인_행만_유효한_목록으로_반환한다(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "name,score\n김하나,88\n최수민, 77 \n\n김하나,91\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == [("김하나", 88), ("최수민", 77), ("김하나", 91)]
    assert skipped == []


def test_잘못된_행은_줄번호와_이유를_기록하고_건너뛴다(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "name,score\n"
        "이두리,105\n"
        "박세찬,\n"
        "한겨울,결석\n"
        "장미르,7 2\n"
        "장미르,72,비고\n"
        ",90\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == [
        (2, "이두리,105", "점수가 0~100 밖"),
        (3, "박세찬,", "점수가 비어 있음"),
        (4, "한겨울,결석", "점수가 정수가 아님"),
        (5, "장미르,7 2", "점수가 정수가 아님"),
        (6, "장미르,72,비고", "열 개수가 2가 아님"),
        (7, ",90", "이름이 비어 있음"),
    ]


def test_점수의_최솟값과_최댓값은_유효하다(tmp_path):
    path = tmp_path / "boundaries.csv"
    path.write_text(
        "name,score\n최저점,0\n최고점,100\n",
        encoding="utf-8",
    )

    kept, skipped = load_scores(path)

    assert kept == [("최저점", 0), ("최고점", 100)]
    assert skipped == []


def test_존재하지_않는_파일은_FileNotFoundError를_그대로_발생시킨다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")

