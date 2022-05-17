from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from blog import schemas, models, database, hashing

router = APIRouter(
    prefix='/user',
    tags=['Users'],
)


@router.get('/', response_model=list[schemas.ShowUser])
def read_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()


@router.get('/{user_id}', response_model=schemas.ShowUser)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    new_user = models.User(name=request.name, email=request.email,
                           password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
