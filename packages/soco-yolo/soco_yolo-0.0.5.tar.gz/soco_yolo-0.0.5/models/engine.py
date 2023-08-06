from models.bases import ObjectDetector
import os
import torch
import urllib
import numpy as np
from PIL import Image
from typing import List, Union
from models.utils.helpers import LRUCache, chunks
from models.config import EnvVar
from models.hubconf import custom
import requests
import io
import base64
from models.hubconf import custom


class Yolov5(ObjectDetector):
	root_dir = os.path.dirname(os.path.abspath(__file__))
	MAX_CACHE = 20

	def __init__(self):
		self._models = LRUCache(self.MAX_CACHE)
		self.batch_size = EnvVar.BATCH_SIZE

	def _load_model(self, model_id):
		if model_id is None:
			raise Exception("Model ID cannot be None.")

		if not self._models.has(model_id):
			# model = torch.hub.load(self.root_dir, model_id, source='local', pretrained=True)
			model = custom(model_id)
			model = model.to(EnvVar.DEVICE)
			model.eval()
			self._models.put(model_id, model)

		return self._models.get(model_id)

	def predict(self, model_id, data: List,
				src_type: str = 'local',
				threshold: float = 0.5,
				include_classes: Union[List, None] = None):
		if src_type == 'local':
			image_data = [Image.open(x).convert('RGB') for x in data]

		elif src_type == 'url':
			image_data = []
			for x in data:
				# temp = Image.open(io.BytesIO(requests.get(x).content))
				# temp = Image.open(requests.get(x, stream=True).raw).convert('RGB')
				temp = Image.open(urllib.request.urlopen(x)).convert('RGB')
				image_data.append(temp)

		elif src_type == 'base64':
			image_data = []
			for x in data:
				temp = Image.open(io.BytesIO(base64.b64decode(x)))
				image_data.append(temp)
		else:
			raise Exception("Unknown mode {}.".format(src_type))

		if include_classes is not None:
			include_classes = set(include_classes)
		
		model = self._load_model(model_id)

		resp = []
		for batch in chunks(image_data, self.batch_size):
			with torch.no_grad():
				y = model(batch)

			for z in y.tolist():
				temp = []
				for pred in z.pred:
					x, y, xx, yy, conf, cls = pred
					cls = z.files[int(cls)]
					conf = float(conf)
					if conf > threshold:
						if include_classes is None or cls in include_classes:
							temp.append({'xmin': float(x),
										 'ymin': float(y),
										 'xmax': float(xx),
										 'ymax': float(yy),
										 'conf': conf,
										 'label': cls})

				resp.append(temp)

		return resp

	def destroy_model(self):
		self._models = LRUCache(self.MAX_CACHE)

