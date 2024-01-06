import logging

# Gearman config
GEARMAN_SERVERS = ["127.0.0.1:4730"]
RECORDING_IMPORT_TASK_NAME = "recording-import"

# Recording data config
RECORDING_DATE = "2023-10-18"
RECORDER_ID = "recorder-1"
FILESHARE_DIR = f"/tmp/recording_import_worker/import/{RECORDER_ID}/{RECORDING_DATE}"
RECORDING_FILE_ID = "recording1"

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
