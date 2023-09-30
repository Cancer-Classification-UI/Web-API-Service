import gradio as gr
def setup(acc_creation_col):
    """
    Setup the account creation interface
    """
    with acc_creation_col:
        gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Account Creation Page</h1>")