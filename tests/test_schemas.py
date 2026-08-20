import pytest
from pydantic import ValidationError

from backend.schemas import ActivityCreate, EmotionCreate, FlowCurveCreate, UserCreate


def test_user_create_requires_name_and_email():
    user = UserCreate(name="Test User", email="test@example.com")

    assert user.name == "Test User"
    assert user.email == "test@example.com"


def test_emotion_create_allows_selected_or_free_text_input():
    selected = EmotionCreate(user_id="user-1", emotion="happy")
    free_text = EmotionCreate(user_id="user-1", free_text="오늘은 기분이 좋다")

    assert selected.emotion == "happy"
    assert selected.free_text is None
    assert free_text.free_text == "오늘은 기분이 좋다"


def test_activity_create_requires_activity_type():
    with pytest.raises(ValidationError):
        ActivityCreate(user_id="user-1", description="Morning run")


def test_flow_curve_requires_time_and_satisfaction():
    flow = FlowCurveCreate(user_id="user-1", time_spent=1.5, satisfaction=4.5)

    assert flow.time_spent == 1.5
    assert flow.satisfaction == 4.5
