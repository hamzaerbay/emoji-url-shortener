import secrets

# import string
from sqlalchemy.orm import Session

# import emoji
from . import crud


def get_emojis():
    # TODO: use emoji lib
    return "๐๐๐๐๐๐๐๐คฃ๐ฅฒ๐๐๐๐๐๐๐๐ฅฐ๐๐๐๐๐๐๐๐๐คช๐คจ๐ง๐ค๐๐ฅธ๐คฉ๐ฅณ๐๐๐๐๐๐๐๐ฃ๐๐ซ๐ฉ๐ฅบ๐ข๐ญ๐ค๐ ๐ก๐คฌ๐คฏ๐ณ๐ฅต๐ฅถ๐ฑ๐จ๐ฐ๐ฅ๐๐ค๐ค๐คญ๐คซ๐คฅ๐ถ๐๐๐ฌ๐๐ฏ๐ฆ๐ง๐ฎ๐ฒ๐ฅฑ๐ด๐คค๐ช๐ต๐ค๐ฅด๐คข๐คฎ๐คง๐ท๐ค๐ค๐ค๐ค ๐๐ฟ๐น๐บ๐คก๐ฉ๐ป๐๐ฝ๐พ๐ค๐๐บ๐ธ๐น๐ป๐ผ๐ฝ๐๐ฟ๐พ"


def create_random_key(length: int = 5) -> str:
    # chars = string.ascii_uppercase + string.digits
    chars = get_emojis()
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
