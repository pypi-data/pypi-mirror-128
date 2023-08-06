import threading

import requests

from .config import HUB_API_ROOT
from .utils.general import colorstr

PREFIX = colorstr('Ultralytics HUB: ')


class HUBLogger:
    def __init__(self, model_id, auth):
        self.model_id = model_id
        self.auth = auth

    def on_model_save(self, *args, **kwargs):
        """
        Runs after each model save

        Args:
             *args     last, epoch, final_epoch, best_fitness, fi
        """

        print(f"{PREFIX}Submitting checkpoint for " + self.model_id)

        # Set args
        last, epoch, final_epoch, best_fitness, fi = (
            args[0],
            args[1],
            args[2],
            args[3],
            args[4],
        )

        is_best = (best_fitness == fi).all()

        thread = threading.Thread(
            target=self._upload_model,
            args=(epoch, is_best, last),
            daemon=True,
        ).start()

    def _upload_model(self, epoch, is_best, weights):
        api_url = HUB_API_ROOT + "model-checkpoint"
        payload = {
            "modelId": self.model_id,
            "epoch": epoch,
            "isBest": bool(is_best)
        }
        payload.update(self.auth.get_auth_string())
        files = {"last.pt": open(weights, "rb")}

        r = requests.post(api_url, data=payload, files=files)
        if r.status_code != 200:
            print(f"{PREFIX}Unable to upload checkpoint!")

    def on_train_end(self, *args, **kwargs):
        """"
        Args:

            *args   last, best, plots, epoch
        """
        # Set args
        last, best, plots, epoch, results = (args[0], args[1], args[2],
                                             args[3], args[4])

        # mAP0.5:0.95
        map_new = results[3]

        api_url = HUB_API_ROOT + "model-final"
        payload = {"modelId": self.model_id, "epoch": epoch, "map": map_new}
        payload.update(self.auth.get_auth_string())
        files = {"last.pt": open(last, "rb"), "best.pt": open(best, "rb")}

        r = requests.post(api_url, data=payload, files=files)
        if r.status_code != 200:
            print(f"{PREFIX}Unable to upload final models!")
