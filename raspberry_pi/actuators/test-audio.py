import os, pwd, subprocess 
def play_as_user(file): 
    user = pwd.getpwuid(os.getuid()).pw_name 
    # 获取当前用户名 
    # cmd = f'sudo -u xw0418 mpg123 "{file}"' # 以原用户身份播放 
    cmd = f'mpg123 "{file}"' # 以原用户身份播放`
    subprocess.run(cmd, shell=True)
    
    
f = "/home/xw0418/cse237A/SittingPostureDetection/data/audio/posture_alert.mp3"
play_as_user(f)
# user = pwd.getpwuid(os.getuid()).pw_name 
# print(user)

# sudo XDG_RUNTIME_DIR=/run/user/$(id -u) \
#     DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus \
#     PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native \
#     python test-audio.py

# sudo XDG_RUNTIME_DIR=/run/user/$(id -u) DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus PULSE_SERVER=unix:/run/user/$(id -u)/pulse/native python test-audio.py