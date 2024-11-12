from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
import asyncio

app = FastAPI()

# Allow CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FileData(BaseModel):
    username: str
    files: List[str]

data_storage = []
new_data_available = asyncio.Event()  # Event to indicate new data

@app.post("/receive-data/")
async def receive_data(data: FileData):
    data_storage.append(data)
    new_data_available.set()  # Indicate new data is available
    return {"status": "Data received successfully"}

@app.get("/display-data/")
async def display_data():
    return [{"username": entry.username, "files": entry.files} for entry in data_storage]


@app.get("/stream-data/")
async def stream_data():
    async def event_generator():
        while True:
            await new_data_available.wait()  # Wait for new data
            data = {"username": data_storage[-1].username, "files": data_storage[-1].files}  # Construct latest data as JSON
            yield f"data: {json.dumps(data)}\n\n"  
            new_data_available.clear()  # Reset the event for the next data

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)






# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from typing import List, Optional
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Allow CORS for local testing
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )



# class FileData(BaseModel):
#     username: str
#     files: List[str]

# # In-memory storage for received data
# data_storage = []

# @app.post("/receive-data/")
# async def receive_data(data: FileData):
#     print(f"Received data from {data.username}:")
#     # for file in data.files:
#     #     print(f"- {file}")
#     # Store the data in memory
#     data_storage.append(data)
#     return {"status": "Data received successfully"}



# @app.get("/display-data/")
# async def display_data(request: Request):
#     # Format the data for JSON response
#     data = [{"username": entry.username, "files": entry.files} for entry in data_storage]
#     # print(data)
#     return data


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)   


