import logging
import os
import gradio as gr
import pandas as pd
import requests

log = logging.getLogger('web-api')
column_names = ["Reference ID", "Name", "Patient ID", "Samples", "Date"]

def setup(patient_col, 
          current_user, 
          patient_refresh_flag, 
          classification_col, 
          current_patient_data_df, 
          classification_refresh_flag):
    """
    Setup the patient list interface

    Parameters:
    patient_col (gradio.Column): The column to add the interface to
    current_user (gradio.State): The state to get the current user from
    patient_refresh_flag (gradio.Number): The flag to refresh the patient list
    classification_col (gradio.Column): The column to switch to when a patient is selected
    current_patient_data_df (gradio.Dataframe): The dataframe to update when a patient is selected
    classification_refresh_flag (gradio.Number): The flag to refresh the classification view
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
                col_count=(5, "fixed"),
                elem_id="tablerowfix",
                interactive=False
            )

        # Workaround for automatic stateful change (States dont have eventlistenrs)
        # Event Handlers
        patient_refresh_flag.change(get_patient_list, 
                               inputs=current_user, 
                               outputs=[patient_data_df, backup_df])
        
        patient_refresh_flag.change(update_doctor_name,
                                    inputs=current_user,
                                    outputs=doctor_name_md)

        refresh_btn.click(get_patient_list, 
                          inputs=current_user, 
                          outputs=[patient_data_df, backup_df])

        search_btn.click(search_name, 
                         inputs=[backup_df, search_txt, search_column_dropdown], 
                         outputs=patient_data_df)
        
        search_column_dropdown.select(update_placeholder_searchtxt, 
                                      outputs=search_txt)
        
        patient_data_df.select(swap_to_classification_view,
                               inputs=[patient_data_df, classification_refresh_flag],
                               outputs=[patient_col, 
                                        classification_col, 
                                        current_patient_data_df,
                                        classification_refresh_flag])


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


def get_patient_list(doctor_name):
    """
    Get patient list from server

    Parameters:
    doctor_name (str): The name of the doctor to get patient data for

    Returns:
    pd.DataFrame: The patient data (twice)
    """

    log.debug("Getting patient data for doctor: " + doctor_name)

    # Get the cdn api address from env
    address = os.getenv("CDN_API_ADDRESS")
    if address is None:
        log.warning("CDN_API_ADDRESS not specified in env, defaulting to 127.0.0.1:8086")
        address = '127.0.0.1:8086'

    if (address == 'None'):
        log.warning("Bypassing CDN API")
        data = {"Reference ID":{"0":1000,"1":1001,"2":1002,"3":1003,"4":1004,"5":1005,"6":1006,"7":1007,"8":1008,"9":1009,"10":1010,"11":1011,"12":1012,"13":1013,"14":1014,"15":1015,"16":1016,"17":1017,"18":1018},
                "Name":{"0":"John Doe","1":"Jane Doe","2":"Greg Smith","3":"Alice Smith","4":"John Johnson","5":"Jane Johnson","6":"Thomas Williams","7":"Nicole Williams","8":"John Brown","9":"Jane Brown","10":"Adam Jones","11":"Keith Jones","12":"Ian Miller","13":"Jane Miller","14":"John Davis","15":"Jane Davis","16":"John Garcia","17":"Jane Garcia","18":"John Rodriguez"},
                "Patient ID":{"0":1000,"1":1001,"2":1002,"3":1003,"4":1004,"5":1005,"6":1006,"7":1007,"8":1008,"9":1009,"10":1010,"11":1011,"12":1012,"13":1013,"14":1014,"15":1015,"16":1016,"17":1017,"18":1018},
                "Samples":{"0":1,"1":2,"2":3,"3":4,"4":5,"5":6,"6":7,"7":8,"8":9,"9":10,"10":11,"11":12,"12":13,"13":14,"14":15,"15":16,"16":17,"17":18,"18":19},
                "Date":{"0":"2021-01-01","1":"2021-01-01","2":"2021-01-01","3":"2021-01-01","4":"2021-01-01","5":"2021-01-01","6":"2021-01-01","7":"2021-01-01","8":"2021-01-01","9":"2021-01-01","10":"2021-01-01","11":"2021-01-01","12":"2021-01-01","13":"2021-01-01","14":"2021-01-01","15":"2021-01-01","16":"2021-01-01","17":"2021-01-01","18":"2021-01-01"}}
        patients_df = pd.DataFrame(data)

    else:
        # Send the cdn request
        try:
            log.debug("Sending CDN request for patient list for doctor " + str(doctor_name))
            response = requests.get('http://' + address + '/api/v1/patient-list', 
                                    params={'username': doctor_name})
        except requests.exceptions.ConnectionError:
            raise gr.Error("CDN API connection error")
        except Exception as e:
            raise gr.Error("CDN API error: " + str(e))
        
        # Extract data from response, and handle errors
        if response.status_code == 200:
            data = response.json().get('patients')  
            patients_df = pd.DataFrame(data)
            column_mapping = {
                'ref_id': 'Reference ID',
                'name': 'Name',
                'patient_id': 'Patient ID',
                'samples': 'Samples',
                'date': 'Date'
            }
            patients_df.rename(columns=column_mapping, inplace=True)

        else: # TODO Add more error handling
            raise gr.Error("CDN API response not ok: " + str(response))

    patients_df = patients_df.astype(str)
    return patients_df, patients_df

def swap_to_classification_view(df, refresh_flag, evt: gr.SelectData):
    """
    Swap to the classification view

    Parameters:
    df (pd.DataFrame): The patient list dataframe
    refresh_flag (gradio.Number): The refresh flag
    evt (gr.SelectData): The event data from the patient list

    Returns:
    gradio.Column: The patient list column
    gradio.Column: The classification column
    gradio.Dataframe: The dataframe to update
    gradio.Number: The refresh flag to update
    """

    return gr.update(visible=False), \
           gr.update(visible=True), \
           pd.DataFrame(df.iloc[[evt.index[0]]]), \
           gr.update(value=False) if refresh_flag else gr.update(value=True)