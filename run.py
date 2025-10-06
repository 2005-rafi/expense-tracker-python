# run.py

import threading
import time
import logging
from settings_config import configure_django

# FIRST: Configure Django settings properly
configure_django()

# THEN import backend
from backend import run_django_server
from frontend import run_streamlit_app

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Start Django server
    django_thread = threading.Thread(target=run_django_server, daemon=True)
    django_thread.start()

    logger.info("Starting Django server...")
    time.sleep(2)

    logger.info("Starting Streamlit app...")
    run_streamlit_app()
