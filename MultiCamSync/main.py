import PySimpleGUI as sg
from Sync_by_time import SyncByTime
from sync_by_audio import SyncByAudio
from Utilies import *

sg.theme('DarkGrey2')
layout = [
    [sg.Text('VIDEO_1'), sg.InputText(key='VIDEO_1'), sg.FileBrowse()],
    [sg.Text('VIDEO_2'), sg.InputText(key='VIDEO_2'), sg.FileBrowse()],
    [sg.Radio('Sync by Creation Date', 'RADIO1', default=True,key='creation_date'), sg.Radio('Sync by Audio', "RADIO1", key='audio')],
     [sg.Button('Sync', key='SYNC',disabled=False)]
]

window = sg.Window('Video Syning Tool', layout)


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    sync_method = get_radio_val(window)
    path_video_1,path_video_2 = values['VIDEO_1'],values['VIDEO_2']
    sync_method = get_radio_val(window)            
    if event =='SYNC'and  path_video_1 and path_video_2 and  sync_method :

        if sync_method == 'creation_date':        
            time_sync= SyncByTime(path_video_1,path_video_2,sync_method)
            success =time_sync.sync()

        elif sync_method == 'audio':
            audio_sync = SyncByAudio(path_video_1,path_video_2)
            res =audio_sync.sync()

        if success:
            sg.popup_auto_close('Done!', auto_close_duration=3)
        else:
            sg.popup_error(success)
    else:
        sg.popup_error('video paths or sync method is not selected'.title())

window.close()
