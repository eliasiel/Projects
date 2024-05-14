import PySimpleGUI as sg
import os
from datetime import datetime
import tkinter as tk

def get_radio_val(gui_element):
    radio_elements = []
    for k,v in gui_element.AllKeysDict.items():
        if  isinstance(v, sg.Radio):
            enabled = gui_element.AllKeysDict[k].get()
            if enabled:
                radio_elements=k
    if not radio_elements:
        return None
    else:
        return radio_elements

            
def get_true_key(layout):
    for key, element in layout.items():
        if isinstance(element, sg.Radio):
            if element.get():
                return key

def get_creation_date(file_path):
    return datetime.fromtimestamp(os.path.getctime(file_path))


def tk_window_ontop():
    window = tk.Tk()
    window.wm_attributes("-topmost", 1)
    window.withdraw()  # this supress the tk window


def get_file_name(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    return filename

def disable_button(gui_el,*dependecies):
    pass