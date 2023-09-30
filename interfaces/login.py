import gradio as gr
import hashlib
import logging

def setup(login_col, patient_col):
    """
    Setup the login interface
    """
    login_status = gr.State(False)
    with login_col:
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
            gr.Button("Create an account", elem_id="linkbutton-left", variant="secondary", size="sm")
    
        user = gr.Textbox(label="Username", max_lines=1)
        passw = gr.Textbox(label="Password", max_lines=1, type="password")

        gr.Button(value="Forgot Password?", elem_id="linkbutton", variant="secondary", size="sm")
        btn = gr.Button("Login")
        
    btn.click(send_login_request, inputs=[user, passw], outputs=login_status).then(toggle_visibility, inputs=login_status, outputs=[login_col, patient_col])


def validate_input(user, passw):
    """
    Validate user and password inputs
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
    """
    user_elem, passw_elem = validate_input(user, passw)

    if (user_elem is not None) or (passw_elem is not None):
        return False

    # Encrypt the password
    encrypted_passw = hashlib.sha256(passw.encode('utf-8')).hexdigest()
    logging.info('Sent login request: ' + str({'username': user, 'password': encrypted_passw}))

    # response = requests.post('127.0.0.1:0804', data={'username': user, 'password': encrypted_passw})
    # if response.status_code == 200:
    #     print("Login successful!")
    # else:
    #     print("Login failed.")

    gr.Info("Login Successful")
    return True

def toggle_visibility(login_status):
    """
    Toggle visibility of the login interface
    """
    print(login_status)
    if login_status:
        print("Swapping to patient view")
        return gr.update(visible=False), gr.update(visible=True)




