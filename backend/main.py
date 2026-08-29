from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from bson import ObjectId
from datetime import datetime

from models import Task, TaskCreate, TaskUpdate
from database import tasks_collection, client

app = FastAPI(
    title="Task API",
    description="API para gerenciar tarefas com MongoDB",
    version="1.0.0"
)

# CORS - Permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite e React padrões
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "message": "Task API rodando",
        "status": "✅ OK",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Verificar saúde da API e conexão com MongoDB"""
    try:
        client.admin.command('ping')
        return {
            "status": "✅ API saudável",
            "database": "✅ MongoDB conectado"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )


# CRUD Operations
@app.post("/api/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task: TaskCreate):
    """Criar uma nova tarefa"""
    task_dict = task.model_dump()
    task_dict["created_at"] = datetime.utcnow()
    task_dict["updated_at"] = datetime.utcnow()
    
    result = tasks_collection.insert_one(task_dict)
    
    new_task = tasks_collection.find_one({"_id": result.inserted_id})
    return Task(**new_task)


@app.get("/api/tasks", response_model=List[Task], tags=["Tasks"])
async def list_tasks(skip: int = 0, limit: int = 100):
    """Listar todas as tarefas com paginação"""
    tasks = list(tasks_collection.find().skip(skip).limit(limit))
    return [Task(**task) for task in tasks]


@app.get("/api/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def get_task(task_id: str):
    """Obter uma tarefa pelo ID"""
    try:
        obj_id = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    task = tasks_collection.find_one({"_id": obj_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return Task(**task)


@app.patch("/api/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(task_id: str, task_update: TaskUpdate):
    """Atualizar uma tarefa (atualização parcial)"""
    try:
        obj_id = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    update_data = task_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    result = tasks_collection.find_one_and_update(
        {"_id": obj_id},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return Task(**result)


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_task(task_id: str):
    """Deletar uma tarefa"""
    try:
        obj_id = ObjectId(task_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    
    result = tasks_collection.delete_one({"_id": obj_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return None


@app.delete("/api/tasks", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
async def delete_all_tasks():
    """Deletar todas as tarefas (apenas para desenvolvimento)"""
    tasks_collection.delete_many({})
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
