import os
import PySimpleGUI as sg
from PIL import Image, ImageTk
import pathlib
import glob
import shutil
from tkinter import filedialog
from collections import OrderedDict

class ImageViewer:
    def __init__(self):
        self.main_image_files = []
        self.secondry_image_files = []
        self.current_image_index = 0
        self.main_folder = ""
        self.dirs =""

        # Main window layout
        self.layout = [
            [sg.Image(key="-IMAGE-", size=(400, 400)), sg.Image(key="-SECONDARY_IMAGE-", size=(400, 400))],

            [sg.Button("Previous", enable_events=True, key="-PREV-"), sg.Button("Next", enable_events=True, key="-NEXT-")],
            [sg.Button("Add to New Folder ", enable_events=True, key="-ADD-"),sg.Button("Copy to Folder ", enable_events=True, key="-COPY-")],
            [sg.Button("Exit")],
            [sg.Column([[sg.Listbox(values=[], key="-LISTBOX-", size=(70, 20), enable_events=True)]])],

        ]

        self.window = sg.Window("Image Viewer", self.layout, resizable=True, finalize=True)
        self.window.bind('<Right>', "-NEXT-")
        self.window.bind('<Left>', "-PREV-")
        self.window.bind('<Up>', "-PREV_LISTBOX-")
        self.window.bind('<Down>', "-NEXT_LISTBOX-")
        self.load_images()
        self.dirs = self.get_dirs()
        
        
        

    def load_images(self):
        global folder_path
        folder_path= filedialog.askdirectory(title="Select Folder Containing Images")
        if folder_path:
            self.main_folder = folder_path
            self.image_files =glob.glob(self.main_folder+'/*.jpg')+glob.glob(self.main_folder+'/*.png')
            self.image_files.sort()
            self.show_image("-IMAGE-")


    def show_image(self,key):
        if self.image_files:
            img_path = self.image_files[self.current_image_index]
            img = Image.open(img_path)
            img.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(img)

            self.window[key].update(data=photo)
    
    def show_sec_image(self,img_path):
            img = Image.open(img_path)
            img.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(img)

            self.window['-SECONDARY_IMAGE-'].update(data=photo)
    
    def add_new_dir(self):
        # Get a list of all folders in the base path
        folders = [folder for folder in os.listdir(self.main_folder) if os.path.isdir(os.path.join(self.main_folder, folder))]
        for i, num in enumerate(folders):
            folders[i]= int(num)


        # Find the next available number
        next_number = 1 if not folders else max(folders) + 1

        # Create a new folder with the next number
        new_folder_path = os.path.join(self.main_folder, str(next_number))
        os.makedirs(new_folder_path)
        return new_folder_path
    
    def copy_file(self,src,dest):
        shutil.move(src, dest)

    def show_next_image(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.show_image("-IMAGE-")

    def show_previous_image(self):
        if self.current_image_index > 0:
                self.current_image_index -= 1
                self.show_image("-IMAGE-")

    def get_dirs(self):
        path = pathlib.Path(self.main_folder)
        dirs = dict()
        for item in path.iterdir():
            if item.is_dir():
                path = item._str
                imgs = glob.glob(path+'/*.jpg')+glob.glob(path+'/*.png')
                if len(imgs)== 0:
                    continue
                else:
                    dirs[os.path.basename(path)]=(imgs[0])
        dirs  = OrderedDict((key, dirs[key]) for key in sorted(dirs.keys(), key=int))


        self.window["-LISTBOX-"].update(dirs.values()) 
        self.window['-LISTBOX-'].update(set_to_index=0)


    def run(self):
        while True:
            event, values = self.window.read(timeout=100)
            

            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event ==  "-NEXT-":
                self.show_next_image()
            elif event == "Previous" or event == "-PREV-":
                self.show_previous_image()
            elif event == "-NEXT_LISTBOX-":
                try:
                    cur_selection_in = self.window['-LISTBOX-'].GetIndexes()[0]
                    index = cur_selection_in+1
                    selected_item= self.window['-LISTBOX-'].Values[index]
                    self.show_sec_image(selected_item)
                    self.window['-LISTBOX-'].update(set_to_index=index)
                except IndexError:
                    continue                
            elif event == "-PREV_LISTBOX-":
                try:
                    cur_selection_in = self.window['-LISTBOX-'].GetIndexes()[0]
                    index = cur_selection_in-1 
                    selected_item= self.window[ '-LISTBOX-'].Values[index]
                    self.show_sec_image(selected_item)
                    self.window['-LISTBOX-'].update(set_to_index=index)
                except IndexError:
                    continue
            elif event == '-LISTBOX-':
                selected_item = values['-LISTBOX-'][0]
                cur_img_path =self.image_files[self.current_image_index]
                src_path = os.path.dirname(selected_item)
                self.show_sec_image(selected_item)
            elif event == '-COPY-':
                cur_selection_in = self.window['-LISTBOX-'].GetIndexes()[0]
                selected_item = values['-LISTBOX-'][0]
                cur_img_path =self.image_files[self.current_image_index]
                src_path = os.path.dirname(selected_item)
                self.copy_file(cur_img_path,src_path)
                self.show_next_image()
                self.get_dirs()
                self.window['-LISTBOX-'].update(set_to_index=cur_selection_in)

            elif event == '-ADD-':
                path = self.add_new_dir()
                cur_img_path =self.image_files[self.current_image_index]
                self.copy_file(cur_img_path,path)
                self.show_next_image()
                self.get_dirs()


        self.window.close()
    
if __name__ == "__main__":
    viewer = ImageViewer()
    viewer.run()
    
