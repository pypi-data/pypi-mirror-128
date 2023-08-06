from typing import List
from pydantic import BaseModel


class QueryBody(BaseModel):
    model_id: str
    data: List[str]
    src_type: str = "url"
    include_classes: List[str]=None
    threshold: float = 0.5



