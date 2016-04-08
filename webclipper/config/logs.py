import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
logger = logging.getLogger("webclipper")
logger.setLevel(logging.INFO)
