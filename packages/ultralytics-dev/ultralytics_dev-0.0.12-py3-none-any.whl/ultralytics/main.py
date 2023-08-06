# Trains and Updates Ultralytics HUB Models

from .auth import Auth
from .config import BY_PASS_LOGIN
from .trainer import Trainer
from .yolov5_wrapper import verifyInstall

auth = Auth()


def setupYOLO() -> None:
    """Checks if yolov5 exists and if not clones it"""
    verifyInstall()


def trainModel() -> None:
    """Starts training from next in queue"""
    trainer = Trainer(None, auth)  # No model so next in train queue is fetched
    trainer.start()


def connectToHUB(password=False) -> bool:
    """Authenticates user with Ultralytics HUB"""

    if password:
        success = auth.attempt_signin()
    else:
        success = auth.attempt_api_key()

    return success


def main():
    setupYOLO()
    if BY_PASS_LOGIN:
        auth.sign_in_with_email_and_password("kalen.michael@ultralytics.com",
                                             "7654321")
        if auth.idToken:
            trainModel()
        else:
            print("Incorrect Login Details.")
    elif connectToHUB():
        trainModel()


main()
