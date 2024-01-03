import logging
import os
import shutil
import subprocess

from python3_gmtasks.jsonclass import GearmanClient

import config

logger = logging.getLogger(__name__)


# TODO: get args - arg to include is boolean "--configure_worker"
# TODO: if dirs don't exist...?


def get_gearman_client(servers: list[str]):
    return GearmanClient(servers)


def copy(source_path: str, destination_path: str):
    destination_dir = os.path.dirname(destination_path)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    if os.path.exists(destination_path):
        os.remove(destination_path)

    shutil.copy(source_path, destination_path)


def copy_riw_config():
    """
    Copy the recording import worker config yaml to the config location on the host machine
    """
    copy(
        source_path="./data/config.yaml",
        destination_path="/opt/intelligent-voice/data/recording_import_worker/config.yaml",
    )


def copy_recordings_to_fileshare():
    """
    Copy the recording data to import to the fileshare location
    """
    copy(
        source_path="./data/recordings/",
        destination_path=os.path.join(config.FILESHARE_DIR, config.RECORDING_DATE),
    )


def copy_custodian_file():
    """
    Copy to custodian file to the host machine
    """
    copy(
        source_path="./data/custodians.xml",
        destination_path="/opt/intelligent-voice/data/recording_import_worker/custodians/custodian.xml",
    )


def restart_recording_import_worker():
    command = "sudo systemctl restart recording_import_worker"
    subprocess.run(command, shell=True, check=True)


def prep_recording_import_worker_for_test():
    copy_riw_config()
    copy_recordings_to_fileshare()
    copy_custodian_file()
    restart_recording_import_worker()


def submit_gearman_task(taskname: str, job_data: dict) -> None:
    """
    Initialise a Gearman client and submit a job to the queue
    """
    client = get_gearman_client()
    logger.info(f"Submitting task {taskname} with payload: {job_data}")
    client.submit_job(taskname, job_data, wait_until_complete=False, background=True)
    logger.info(f"Successfully submitted task {taskname}")


def start_recording_import_task():
    """
    Start a recording import task with the example audio and metadata
    """
    logger.info(
        f"Starting recording import worker test with test call '{config.RECORDING_FILE_ID}'"
    )
    submit_gearman_task(
        taskname=config.RECORDING_IMPORT_TASK_NAME,
        job_data={
            "ticket": {
                "recorder_id": config.RECORDER,
                "recorder_id": config.RECORDING_DATE,
                "recording_file_id": config.RECORDING_FILE_ID,
            }
        },
    )


if __name__ == "__main__":
    logger.info("Starting recording import worker end to end test...")
    logger.info("Configuring worker and copying test data to host machine")
    prep_recording_import_worker_for_test()
    logger.info("Recording import worker configured and restarted successfully")
    logger.info("Starting import task...")
    start_recording_import_task()
    logger.info("Recording import worker test run finished")
    logger.info("Check worker logs: `sudo docker logs recording_import_worker -f`")
