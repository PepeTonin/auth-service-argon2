from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

import mysql.connector

from db.service import init_db, create_new_user, get_user_by_username

from schemas.schemas import Request, RequestBody, ReqMetadata, ReqUser

from utils.hash_argon2 import hash_password_argon2, verify_password_argon2
from utils.hash_pbkdf2 import hash_password_pbkdf2, verify_password_pbkdf2
from utils.hash_migration import verify_hashing_type, change_hash_type
from utils.crypt import decrypt_body


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def test_connection():
    return JSONResponse(content={"message": "server is running"}, status_code=200)


@app.post("/signup/{hash_type}")
def signup(hash_type: str, request: Request):

    if hash_type.lower() not in ["argon2", "pbkdf2"]:
        raise HTTPException(status_code=400, detail="Invalid hash type")

    body = bytes.fromhex(request.body)
    iv = bytes.fromhex(request.iv)
    decryted_body: RequestBody = decrypt_body(iv, body)

    user: ReqUser = decryted_body["user"]
    if hash_type.lower() == "argon2":
        hashed_password = hash_password_argon2(user["password"])
    else:
        hashed_password = hash_password_pbkdf2(user["password"])

    metadata: ReqMetadata = decryted_body["metadata"]

    try:
        user_id = create_new_user(
            user["username"], hashed_password, metadata["created_at"]
        )

        response = JSONResponse(
            content={"message": "User created", "id": user_id}, status_code=201
        )

        return response

    except mysql.connector.Error as _:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")


@app.post("/login")
async def login(request: Request, background_tasks: BackgroundTasks):

    body = bytes.fromhex(request.body)
    iv = bytes.fromhex(request.iv)
    decryted_body: RequestBody = decrypt_body(iv, body)

    user: ReqUser = decryted_body["user"]

    try:
        fetched_user = get_user_by_username(user["username"])

        if fetched_user is None:
            raise HTTPException(status_code=401, detail="Auth failed")

        if verify_hashing_type(fetched_user["password"]) == "argon2":
            if verify_password_argon2(fetched_user["password"], user["password"]):
                response = JSONResponse(
                    content={"message": "Login successful", "id": fetched_user["id"]},
                    status_code=200,
                )
                return response
            else:
                raise HTTPException(status_code=401, detail="Auth failed")
        else:
            if verify_password_pbkdf2(fetched_user["password"], user["password"]):
                response = JSONResponse(
                    content={"message": "Login successful", "id": fetched_user["id"]},
                    status_code=200,
                )
                background_tasks.add_task(
                    change_hash_type, user["username"], user["password"]
                )

                return response
            else:
                raise HTTPException(status_code=401, detail="Auth failed")

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail="Failed to connect to the database")
