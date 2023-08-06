__version__ = '0.0.18'  # print(ultralytics.__version__)

AUTH = None


def login():
    # Login to Ultralytics HUB
    global AUTH
    from .auth import Auth
    AUTH = Auth()


def start():
    # Start training models with Ultralytics HUB
    from .main import main
    main()