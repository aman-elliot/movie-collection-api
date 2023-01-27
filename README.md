
# *Movie Collection APP*

This is a Django web application which enables users to keep a record of the movies they like by providing them the accessibility to create, retrieve, update and delete collections of movies.






## Technologies

- **Django Web Framework** - Django is a back-end server side web framework. Django is free, open source and written in Python.
- **Django Rest Framework** - Django Rest Framework is a powerful and flexible toolkit for building Web APIs



## Overview

*Movie-Collection* App integrates with a third-party movie API to serve a paginated list of movies and their respective genres.

Using the REST APIs of the App, users can view the movie details and add them to their collections.
It also allows users to create multiple collection of movies while keeping a track of top 3 genres present across the collections owned by each user.

All the user, movie and collection details are stored in sqlite3 database intrinsic to Django. 

Users can also retrieve, update or delete a collection as per their requirement.

*Movie-Collection* also inherently keeps a count of number of requests served by the server using middleware. APIs are built to return the number of requests and also to reset the counter.














## API Reference



|   API  | Parameter     | Description                |
| :-------- | :------- | :------------------------- |
| `POST http://localhost:8000/register/` | `username, password` | **Required** for registration |
| `GET http://localhost:8000/movies/` | `-` | Return paginated list of movies from 3rd party API |
| `GET http://localhost:8000/collection/` | `-` | Return all collections of user |
| `POST http://localhost:8000/collection/` | `-` | Creates a collection of movies |
| `PUT http://localhost:8000/collection/<collection_uuid>/` | `collection_uuid` |Update the particular collection |
| `GET http://localhost:8000/collection/<collection_uuid>/` | `collection_uuid` |Returns data of the particular collection |
| `DELETE http://localhost:8000/collection/<collection_uuid>/` | `collection_uuid` | Deletes the particular collection|
| `GET http://localhost:8000/request-count/` | `-` |Returns the counter number of request served|
| `POST http://localhost:8000/request-count/reset/` | `-` |Resets the request counter |



## Installation and Usage

1. Clone the project.
    ```
    git clone https://github.com/eknathyadav/met-office-climate.git
    ```

2. Run virtual environment in the root folder
    ```
    python -m venv vevn
    venv\Scripts\activate
    ```

3. Install required packages using requirement.txt in the movieCollection folder.

    ```
    pip install -r requirement.txt
    ```


4. Run the Django Server
    ```
    python manage.py runserver
    ```

5. Use **POST http://localhost:8000/register/** to register with a username and password.

6. After registering, you will receive an **access token**. Use the token for authorization in the following requests that you will be making.



7. Refer to the **API Reference table** above to use the API endpoints as per your requirement. 




## Get list of movies
![mpvie_movies](https://user-images.githubusercontent.com/55498772/215168400-20c9ab7c-e814-4a3a-a215-7ca400825882.JPG)

## Create Collection
![movie_createcollection](https://user-images.githubusercontent.com/55498772/215169892-eab58c74-2957-4c5b-b0a1-2bc7741d1ea1.JPG)

## Get Collections
![movie_getcollections](https://user-images.githubusercontent.com/55498772/215176814-9d34e4b5-97fe-4abc-852f-6ef606a2fb2c.JPG)

## Update particular Collection
![movie_update](https://user-images.githubusercontent.com/55498772/215177801-db69b3ac-48a2-4fe0-b789-5a490b116905.JPG)

## Get particular Collection

![movie_getafterupdate](https://user-images.githubusercontent.com/55498772/215177976-978e948a-4f9b-4648-99d8-2ae2596776a2.JPG)

## Delete particular Collection
![movie_delete](https://user-images.githubusercontent.com/55498772/215178203-e2a5bab4-5496-43f2-9896-78ed7961a3e4.JPG)


## Get Request Count
![movie_count](https://user-images.githubusercontent.com/55498772/215178591-ee7e8d08-5674-4729-b807-ae97c58e49da.JPG)

## Reset Request Count

![movie_reset](https://user-images.githubusercontent.com/55498772/215178808-e53afd63-f4ee-4d9c-b1e7-a12de4151dc0.JPG)
