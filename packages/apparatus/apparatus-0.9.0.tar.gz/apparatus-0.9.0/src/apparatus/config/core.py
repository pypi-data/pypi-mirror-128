from typing import Optional
from pydantic import BaseModel


class Repository(BaseModel):
    config: str


class Kubernetes(BaseModel):
    config: Optional[str] = None


class Config(BaseModel):
    repository: Optional[Repository] = None
    kubernetes: Optional[Kubernetes] = None
