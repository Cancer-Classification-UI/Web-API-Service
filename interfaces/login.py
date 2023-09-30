import gradio as gr
import hashlib
import logging
import requests

def setup():
    """
    Setup the login interface
    """
    input_col = gr.Column(elem_id="userinput", scale=1)
    with input_col:
        gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Log In</h1>")
        gr.Markdown("<h3 style=\"text-align: center;\">New User? <a>Create an account</a></h3>")
    
        user = gr.Textbox(label="Username", max_lines=1)
        passw = gr.Textbox(label="Password", max_lines=1, type="password")

        gr.Markdown("<h3 style=\"text-align: center;\"><a>Forgot Password?</a></h3>")
        btn = gr.Button("Login")
        
    btn.click(send_login_request, inputs=[user, passw])


def send_login_request(user, passw):
    """
    Send login request to backend
    """
    # Check inputs to make sure they have something in them
    if user == "" or passw == "":
        gr.Interface.alert("Please fill out all fields.")
        return

    # Encrypt the password
    encrypted_passw = hashlib.sha256(passw.encode('utf-8')).hexdigest()
    logging.info('Sent login request: ' + str({'username': user, 'password': encrypted_passw}))

    # response = requests.post('127.0.0.1:0804', data={'username': user, 'password': encrypted_passw})
    # if response.status_code == 200:
    #     print("Login successful!")
    # else:
    #     print("Login failed.")

    gr.Info("Login Successful")




