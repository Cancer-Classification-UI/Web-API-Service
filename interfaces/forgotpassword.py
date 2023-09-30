import gradio as gr
def setup(forgot_passwd_col):
    """
    Setup the forgot password interface
    """
    with forgot_passwd_col:
        gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Forgot Pass Page</h1>")
