import importlib, os  # To import YOLOv5 as module
import subprocess
import io, sys

from .config import REPO_URL, REPO_BRANCH, ENVIRONMENT


def installDependencies():
    print('Installing YOLOv5 Requirements...', end=" ")
    if ENVIRONMENT == 'development':
        subprocess.call(['pip', 'install', '-r', 'yolov5/requirements.txt'])
    else:
        subprocess.call(['pip', 'install', '-r', 'yolov5/requirements.txt'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
    print('Done')


def verifyInstall():
    """
    Check that YOLOv5 is on the system and clone if not found
    """
    if not os.path.isdir("./yolov5"):
        from git import Repo, head
        try:
            print(f"Cloning YOLOv5 Repo from {REPO_URL}...", end=" ")
            Repo.clone_from(REPO_URL, "yolov5", branch=REPO_BRANCH
                            )  #Temp solution while waiting on pull request
            print("Done")
            installDependencies()

        except Exception as e:
            print("Failed")
            print('Error: ' + str(e))


verifyInstall()


class YOLOv5Wrapper:
    def export(**kwargs):
        """Calls the YOLOv5 export module"""
        _export = importlib.import_module("yolov5.export")
        _export.run(**kwargs)

    def detect(**kwargs):
        """Calls the YOLOv5 detect module"""
        _detect = importlib.import_module("yolov5.detect")
        _detect.run(**kwargs)

    def train(callback_handler, **kwargs):
        """Calls the YOLOv5 train module"""
        _train = importlib.import_module("yolov5.train")
        opt = _train.parse_opt(True)
        for k, v in kwargs.items():
            setattr(opt, k, v)

        # _train.run(**kwargs)
        # text_trap = io.StringIO()
        # sys.stdout = text_trap # Trap output
        _train.main(opt, callback_handler)
        # sys.stdout = sys.__stdout__ # Restore output

    def newCallbackHandler():
        """Returns a YOLOv5 callback handler"""
        _callback_handler = importlib.import_module("yolov5.utils.callbacks")
        return _callback_handler.Callbacks()
