from pydantic import BaseModel, Field, GetJsonSchemaHandler, ConfigDict, field_serializer
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    """Custom Pydantic type for BSON ObjectId with JSON serialization"""
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.str_schema(),
            ]),
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        """Validate and convert to ObjectId"""
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId string")
            return ObjectId(v)
        raise ValueError(f"Invalid ObjectId type: {type(v)}")

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        return {"type": "string"}


class TaskBase(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Fazer compras",
                "description": "Comprar leite, pão e ovos",
                "completed": False
            }
        }
    )
    
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Fazer compras",
                "completed": True
            }
        }
    )
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class Task(TaskBase):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_serializer('id')
    def serialize_id(self, value: PyObjectId) -> str:
        return str(value)
