# voting-api
Voting API powered by FastAPI

You can find and play with API at https://vaniksarajyan.site

# To run locally
First clone this repo by using following command
````

git clone https://github.com/VanikSarajyan/voting-api.git

````
then 
````

cd voting-api

````

Then install dependencies

````

pip install -r requirements.txt

````

Make sure you have postgres database created and all necessary environmental variables set in .env file in your app/ directory
For database connection and jwt authentication [congif.py](https://github.com/VanikSarajyan/voting-api/blob/main/app/config.py)

To Migrate run 

````
alembic upgrade head
````


Then run the server by uvicorn
````

uvicorn main:app --reload

````

Then you can use following link to see the Swagger docs and use the  API

````

http://127.0.0.1:8000/docs 

````
