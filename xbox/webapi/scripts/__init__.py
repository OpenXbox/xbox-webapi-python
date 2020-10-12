import os

from appdirs import user_data_dir

CLIENT_ID = "388ea51c-0b25-4029-aae2-17df49d23905"
# No secret needed, we registered as "Desktop App" in Azure AD
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8080/auth/callback"

DATA_DIR = user_data_dir("xbox", "OpenXbox")
TOKENS_FILE = os.path.join(DATA_DIR, "tokens.json")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
