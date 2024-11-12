Here’s a structured README file for your `backend_server_fastapi` project:

---

# Backend Server FastAPI

This project is a FastAPI-based backend server deployed on Vercel, providing API endpoints for managing user-uploaded files. It includes basic authentication and CORS configuration to restrict access to authorized clients only.

## Live Links

- **Live Backend API Server**: [https://backend-server-fastapi.vercel.app/docs](https://backend-server-fastapi.vercel.app/docs)
- **Live Client Side/Frontend**: [https://backend-server-fastapi-frontend.vercel.app/](https://backend-server-fastapi-frontend.vercel.app/)

## Features

- **File Upload and Management**: Allows users to send file data from specified directories.
- **Token-Based Authentication**: Protects certain endpoints to ensure only authorized requests can access them.
- **CORS Configuration**: Limits access to specific origins to secure cross-origin requests.
- **Automatic Directory Scanning**: Automatically fetches files from specified directories on a user’s system (Desktop, Downloads, Documents, and OneDrive).

## Project Structure

```plaintext
backend_server_fastapi/
├── api/
│   └── server.py            # FastAPI application and API routes
├── requirements.txt       # Python dependencies
├── Script.py             # Script to send the user file system to the api route
└── vercel.json            # Vercel configuration for deployment
```

## Endpoints

### POST `/receive-data`
- **Description**: Receives file data from a client and stores it temporarily.
- **Request Headers**:
  - `Authorization`: `Bearer <token>`
- **Request Body**:
  ```json
  {
    "username": "user_name",
    "files": ["file1.txt", "file2.doc", ...]
  }
  ```

### GET `/display-data`
- **Description**: Returns all stored file data.
- **Authorization**: Requires a valid bearer token.

### DELETE `/delete-data`
- **Description**: Deletes all stored file data.
- **Authorization**: Requires a valid bearer token.

### GET `/download-data`
- **Description**: Allows authorized users to download a specific file from the server.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd backend_server_fastapi
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server Locally

```bash
uvicorn api.main:app --reload
```

The server should now be accessible at `http://127.0.0.1:8000`.

### 4. Deploy to Vercel

- Ensure `vercel.json` is configured to use the FastAPI server in `api/main.py`.
- Deploy via Vercel CLI or web interface.

## Usage

### 1. Sending Data

Use the provided Python script to gather files from specified directories and send them to the backend.

### 2. Downloading Files

To download a file, visit the frontend and click the download button, which will initiate a request with the required authorization token.

## Dependencies

- **FastAPI**: The main framework used for building the backend API.
- **Uvicorn**: ASGI server for running the FastAPI application.
- **Requests**: Python library for sending HTTP requests (used in client scripts).

## License

This project is licensed under the MIT License.

---

This README covers the core features, setup, usage, and deployment of your FastAPI backend project. Let me know if you’d like any additional details added!
