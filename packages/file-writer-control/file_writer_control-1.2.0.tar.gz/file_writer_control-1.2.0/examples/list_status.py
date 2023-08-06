import time

from file_writer_control import WorkerCommandChannel
from file_writer_control import JobHandler


def print_current_state(channel: WorkerCommandChannel):
    print("Known workers")
    w_format = "{:45s}{:30s}"
    print(w_format.format("Service id", "Current state"))
    print("-" * 80)
    for worker in channel.list_known_workers():
        print(w_format.format(worker.service_id, worker.state))

    print("\nKnown jobs")
    j_format = "{:26s}{:30s}{:30s}"
    print(j_format.format("Service id", "Job id", "Current state"))
    print("-" * 80)
    for job in channel.list_known_jobs():
        print(j_format.format(job.service_id, job.job_id, job.state))
        if job.file_name is not None:
            print(f"    File name: {job.file_name}")
        if len(job.message) > 0:
            print(f"    Message: {job.message}")
        handler = JobHandler(channel, job_id=job.job_id)
        handler.stop_now()
        time.sleep(1)

    print("\nKnown commands")
    c_format = j_format
    print(c_format.format("Job id", "Command id", "Current state"))
    print("-" * 80)
    for command in channel.list_known_commands():
        print(c_format.format(command.job_id, command.command_id, command.state))
        if len(command.message) > 0:
            print("    Message: {}".format(command.message))


if __name__ == "__main__":
    kafka_host = "dmsc-kafka01:9092"
    command_channel = WorkerCommandChannel("{}/command_topic".format(kafka_host))
    time.sleep(10)
    print_current_state(command_channel)
