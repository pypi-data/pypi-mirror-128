# Trains and Updates Ultralytics HUB Models

from . import AUTH
from .config import BY_PASS_LOGIN
from .trainer import Trainer
from .yolov5_wrapper import verify_install


def setup_yolo() -> None:
    """Checks if yolov5 exists and if not clones it"""
    verify_install()


def train_model() -> None:
    """Starts training from next in queue"""
    trainer = Trainer(None, AUTH)  # No model so next in train queue is fetched
    if trainer.model is not None:
        trainer.start()


def connect_to_hub(password=False) -> bool:
    """Authenticates user with Ultralytics HUB"""

    if password:
        success = AUTH.attempt_signin()
    else:
        success = AUTH.attempt_api_key()

    return success


def main():
    setup_yolo()
    if BY_PASS_LOGIN:
        AUTH.sign_in_with_email_and_password("kalen.michael@ultralytics.com", "7654321")
        if AUTH.idToken:
            train_model()
        else:
            print("Incorrect Login Details.")
    elif connect_to_hub():
        train_model()


main()
