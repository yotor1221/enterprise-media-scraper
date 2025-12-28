import logging

def setup_logger():
    # Create a custom logger
    logger = logging.getLogger("ScraperOrchestrator")
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('scraper_errors.log')
    
    # Set levels
    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.ERROR) # Only save errors to the file

    # Create formatters and add to handlers
    format_str = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(format_str)
    file_handler.setFormatter(format_str)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger