import logging
import os
from datetime import datetime, timezone

# Configuracion de la base de datos
DATABASE_URL = "sqlite:///./todos.db"

# Configuracion del logging
def setup_logging(): 
    log_directory = "logs"

    if not os.path.exists(log_directory): 
        os.makedirs(log_directory)

    log_file = os.path.join(log_directory, f"app_{datetime.now(timezone.utc).strftime('%Y%m%d')}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s [%(pathname)s: %(lineno)d] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

logger = setup_logging()
