from backend.utils.emotion_processing import process_emotion_text


def test_process_emotion_text_detects_positive_words():
    result = process_emotion_text("오늘은 행복 신나다")

    assert result["final_emotion"] == "positive"
    assert result["emotion_score"] > 0
    assert "행복" in result["keywords"]


def test_process_emotion_text_detects_negative_words():
    result = process_emotion_text("요즘 우울 힘들다")

    assert result["final_emotion"] == "negative"
    assert result["emotion_score"] < 0
    assert "우울" in result["keywords"]


def test_process_emotion_text_defaults_to_neutral():
    result = process_emotion_text("오늘은 평범한 하루")

    assert result["final_emotion"] == "neutral"
    assert result["emotion_score"] == 0.0
