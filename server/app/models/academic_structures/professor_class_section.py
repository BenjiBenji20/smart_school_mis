"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String, Table
from app.db.base import Base


"""
    Association table
        professor -> professor_class_section -> enrollment -> student
"""
professor_class_section = Table( 
        "professor_class_section",
        Base.metadata,
        Column('id', String(36), primary_key=True, default=lambda: str(uuid.uuid4())),

        # foreign keys
        Column("professor_id", String(36), ForeignKey("professor.id"), primary_key=True),
        Column("class_section_id", String(36), ForeignKey("class_section.id"), primary_key=True)
    )
