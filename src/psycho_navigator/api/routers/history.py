from datetime import UTC, datetime
from secrets import compare_digest
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from psycho_navigator.api.routers.tests import calculate_result
from psycho_navigator.history import attempts, users
from psycho_navigator.schemas.results import (
    EpiResult,
    QuestionnaireResultRequest,
    QuestionnaireResultResponse,
)
from starlette.concurrency import run_in_threadpool


def authenticate(
    request: Request,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(HTTPBearer(auto_error=False))
    ],
):
    token = request.app.state.history_token
    if (
        not credentials
        or not token
        or not compare_digest(credentials.credentials.encode(), token.encode())
    ):
        raise HTTPException(401, "Service authentication required")


router = APIRouter(
    prefix="/users/{telegram_id}/attempts", dependencies=[Depends(authenticate)]
)
Owner = Annotated[int, Path(gt=0)]


class AttemptSummary(BaseModel):
    attempt_id: UUID
    test_name: str
    completed_at: datetime


class SavedAttempt(AttemptSummary):
    profile: QuestionnaireResultResponse | EpiResult


def owner_id(telegram_id):
    return (
        select(users.c.id)
        .where(users.c.telegram_user_id == telegram_id)
        .scalar_subquery()
    )


@router.get("", response_model=list[AttemptSummary])
def history(
    request: Request,
    telegram_id: Owner,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    with request.app.state.db.connect() as conn:
        query = (
            select(attempts.c.attempt_id, attempts.c.test_name, attempts.c.completed_at)
            .where(attempts.c.user_id == owner_id(telegram_id))
            .order_by(attempts.c.completed_at.desc(), attempts.c.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return conn.execute(query).mappings().all()


def lookup(conn, telegram_id, attempt_id):
    query = select(attempts).where(
        attempts.c.user_id == owner_id(telegram_id),
        attempts.c.attempt_id == str(attempt_id),
    )
    return conn.execute(query).mappings().one_or_none()


@router.get("/{attempt_id}", response_model=SavedAttempt)
def detail(request: Request, telegram_id: Owner, attempt_id: UUID):
    with request.app.state.db.connect() as conn:
        row = lookup(conn, telegram_id, attempt_id)
        if row is None:
            raise HTTPException(404, "Attempt not found")
        return row


@router.post("/{attempt_id}", response_model=SavedAttempt)
async def save(
    request: Request,
    telegram_id: Owner,
    attempt_id: UUID,
    submission: QuestionnaireResultRequest,
    test_id: Annotated[int, Query(ge=1, le=2)] = 1,
):
    tests = request.app.state.questionnaires
    profile = await calculate_result(test_id, submission, tests, request)
    name = next(test.name for test in tests if test.id == test_id)
    code, version = {1: ("BFI-2", "B-1"), 2: ("EPI", "A-1")}[test_id]

    def persist():
        with request.app.state.db.begin() as conn:
            conn.execute(
                insert(users)
                .values(telegram_user_id=telegram_id)
                .on_conflict_do_nothing()
            )
            conn.execute(
                insert(attempts)
                .values(
                    user_id=owner_id(telegram_id),
                    attempt_id=str(attempt_id),
                    test_code=code,
                    version=version,
                    completed_at=datetime.now(UTC).isoformat(),
                    test_name=name,
                    profile=profile.model_dump(mode="json"),
                )
                .on_conflict_do_nothing(index_elements=["user_id", "attempt_id"])
            )
            saved = lookup(conn, telegram_id, attempt_id)
            if saved["test_code"] != code:
                raise HTTPException(409, "Attempt belongs to another questionnaire")
            return saved

    return await run_in_threadpool(persist)


@router.delete("/{attempt_id}", status_code=204)
def delete_attempt(request: Request, telegram_id: Owner, attempt_id: UUID):
    with request.app.state.db.begin() as conn:
        result = conn.execute(attempts.delete().where(
            attempts.c.user_id == owner_id(telegram_id),
            attempts.c.attempt_id == str(attempt_id),
        ))
        if not result.rowcount:
            raise HTTPException(404, "Attempt not found")
