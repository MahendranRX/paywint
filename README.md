Steps to run this project

1. Create virutal environment and activate.

2. run in terminal 'pip install requirements.txt'.

3. Create the Postgresql database in loacal system

4. create .env file and inside create Postgresql database connection string
   ex: DATABASE_URL = postgresql://postgres:mahipost@localhost:5432/expense

5. run the project in terminal => uvicorn main:app --host localhost --port 8000 --reload

6. finds api in swagger docs and try it.
