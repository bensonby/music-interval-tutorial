import moviepy.editor as mpy
clip = mpy.TextClip("Hello World!", font="Noto-Sans-CJK-HK", fontsize=30, color="yellow")
clip.set_duration(5).write_videofile('hello-world.mp4', fps=30)
