import os
import PySimpleGUI as sg
from PIL import Image, ImageTk
from tkinter import filedialog
from Utilies import Utilies
import operator

class ImageSorter:
    def __init__(self):
        self.extention= ['jpg','jpeg','raw','tiff']
        self.current_image_index = 0
        self.main_folder = ""
        self.img_dim= (500,500)
        self.image_files = []
        self.dirs =  []
        
        self.layout = [
            [sg.Image(key="-IMAGE-", size=self.img_dim), sg.Image(key="-SECONDARY_IMAGE-", size=self.img_dim)],
            [sg.Button("Load Images", enable_events=True, key="-LOAD_IMAGES-")],
            [sg.Button("Previous", enable_events=True, key="-PREV-"), sg.Button("Next", enable_events=True, key="-NEXT-")],
            [sg.Button("Add to New Folder", enable_events=True, key="-ADD-"), sg.Button("Copy to Selected Folder", enable_events=True, key="-COPY-")],
            [sg.Button("Exit")],
            [sg.Column([[sg.Listbox(values=[], key="-LISTBOX-", size=(70, 20), enable_events=True)]])],
        ]


        self.window = sg.Window("Image Viewer", self.layout, resizable=True, finalize=True)
        
        self.statup()     
  
    def statup(self):
        self.load_images()
        self.dirs=Utilies.get_dirs(path=self.main_folder,extention=self.extention)
        self.load_list_box()
        
    def load_images(self):
        global folder_path
        folder_path= filedialog.askdirectory(title="Select Folder Containing Images")
        if folder_path:
            self.main_folder = folder_path 
            self.image_files =Utilies.get_imgs(folder_path,self.extention)
            if len(self.image_files)>0:
                self.image_files.sort()
                self.show_image("-IMAGE-",self.image_files[self.current_image_index])
            else:
                sg.popup_error('No Images or wrong file types!')
        
  

    def show_image(self,key,img_path):
        img = Image.open(img_path)
        img.thumbnail(self.img_dim)
        photo = ImageTk.PhotoImage(img)
        self.window[key].update(data=photo)
    
    def navigate_main(self,action,index,img_lst,steps):
        if len(img_lst)>0:
            try:
                self.current_image_index = action(index,steps)
                img_path = img_lst[self.current_image_index]
            except IndexError:
                self.current_image_index = 0
                img_path = img_lst[self.current_image_index]
            self.show_image("-IMAGE-",img_path)
        else:
            return  

    def navigate_list_box(self,action,steps):
        cur_selection_in = self.window['-LISTBOX-'].GetIndexes()[0]
        index = action(cur_selection_in,steps) 
        try:
            selected_item= self.window[ '-LISTBOX-'].Values[index]
        except IndexError:
            index =0
            selected_item= self.window[ '-LISTBOX-'].Values[index]
        self.show_image('-SECONDARY_IMAGE-',selected_item)
        self.window['-LISTBOX-'].update(set_to_index=index)
    
    def load_list_box(self):
        dirs = Utilies.get_dirs(path=self.main_folder,extention=self.extention)
        if len(dirs)>0:
            self.window["-LISTBOX-"].update(dirs.values()) 
            self.window['-LISTBOX-'].update(set_to_index=0)
            self.show_image('-SECONDARY_IMAGE-',self.window["-LISTBOX-"].Values[0])


    def run(self):
        self.window.bind('<Right>', "-NEXT-")
        self.window.bind('<Left>', "-PREV-")
        self.window.bind('<Up>', "-PREV_LISTBOX-")
        self.window.bind('<Down>', "-NEXT_LISTBOX-")
        while True:
            event, values = self.window.read(timeout=100)
            
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event =='-LOAD_IMAGES-':
                self.load_images()
            elif event ==  "-NEXT-":
                self.navigate_main(operator.add,self.current_image_index,self.image_files,1)
            elif event == "Previous" or event == "-PREV-":
                self.navigate_main(operator.sub,self.current_image_index,self.image_files,1)
            elif event == "-NEXT_LISTBOX-":
                    self.navigate_list_box(operator.add,1)
            elif event == "-PREV_LISTBOX-":
                self.navigate_list_box(operator.sub,1)                                
            elif event == '-LISTBOX-':
                self.navigate_list_box(operator.add,0)
                
            elif event == '-COPY-':
                cur_selection_in = self.window['-LISTBOX-'].GetIndexes()[0]
                selected_item = values['-LISTBOX-'][0]
                cur_img_path =self.image_files[self.current_image_index]
                src_path = os.path.dirname(selected_item)
                Utilies.copy_file(cur_img_path,src_path)
                self.dirs = Utilies.get_dirs(path=self.main_folder,extention=self.extention)
                self.window['-LISTBOX-'].update(set_to_index=cur_selection_in)
                self.window.write_event_value('-NEXT-','')
                self.load_list_box() 

            elif event == '-ADD-':
                path = Utilies.add_new_dir(self.main_folder)
                cur_img_path =self.image_files[self.current_image_index]
                Utilies.copy_file(cur_img_path,path)
                self.dirs = Utilies.get_dirs(path=self.main_folder,extention=self.extention)
                self.window.write_event_value('-NEXT-','')
                self.load_list_box()  


        self.window.close()
    

