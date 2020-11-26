import moviepy.editor as mpy

width = 300
height = 240
background = [255, 255, 255]
font = "Noto-Sans-CJK-HK"
font_size = {
    "h1": 18,
}
title_color = "yellow"
title_duration = 2

title = mpy.TextClip(
    "Identify an interval in 3 simple steps",
    font=font,
    fontsize=font_size["h1"],
    color=title_color,
).set_duration(title_duration)

background = mpy.ColorClip(size=(width, height), color=background)
clips = [title, title]
output = mpy.concatenate_videoclips(clips)
add_bg = mpy.CompositeVideoClip([background, output])
add_bg.write_videofile("result.mp4", fps=5)
