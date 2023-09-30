import gradio as gr
import os
import logging
from dotenv import load_dotenv
import interfaces.login as login_interface

# Main function
def main():
    print("Starting Login-API microservice...")
    print("No logs will be generated here. Please see log.txt file for logging")

    load_dotenv()
    setup_logging()

    # Readin css
    with open("interfaces/main.css") as f:
        css = f.read()

    demo = setup_main_interface(css)

    demo.queue().launch(server_port=int(os.getenv("APP_PORT")), share=False)

def setup_logging():
    """
    Setup logging config, valid log levels are:
    DEBUG, INFO, WARNING, ERROR, CRITICAL
    """

    # Get log level from .env
    log_level = os.getenv("LOG_LEVEL")
    if log_level is None:
        logging.warning("LOG_LEVEL not specified in .env, defaulting to info")
        log_level = "info"

    # Convert log level to actual level
    numeric_level = getattr(logging, log_level, None)
    if not isinstance(numeric_level, int):
        logging.error('Invalid log level, defaulting to info')
        numeric_level = logging.INFO

    # Setup logging config
    logging.basicConfig(filename='log.txt', level=numeric_level)

    logging.info("STARTING LOG...")
    logging.info("LOG_LEVEL: " + logging.getLevelName(numeric_level))

def setup_main_interface(css):
    """
    Setup the main interface
    :param css: css string
    """

    logging.info("Setting up interface")
    with gr.Blocks(css=css, theme=gr.themes.Soft(primary_hue="blue",
                                                 secondary_hue="blue")) as demo:
        login_interface.setup()
    
    return demo

main()