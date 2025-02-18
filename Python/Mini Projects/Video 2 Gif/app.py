from moviepy import VideoFileClip

file_path = "Add you video clip"

videoClip = VideoFileClip(file_path)


videoClip.write_gif(file_path.split('.')[0] + '.gif')



print(file_path.split('.')[0] + '.gif')