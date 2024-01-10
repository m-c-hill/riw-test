import argparse
import os
import shutil
import subprocess

from python3_gmtasks.jsonclass import GearmanClient

import config
from config import logger

def get_gearman_client(servers: list[str]):
    return GearmanClient(servers)


def copy(source_path: str, destination_path: str, directory: bool = False):
    destination_dir = os.path.dirname(destination_path)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    if os.path.exists(destination_path):
        if os.path.isfile(destination_path):
            os.remove(destination_path)
        elif os.path.isdir(destination_path):
            shutil.rmtree(destination_path)

    if directory:
        shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
    else:
        shutil.copy(source_path, destination_path)


def copy_riw_config():
    """
    Copy the recording import worker config yaml to the config location on the host machine
    """
    copy(
        source_path="./data/config.yaml",
        destination_path="/opt/intelligent-voice/data/recording_import_worker/config.yaml"
    )


def copy_recordings_to_fileshare():
    """
    Copy the recording data to import to the fileshare location
    """
    copy(
        source_path="./data/recordings",
        destination_path=os.path.join(config.FILESHARE_DIR),
        directory=True
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
    client = get_gearman_client(servers=config.GEARMAN_SERVERS)
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
                "recorder_id": config.RECORDER_ID,
                "recording_date": config.RECORDING_DATE,
                "recording_file_id": config.RECORDING_FILE_ID,
            }
        },
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the recording import worker script.')
    parser.add_argument('--configure-worker', action='store_true', help='If set, configure the recording import worker')
    args = parser.parse_args()

    logger.info("Starting recording import worker end to end test...")

    if args.configure_worker:
        logger.info("Configuring worker and copying test data to host machine")
        prep_recording_import_worker_for_test()
        logger.info("Recording import worker configured and restarted successfully")

    logger.info("Starting import task...")
    start_recording_import_task()
    logger.info("Recording import worker test run finished")
    logger.info("Check worker logs: `sudo docker logs recording_import_worker -f`")
