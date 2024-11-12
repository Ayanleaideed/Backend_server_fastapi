from fastapi import FastAPI, Request, Response, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
import json
import asyncio
import os

app = FastAPI()

# Define a constant for the API token 
API_TOKEN = "TestTokenDemo_123"

# Allow CORS only for specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Define the data model for the API
class FileData(BaseModel):
    username: str
    files: List[str]

# temporary storage for the data
data_storage = []
 # Event to indicate new data
new_data_available = asyncio.Event() 


# Dependency to check for a valid API token
def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

# Receive data from the frontend
@app.post("/receive-data/")
async def receive_data(data: FileData, token: str = Depends(verify_token)):
    print(new_data_available)
    print("storage", data_storage)
    data_storage.append(data)
    new_data_available.set()  # Indicate new data is available
    return {"status": "Data received successfully"}

# Display data from the backend
@app.get("/display-data/")
async def display_data(token: str = Depends(verify_token)):
    return [{"username": entry.username, "files": entry.files} for entry in data_storage]

# Stream data from the backend
@app.get("/stream-data/")
async def stream_data(token: str = Depends(verify_token)):
    async def event_generator():
        while True:
            await new_data_available.wait()  # Wait for new data
            data = {"username": data_storage[-1].username, "files": data_storage[-1].files}  
            yield f"data: {json.dumps(data)}\n\n"  
            new_data_available.clear()  # Reset the event for the next data

    return StreamingResponse(event_generator(), media_type="text/event-stream")



# Download data from the backend
@app.get("/download-data/")
def download_data(token: str = Depends(verify_token)):
    file_path = "Script.py"
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path, 
            filename="Script.py", 
            media_type='application/octet-stream'
        )
    return Response(content="File not found.", status_code=404)


# Delete endpoint to clear data storage
@app.delete("/delete-data/")
async def delete_data():
    if not data_storage:
        raise HTTPException(status_code=404, detail="No data to delete")
    data_storage.clear()
    return {"status": "All data deleted successfully"}


# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
