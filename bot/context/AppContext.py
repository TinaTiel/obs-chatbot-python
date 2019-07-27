import bot
import os
from pathlib import Path
import logging
import logging.config

#print('INIT APP CONTEX')

# Configure Logging
#log_level = getattr(logging, data.get('log_level', "INFO"))
log_level = logging.DEBUG
logging.basicConfig(level=log_level)
logging.getLogger("obswebsocket").setLevel(logging.ERROR) # OBS websocket Core is spammy

log = logging.getLogger(__name__)
log.info("Initializing App Context...")

# Define the various file roots
proj_root = Path(os.path.dirname(bot.__file__))
conf_root = Path(proj_root, '..', 'config')
secrets_root = Path(conf_root, 'secrets')

log.info("...Done.")