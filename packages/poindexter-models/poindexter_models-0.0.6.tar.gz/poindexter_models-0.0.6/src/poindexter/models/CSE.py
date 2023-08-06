from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from poindexter.models import Base
from poindexter.models.Domain import Domain


CSE_Domain_Table = Table(
  'cse_domain_association',
  Base.metadata,
  Column('cse_id', ForeignKey('cses.id')),
  Column('domain_id', ForeignKey('domains.id'))
)


class CSECreate(BaseModel):
  name: str
  cx: str
  description: str


class CSE(CSECreate):
  id: int
  domains: List[Domain] = []
  class Config:
    orm_mode = True


class CSEModel(Base):
  __tablename__ = 'cses'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  cx = Column(String)
  description = Column(String)
  domains = relationship("DomainModel", secondary=CSE_Domain_Table)
