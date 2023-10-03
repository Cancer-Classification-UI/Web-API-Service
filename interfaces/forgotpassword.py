import gradio as gr
import logging

def setup(forgot_passwd_col):
    """
    Setup the forgot password interface

    Parameters:
    forgot_passwd_col (gradio.Column): The column to add the interface to
    """
    with forgot_passwd_col:
        logging.debug("Setting up forgot password interface")
        gr.Markdown("""
                    <h1 style=\"text-align: center; 
                                   font-size: 48px;\">
                    Forgot Pass Page
                    </h1>""")
