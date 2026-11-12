from load_scores import load_scores

def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5 
 
# def test_일부러_틀린_테스트():
#     kept, skipped = load_scores("scores.csv")
#     assert len(kept) == 99          # ← 일부러 틀린 숫자

