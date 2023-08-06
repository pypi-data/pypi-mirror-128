import os
from unimatrix.ext import jose


os.environ.setdefault('SECRET_KEY', "my secret key")


data = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    "eyJzdWIiOiJhbGljZUBhY21lLmluYyJ9."
    "dcOMuAtjlUkfbwE5nB3VjohA9xWnZoqy8zSpLWzkYdE"
)


jwt = jose.payload.sync(data)
print(jwt['sub'])
