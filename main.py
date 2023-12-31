import os
import logging
import gradio as gr
from dotenv import load_dotenv
import interfaces as interfaces

log = logging.getLogger('web-api')

# Main function
def main():
    print("Starting Login-API microservice...")

    load_dotenv(verbose=True, override=True) # Loads .env if present
    setup_logging()

    # Readin css
    with open("interfaces/main.css") as f:
        css = f.read()
        f.close()

    demo = setup_main_interface(css)

    port = os.getenv("APP_PORT") # Default to 8082
    if port is None:
        logging.warning("APP_PORT not specified in env, default to 8082")
        port = "8082"

    demo.queue(api_open=False).launch(server_port=int(port), share=False, show_api=False)

def setup_logging():
    """
    Setup logging config, valid log levels are:
    DEBUG, INFO, WARNING, ERROR, CRITICAL
    """

    # Get log level from .env
    log_level = os.getenv("LOG_LEVEL")
    if log_level is None:
        print("WARNING: LOG_LEVEL not specified in env, defaulting to info")
        log_level = "info"

    # Convert log level to actual level
    numeric_level = logging.getLevelName(log_level.upper())
    if not isinstance(numeric_level, int):
        print('ERROR: Invalid log level, defaulting to info')
        numeric_level = logging.INFO

    # Setup logging config
    log.setLevel(level=numeric_level)
    fh = logging.StreamHandler()
    fh_formatter = logging.Formatter('time=\"%(asctime)s\" level=%(levelname)s msg=\"%(message)s\"')
    
    fh.setFormatter(fh_formatter)
    log.addHandler(fh)

    log.info("STARTING LOG...")
    log.info("LOG_LEVEL: " + logging.getLevelName(numeric_level))


def setup_main_interface(css):
    """
    Setup the main interface

    Parameters:
    css (str): The css to apply to the interface
    """
    
    log.info("Setting up interface")
    with gr.Blocks(css=css, theme=interfaces.SoftCustom(primary_hue="blue",
                                                 secondary_hue="blue")) as demo:
        
        # Setup doctor name
        current_user = gr.State("")
        current_patient_data_df = gr.Dataframe(visible=False)

        patient_refresh_flag = gr.Number(0, visible=False)
        classification_refresh_flag = gr.Number(0, visible=False)

        # Setup columns
        login_col = gr.Column(elem_id="userinput", visible=True)
        patient_col = gr.Column(visible=False)
        acc_creation_col = gr.Column(elem_id="userinput", visible=False)
        forgot_passwd_col = gr.Column(elem_id="userinput", visible=False)
        classification_col = gr.Column(visible=False)

        # Setup interfaces
        interfaces.patient.setup(patient_col, 
                                 current_user, 
                                 patient_refresh_flag, 
                                 classification_col, 
                                 current_patient_data_df,
                                 classification_refresh_flag)
        interfaces.login.setup(login_col, 
                               patient_col,
                               acc_creation_col, 
                               forgot_passwd_col,
                               current_user, 
                               patient_refresh_flag)
        interfaces.accountcreate.setup(acc_creation_col,
                                       login_col)
        interfaces.forgotpassword.setup(forgot_passwd_col,
                                        login_col)
        interfaces.classification.setup(classification_col,
                                        patient_col,
                                        current_patient_data_df,
                                        classification_refresh_flag)
        log.info("Interface setup complete")
    return demo


main()