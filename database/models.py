# database/models.py
from sqlalchemy import Column, Integer, String, Text, Index
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """全モデルの基底クラス"""
    pass


class Employee(Base):
    """社員テーブルモデル"""
    __tablename__ = "employees"

    employee_id = Column(String, primary_key=True)
    name        = Column(String, nullable=False)
    name_kana   = Column(String, nullable=False)
    department  = Column(String, nullable=False)
    position    = Column(String, nullable=False)
    hire_date   = Column(String, nullable=False)
    salary      = Column(Integer, nullable=False)
    email       = Column(String, nullable=False, unique=True)
    phone       = Column(String)
    postal_code = Column(String)
    address     = Column(Text)
    notes       = Column(Text)
    created_at  = Column(String, nullable=False, server_default=func.current_timestamp())
    updated_at  = Column(String, nullable=False, server_default=func.current_timestamp())

    __table_args__ = (
        Index("idx_employees_name", "name"),
        Index("idx_employees_department", "department"),
        Index("idx_employees_hire_date", "hire_date"),
    )
