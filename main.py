from fastapi import FastAPI

from app_db import models
from app_db.database import engine
from routers import blog, authentication, user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)


@app.get('/')
def root():
    return {'status': 'ok'}
