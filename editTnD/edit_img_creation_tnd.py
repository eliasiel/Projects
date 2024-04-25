import PySimpleGUI as sg
import os
from datetime import datetime
import piexif
from datetime import datetime, timedelta

def calculate_future_date(birth_date_str, target_age):
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        
        # Convert target_age to an integer to handle both int and float inputs
        target_age = float(target_age)

        # Calculate the target date based on the given age
        target_date = birth_date + timedelta(days=target_age * 365)
        
        return target_date.strftime("%Y-%m-%d")
    except ValueError as e:
        return str(e)

def dir_name(path):
    return os.path.dirname(path)

def rename_folder(path,new_name):
    old_name = dir_name(path).split(os.sep)[-1]
    new_path = path.replace(old_name,new_name)
    os.rename(dir_name(path), dir_name(new_path))

def add_dates_to_images(folder_path, selected_date):
    try:
        for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                # Open the image using Pillow
                exif_dict = piexif.load(file_path)

                creation_time = os.path.getctime(file_path)
                creation_datetime = datetime.utcfromtimestamp(creation_time)

                # Update the datetime with the selected date
                new_datetime = datetime(
                    selected_date['-YEAR-'],
                    selected_date['-MONTH-'],
                    selected_date['-DAY-'],
                    creation_datetime.hour,
                    creation_datetime.minute,
                    creation_datetime.second
                )

                # Update EXIF data with the new datetime

                new_date = new_datetime.strftime("%Y:%m:%d %H:%M:%S")
                exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
                exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
                exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, file_path)   
       
    except Exception as e:
        sg.popup_error(f"Error: {e}")
        return False  
    return True
    
   

layout = [
    [sg.Text('Select a folder containing images:')],
    [sg.InputText(key='-FOLDER-'), sg.FolderBrowse()],
    [sg.Text('Select date:')],
    [sg.Combo(values=list(range(1, 32)), default_value=1, size=(5, 1), key='-DAY-'),
     sg.Combo(values=list(range(1, 13)), default_value=1, size=(5, 1), key='-MONTH-'),
     sg.Combo(values=list(range(1900, 2031)), default_value=datetime.now().year, size=(5, 1), key='-YEAR-')],
    [sg.Button('Add Dates'), sg.Button('Exit')],
    [sg.Text('Age Calculator:'),sg.InputText(key='-CAL_TEXT-'),sg.Button('Calculate Age',key='CAL')],
    [    [sg.Combo(values=list(range(1, 32)), default_value=1, size=(5, 1), key='-DAY_CAL-'),
     sg.Combo(values=list(range(1, 13)), default_value=1, size=(5, 1), key='-MONTH_CAL-'),
     sg.Combo(values=list(range(1900, 2031)), default_value=datetime.now().year, size=(5, 1), key='-YEAR_CAL-')],]
]

window = sg.Window('Image Date Editor', layout)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Add Dates':
        folder_path = values['-FOLDER-']
        selected_date = {'-DAY-': int(values['-DAY-']),'-MONTH-': int(values['-MONTH-']),'-YEAR-': int(values['-YEAR-'])}
        new_datetime= add_dates_to_images(folder_path, selected_date)
        if new_datetime:            
            sg.popup('Dates added successfully!', title='Success')
        else:
            sg.popup_error('Dates adding Failed!', title='Error')
    elif event == 'CAL':
        birth_date_str= str(values['-YEAR_CAL-'])+'-'+str(values['-MONTH_CAL-'])+'-'+str(values['-DAY_CAL-'])
        target_age = values['-CAL_TEXT-']
        future_date = calculate_future_date(birth_date_str, target_age)

        event= sg.PopupOKCancel(future_date)
        if event == 'OK':
            future_date =future_date.split('-')
            window['-DAY-'].update(future_date[2])
            window['-MONTH-'].update(future_date[1])
            window['-YEAR-'].update(future_date[0])
        
                
window.close()
