import os

is_dev = os.environ.get("LABELKIT_ENV", "development") == "development"
