from typing import List

from pydantic import BaseModel 
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from poindexter.models import Base
from poindexter.models.Tag import Tag


Link_Tag_Table = Table(
  'link_tag_association',
  Base.metadata,
  Column('link_id', ForeignKey('links.id')),
  Column('tag_id', ForeignKey('tags.id'))
)


class LinkCreate(BaseModel):
  value: str
  screenshot: str


class Link(LinkCreate):
  id: int
  tags: List[Tag]
  class Config:
    orm_mode = True


class LinkModel(Base):
  __tablename__ = 'links'
  id = Column(Integer, primary_key=True, index=True)
  value = Column(String)
  screenshot = Column(String)
  tags = relationship("TagModel", secondary=Link_Tag_Table)
