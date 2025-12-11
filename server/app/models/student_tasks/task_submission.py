"""
    Date written: 12/10/2025 at 8:49 PM
"""

import uuid
from sqlalchemy import Column, ForeignKey, String
from app.db.base import Base
from sqlalchemy.orm import relationship

class TaskSubmission(Base): 
    __tablename__ = "task_submission"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # foreign keys
    task_id = Column(String(36), ForeignKey("task.id"), unique=True, nullable=False)
    student_id = Column(String(36), ForeignKey("student.id"), unique=True, nullable=True)
    professor_id = Column(String(36), ForeignKey("professor.id"), nullable=True)
    
    
    # many-to-one relationship with Task
    task = relationship(
        "Task",
        back_populates="task_submissions",
        uselist=False
        
    )    
    
    
    # many-to-one relationship with Student
    student = relationship(
        "Student",
        back_populates="task_submissions",
        uselist=False
        
    )
    
    
    # many-to-one relationship with Task
    professor = relationship(
        "Professor",
        back_populates="task_submissions",
        uselist=False
    )