from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.task_router import router as task_router
from .api.auth_router import router as auth_router
import uvicorn

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(task_router)
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Read PORT env variable
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
