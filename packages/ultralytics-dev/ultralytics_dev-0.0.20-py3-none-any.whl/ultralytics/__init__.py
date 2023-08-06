__version__ = '0.0.20'  # print(ultralytics.__version__)

from .yolov5_wrapper import clone_yolo

clone_yolo()


def login():
    # Login to Ultralytics HUB
    from .main import connect_to_hub
    connect_to_hub()


def start():
    # Start training models with Ultralytics HUB
    from .main import train_model
    train_model()
