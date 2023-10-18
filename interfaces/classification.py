import gradio as gr
import logging
import interfaces as interfaces
from PIL import Image

def setup(classification_col, patient_col, current_patient_data_df, classification_refresh_flag):
    """
    Setup the account creation interface

    Parameters:
    classification_col (gradio.Column): The column to add the interface to
    """
    with classification_col:
        logging.debug("Setting up classification interface")

        sel_image_path = gr.State()
        cancel_btn = gr.Button("X", elem_id="canelbutton", variant="secondary", size="sm", interactive=True)

        with gr.Row():
            gr.Markdown("<h1 style=\"font-size: 48px;\">Cancer Classification</h1>")
        with gr.Row():
            with gr.Column():
                curr_patient_df = gr.Dataframe(max_rows=1)
                notes_txt = gr.Textbox(label="Notes", 
                           max_lines=3, 
                           placeholder="No notes attached")
                reference_id_gal = gr.Gallery(label="Dermoscopy Images", 
                                              columns=3)
                submit_btn = gr.Button("Submit")

            with gr.Column():
                attribution_img = gr.Image(label="Attribution", interactive=False)
                output_label = gr.Label(label="Lesion Classification", num_top_classes=3)

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
        
        cancel_btn.click(reset, outputs=[curr_patient_df, sel_image_path, attribution_img, output_label]) \
                  .then(swap_to_patient_view, outputs=[patient_col, classification_col])
        

def get_reference_id_imgs(df):

    logging.info("Getting reference images for" + str(df["Reference ID"]))

    # TODO, REPLACE WITH CDN ENDPOINT FOR GETTING IMAGES
    images = [Image.open("./interfaces/resources/ISIC_0034525.jpg"),
              Image.open("./interfaces/resources/ISIC_0034526.jpg"),
              Image.open("./interfaces/resources/ISIC_0034527.jpg"),
              Image.open("./interfaces/resources/ISIC_0034528.jpg"),
              Image.open("./interfaces/resources/ISIC_0034529.jpg")]

    return images

def update_sel_img(imgs, evt: gr.SelectData):
    return imgs[evt.index]['name']

def classify(img_path):
    logging.info("Classifying image")

    if img_path is None:
        raise gr.Error("Please select an image to classify")
    else:
        gr.Info("Classifiying image...")

    # TODO, REPLACE WITH CLASSIFICATION, only show top 3
    labels = {
        'Melanocytic nevi': 0.85,
        'dermatofibroma': 0.27,
        'Benign keratosis-like lesions': 0.12,
        'Basal cell carcinoma': 0.03,
        'Actinic keratoses': 0.002,
        'Vascular lesions': 0.001,
        'Dermatofibroma': 0.0001
    }

    return Image.open(img_path), labels

def reset():
    return gr.update(value=None), gr.update(value=None), gr.update(value=None), gr.update(value=None)

def swap_to_patient_view():
    return gr.update(visible=True), gr.update(visible=False)