import gradio as gr
import logging

def setup(forgot_passwd_col, login_col):
    """
    Setup the forgot password interface

    Parameters:
    forgot_passwd_col (gradio.Column): The column to add the interface to
    """
    with forgot_passwd_col:
        logging.debug("Setting up forgot password interface")

        # Setup inital forgot password interface
        initial_forgot_col = gr.Column(elem_id="userinput")
        with initial_forgot_col:
            gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Forgot Password</h1>")
            gr.Markdown("<p style=\"text-align: center;\">Enter the email address associated with you account and we'll send you a code to reset your password.</p>")
            user_txt = gr.Textbox(label="Email", interactive=True, max_lines=1, value=None)
            continue_initial_btn = gr.Button("Continue")


        validate_forgot_col = gr.Column(visible=False)
        with validate_forgot_col:
            gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Enter 4 Digit Code</h1>")
            gr.Markdown("<p style=\"text-align: center;\">Enter your 4 digit code that you received in your email.</p>")
            with gr.Row():
                valid1_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
                valid2_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
                valid3_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
                valid4_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
            continue_validate_btn = gr.Button("Continue")

        reset_pass_col = gr.Column(visible=False)
        with reset_pass_col:
            gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Reset Password</h1>")
            gr.Markdown("<p style=\"text-align: center;\">Set the new password for your account</p>")
            new_pass_txt = gr.Textbox(label="New Password", interactive=True, type="password", max_lines=1, value=None)
            c_new_pass_txt = gr.Textbox(label="Confirm Password", interactive=True, type="password", max_lines=1, value=None)
            reset_pass_btn = gr.Button("Reset Password")

        cancel_btn = gr.Button("Cancel", elem_id="linkbutton", variant="secondary", size="sm",)

        cancel_btn.click(reset, outputs=[login_col, forgot_passwd_col, initial_forgot_col, validate_forgot_col, reset_pass_col, user_txt, valid1_num, valid2_num, valid3_num, valid4_num, new_pass_txt, c_new_pass_txt])

        continue_initial_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                         outputs=[initial_forgot_col, validate_forgot_col])
        
        continue_validate_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                             outputs=[validate_forgot_col, reset_pass_col])
def reset():
    """
    Reset the forgot password interface

    Returns:
    login_col (gradio.Column): The column responsible for login
    forgot_passwd_col (gradio.Column): The column responsible for forgot password
    initial_forgot_col (gradio.Column): The column responsible for the initial forgot password interface
    validate_forgot_col (gradio.Column): The column responsible for validating the forgot password request
    user_txt (gradio.Textbox): The textbox responsible for the user's email
    """
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(value=None), gr.update(value=0), gr.update(value=0), gr.update(value=0), gr.update(value=0), gr.update(value=None), gr.update(value=None)