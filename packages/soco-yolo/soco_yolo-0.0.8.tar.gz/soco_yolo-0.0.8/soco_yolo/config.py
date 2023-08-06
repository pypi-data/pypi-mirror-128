import os
import yaml
import json

class EnvVar(object):
	APP_VERSION = "1.0"
	APP_NAME = "Yolov5"
	root_dir = os.path.dirname(os.path.realpath(__file__)).replace('soco_yolo', '')

	#default = yaml.load(open(os.path.join(root_dir, 'configs/default.yaml'), 'r'), Loader=yaml.FullLoader)

	#API_PREFIX = os.environ.get('API_PREFIX', default['API_PREFIX'])
	API_PREFIX = "/yolo"
	#IS_DEBUG = bool(os.environ.get('IS_DEBUG', default['IS_DEBUG']))
	IS_DEBUG = False
	#MODEL_DIR = os.environ.get("MODEL_DIR", default['MODEL_DIR'])
	MODEL_DIR = "./"
	#DEVICE = os.environ.get("DEVICE", default['DEVICE'])
	DEVICE = "cuda"
	#BATCH_SIZE = int(os.environ.get("BATCH_SIZE", default['BATCH_SIZE']))
	BATCH_SIZE = 160


	@classmethod
	def deepcopy(cls, x):
		return json.loads(json.dumps(x))




