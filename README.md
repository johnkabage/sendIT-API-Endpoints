![license](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Build Status](https://travis-ci.org/johnz99/sendIT-API-Endpoints.svg?branch=challenge-2-develop)](https://travis-ci.org/johnz99/sendIT-API-Endpoints)
[![Coverage Status](https://coveralls.io/repos/github/johnz99/sendIT-API-Endpoints/badge.svg?branch=challenge-2-develop)](https://coveralls.io/github/johnz99/sendIT-API-Endpoints?branch=challenge-2-develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2b1910842a1a4b4886fd198b4192c538)](https://www.codacy.com/app/johnz99/sendIT-API-Endpoints?utm_source=github.com&utm_medium=referral&utm_content=johnz99/sendIT-API-Endpoints&utm_campaign=Badge_Grade)

# sendIT-API-Endpoints

SendIT is a parcel delivery application

##HOW IT WORKS

- A user can sign up
- A user can log in
- A user can create a parcel delivery order
- A user can get a specific parcel order
- A user can get all parcel delivery orders
- A user can delete a specific parcel delivery order
- A user can cancel a parcel delivery order
- Admin can get all users
- Admin can get all parcels from a specifc user

## Prerequisite

- [Python3.6](https://www.python.org/downloads/release/python-365/)
- [Virtua Environment](https://virtualenv.pypa.io/en/stable/installation/)

# Installation and Setup

Clone the repository below

```
git clone git@github.com:johnz99/sendIT-API-Endpoints.git
```

### Create and activate a virtual environment

    virtualenv env --python=python3.6

    source env/bin/activate

### Install required Dependencies

    pip install -r requirements.txt

## Running the application

```bash
$ export FLASK_APP = run.py

$ export MODE = development

$ flask run
```

## Endpoints Available

| Method | Endpoint                 | Description                         |
| ------ | ------------------------ | ----------------------------------- |
| POST   | /api/v1/auth/signup      | sign up a user                      |
| POST   | /api/v1/auth/login       | login a user                        |
| POST   | /api/v1/parcels          | create a parcel                     |
| GET    | /api/v1/parcels          | get all parcels                     |
| GET    | /api/v1/parcels/1        | get a specific parcel               |
| DEL    | /api/v1/parcels/1        | delete a specific parcel            |
| PUT    | /api/v1/parcels/1/cancel | cancel a specific parcel            |
| GET    | /api/v1/users            | get all users                       |
| GET    | /api/v1/users/1/parcels  | get all parcels for a specific user |


### post a parcel delivery order

    {
    "sender":"kimww1",
    "_from":"qwert",
    "destination":"Nyeri",
    "weight":1,
    "parcel":"Combs",
    "recipient":"Alice"
    }


### Testing

    nosetests

    - Testing with coverage

    nosetests --with-coverage --cover-package=app

### Author

John Mburu
