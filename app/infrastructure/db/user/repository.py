"""
User repository for MongoDB.
Similar structure to SQL UserRepository.
"""

from typing import List, Optional, Tuple

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.common.utils.pagination import PaginatedResponse, PaginationParams
from app.infrastructure.db.base.base_repository import BaseRepository
from app.infrastructure.db.user.model import User


class UserRepository(BaseRepository[User]):
    """
    User repository with user-specific MongoDB operations.
    Extends BaseRepository with common CRUD + user-specific methods.
    """

    def __init__(self):
        super().__init__("users", User)

    async def get_by_email(self, db: AsyncIOMotorDatabase, email: str) -> Optional[User]:
        """Get user by email"""
        collection = self._get_collection(db)
        doc = await collection.find_one({"email": email})
        return self._dict_to_model(doc)

    async def get_by_phone(self, db: AsyncIOMotorDatabase, phone: str) -> Optional[User]:
        """Get user by phone"""
        collection = self._get_collection(db)
        doc = await collection.find_one({"phone": phone})
        return self._dict_to_model(doc)

    async def get_by_email_or_phone(
        self, db: AsyncIOMotorDatabase, email: str | None = None, phone: str | None = None
    ) -> Optional[User]:
        """Get user by email or phone"""
        if email:
            return await self.get_by_email(db, email)
        elif phone:
            return await self.get_by_phone(db, phone)
        return None

    async def deactivate(self, db: AsyncIOMotorDatabase, user_id: str) -> Optional[User]:
        """Soft delete user (set is_active to False)"""
        return await self.update(db, user_id, {"is_active": False})

    async def get_all_active(
        self, db: AsyncIOMotorDatabase, skip: int = 0, limit: Optional[int] = None
    ) -> List[User]:
        """Get all active users"""
        return await self.get_all(
            db, skip=skip, limit=limit or 100, filter_dict={"is_active": True}
        )

    async def get_all_active_paginated(
        self, db: AsyncIOMotorDatabase, pagination: PaginationParams
    ) -> PaginatedResponse[User]:
        """Get all active users with pagination"""
        return await self.get_all_paginated(db, pagination, filter_dict={"is_active": True})

    async def get_all_active_with_count(
        self, db: AsyncIOMotorDatabase, skip: int = 0, limit: Optional[int] = None
    ) -> Tuple[List[User], int]:
        """
        Get all active users with total count.
        Useful when you need both data and count in one call.
        """
        total = await self.count(db, {"is_active": True})
        items = await self.get_all_active(db, skip=skip, limit=limit)
        return items, total

    async def get_by_role(
        self, db: AsyncIOMotorDatabase, role: str, skip: int = 0, limit: Optional[int] = None
    ) -> List[User]:
        """Get users by role"""
        filter_dict = {"role": role, "is_active": True}
        return await self.get_all(db, skip=skip, limit=limit or 100, filter_dict=filter_dict)

    async def get_by_role_paginated(
        self, db: AsyncIOMotorDatabase, role: str, pagination: PaginationParams
    ) -> PaginatedResponse[User]:
        """Get users by role with pagination"""
        filter_dict = {"role": role, "is_active": True}
        return await self.get_all_paginated(db, pagination, filter_dict=filter_dict)

    async def get_by_role_with_count(
        self, db: AsyncIOMotorDatabase, role: str, skip: int = 0, limit: Optional[int] = None
    ) -> Tuple[List[User], int]:
        """Get users by role with total count"""
        filter_dict = {"role": role, "is_active": True}
        total = await self.count(db, filter_dict)
        items = await self.get_by_role(db, role, skip=skip, limit=limit)
        return items, total
