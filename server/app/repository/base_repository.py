"""
    Date: 12/13/2025 at 7:30 PM
"""

from typing import Generic, TypeVar, Type, List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
        Async base repository with common CRUD operations.
    """
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db
    
    # ============================================
    # CREATE
    # ============================================
    async def create(self, **kwargs) -> ModelType:
        """Create a new record."""
        if "email" in kwargs:
            kwargs["email"] = kwargs["email"].lower().strip()
        
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    
    async def create_many(self, objects: List[Dict[str, Any]]) -> List[ModelType]:
        """Create multiple records."""
        instances = [self.model(**obj) for obj in objects]
        self.db.add_all(instances)
        await self.db.commit()
        for instance in instances:
            await self.db.refresh(instance)
        return instances
    
    
    # ============================================
    # READ
    # ============================================
    async def get_by_id(self, id: str) -> Optional[ModelType]:
        """Get single record by ID."""
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalars().first()
    
    
    async def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Get single record by any field."""
        result = await self.db.execute(
            select(self.model).where(getattr(self.model, field) == value)
        )
        return result.scalars().first()
    
    
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        desc: bool = False
    ) -> List[ModelType]:
        """Get all records with pagination."""
        query = select(self.model)
        
        if order_by:
            order_field = getattr(self.model, order_by)
            if desc:
                order_field = order_field.desc()
            query = query.order_by(order_field)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    
    async def filter_by(self, **filters) -> List[ModelType]:
        """Filter records by multiple fields."""
        query = select(self.model).filter_by(**filters)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    
    async def count(self, **filters) -> int:
        """Count records matching filters."""
        query = select(func.count()).select_from(self.model)
        if filters:
            for key, value in filters.items():
                query = query.where(getattr(self.model, key) == value)
        result = await self.db.execute(query)
        return result.scalar()
    
    
    async def exists(self, **filters) -> bool:
        """Check if record exists."""
        query = select(self.model).filter_by(**filters).limit(1)
        result = await self.db.execute(query)
        return result.scalars().first() is not None
    
    
    # ============================================
    # UPDATE
    # ============================================
    async def update(self, id: str, **kwargs) -> Optional[ModelType]:
        """Update record by ID."""
        instance = await self.get_by_id(id)
        if not instance:
            return None
        
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        await self.db.commit()
        await self.db.refresh(instance)
        return instance
    
    
    async def update_many(self, filters: Dict[str, Any], updates: Dict[str, Any]) -> int:
        """Update multiple records."""
        stmt = update(self.model).where(
            *[getattr(self.model, k) == v for k, v in filters.items()]
        ).values(**updates)
        
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount
    
    # ============================================
    # DELETE
    # ============================================
    async def delete(self, id: str) -> bool:
        """Delete record by ID."""
        instance = await self.get_by_id(id)
        if not instance:
            return False
        
        await self.db.delete(instance)
        await self.db.commit()
        return True
    
    
    async def delete_many(self, **filters) -> int:
        """Delete multiple records."""
        stmt = delete(self.model).where(
            *[getattr(self.model, k) == v for k, v in filters.items()]
        )
        
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount
    
    
    async def soft_delete(self, id: str) -> Optional[ModelType]:
        """Soft delete (set is_active=False)."""
        if not hasattr(self.model, 'is_active'):
            raise AttributeError(f"{self.model.__name__} doesn't have is_active field")
        
        return await self.update(id, is_active=False)
    