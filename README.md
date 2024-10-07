This project is a microservice for managing user registration, login, and user data. It uses FastAPI with SQLAlchemy for database interaction and PostgreSQL for data storage. The service is dockerized to make it easy to deploy and scale.

Features
- User Registration with password hashing
- User Login with JWT authentication
- Token-based authorization for CRUD operations on users
- Token Blacklisting for secure logout
- RESTful API built using FastAPI
- PostgreSQL database for storing user information
- Dockerized for easy deployment

Prerequisites
- Docker installed
- Docker Compose installed
- Python 3.12 (if running locally without Docker)
- PostgreSQL (if running locally without Docker)

Create a .env file in the root of the project to manage environment variables for both services. Here’s an example of the variables required:

API Endpoints
Authentication Endpoints:
- Register
POST /register
Register a new user.
Request body: RegisteredUserCreate (JSON)

- Login
POST /login
Authenticate a user and get an access token.
Request body: OAuth2PasswordRequestForm (Form)

- Logout
POST /logout
Log out a user by blacklisting their token.
Authorization: Bearer Token

User Management Endpoints:
- Get All Users
GET /getallusers
Retrieve all users (requires token).
Authorization: Bearer Token

- Get User by ID
GET /getbyid/{user_id}
Retrieve a user by ID.
Authorization: Bearer Token

- Add User
POST /adduser
Add a new user (requires token).
Authorization: Bearer Token

- Update User
PUT /updateuser/{user_id}
Update an existing user by ID (requires token).
Authorization: Bearer Token

- Delete User
DELETE /deleteuser/{user_id}
Delete a user by ID (requires token).
Authorization: Bearer Token

Running with Docker
1. Build and Run the Containers
To build and run the containers using Docker Compose, follow these steps:
```
docker-compose up --build
```
2. Verify the Service
Once the containers are up and running, the FastAPI service will be available at:
```
http://localhost:8000
```

Stopping the Service
To stop and remove the containers, use:
```
docker-compose down
```