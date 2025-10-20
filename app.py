import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="Simple FastAPI APP", version="1.0")

data = [
    {"name": "Augustine Aura", "age": 23, "track" : "FullStack Deceloper"},
    {"name": "Jaden Smith", "age": 20, "track" : "Backend Engineer"},
    {"name": "Azeezat Olamide", "age": 21, "track" : "AI Developer"}]


class item(BaseModel):
    name : str
    age : int
    track : str



# @app.get("/", description="This endpoint is just to return a welcome message!")
# def root():
#     return {"Message": "Welcome to my FASTAPI Application"}

@app.get("/", description="This gets the data from the student's database")
def get_data():
    return {"Message":"To retrieve data of the students", "Data": data }

@app.post("/Create_data")
def create_data(request : item):
    data.append(request.dict())
    return {"Message": "New Data received", "Data": data}

@app.put("/Update_data/{id}")
def update_data(id: int, request : item):
    data[id] = request.dict()
    print(data)
    return {"Message": "Updated data", "Data": data}


@app.patch("/update_info/{id}")
def updated_info(id: int, request:item):
    data[id] = request.dict()
    return {"Message": "Updated Info", "Data" : data}


@app.delete("/delete_data/{id}")
def delete_data(id:int):
    for i in data:
        if data[id] == id:
            data.pop(id)

    return {"Message": "Data deleted", "Data": data}
 



if __name__ == "__main__":
    print(os.getenv("host"))
    print(os.getenv("port"))
    uvicorn.run(app, host=os.getenv("host"), port=os.getenv("port"))


