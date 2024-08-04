# FastAPI-JWT-StarterKit

## Overview

**FastAPI-JWT-StarterKit** is a boilerplate codebase designed to help developers quickly set up a new FastAPI project. It includes essential functionalities such as user management and JWT-based authentication. The kit provides a solid foundation, allowing you to focus on building the core features of your application without having to write common setup code from scratch.

## Features

- **User Management**:
  - User registration and login.
  - Secure password hashing using bcrypt.
- **JWT Authentication**:
  - Issuing and verifying JWT tokens for secure user authentication.
  - Token-based authentication for protected endpoints.
- **Modular Project Structure**:
  - Organized codebase with separate modules for API endpoints, database models, schemas, and services.
- **Environment Variable Management**:
  - Easy configuration using `.env`.


## Endpoints

### Users

#### Get All Users


- **Summary**: Read Users
- **Responses**:
  - `200`: Successful Response

#### Create User


- **Summary**: Create User
- **Request Body**:
  - `application/json`:
    - `UserCreate` schema
- **Responses**:
  - `201`: Successful Response
  - `422`: Validation Error

#### Update User


- **Summary**: Update User
- **Parameters**:
  - `user_id` (path): integer
- **Request Body**:
  - `application/json`:
    - `User` schema
- **Responses**:
  - `200`: Successful Response
  - `422`: Validation Error

#### Delete User


- **Summary**: Delete User
- **Parameters**:
  - `user_id` (path): integer
- **Responses**:
  - `200`: Successful Response
  - `422`: Validation Error

#### Get Current User Details


- **Summary**: Get Current User Details
- **Responses**:
  - `200`: Successful Response

### Auth

#### Login


- **Summary**: Login
- **Request Body**:
  - `application/x-www-form-urlencoded`:
    - `Body_login_auth_token_post` schema
- **Responses**:
  - `200`: Successful Response
  - `422`: Validation Error

## How to Use

1. **Clone the repository**:
```bash 
git clone https://github.com/yourusername/fastapi-jwt-starterkit.git
cd fastapi-jwt-starterkit
```


2. **Create Virtual Environment**:
```properties
python -m venv .venv
```

3. **Activate Virtual Environment**:

    On Unix or MacOS:
        ```
        source .venv/bin/activate
        ```
    <br>On Windows: ```.venv/scripts/activate```


4. **Install required packages**:
```properties
pip install -r requirements.txt
```

6. **Generate Keys**:
```properties
- openssl genpkey -algorithm RSA -out keys/private_key.pem -pkeyopt rsa_keygen_bits:2048
- openssl rsa -pubout -in keys/private_key.pem -out keys/public_key.pem
```


6. **Run the application**:
```properties
fastapi dev main.py
```

7. **Test the API**:
```properties
Swagger Documentation http://127.0.0.1:8000/docs
```
```properties
Redoc Documentation http://127.0.0.1:8000/redoc
```

## Notes
- The current implementation uses SQLite for simplicity, but it can be easily changed to any other database supported by SQLAlchemy.
- Customize the User model and other configurations in app/models to suit your needs.

## License
This project is licensed under the MIT License.