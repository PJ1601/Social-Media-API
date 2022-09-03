# Social-Media-API
      
### Interactive Documentation: https://apicrud-1-pj.herokuapp.com/docs

# About

FastAPI is a mordern, fast web framework for building APIs
with Python 3.6+.

But if you're here than you probably already knew that!

This API is Social Media like, So you get all the features that you came
to excepet by reading the title.This API is a CRUD based as most of them are
you can Create User, Login, Create post, Update post, Delete one and Get post 
all of them or individual. Don't worry while creating user you're password is
safe the moment you enter and save it get hased so even if someone got it they 
won't use it because hasing is a one way trip there is no going back.if this may
become False in future than do let me know.

# Features

- HTTP request: This API uses HTTP GET, POST, PUT and DELETE request according to
                action you want to perform.(For info please cheak router / post)

- HTTP Exception: HTTP response status code according to request you'll recive 
                  response.Some response code are 200, 201,401, 403, 404 etc.
                  
- Pydantic: FastAPI uses pydantic for Data validation and settings management using 
            python type annotations.With pydantic's BaseModel we create reusable 
            base class of defining request and response model or schemas with predefine
            datatype so the possibilty of having error and bug becomes less.
            With BaseSettings we can easily configure environment variable.
            
- SQLALCHEMY: SQLAlchemy is the Python SQL toolkit and Object Relational Mapper
              that gives application developers the full power and flexibility
              of SQL.With SQLAlchemy using OOPs we can define database models.
              The FastAPISessionMaker class provides an esaily-customized SQL-
              Alcheny Session dependency.(For more info visit app/models.py).
 
- OAuth2: For authentication purposes i've utilized Oauth2 to take email id
          password as parameters. Once the user created the password is hashed
          so even if our database compromized nothing could be done with that
          information.FastAPI also provide Jose to generate JWT tokens. So, when
          you receive a token that you emitted, you can verify that you actually
          emitted it.That way, you can create a token with an expiration time. 
          And then when the user comes back the next day with the
          token, you know that user is still logged in to your system.

- Alembic: Alembic is a database migrations tool that works with SQLalchemy
           .Alembic allows you to change your models and revert back to a specific
           one without any data loss.
           
- PostgreSQL: Postgres is used as our development and Production database as well.

# Requirements

   This package is intended for use with any recent version of FastAPI (depending on 
   pydantic),and python 3.6+ but I preferred using 3.9+ if possible(For more info on 
   this I strongly recomend check requirement.txt).
   

