from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.tea import TeaModel
from models.comment import CommentModel
from serializers.comment import (
    CommentSchema,
    CreateCommentSchema,
    UpdateCommentSchema
)
from database import get_db


router = APIRouter(tags=["Tea Managment"])


# Get all comments for a specific tea
@router.get("/teas/{tea_id}/comments", response_model=List[CommentSchema])
def get_comments_for_tea(
    tea_id: int,
    db: Session = Depends(get_db)
):
    tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()

    if not tea:
        raise HTTPException(
            status_code=404,
            detail="Tea not found"
        )

    return tea.comments


# Get a single comment by id
@router.get("/comments/{comment_id}", response_model=CommentSchema)
def get_comment_by_id(
    comment_id: int,
    db: Session = Depends(get_db)
):
    comment = (
        db.query(CommentModel)
        .filter(CommentModel.id == comment_id)
        .first()
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    return comment


# Add a new comment to a tea
@router.post(
    "/teas/{tea_id}/comments",
    response_model=CommentSchema,
    status_code=201
)
def create_comment(
    tea_id: int,
    comment: CreateCommentSchema,
    db: Session = Depends(get_db)
):
    tea = db.query(TeaModel).filter(TeaModel.id == tea_id).first()

    if not tea:
        raise HTTPException(
            status_code=404,
            detail="Tea not found"
        )

    new_comment = CommentModel(
        content=comment.content,
        tea_id=tea_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


# Update an existing comment
@router.put("/comments/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment: UpdateCommentSchema,
    db: Session = Depends(get_db)
):
    db_comment = (
        db.query(CommentModel)
        .filter(CommentModel.id == comment_id)
        .first()
    )

    if not db_comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    db_comment.content = comment.content

    db.commit()
    db.refresh(db_comment)

    return db_comment


# Delete a comment
@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    db_comment = (
        db.query(CommentModel)
        .filter(CommentModel.id == comment_id)
        .first()
    )

    if not db_comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found"
        )

    db.delete(db_comment)
    db.commit()

    return None