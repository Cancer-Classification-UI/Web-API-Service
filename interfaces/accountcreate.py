import gradio as gr
import requests
import logging
import hashlib
import re
import os

log = logging.getLogger('web-api')

def setup(acc_creation_col, login_col):
    """
    Setup the account creation interface

    Parameters:
    acc_creation_col (gradio.Column): The column to add the interface to
    login_col (gradio.Column): The column to switch to when the cancel button is clicked
    """
    with acc_creation_col:
        log.debug("Setting up account creation interface")
        gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Create Account</h1>")
        gr.Markdown("<p style=\"text-align: center;\">Create an account by filling in info below.</p>")
        username_txt = gr.Textbox(label="Username", interactive=True, max_lines=1, value=None)
        passwd_txt = gr.Textbox(label="Password", interactive=True, max_lines=1, type="password", value=None)
        c_passwd_txt = gr.Textbox(label="Confirm Password", interactive=True, max_lines=1, type="password", value=None)
        user_email_txt = gr.Textbox(label="Email", interactive=True, max_lines=1, value=None)
        name_txt = gr.Textbox(label="Name", interactive=True, max_lines=1, value=None)

        sign_up_btn = gr.Button("Sign Up")

        # TODO, refactor so it uses the same reset as cancel, conditionaly
        sign_up_btn.click(sign_up, inputs=[username_txt, passwd_txt, c_passwd_txt, user_email_txt, name_txt], outputs=[login_col, acc_creation_col, username_txt, passwd_txt, c_passwd_txt, user_email_txt, name_txt])
        cancel_btn = gr.Button("Cancel", elem_id="linkbutton", variant="secondary", size="sm",)
        cancel_btn.click(reset, outputs=[login_col, acc_creation_col, username_txt, passwd_txt, c_passwd_txt, user_email_txt, name_txt])

def sign_up(username, passw, c_passwd, user_email, name):
    """
    Signs up the user

    Parameters:
    user_email_txt (gradio.Textbox): The textbox containing the user's email
    username_txt (gradio.Textbox): The textbox containing the user's username
    passwd_txt (gradio.Textbox): The textbox containing the user's password
    c_passwd_txt (gradio.Textbox): The textbox containing the user's password confirmation

    Returns:
    gradio.Column: The column responsible for login
    gradio.Column: The column responsible for account creation
    gradio.Textbox: The textbox responsible for the user's username
    gradio.Textbox: The textbox responsible for the user's password
    gradio.Textbox: The textbox responsible for the user's password confirmation
    gradio.Textbox: The textbox responsible for the user's email
    graido.Textbox: The textbox responsible for the user's name

    """
    log.info("Signing up user")

    # TODO, return dict, allws us to skip out on updating values.
    # Check if any of the inputs are empty
    if username == "" or passw == "" or c_passwd == "" or user_email == "" or name == "":
        gr.Warning("One or more inputs are empty")
        return [gr.update(), gr.update(), None, None, None, None, None]
    
    # Check if the passwords match
    if passw != c_passwd:
        gr.Warning("Passwords do not match")
        return [gr.update(), gr.update(), username, passw, c_passwd, user_email, name]
    
    # Check if email is valid  by checking against this regex: ^..*@.*.\.(com|net|org)$
    if not re.match(r"^..*@.*.\.(com|net|org)$", user_email):
        gr.Warning("Email is not valid")
        return [gr.update(), gr.update(), username, passw, c_passwd, user_email, name]

    # Encrypt the password
    encrypted_passw = hashlib.sha256(passw.encode('utf-8')).hexdigest()
    print(encrypted_passw)

    # Get the login api address from env
    address = os.getenv("LOGIN_API_ADDRESS")
    if address is None:
        log.warning("LOGIN_API_ADDRESS not specified in env, defaulting to 127.0.0.1:8084")
        address = '127.0.0.1:8084'

    if (address == 'None'):
        log.warning("Bypassing login API")
        success = True
        name = 'Admin'
    else:
        # Send the create account request
        try:
            log.debug("Sending create account request for username and passwd: " + username + ", " + encrypted_passw)
            response = requests.post('http://' + address + '/api/v1/create-account', 
                                params={'username': username, 'password_hash': encrypted_passw, 'email': user_email, 'name': name})
            
        except requests.exceptions.ConnectionError:
            raise gr.Error("Login API connection error")
        except Exception as e:
            raise gr.Error("Login API error: " + str(e))
        
        # Extract data from response, and handle errors
        success = False
        if response.status_code == 200:
            data = response.json()
            success = bool(data.get('success'))
        else: # TODO Add more error handling
            raise gr.Error("Login API response not ok: " + str(response))

    # Inform user of create account status
    if success:
        gr.Info("Account creation successful")
        return gr.update(visible=True), gr.update(visible=False), gr.update(value=None), gr.update(value=None), gr.update(value=None), gr.update(value=None), gr.update(value=None)
    else:
        gr.Warning("Account creation unsuccessful: Username or Email already taken")
        return [gr.update(), gr.update(), username, passw, c_passwd, user_email, name]


def reset():
    """
    Resets the account creation page, and also all the inputs
    
    Returns:
    gradio.Column: The column responsible for login
    gradio.Column: The column responsible for account creation
    gradio.Textbox: The textbox responsible for the user's username
    gradio.Textbox: The textbox responsible for the user's password
    gradio.Textbox: The textbox responsible for the user's password confirmation
    gradio.Textbox: The textbox responsible for the user's email
    graido.Textbox: The textbox responsible for the user's name
    """

    return gr.update(visible=True), gr.update(visible=False), gr.update(value=None), gr.update(value=None), gr.update(value=None), gr.update(value=None), gr.update(value=None)
