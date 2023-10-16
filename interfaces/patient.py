import logging
import gradio as gr
import pandas as pd

column_names = ["Name", "Reference ID", "Samples", "Date"]

def setup(patient_col, current_user, patient_refresh_flag):
    """
    Setup the patient list interface

    Parameters:
    patient_col (gradio.Column): The column to add the interface to
    """
    # Setup patient list interface
    with patient_col:
        backup_df = gr.State() # Backup dataframe for searching

        # Header
        with gr.Row(elem_id="patientheader"):
            gr.Markdown("<h1 style=\"font-size: 48px; margin-bottom:0px;\">Patients</h1>")
            doctor_name_md = gr.Markdown("<h3 style=\"text-align: right; margin-bottom:0px;\">Profile: </h3>", elem_id="doctorname")

        # Patient list with search and refresh
        with gr.Row():
            refresh_btn = gr.Button("",
                                    icon="./interfaces/resources/arrows-rotate-solid.svg",
                                    variant="primary", 
                                    elem_id="iconbutton", 
                                    scale=0)
            search_btn = gr.Button("",
                                   icon="./interfaces/resources/magnifying-glass-solid.svg",
                                   variant="primary", 
                                   elem_id="iconbutton", 
                                   scale=0)
            search_txt = gr.Textbox(placeholder="Search by Name", 
                                     show_label=False, 
                                     show_copy_button=False, 
                                     max_lines=1, 
                                     lines=1, 
                                     scale=1, 
                                     container=False, 
                                     interactive=True, 
                                     elem_id="searchbox")
            search_column_dropdown = gr.Dropdown(value=column_names[0], 
                                                 choices=column_names, 
                                                 interactive=True,
                                                 show_label=False,
                                                 container=False,
                                                 scale=0)
        with gr.Row():
            patient_data_df = gr.Dataframe(
                headers=column_names,
                datatype=["str", "number", "number", "date"],
                col_count=(4, "fixed"),
                elem_id="tablerowfix"
            )


        # Workaround for automatic stateful change (States dont have eventlistenrs)
        # Event Handlers
        patient_refresh_flag.change(get_patient_data, 
                               inputs=current_user, 
                               outputs=[patient_data_df, backup_df])
        
        
        patient_refresh_flag.change(update_doctor_name,
                                    inputs=current_user,
                                    outputs=doctor_name_md)
        

        refresh_btn.click(get_patient_data, 
                          inputs=current_user, 
                          outputs=[patient_data_df, backup_df])

        search_btn.click(search_name, 
                         inputs=[backup_df, search_txt, search_column_dropdown], 
                         outputs=patient_data_df)
        
        search_column_dropdown.select(update_placeholder_searchtxt, 
                                      outputs=search_txt)


def search_name(df, inp, col):
    """
    Search for a name in the patient list

    Parameters:
    df (pd.DataFrame): The dataframe to search
    inp (str): The string to search for
    col (str): The column to search in

    Returns:
    pd.DataFrame: The filtered dataframe
    """
    result = df[df[col].str.contains(inp)]
    if result.empty:
        gr.Warning("No results found")
        return df
    else:
        return df[df[col].str.contains(inp)]


def update_placeholder_searchtxt(evt: gr.SelectData):
    """
    Update the placeholder text for the search textbox

    Parameters:
    evt (gr.SelectData): The event data from the dropdown

    Returns:
    gradio.Textbox: The textbox to update
    """
    return gr.Textbox.update(placeholder="Search by " + evt.value)


def update_doctor_name(name):
    """
    Update doctor name in patient list

    Parameters:
    name (str): The name of the doctor to update to

    Returns:
    gradio.Markdown: The markdown element to update
    """
    return gr.Markdown.update(value="<h3 style=\"text-align: right; margin-bottom:0px;\">Profile: " + name + "</h3>")


def get_patient_data(doctor_name):
    """
    Get patient data from server

    Parameters:
    doctor_name (str): The name of the doctor to get patient data for

    Returns:
    pd.DataFrame: The patient data
    """

    # Get patients from server
    # Include some data about doctor, so we only get data for the logged in doctor
    # patients = requests.get("http://localhost:8085/patients").json()
    logging.debug("Getting patient data for doctor: " + doctor_name)

    raw_json = {"Name":{"0":"John Doe","1":"Jane Doe","2":"Greg Smith","3":"Alice Smith","4":"John Johnson","5":"Jane Johnson","6":"Thomas Williams","7":"Nicole Williams","8":"John Brown","9":"Jane Brown","10":"Adam Jones","11":"Keith Jones","12":"Ian Miller","13":"Jane Miller","14":"John Davis","15":"Jane Davis","16":"John Garcia","17":"Jane Garcia","18":"John Rodriguez"},"Reference ID":{"0":1000,"1":1001,"2":1002,"3":1003,"4":1004,"5":1005,"6":1006,"7":1007,"8":1008,"9":1009,"10":1010,"11":1011,"12":1012,"13":1013,"14":1014,"15":1015,"16":1016,"17":1017,"18":1018},"Samples":{"0":1,"1":2,"2":3,"3":4,"4":5,"5":6,"6":7,"7":8,"8":9,"9":10,"10":11,"11":12,"12":13,"13":14,"14":15,"15":16,"16":17,"17":18,"18":19},"Date":{"0":"2021-01-01","1":"2021-01-01","2":"2021-01-01","3":"2021-01-01","4":"2021-01-01","5":"2021-01-01","6":"2021-01-01","7":"2021-01-01","8":"2021-01-01","9":"2021-01-01","10":"2021-01-01","11":"2021-01-01","12":"2021-01-01","13":"2021-01-01","14":"2021-01-01","15":"2021-01-01","16":"2021-01-01","17":"2021-01-01","18":"2021-01-01"}}

    patients_df = pd.DataFrame(raw_json)
    patients_df = patients_df.astype(str)
    return patients_df, patients_df