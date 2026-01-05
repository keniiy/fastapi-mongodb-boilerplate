"""
Base Pydantic model for MongoDB documents.
Similar to SQL BaseModel but using Pydantic instead of SQLAlchemy.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseMongoModel(BaseModel):
    """
    Abstract base model with common fields.
    All MongoDB models should inherit from this.
    """

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )

    id: str | None = Field(None, alias="_id")
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
