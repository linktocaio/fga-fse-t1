
from datetime import datetime
import logging


now = datetime.now()
file_name = "./logs/"  
file_name += now.strftime("%d/%m/%Y_%H:%M:%S")
logging.basicConfig(filename=file_name,
					format='%(asctime)s %(message)s',
					filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)
logger.info("HORA; LOG")
