from fastapi import APIRouter
from starlette.requests import Request
from models.http.schemas.payload import QueryBody
from models.http.schemas.response import DetectionRes
from models.engine import Yolov5
import time

router = APIRouter()


@router.post("/detect", response_model=DetectionRes, name="Detect objects")
async def detect_urls(
        request: Request,
        body: QueryBody = None
) -> DetectionRes:
    s_time = time.time()
    detector: Yolov5 = request.app.state.detector
    out = detector.predict(body.model_id, body.data,
                           src_type=body.src_type,
                           threshold=body.threshold,
                           include_classes=body.include_classes)

    resp = DetectionRes(took=(time.time()-s_time)*1000, objects=out)
    return resp

