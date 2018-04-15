import os
from appdirs import user_data_dir


DATA_DIR = user_data_dir('xbox', 'OpenXbox')
TOKENS_FILE = os.path.join(DATA_DIR, 'tokens.json')
