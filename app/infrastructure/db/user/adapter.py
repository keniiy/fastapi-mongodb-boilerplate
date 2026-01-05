"""
Repository adapter - bridges infrastructure repository with domain interface.
Converts between MongoDB models and domain entities.
This is infrastructure concern - adapting infrastructure to domain.
"""

from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.common.enums.user import UserRole
from app.domain.user.entities.user import User as UserEntity
from app.domain.user.types.repository import IUserRepository
from app.infrastructure.db.user.model import User as UserModel
from app.infrastructure.db.user.repository import UserRepository as InfraUserRepository


class UserRepositoryAdapter(IUserRepository):
    """Adapter that implements IUserRepository using infrastructure repository"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self._repo = InfraUserRepository()

    def _model_to_entity(self, model: UserModel) -> UserEntity | None:
        """Convert MongoDB model to domain entity"""
        if not model:
            return None
        return UserEntity(
            id=model.id,
            email=model.email,
            phone=model.phone,
            role=UserRole(model.role.value) if model.role else UserRole.STUDENT,
            is_active=model.is_active,
            created_at=model.created_at or datetime.utcnow(),
            updated_at=model.updated_at,
        )

    def _entity_to_model(self, entity: UserEntity, password_hash: str = "") -> UserModel:
        """Convert domain entity to MongoDB model"""
        return UserModel(
            id=entity.id,
            email=entity.email,
            phone=entity.phone,
            password_hash=password_hash,
            role=entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, user: UserEntity, password_hash: str = "") -> UserEntity:
        """Create a new user"""
        model = self._entity_to_model(user, password_hash)
        created = await self._repo.create(self.db, model)
        return self._model_to_entity(created)

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """Get user by ID"""
        model = await self._repo.get_by_id(self.db, user_id)
        return self._model_to_entity(model)

    async def get_by_email(self, email: str) -> UserEntity | None:
        """Get user by email"""
        model = await self._repo.get_by_email(self.db, email)
        return self._model_to_entity(model)

    async def get_by_phone(self, phone: str) -> UserEntity | None:
        """Get user by phone"""
        model = await self._repo.get_by_phone(self.db, phone)
        return self._model_to_entity(model)

    async def get_by_email_with_password(self, email: str) -> tuple[UserEntity, str] | None:
        """Get user by email with password hash for authentication"""
        model = await self._repo.get_by_email(self.db, email)
        if not model:
            return None
        entity = self._model_to_entity(model)
        if not entity:
            return None
        return entity, model.password_hash

    async def get_by_phone_with_password(self, phone: str) -> tuple[UserEntity, str] | None:
        """Get user by phone with password hash for authentication"""
        model = await self._repo.get_by_phone(self.db, phone)
        if not model:
            return None
        entity = self._model_to_entity(model)
        if not entity:
            return None
        return entity, model.password_hash

    async def update(self, user: UserEntity) -> UserEntity:
        """Update user"""
        # Get existing model
        model = await self._repo.get_by_id(self.db, user.id)
        if not model:
            raise ValueError("User not found")

        # Update fields
        update_data = {
            "email": user.email,
            "phone": user.phone,
            "role": user.role.value,
            "is_active": user.is_active,
            "updated_at": user.updated_at or datetime.utcnow(),
        }

        updated = await self._repo.update(self.db, user.id, update_data)
        if not updated:
            raise ValueError("Failed to update user")
        return self._model_to_entity(updated)

    async def update_password(self, user_id: str, password_hash: str) -> bool:
        """Update user password"""
        updated = await self._repo.update(self.db, user_id, {"password_hash": password_hash})
        return updated is not None

    async def deactivate(self, user: UserEntity) -> UserEntity:
        """Deactivate user"""
        updated = await self._repo.deactivate(self.db, user.id)
        if not updated:
            raise ValueError("User not found")
        return self._model_to_entity(updated)
