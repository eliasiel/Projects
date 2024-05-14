import numpy as np
from moviepy.editor import VideoFileClip
import matplotlib.pyplot as plt
from Utilies import *

# Load the video clips
class SyncByAudio:
    def __init__(self,video_clip1_path,video_clip2_path):
        self.video_clip1 = VideoFileClip(video_clip1_path)
        self.video_clip2 = VideoFileClip(video_clip2_path)

# Load and process the audio from the video clips
    def process_audio(self, *video_clips):
        audios = []
        for video_clip in video_clips:
            audio = video_clip.audio.to_soundarray()
            audio = audio.mean(axis=1)  # Convert stereo to mono
            audios.append(audio)
        return tuple(audios)


    def sync(self):
        try:
            audio1,audio2 = self.process_audio(self.video_clip1,self.video_clip2)
            max_idx1 = np.argmax(audio1)
            max_idx2 = np.argmax(audio2)

            # Calculate the difference
            if max_idx1> max_idx2:
                shift_amount= max_idx1-max_idx2
                shift_amount_frames = int(abs(max_idx1 - max_idx2) * self.video_clip1.fps / self.video_clip1.audio.fps)
                shift_amount_sec = shift_amount_frames / self.video_clip1.fps
                self.video_clip1 = self.video_clip1.subclip(shift_amount_sec)
            
            elif max_idx2>max_idx1:
                shift_amount= max_idx2-max_idx1
                audio1 = np.concatenate((np.zeros(shift_amount), audio1[:-shift_amount]))
                self.video_clip1 = self.video_clip1.subclip(shift_amount / self.video_clip1.fps)

            # Write the synchronized video clips to files
            for vid_obj in vars(self).values():
                out_name = get_file_name(vid_obj.filename)
                out_name = f'{out_name}_syncd.mp4'
                vid_obj.write_videofile(out_name, codec="libx264", fps=vid_obj.fps)
            
            return True
        
        except Exception as e:
            return e




