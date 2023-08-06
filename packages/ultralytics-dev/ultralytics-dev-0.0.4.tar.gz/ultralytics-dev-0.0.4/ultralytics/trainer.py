from .hub_logger import HUBLogger
from .yolov5_wrapper import YOLOv5Wrapper as YOLOv5
import requests
import json
from .config import HUB_API_ROOT

import sys


class Trainer:
    def __init__(self, model_id, auth):
        self.auth = auth
        self.model = self._getModel(model_id)

        self._connectCallbacks()

    def _get_model_by_id():
        # return a specific model
        return

    def _get_next_model():
        # return next model in queue
        return

    def _getModel(self, model_id):
        """
        Returns model from database by id
        """
        api_url = HUB_API_ROOT + "/model"
        payload = {"modelId": model_id}
        payload.update(self.auth.get_auth_string())

        try:
            r = requests.post(api_url, json=payload)
            res = r.json()

            if res["data"] == None:
                print("\nERROR: Unable to fetch model")
                sys.exit()  # Cannot train without model
            elif not res["data"]:
                print("\nYou have no models pending training.")
                sys.exit()  # Cannot train without model
            else:
                self.model_id = res["data"][
                    "id"]  # Append id as it may be fetched from queue and unknown
                return res["data"]
        except requests.exceptions.ConnectionError:
            print(
                '\nERROR: The HUB server is not online. Please try again later.'
            )
            sys.exit(141)

    def _connectCallbacks(self):
        callback_handler = YOLOv5.newCallbackHandler()
        hub_logger = HUBLogger(self.model_id, self.auth)
        callback_handler.register_action("on_model_save", "HUB",
                                         hub_logger.on_model_save)
        callback_handler.register_action("on_train_end", "HUB",
                                         hub_logger.on_train_end)
        self.callbacks = callback_handler

    def start(self):
        # Force sandbox key
        self.model.update({"sandbox": self.model["project"]})
        YOLOv5.train(self.callbacks, **self.model)
