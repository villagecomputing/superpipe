import os

is_dev = os.environ.get("ENV", "development") == "development"
