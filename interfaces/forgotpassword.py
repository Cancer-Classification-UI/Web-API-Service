import gradio as gr
import logging
import requests
import re
import os

log = logging.getLogger('web-api')

def setup(forgot_passwd_col, login_col):
    """
    Setup the forgot password interface

    Parameters:
    forgot_passwd_col (gradio.Column): The column to add the interface to
    login_col (gradio.Column): The column to switch to when the cancel button is clicked
    """

    # Setup forgot password interface
    with forgot_passwd_col:
        log.debug("Setting up forgot password interface")

        # Setup inital forgot password interface
        initial_forgot_col = gr.Column(elem_id="userinput")
        with initial_forgot_col:
            gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Forgot Password</h1>")
            gr.Markdown("<p style=\"text-align: center;\">Enter the email address associated with you account and we'll send you a code to reset your password.</p>")
            user_txt = gr.Textbox(label="Email", interactive=True, max_lines=1, value=None)
            continue_initial_btn = gr.Button("Continue")

        # Setup validate forgot password interface
        validate_forgot_col = gr.Column(visible=False)
        with validate_forgot_col:
            gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Enter 4 Digit Code</h1>")
            gr.Markdown("<p style=\"text-align: center;\">Enter your 4 digit code that you received in your email.</p>")
            with gr.Row():
                valid1_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
                valid2_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
                valid3_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
                valid4_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
                valid5_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
                valid6_num = gr.Number(elem_id="simplenum", show_label=False, interactive=True, min_width=25, precision=0, minimum=0, maximum=9)
            continue_validate_btn = gr.Button("Continue")

        # Setup reset password interface
        reset_pass_col = gr.Column(visible=False)
        with reset_pass_col:
            gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Reset Password</h1>")
            gr.Markdown("<p style=\"text-align: center;\">Set the new password for your account</p>")
            new_pass_txt = gr.Textbox(label="New Password", interactive=True, type="password", max_lines=1, value=None)
            c_new_pass_txt = gr.Textbox(label="Confirm Password", interactive=True, type="password", max_lines=1, value=None)
            reset_pass_btn = gr.Button("Reset Password")

        # Setup cancel button
        cancel_btn = gr.Button("Cancel", elem_id="linkbutton", variant="secondary", size="sm",)

        # Event handlers
        cancel_btn.click(reset, outputs=[login_col, forgot_passwd_col, initial_forgot_col, validate_forgot_col, reset_pass_col, user_txt, valid1_num, valid2_num, valid3_num, valid4_num, valid5_num, valid6_num, new_pass_txt, c_new_pass_txt])
        
        continue_initial_btn.click(send_forgot_passwd_request_email, 
                                   inputs=[user_txt], 
                                   outputs=[initial_forgot_col, validate_forgot_col])
        
        
        continue_validate_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                             outputs=[validate_forgot_col, reset_pass_col])
        
def send_forgot_passwd_request_email(user_email):
    log.info("Starting reseting password for user")

    if user_email == "":
        gr.Warning("Please enter an email to reset password")
        return [gr.update(visible=True), gr.update(visible=False), None]
    
    # Check if email is valid  by checking against this regex: ^..*@.*.\.(com|net|org)$
    if not re.match(r"^..*@.*.\.(com|net|org)$", user_email):
        gr.Warning("Email is not valid")
        return [gr.update(visible=True), gr.update(visible=False), user_email]

    # Get the login api address from env
    address = os.getenv("LOGIN_API_ADDRESS")
    if address is None:
        log.warning("LOGIN_API_ADDRESS not specified in env, defaulting to 127.0.0.1:8084")
        address = '127.0.0.1:8084'

    if (address == 'None'):
        log.warning("Bypassing login API")
        success = True
    else:
        # Send the login request
        try:
            log.debug("Sending password reset request for email: " + user_email)
            response = requests.post('http://' + address + '/api/v1/password-change-email', 
                                params={'email': user_email})
        except requests.exceptions.ConnectionError:
            raise gr.Error("Login API connection error")
        except Exception as e:
            raise gr.Error("Login API error: " + str(e))
        
        # Extract data from response, and handle errors
        success = False
        if response.status_code == 200:
            data = response.json()
            success = bool(data.get('success'))
        elif response.status_code == 500: # Email not found or connection error
            if response.text == "\"Error sending reset email\"": # Bypass
                success = True
            else:
                success = False
                log.warning("Unknown 500 error when trying to send password reset email request: " + str(response.text))
        else: # TODO Add more error handling
            raise gr.Error("Login API response not ok: " + str(response))

    # Inform user of login status
    if success:
        return [gr.update(visible=False), gr.update(visible=True), None]
    else:
        gr.Warning("Forgot password code not sent")
        return [gr.update(visible=True), gr.update(visible=False), user_email]


# def validate_forgot_passwd_code(valid1_num, valid2_num, valid3_num, valid4_num, valid5_num, valid6_num):

def reset():
    """
    Reset the forgot password interface

    Returns:
    gradio.Column: The column responsible for login
    gradio.Column: The column responsible for forgot password
    gradio.Column: The column responsible for the initial forgot password interface
    gradio.Column: The column responsible for validating the forgot password request
    gradio.Textbox: The textbox responsible for the user's email
    """
    return gr.update(visible=True), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(value=None), gr.update(value=0), gr.update(value=0), gr.update(value=0), gr.update(value=0), gr.update(value=0), gr.update(value=0), gr.update(value=None), gr.update(value=None)