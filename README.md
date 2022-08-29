
### Setup
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run
```
# run server
source venv/bin/activate
uvicorn shortener_app.main:app --reload
```
### GET
`/{url_key}`
### POST 
`/url`
### GET
`/admin/{secret_key}`
#### Response
```
{
  "target_url": "https://www.foo.com",
  "is_active": true,
  "clicks": 3,
  "url": "http://127.0.0.1:8000/😨😅😯😐👺",
  "admin_url": "http://127.0.0.1:8000/admin/🥑😨😅😯😐👺_😒😈😖🤥😿😂🤫😯"
}
```
### DELETE
`/admin/{secret_key}`
```
{
  "detail": "Succsessfully deleted the 'https://www.foo.com'"
}
```

### Swaggger
http://127.0.0.1:8000/docs