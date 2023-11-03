import hashlib
import logging
import os
import gradio as gr
import requests
import interfaces as interfaces

log = logging.getLogger('web-api')

def setup(login_col, patient_col, acc_creation_col, forgot_passwd_col, current_user, patient_refresh_flag):
    """
    Sets up the login interface with the given columns for account creation, password recovery, and patient view.
    
    Parameters:
    login_col (gradio.Column): The column where the login interface will be displayed.
    patient_col (gradio.Column): The column where the patient view will be displayed after successful login.
    acc_creation_col (gradio.Column): The column where the account creation interface will be displayed after clicking the "Create an account" button.
    forgot_passwd_col (gradio.Column): The column where the password recovery interface will be displayed after clicking the "Forgot Password?" button.
    current_user (gradio.State): The state where the current user will be stored.
    patient_refresh_flag (gradio.State): The state where the patient view's refresh flag will be stored.
    """
    
    login_status = gr.State(False) # True if login successful, False otherwise

    # Setup login interface
    with login_col:
        log.debug("Setting up login interface")

        # Header
        gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Log In</h1>")
        with gr.Row(elem_id="account-create-action"):
            gr.Markdown("""
                        <p style=\"padding: var(--button-small-padding); 
                                   padding-right: 16px;
                                   margin-bottom: 0px; 
                                   text-align: right; 
                                   white-space: nowrap; \">
                        New User?
                        </p>
                        """)
            create_btn = gr.Button("Create an account", 
                                   elem_id="linkbutton-left", 
                                   variant="secondary", 
                                   size="sm")
    
        # Login form
        user_txt = gr.Textbox(label="Username", max_lines=1)
        passw_txt = gr.Textbox(label="Password", max_lines=1, type="password")

        forgot_btn = gr.Button(value="Forgot Password?", 
                               elem_id="linkbutton", 
                               variant="secondary", 
                               size="sm")
        login_btn = gr.Button("Login")


    # Event handlers
    log.debug("Setting up login interface callbacks")
    create_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                     outputs=[login_col, acc_creation_col])
    
    forgot_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                    outputs=[login_col, forgot_passwd_col])
    
    login_btn.click(send_login_request, 
              inputs=[user_txt, passw_txt], 
              outputs=[login_status, current_user]) \
             .then(swap_to_patient_view, 
             inputs=login_status, 
             outputs=[login_col, patient_col, patient_refresh_flag])


def validate_input(user, passw):
    """
    Validate user and password inputs

    Parameters:
    user (str): The username inputted by the user.
    passw (str): The password inputted by the user.

    Returns:
    gradio.Textbox: The username textbox.
    gradio.Textbox: The password textbox.
    """
    user_elem, passw_elem = None, None

    if user == "":
        gr.Warning("Please enter a username")
        user_elem=True # Temp until gradio css release
        # user_elem = gr.Textbox(elem_id="#wronginput", value="")

    if passw == "":
        gr.Warning("Please enter a password")
        passw_elem=True # Temp until gradio css release
        # passw_elem = gr.Textbox(elem_id="#wronginput", value="")

    return user_elem, passw_elem


def send_login_request(user, passw):
    """
    Send login request to backend

    Parameters:
    user (str): The username inputted by the user.
    passw (str): The password inputted by the user.\
    
    Returns:
    bool: The login status.
    str: The username.
    """
    user_elem, passw_elem = validate_input(user, passw)

    if (user_elem is not None) or (passw_elem is not None):
        return False, ""

    # Encrypt the password
    encrypted_passw = hashlib.sha256(passw.encode('utf-8')).hexdigest()
    print(encrypted_passw)

    # Get the login api address from env
    address = os.getenv("LOGIN_API_ADDRESS")
    if address is None:
        print("WARNING: LOGIN_API_ADDRESS not specified in env, defaulting to 127.0.0.1:8084")
        address = '127.0.0.1:8084'

    # Send the login request
    try:
        log.debug("Sending login request: " + str(user) + ", " + str(encrypted_passw))
        response = requests.get('http://' + address + '/api/v1/signin', 
                            params={'username': user, 'password_hash': encrypted_passw})
    except requests.exceptions.ConnectionError:
        raise gr.Error("Login API connection error")
    except Exception as e:
        raise gr.Error("Login API error: " + str(e))
    
    # Extract data from response, and handle errors
    success = False
    if response.status_code == 200:
        data = response.json()
        success = bool(data.get('success'))
        name = data.get('name')
    else: # TODO Add more error handling
        raise gr.Error("Login API response not ok: " + str(response))

    # Inform user of login status
    gr.Info("Login successful") if success else gr.Warning("Login unsuccessful")

    # Make sure to update doctor name 
    return success, name


def swap_to_patient_view(login_status):
    """
    Toggle visibility of the login interface

    Parameters:
    login_status (bool): The login status returned from the login request.

    Returns:
    gradio.Column: The login column.
    gradio.Column: The patient view column.
    gradio.Column: The patient view column's refresh flag.
    """
    if login_status:
        log.debug("Swapping to patient view")
        return gr.update(visible=False), gr.update(visible=True), gr.update(value=1)
    else:
        return gr.update(visible=True), gr.update(visible=False), gr.update(value=0)