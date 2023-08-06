import os

__version__ = "1.1.11"

cloud_endpoint = "https://api.snit.ch/"
endpoint_address = os.getenv("SNITCH_ENDPOINT_ADDRESS", cloud_endpoint)
access_token = os.getenv("SNITCH_ACCESS_TOKEN")
verbose = os.getenv("SNITCH_VERBOSE", True)

from snitch_ai.internal.project import create_project, get_project, select_project
