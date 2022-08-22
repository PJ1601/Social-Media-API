from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. database import get_db

router = APIRouter( 
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=list[schemas.Post_Vote])

# @router.get("/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
 , Limit: int= 10, skip: int= 0, search: Optional[str]= ""):
    
    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # posts = db.execute(""" 
    # SELECT posts.*, COUNT(votes.post.id) AS votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id
    # GROUP BY posts.id""")
    # results = []
    # for post in posts:
    #     results.append(dict(post))
    # print(results)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()   

    return posts



@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def createposts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends
               (oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                 
    #              (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    print(current_user.email)
    new_post = models.Post( owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



@router.get("/{id}", response_model=schemas.Post_Vote)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s RETURNING * """, (str(id)))
    #post = cursor.fetchone()
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                           detail=f"Post with id: {id} was not found")
    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    deleted_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested axtion")

    deleted_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def update_post(id: int, post:schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends
               (oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *"""
    #                , (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested axtion")


    update_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return update_query.first()