"""
    Date written: 12/10/2025 at 8:49 PM
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


"""
    Association table
        professor -> professor_class_section -> enrollment -> student
"""
class ProfessorClassSection(Base):
    __tablename__ = "professor_class_section"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # foreign keys
    professor_id = Column(String(36), ForeignKey("professor.id"), nullable=False)
    class_section_id = Column(String(36), ForeignKey("class_section.id"), nullable=False)
    
    professor = relationship(
        "Professor", 
        back_populates="class_section_links"
    )
    
    
    class_section = relationship(
        "ClassSection", 
        back_populates="professor_links"
    )

    # the same professor cannot be assigned to the same class section
    __table_args__ = (
        UniqueConstraint(
            "professor_id",
            "class_section_id",
            name="uq_professor_class_section_professor_section"
        ),
    )
