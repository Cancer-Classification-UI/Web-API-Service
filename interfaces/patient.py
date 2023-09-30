import gradio as gr

def setup(patient_col):
    """
    Setup the patient list interface

    Parameters:
    patient_col (gradio.Column): The column to add the interface to
    """
    with patient_col:
        gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Patient List Page</h1>")