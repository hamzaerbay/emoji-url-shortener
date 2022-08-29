import secrets
import validators

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from http.client import HTTPException
from sqlalchemy.orm import Session
from starlette.datastructures import URL


from . import schemas, models, crud
from .database import SessionLocal, engine
from .config import get_settings

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=400, detail=message)


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
def read_root():
    return "Welcome to the Emoji URL shortener API 😎"


@app.get("/{url_key}")
def forward_to_target_url(
    url_key: str, request: Request, db: Session = Depends(get_db)
):

    db_url = crud.get_db_url_by_key(db=db, url_key=url_key)

    if db_url:
        # update clicks
        crud.update_url_clicks(db=db, db_url=db_url)
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="😵 😵 😵 Provided URL is not valid")

    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    return get_admin_info(db_url)


@app.get(
    "/admin/{secret_key}",
    name="admin info",
    response_model=schemas.URLInfo,
)
def get_url_info(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        db_url.url = db_url.key
        db_url.admin_url = db_url.secret_key

        return get_admin_info(db_url)
    else:
        raise_not_found(request)


def get_admin_info(db_url: models.URL) -> schemas.URLInfo:
    base_url = URL(get_settings().base_url)
    admin_endpoint = app.url_path_for(
        "admin info", secret_key=db_url.secret_key
    )
    db_url.url = str(base_url.replace(path=db_url.key))
    db_url.admin_url = str(base_url.replace(path=admin_endpoint))
    return db_url


@app.delete("/admin/{secret_key}")
def delete_url(secret_key: str, request: Request, db: Session = Depends(get_db)):
    if db_url := crud.deactivate_url_by_secret_key(db, secret_key=secret_key):
        message = f"Succsessfully deleted the '{db_url.target_url}'"
        return {"detail": message}
    else:
        raise_not_found(request)
