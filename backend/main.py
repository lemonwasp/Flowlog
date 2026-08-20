import os
import traceback
import uuid

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend import crud
from backend.database import SessionLocal, engine
from backend.models import Base
from backend.schemas import (
    ActivityCreate,
    ActivityTypeCreate,
    EmotionCreate,
    FlowCurveCreate,
    UserCreate,
)
from backend.utils.emotion_processing import process_emotion_text

app = FastAPI(title="Flowlog API")

DEFAULT_CORS_ORIGINS = "http://localhost:3000,http://127.0.0.1:5500"
allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", DEFAULT_CORS_ORIGINS).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Flowlog API with Supabase & SQLAlchemy"}


@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.name, user.email)


@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/emotions/")
def add_emotion(emotion_data: EmotionCreate, db: Session = Depends(get_db)):
    try:
        if emotion_data.free_text:
            processed = process_emotion_text(emotion_data.free_text)
            emotion = processed["final_emotion"]
            score = processed["emotion_score"]
            keywords = ",".join(processed["keywords"])
        else:
            emotion = emotion_data.emotion
            score = None
            keywords = None

        return crud.create_emotion(
            db,
            uuid.UUID(emotion_data.user_id),
            emotion,
            score,
            keywords,
        )
    except Exception as exc:
        print(f"ERROR in add_emotion: {exc}")
        raise


@app.post("/activity-types/")
def add_activity_type(activity_type: ActivityTypeCreate, db: Session = Depends(get_db)):
    return crud.create_activity_type(db, activity_type.name)


@app.post("/activities/")
def add_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    return crud.create_activity(
        db,
        uuid.UUID(activity.user_id),
        uuid.UUID(activity.activity_type_id),
        activity.description,
    )


@app.post("/flow-curve/")
def add_flow_curve(flow_curve: FlowCurveCreate, db: Session = Depends(get_db)):
    return crud.create_flow_curve(
        db,
        uuid.UUID(flow_curve.user_id),
        flow_curve.time_spent,
        flow_curve.satisfaction,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    print("=" * 50)
    print(f"Unhandled Exception: {exc!r}")
    traceback.print_exc()
    print("=" * 50)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error - check server logs."},
    )
