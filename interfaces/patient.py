import gradio as gr
def setup(patient_col):
    """
    Setup the patient list interface
    """
    with patient_col:
        gr.Markdown("<h1 style=\"text-align: center; font-size: 48px;\">Patient List Page</h1>")