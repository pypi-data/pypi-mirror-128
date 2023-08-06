# Trains and Updates Ultralytics HUB Models

from .auth import Auth
from .config import BY_PASS_LOGIN
from .trainer import Trainer
from .yolov5_wrapper import clone_yolo

AUTH = Auth()


def train_model() -> None:
    """Starts training from next in queue"""
    clone_yolo()
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
    clone_yolo()
    if BY_PASS_LOGIN:
        AUTH.sign_in_with_email_and_password("kalen.michael@ultralytics.com", "7654321")
        if AUTH.idToken:
            train_model()
        else:
            print("Incorrect Login Details.")
    elif connect_to_hub():
        train_model()
