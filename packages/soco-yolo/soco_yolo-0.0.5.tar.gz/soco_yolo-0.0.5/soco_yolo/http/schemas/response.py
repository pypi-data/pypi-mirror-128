from pydantic import BaseModel
from typing import List

class Object(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    conf: float
    label: str

class DetectionRes(BaseModel):
    took: int
    objects: List[List[Object]] = []

