import datetime
from tkinter import  filedialog
from datetime import datetime
import cv2
import subprocess
import json
from tkinter import filedialog
from tqdm import tqdm
import os 
from pathlib import Path
from Utilies import *

tk_window_ontop()


class SyncByTime:
    def __init__(self,len_src1_path,len_src2_path,sync_by):
        #!Paths!#
        self.len_src1_path = len_src1_path
        self.len_src2_path = len_src2_path
        #!Time!#
        self.src1_time = ''
        self.src2_time = ''
        self.time_gap_sec = 0
        self.time_gap_ms = 0
        self.higer_time_value =''
        self.lower_time_value =''
        #!fps!#
        self.len_src1_fps = 0
        self.len_src2_fps = 0
        #!dimensions!#
        self.len_src1_dim =0
        self.len_src2_dim =0

        self.time_gap_frames =0
        
        self.target_dim = (3840,2180)
        
        self.sync_by =sync_by 


    
    def get_video_metadata(self,video_path):
        command = ['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-print_format', 'json', video_path]
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = result.communicate()
        metadata = json.loads(output.decode('utf-8'))
        return metadata['streams'][0]['tags']['creation_time']

    def get_creation_time(self,file_path):
        if self.sync_by == 'creation_date':
            creation_timestamp= self.get_video_metadata(file_path)
            unix_c_time  = os.path.getctime(file_path)
            datetime_obj = datetime.datetime.fromtimestamp(unix_c_time)
            formatted_creation_time = datetime_obj.strftime("%H:%M:%S.%f")

        elif self.sync_by == 'file_name':
            file_name= Path(file_path).stem
            file_name = file_name.replace('_','-')
            creation_datetime =  datetime.strptime(file_name, '%Y-%m-%d-%H-%M-%S.%f')
            formatted_creation_time = creation_datetime.strftime("%H:%M:%S.%f")
        return formatted_creation_time

    def time_difference_cal(self,str_1,str_2):
    # convert time string to datetime
        print('calculting time difference'.title())
        t1 = datetime.datetime.strptime(str_1, "%H:%M:%S.%f")
        t2 = datetime.datetime.strptime(str_2, "%H:%M:%S.%f")
        # get difference
        if t2>t1:
            delta = t2 - t1
        else:
            delta = t1 - t2

        # time difference in seconds
        self.time_gap_sec = int(delta.total_seconds())
        # time difference in milliseconds
        self.time_gap_ms =delta.microseconds
        if self.src1_time > self.src2_time:
            self.higer_time_value ='src1'
            self.lower_time_value = self.src2_time
            self.time_gap_frames =int((self.len_src2_fps/1000) * self.time_gap_ms)

        

        elif self.src1_time < self.src2_time:
            self.higer_time_value = 'src2'
            self.lower_time_value = self.src1_time

            self.time_gap_frames =int((self.len_src1_fps/1000) * self.time_gap_ms)

        print(f"==>> self.time_gap_frames: {self.time_gap_frames}")
        
        if self.higer_time_value=='':
            print('Video start at the same time'.title())
        else:
            
            print(f'higher time value: {self.higer_time_value }'.title())

    
    def export_in_out(self,cap,out,in_point,out_point):
        cap.set(cv2.CAP_PROP_POS_FRAMES, in_point - 1)
        frame_num= in_point
        with tqdm(total=out_point - in_point) as pbar:
            while frame_num < out_point:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_num >= in_point:
                    

                    # Add frame number to the frame
                    frame = cv2.resize(frame,self.target_dim)
                
                    out.write(frame)
                    pbar.update(1)


                frame_num += 1
            out.release()
            cap.release()
            
    def conc_video(self,paths):
        frames = []
        for path in paths:
            cap = cv2.VideoCapture(path)
            while True:            
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frames.append(frame)
            return frames

    def sync(self):
            #!Reading Properties!#
            try:
                cap_src1 = cv2.VideoCapture(self.len_src1_path)
                cap_src2 = cv2.VideoCapture(self.len_src2_path)
                #!src1F!#
                self.len_src1_fps =cap_src1.get(cv2.CAP_PROP_FPS)
                self.len_src1_dim = int(cap_src1.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap_src1.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.len_src1_frame_num = int(cap_src1.get(cv2.CAP_PROP_FRAME_COUNT))
                #!src2F!#
                
                self.len_src2_fps =   cap_src2.get(cv2.CAP_PROP_FPS)
                self.len_src2_dim = int(cap_src2.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap_src2.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.len_src2_frame_num = int(cap_src2.get(cv2.CAP_PROP_FRAME_COUNT))

                if cap_src1.isOpened()== False:
                    print("Error camera 1 isn't connecting")
                if cap_src2.isOpened()== False:
                    print("Error camera 2 isn't connecting")

                while (cap_src1.isOpened() or cap_src2.isOpened()): # reading both src1 and src2 frame by frames
                    ret, frame_src1 = cap_src1.read()
                    ret1, frame_src2 = cap_src2.read()
                    if ret == True:

                        self.src1_time = self.get_creation_time(self.len_src1_path)
                        print(f"==>> self.src1_time: {self.src1_time}")
                        
                        self.src2_time = self.get_creation_time(self.len_src2_path)
                        print(f"==>> self.src2_time: {self.src2_time}")
                        
                        self.time_difference_cal(self.src2_time,self.src1_time) # calculte time difference
                    if self.higer_time_value == 'src1': #looks for a point where the seconds change in order to find syncing point
                        len_src1_dur = int(cap_src1.get(cv2.CAP_PROP_FRAME_COUNT))
                        len_src2_in_point =   self.time_gap_frames
                        len_src2_out_point =  len_src1_dur
                        len_src2_dur = len_src2_out_point-len_src2_in_point 
                        len_src1_in_point = 0
                        len_src1_out_point = len_src2_dur
                    elif self.higer_time_value == 'src2':
                            len_src2_dur = int(cap_src2.get(cv2.CAP_PROP_FRAME_COUNT))
                            len_src1_in_point= self.time_gap_frames
                            len_src1_out_point = len_src2_dur
                            len_src1_dur =len_src1_out_point- len_src1_in_point
                            len_src2_in_point =0
                            len_src2_out_point = len_src1_dur
                    elif self.src1_time==self.src2_time:
                        len_src2_in_point =  0
                        len_src2_out_point =  int(cap_src2.get(cv2.CAP_PROP_FRAME_COUNT))
                        len_src1_in_point = 0
                        len_src1_out_point =int(cap_src1.get(cv2.CAP_PROP_FRAME_COUNT))
                        
                                                                                
                    print('syncing procces complete, rendering'.title() )
        
                    out_path  = filedialog.askdirectory(title='Choose a Directory For Rendering Files')
                    fourcc =cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                    
                    out_src1= cv2.VideoWriter(f'{out_path}/1_src1.mp4', fourcc,30 ,self.target_dim )
                    out_src2 = cv2.VideoWriter(f'{out_path}/1_src2.mp4', fourcc,30,self.target_dim )
                
                    self.export_in_out(cap_src2,out_src2,len_src2_in_point,len_src2_out_point)
                    self.export_in_out(cap_src1,out_src1,len_src1_in_point,len_src1_out_point)
                
                cv2.destroyAllWindows()
                return True
            except Exception as e :
                return e
            
