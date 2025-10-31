from database import db
from sqlalchemy import text
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import uvicorn
import bcrypt
from middleware import create_token, verify_token

load_dotenv()

app = FastAPI(title="Student App", version="1.0.0")

class simple(BaseModel):
    name : str = Field(..., example="John Doe")
    email: str = Field(..., example="John@gmail.com")
    password : str = Field(..., example="Doe123")
    userType : str = Field(..., example='student')


token_time = int(os.getenv("token_time"))

@app.get("/")
def welcome():
    return {"Message": "Welcome back!"}


@app.post("/Signup")
def SignUp(input: simple):
    try:

        # To check for duplicates: using email
        duplicate_query = text("""
                SELECT * FROM users
                WHERE email = :email
                                """)
        
        existing = db.execute(duplicate_query, {"email" : input.email})

        if existing:
            print("Email already exists")
            # raise HTTPException(status_code=400, detail="Email already exists")

        


        # this is inseerting values into the already created table -users
        query = text("""
            INSERT INTO users(name, email, password, userType)
            VALUES(:name, :email, :password, :userType)
                     
        """)
        # this is to encrypt your password
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        print(hashedPassword)

        
        # execute your database
        db.execute(query, {"name": input.name, "email": input.email, "password":hashedPassword, "userType" : input.userType})
        db.commit()  # commit the changes into your database

        return {"message" : "user signed up successfully",
                "data": {"name": input.name, "email": input.email, "userType": input.userType}
                }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


class LoginRequest(BaseModel):
    
    email : str = Field(..., example="John@gmail.com")
    password : str = Field(..., example="Doe123")


@app.post("/login")
def log_in(input: LoginRequest):

    try:
        query = text("""
            SELECT * FROM users
            WHERE email = :email
                       """)
        
        result = db.execute(query, {"email" : input.email}).fetchone()

     

        if not result:
            raise HTTPException(status_code=404, detail="Invalid email or password")
        
        verified_password = bcrypt.checkpw(input.password.encode('utf-8'), result.password.encode('utf-8'))

        if not verified_password:
            raise HTTPException(status_code=404, detail="Invalid email or password")
        
        encoded_token = create_token(details={
        
        "email": result.email,
        "userType": result.userType,
        "userId": result.id
        }, expiry=token_time) 

        return {
            "Message" : "Login Successful",
            "token": encoded_token
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

   
class handlecourses(BaseModel):
    title: str = Field(..., example="Backend course")
    level: str = Field(..., example="intermediate")


@app.post("/courses")
def addcourses(input:handlecourses, user_data = Depends(verify_token)):
    try:
        print(user_data)

        if user_data["userType"] != "admin":
            raise HTTPException(status_code=401, detail="You are not eligible to add course")
            

        query = text("""
            INSERT INTO courses (title, level)
            VALUES(:title, :level)
            """)
        
        db.execute(query, {"title" : input.title, "level": input.level})

        db.commit()

        return{
            "message" : "Inserted successfully",
            "data" : {input.title, input.level}
        }
    
    except Exception as e:
        raise HTTPException(status_code=501, detail=str(e))

class Enrolling(BaseModel):
    courseId : int = Field(...)


@app.post("/enroll")
def enroll_student(input:Enrolling, user_data= Depends(verify_token)):
    try:
        print(user_data)

        if user_data["userType"] != "student":
            raise HTTPException(status_code=400, detail=("Only students can enroll!"))
        
        query = text("""
            INSERT INTO enrollments(userId, courseId)
            VALUES(:userId, :courseId)
        """)
        
        db.execute(query, {"userId": user_data["userId"], "courseId": input.courseId})
        db.commit()

        return{
            "message": "Enrolled successfully",
            "data": {"userId": user_data["userId"], "courseId": input.courseId}
        }
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e)) 

if __name__== "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))

#     {
#   "detail": "(pymysql.err.ProgrammingError) (1064, \"You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '1)' at line 2\")\n[SQL: \n            Insert into enrollments(userId, courseId)\n            Values(%(userId)s %(courseId)s)\n        ]\n[parameters: {'userId': 1, 'courseId': 1}]\n(Background on this error at: https://sqlalche.me/e/20/f405)"
# }