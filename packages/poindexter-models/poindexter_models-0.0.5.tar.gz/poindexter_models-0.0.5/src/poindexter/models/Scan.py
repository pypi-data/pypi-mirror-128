from typing import List
from pydantic import BaseModel 


class ScanCreate(BaseModel):
  job_id: int
  links: List[str]
  plugins: List[str]
