import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set hosting environment, if not set, default to production for security
HOSTING_ENV = os.getenv("HOSTING_ENV", "production")

if HOSTING_ENV == "dev":
    from .dev import *
else:
    from .production import *
