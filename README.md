# Book-Rest-API


## Call External API For Fetching Books data

```
Request Body
GET http://localhost:8000/api/external-books

List All the books fetched from database

Response:
{"data": [], "status": "success", "status_code": 200}


GET http://localhost:8000/api/external-books?name=:nameOfBook

Request Query params 
name: name of book

http://localhost:8000/api/external-books?name=A%20Game%20of%20Thrones

Response

{
    "data": [
        {
            "name": "A Game of Thrones", 
            "isbn": "978-0553103540", 
            "authors": ["George R. R. Martin"], 
            "number_of_pages": 694, 
            "publisher": "Bantam Books", 
            "country": "United States", 
            "released_date": "1996-08-01"
        }], 
    "status": "success", 
    "status_code": 200
}
```

## Add books 
```
Request Body

POST http://localhost:8000/api/v1/books

	{
        "name": "Java Advance part 5",
        "isbn": "123134390138",
        "authors":[{"name": "Rajan"}],
        "number_of_pages": 1234,
        "publisher":{"name": "Rajan Publishers"},
        "country": {"name": "UK"},
        "release_date": "2019-06-03"
    }

Response:
{
    "data": [
        {
            "book": {
                "id": 14,
                "name": "Java Advance part 5",
                "isbn": "123134390138",
                "authors": [
                    "Rajan"
                ],
                "number_of_pages": 1234,
                "publisher": "Rajan Publishers",
                "country": "UK",
                "release_date": "2019-06-03"
            }
        }
    ],
    "status": "success",
    "status_code": 201
}
```


## List Books
```
Request Body

GET http://localhost:8000/api/v1/books

Response:

{
    "data": [
        {
            "id": 14,
            "name": "Java Advance part 5",
            "isbn": "123134390138",
            "authors": [
                "Rajan"
            ],
            "number_of_pages": 1234,
            "publisher": "Rajan Publishers",
            "country": "UK",
            "release_date": "2019-06-03"
        }
    ],
    "status": "success",
    "status_code": 200
}
```

## get Book by ID

```
Request Body

GET http://localhost:8000/api/v1/books/:id

Response:
GET http://localhost:8000/api/v1/books/16
{
    "data": {
        "id": 16,
        "name": "Data",
        "isbn": "12310000138",
        "authors": [
            "anjan"
        ],
        "number_of_pages": 1234,
        "publisher": "Rajan Publishers",
        "country": "UK",
        "release_date": "2019-06-03"
    },
    "status": "success",
    "status_code": 200
}
```