from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Integer, Column, String, Text, DateTime


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=lambda: datetime.now(timezone.utc),
                                                 nullable=False)
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class PostModel(Base):
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
