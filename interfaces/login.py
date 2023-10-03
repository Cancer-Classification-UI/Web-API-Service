import hashlib
import logging
import gradio as gr

def setup(login_col, patient_col, acc_creation_col, forgot_passwd_col):
    """
    Sets up the login interface with the given columns for account creation, password recovery, and patient view.
    
    Parameters:
    login_col (gradio.Column): The column where the login interface will be displayed.
    patient_col (gradio.Column): The column where the patient view will be displayed after successful login.
    acc_creation_col (gradio.Column): The column where the account creation interface will be displayed after clicking the "Create an account" button.
    forgot_passwd_col (gradio.Column): The column where the password recovery interface will be displayed after clicking the "Forgot Password?" button.
    """
    
    login_status = gr.State(False)
    with login_col:
        logging.debug("Setting up login interface")
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
    
        user_txt = gr.Textbox(label="Username", max_lines=1)
        passw_txt = gr.Textbox(label="Password", max_lines=1, type="password")

        forgot_btn = gr.Button(value="Forgot Password?", 
                               elem_id="linkbutton", 
                               variant="secondary", 
                               size="sm")
        login_btn = gr.Button("Login")

    logging.debug("Setting up login interface callbacks")
    create_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                     outputs=[login_col, acc_creation_col])
    
    forgot_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)),
                    outputs=[login_col, forgot_passwd_col])
        
    login_btn.click(send_login_request, 
              inputs=[user_txt, passw_txt], 
              outputs=login_status) \
             .then(swap_to_patient_view, 
             inputs=login_status, 
             outputs=[login_col, patient_col])


def validate_input(user, passw):
    """
    Validate user and password inputs

    Parameters:
    user (str): The username inputted by the user.
    passw (str): The password inputted by the user.
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
    passw (str): The password inputted by the user.
    """
    user_elem, passw_elem = validate_input(user, passw)

    if (user_elem is not None) or (passw_elem is not None):
        return False

    # Encrypt the password
    encrypted_passw = hashlib.sha256(passw.encode('utf-8')).hexdigest()
    logging.debug('Sent login request: ' + 
                 str({'username': user, 'password': encrypted_passw}))

    # response = requests.post('127.0.0.1:0804', data={'username': user, 'password': encrypted_passw})
    # if response.status_code == 200:
    #     print("Login successful!")
    # else:
    #     print("Login failed.")

    gr.Info("Login Successful")
    return True


def swap_to_patient_view(login_status):
    """
    Toggle visibility of the login interface

    Parameters:
    login_status (bool): The login status of the user.
    """
    if login_status:
        logging.debug("Swapping to patient view")
        return gr.update(visible=False), gr.update(visible=True)