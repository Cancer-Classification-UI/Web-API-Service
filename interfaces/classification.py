import logging
import gradio as gr
from PIL import Image
import interfaces as interfaces
from transformers import pipeline

log = logging.getLogger('web-api')
pipe = pipeline("image-classification", model="gianlab/swin-tiny-patch4-window7-224-finetuned-skin-cancer")

def setup(classification_col, 
          patient_col, 
          current_patient_data_df, 
          classification_refresh_flag):
    """
    Setup the account creation interface

    Parameters:
    classification_col (gradio.Column): The column to add the interface to
    patient_col (gradio.Column): The column to switch to when the cancel button is clicked
    current_patient_data_df (gradio.Dataframe): The dataframe to update when a patient is selected
    classification_refresh_flag (gradio.Number): The flag to refresh the classification view
    """

    # Setup classification interface
    with classification_col:
        log.debug("Setting up classification interface")

        sel_image_path = gr.State()

        # Setu up a cancel button so we can swap easily between patient and 
        # classification view
        cancel_btn = gr.Button("X", 
                               elem_id="canelbutton", 
                               variant="secondary", 
                               size="sm", 
                               interactive=True)

        # Header
        with gr.Row():
            gr.Markdown("<h1 style=\"font-size: 48px;\">Cancer Classification</h1>")

        with gr.Row():
            # Inputs, Patient data, and Reference data
            with gr.Column():
                curr_patient_df = gr.Dataframe()
                notes_txt = gr.Textbox(label="Notes", 
                           max_lines=4, 
                           placeholder="No notes attached")
                reference_id_gal = gr.Gallery(label="Dermoscopy Images", 
                                              columns=3)
                submit_btn = gr.Button("Submit")

            # Outputs
            with gr.Column():
                attribution_img = gr.Image(label="Attribution", 
                                           interactive=False)
                output_label = gr.Label(label="Lesion Classification", 
                                        num_top_classes=3)

        # Setup event handlers
        classification_refresh_flag.change(lambda df: df.loc[:, df.columns != 'Notes'], 
                                           inputs=current_patient_data_df,
                                           outputs=curr_patient_df)
        
        classification_refresh_flag.change(lambda df: df['Notes'][0], 
                                    inputs=current_patient_data_df,
                                    outputs=notes_txt)
        
        classification_refresh_flag.change(get_reference_id_imgs,
                                           inputs=current_patient_data_df,
                                           outputs=reference_id_gal)
        
        reference_id_gal.select(update_sel_img,
                                 inputs=reference_id_gal,
                                 outputs=sel_image_path)
        
        submit_btn.click(classify,
                         inputs=sel_image_path,
                         outputs=[attribution_img, output_label])
        
        cancel_btn.click(reset, 
                         outputs=[curr_patient_df, 
                                  sel_image_path, 
                                  attribution_img, 
                                  output_label]) \
                  .then(swap_to_patient_view, 
                        outputs=[patient_col, classification_col])

def get_reference_id_imgs(df):
    """
    Gets the reference images for the given patient

    Parameters:
    df (gradio.Dataframe): The dataframe containing the patient data

    Returns:
    list: The list of reference images, as PIL.Image objects
    """
    log.info("Getting reference images for: " + str(df["Reference ID"][0]))

    # TODO, REPLACE WITH CDN ENDPOINT FOR GETTING IMAGES
    images = [Image.open("./interfaces/resources/ISIC_0034525.jpg"),
              Image.open("./interfaces/resources/ISIC_0034526.jpg"),
              Image.open("./interfaces/resources/ISIC_0034527.jpg"),
              Image.open("./interfaces/resources/ISIC_0034528.jpg"),
              Image.open("./interfaces/resources/ISIC_0034529.jpg")]

    return images

def update_sel_img(imgs, evt: gr.SelectData):
    """
    Updates the selected image

    Parameters:
    imgs (list): The list of images to select from
    evt (gr.SelectData): The event data from the gallery

    Returns:
    str: The path to the selected image
    """
    return imgs[evt.index]['name']

def classify(img_path, progress=gr.Progress()):
    """
    Classifies the given image

    Parameters:
    img_path (str): The path to the image to classify

    Returns:
    PIL.Image: The attribution image to display
    dict: The labels and their respective confidence intervals
    """

    if img_path is None:
        raise gr.Error("Please select an image to classify")
    else:
        gr.Info("Classifiying image...")
        log.info("Classifiying image...")

        labels = {entry['label']: entry['score'] for entry in progress.tqdm(pipe(img_path), 
                                                                            desc="Classifying image...")}

    return Image.open(img_path), labels

def reset():
    """
    Resets the display and all the inputs

    Returns:
    gradio.Column: The column responsible for patient data
    gradio.Column: The column responsible for classification
    gradio.Dataframe: The dataframe responsible for patient data
    gradio.Number: The flag to refresh the classification view
    """
    return gr.update(value=None), \
           gr.update(value=None), \
           gr.update(value=None), \
           gr.update(value=None)

def swap_to_patient_view():
    return gr.update(visible=True), gr.update(visible=False)