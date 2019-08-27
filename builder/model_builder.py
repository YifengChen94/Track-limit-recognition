import sys, os
import tensorflow as tf
import subprocess

sys.path.append("models")

#from models.ICNet import build_icnet
from model.BiSeNet import build_bisenet

SUPPORTED_MODELS = ["FC-DenseNet56", "FC-DenseNet67", "FC-DenseNet103", "Encoder-Decoder", "Encoder-Decoder-Skip", "RefineNet",
    "FRRN-A", "FRRN-B", "MobileUNet", "MobileUNet-Skip", "PSPNet", "GCN", "DeepLabV3", "DeepLabV3_plus", "AdapNet", 
    "DenseASPP", "DDSC", "BiSeNet", "custom","ICNet"]

SUPPORTED_FRONTENDS = ["ResNet50", "ResNet101", "ResNet152", "MobileNetV2", "InceptionV4"]

def download_checkpoints(model_name):
    subprocess.check_output(["python", "utils/get_pretrained_checkpoints.py", "--model=" + model_name])



def build_model(model_name, net_input, num_classes, crop_width, crop_height, frontend="ResNet101", is_training=True):
	# Get the selected model.
	# Some of them require pre-trained ResNet

	print("Preparing the model ...")



	network = None
	init_fn = None

	if model_name == "BiSeNet":
		# BiSeNet requires pre-trained ResNet weights
		network, init_fn = build_bisenet(net_input, preset_model = model_name, frontend=frontend, num_classes=num_classes, is_training=is_training)

	else:
		raise ValueError("Error: the model %d is not available. Try checking which models are available using the command python main.py --help")

	return network, init_fn