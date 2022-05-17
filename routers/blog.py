from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import blogs.schemas
from app_db import database, models
from blogs.schemas import Blog, ShowBlog
from users.schemas import User
from login import oauth2

router = APIRouter(
    prefix='/blogs',
    tags=['Blogs'],
)


@router.get('/', response_model=list[ShowBlog])
def read_blogs(db: Session = Depends(database.get_db),
               current_user: User = Depends(
                   oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/{blog_id}',
            response_model=ShowBlog,
            status_code=status.HTTP_200_OK
            )
def read_blog(blog_id: int, db: Session = Depends(database.get_db),
              current_user: User = Depends(
                  oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Block for error: blogs id - [{blog_id}], not found.'
        )
    return blog


@router.post('/',
             status_code=status.HTTP_201_CREATED
             )
def create_blog(request: Blog, db: Session = Depends(database.get_db),
                current_user: User = Depends(
                    oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, text=request.text, owner_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.put('/{blog_id}',
            status_code=status.HTTP_202_ACCEPTED,
            )
def put_blog(blog_id, request: Blog,
             db: Session = Depends(database.get_db),
             current_user: User = Depends(
                 oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Block for error: blogs id - [{blog_id}], not found.'
        )
    blog.update(request.dict())
    db.commit()
    return 'updated'


@router.delete('/{blog_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               )
def delete_blog(blog_id: int, db: Session = Depends(database.get_db),
                current_user: User = Depends(
                    oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(
        synchronize_session=False)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Block for error: blogs id - [{blog_id}], not found.'
        )
    db.commit()
    return 'deleted'
