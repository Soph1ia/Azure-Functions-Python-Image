import json
from PIL import Image
import time
import statistics
import logging
import os
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    throughput, average = benchmark()
    return func.HttpResponse(f"Image processing run. The results are :: \n {throughput} \n {average}")


def image_processing():
    """
    This method resizes the image.
    :return: image
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_to_process = Image.open(dir_path + "/image.jpg")

    # Resize the image
    resized_image = image_to_process.resize((1024, 1000))

    return resized_image


def benchmark():
    """
    This is the main benchmarking method that runs the function and calculates the throughput and the average time
    :return: None
    """
    throughput_time = {"Image": []}
    average_duration_time = {"Image": []}
    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)

    for i in range(40):  # adjust accordingly so whole thing takes a few sec
        logger.critical('Image Processing execution beginning')
        t0 = time.time()
        image_processing()
        t1 = time.time()
        logger.critical('Image Processing function ended, calculating metrics')
        if i >= 20:  # We let it warmup for first 20 rounds, then consider the last 20 metrics
            throughput_time["Image"].append(1 / (t1 - t0))  # in seconds
            average_duration_time["Image"].append((t1 - t0) / 1)

            # Printing out results for throughput
    for name, numbers in throughput_time.items():
        logger.critical("The throughput time")
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        throughput_output = "FUNCTION {} used {} times. > MEDIAN {} ops/s > MEAN {} ops/s  > STDEV {} ops/s".format(
            name,
            length,
            median,
            mean,
            stdev)
        logger.critical(throughput_output)

    # printing out results for average duration
    for name, numbers in average_duration_time.items():
        logger.critical("The average Duration details")
        length = str(len(numbers))
        median = str(statistics.median(numbers))
        mean = str(statistics.mean(numbers))
        stdev = str(statistics.stdev(numbers))
        average_output = "FUNCTION {} used {} times. > MEDIAN {} s/ops > MEAN {} s/ops  > STDEV {} s/ops".format(name,
                                                                                                                 length,
                                                                                                                 median,
                                                                                                                 mean,
                                                                                                                 stdev)
        logger.critical(average_output)

    logger.critical("The benchmark is finished properly")
    return throughput_output, average_output


