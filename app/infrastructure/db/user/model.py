"""
User MongoDB model using Pydantic.
Similar to SQL User model but for MongoDB.
"""

from pydantic import Field

from app.common.enums.user import UserRole
from app.infrastructure.db.base.base_model import BaseMongoModel


class User(BaseMongoModel):
    """
    User MongoDB document model.
    Represents documents in the 'users' collection.
    """

    email: str | None = Field(None, index=True)
    phone: str | None = Field(None, index=True)
    password_hash: str
    role: UserRole = Field(default=UserRole.STUDENT)
    is_active: bool = Field(default=True)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role.value})>"
