import os

is_dev = os.environ.get("SUPERPIPE_ENV", "development") == "development"
