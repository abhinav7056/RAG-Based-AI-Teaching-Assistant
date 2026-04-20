import os
import subprocess
files = os.listdir("videos")
for file in files:
    lec_number, name = file.split("_", 1)
    file_name = os.path.splitext(name)[0]
    print(lec_number,file_name)
    subprocess.run(["ffmpeg", "-i", f"videos/{file}", f"audios/{lec_number}_{file_name}.mp3"])