import gradio as gr
import logging
def setup(acc_creation_col):
    """
    Setup the account creation interface

    Parameters:
    acc_creation_col (gradio.Column): The column to add the interface to
    """
    with acc_creation_col:
        logging.debug("Setting up account creation interface")
        gr.Markdown("""
                    <h1 style=\"text-align: center; 
                                   font-size: 48px;\">
                    Account Creation Page
                    </h1>""")