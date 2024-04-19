import logging

from python3_gmtasks.jsonclass import GearmanClient

logger = logging.getLogger(__name__)

ITEM_ID = 1000003
GEARMAN_SERVERS = ["127.0.0.1:4730"]
RECORDING_IMPORT_TASK_NAME = "connect-sftp"


def get_gearman_client(servers: list[str]):
    return GearmanClient(servers)


def submit_gearman_task(taskname: str, job_data: dict) -> None:
    """
    Initialise a Gearman client and submit a job to the queue
    """
    client = get_gearman_client(servers=GEARMAN_SERVERS)
    logger.info(f"Submitting task {taskname} with payload: {job_data}")
    client.submit_job(taskname, job_data, wait_until_complete=False, background=True)
    logger.info(f"Successfully submitted task {taskname}")


def start_connect_sftp_task():
    logger.info(f"Starting connect sftp worker test")
    submit_gearman_task(
        taskname=RECORDING_IMPORT_TASK_NAME,
        job_data={
            "itemIds": [ITEM_ID],
            "appServers": ["iv-matt-u22-standalone.chaseits.co.uk:8443"],
            "client": 1,
        },
    )


if __name__ == "__main__":
    logger.info("Starting connect sftp worker end to end test...")
    start_connect_sftp_task()
    logger.info("Check worker logs: `sudo docker logs connect_sftp_worker -f`")
