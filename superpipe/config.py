import os

is_dev = os.environ.get("SUPERPIPE_ENV", "development") == "development"


def studio_enabled():
    studio_url_set = os.environ.get("SUPERPIPE_STUDIO_URL") is not None
    studio_api_key_set = os.environ.get("SUPERPIPE_STUDIO_API_KEY") is not None
    if not studio_url_set and not studio_api_key_set:
        print("Env var SUPERPIPE_STUDIO_URL or SUPERPIPE_STUDIO_API_KEY must be set for Superpipe Studio logging")
        return False
    return True
