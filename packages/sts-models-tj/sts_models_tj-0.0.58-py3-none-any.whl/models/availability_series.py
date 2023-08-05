from . import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship


class AvailabilitySeries(Base):
    """Availability Series Model for connecting availabilities made as a repeating series"""
    __tablename__ = "availability_series"

    id = Column(Integer, primary_key=True, autoincrement=True)
    availabilities = relationship("Availability", cascade="all, delete, delete-orphan")
    tutor = Column(String(255), ForeignKey('users.cognitoId'), nullable=False)

    def __init__(self, tutor):
        self.tutor = tutor
