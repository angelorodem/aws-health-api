import boto3
import multiprocessing

# --------------

def start_all(processes):
    for process in processes:
        try:
            process[0].start()
        except:
            print("Error while starting processes")

def wait_all(processes):
    for process in processes:
        try:
            process[0].join()
        except:
            print("Error while joining processes")

def read_all(processes):
    return_dict = {}
    for process in processes:
        try:
            return_dict.update(process[1].get(False))
        except:
            print("Error while processing queue data")

    return return_dict

