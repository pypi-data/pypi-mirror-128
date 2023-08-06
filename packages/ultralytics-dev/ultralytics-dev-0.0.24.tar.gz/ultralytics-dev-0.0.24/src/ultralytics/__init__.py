__version__ = '0.0.24'  # print(ultralytics.__version__)


def login():
    # Login to Ultralytics HUB
    from .main import connect_to_hub
    connect_to_hub(verbose=True)


def start():
    # Start training models with Ultralytics HUB
    from .main import train_model
    train_model()
