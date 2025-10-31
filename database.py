import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pymysql.constants import CLIENT


load_dotenv()

db_url = f'mysql+pymysql://{os.getenv("dbuser")}:{os.getenv("dbpassword")}@{os.getenv("dbhost")}:{os.getenv("dbport")}/{os.getenv("dbname")}'

engine = create_engine(
    db_url,
    connect_args={"client_flag" : CLIENT.MULTI_STATEMENTS}
    )

session = sessionmaker(bind=engine)

db = session()

#Fetching from database

# query = text("select * from user")

# user = db.execute(query).fetchall()

# print(user)


# Creating the table 

create_tables = text("""

Create table if not exists users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL                             
    );
                     
Create table if not exists courses(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    level VARCHAR(100) NOT NULL
    );
                     
Create table if not exists enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    courseId INT NOT NULL,
    FOREIGN KEY (userId) REFERENCES users(id),
    FOREIGN KEY (courseId) REFERENCES courses(id)
    );
""")

db.execute(create_tables)

print("Table Successfully created")

