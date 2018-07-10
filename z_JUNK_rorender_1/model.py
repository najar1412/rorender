"""
Contains source code rorender database models.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


base = declarative_base()

class Machine(Base):
    __tablename__ = 'machines'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ip = Column(String)

    def __repr__(self):
        return f"<Machine(name={self.name}, ip={self.ip})>"



