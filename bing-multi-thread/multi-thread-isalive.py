def queue_worker(camera_q, result_q):
    '''
    Function takes camera off the queue and calls healthchecks
    '''

    try:
        camera = camera_q.get()
        camera_status, remove_camera = process_camera(camera)

        result_q.put("Success")
        return True
    except queue.Empty:
        logging.info("Queue is empty")
        result_q.put("Fail")
        return False


def process_worker(camera_q, result_q, process_num, stop_event):
    while not stop_event.is_set():
        # Create configured number of threads and provide references to both Queues to each thread
        threads = []
        for i in range(REQUEST_THREADS):
            thread = threading.Thread(target=queue_worker, args=(camera_q, result_q))
            thread.setName("CameraThread-{}".format(i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(timeout=120)

        if camera_q.empty():
            num_active = sum([t.is_alive() for t in threads])
            logging.info("[Process {}] << {} >> active threads and << {} >> cameras left to process. << {} >> processed.".format(process_num, num_active, camera_q.qsize(), result_q.qsize()))


def main():
    '''
    Main application entry
    '''

    logging.info("Starting Scan With << " + str(REQUEST_THREADS) + " Threads and " + str(CHILD_PROCESSES) + " Processors >>")
    logging.info("Reference Images Stored During Scan << " + str(store_images) + " >>")

    stop_event = multiprocessing.Event()
    camera_q, result_q = multiprocessing.Queue(), multiprocessing.Queue()

    # Create a Status thread for maintaining process status
    create_status_thread()

    all_cameras = get_oversite_cameras(True)
    for camera in all_cameras:
        camera_q.put(camera)

    logging.info("<< {} >> cameras queued up".format(camera_q.qsize()))

    processes = []
    process_num = 0
    finished_processes = 0
    for i in range(CHILD_PROCESSES):
        process_num += 1
        proc = multiprocessing.Process(target=process_worker, args=(camera_q, result_q, process_num, stop_event))
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()
        finished_processes += 1
        logging.info("{} finished processes".format(finished_pr))

    logging.info("All processes finished")