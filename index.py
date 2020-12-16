import moviepy.editor as mpy

COLOR = {
    'white': [255, 255, 255],
    'black': [0, 0, 0],
}
WIDTH = 720
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)
BACKGROUND = COLOR['white']
FONT = 'Noto-Sans-CJK-HK'
FONT_SIZE = {
    'h1': 32,
    'h2': 24,
    'body': 20,
}
PADDING = {
    'h1': 60,
}
MARGIN = 60
FPS = 5
DURATION = {
    'title': 4,
    'step1': {
        'total': 10,
        'heading': 2,
        'description': 3,
    },
}

def title():
    return mpy.CompositeVideoClip([mpy.TextClip(
        'Identify an interval in 3 simple steps',
        font=FONT,
        fontsize=FONT_SIZE['h1'],
        color='black',
        ).set_duration(DURATION['title']).set_position('center'),
    ], size=SIZE)

def step1():
    duration = DURATION['step1']
    heading = mpy.TextClip(
        'Step 1: Count',
        font=FONT,
        fontsize=FONT_SIZE['h1'],
        color='black'
    ).set_duration(DURATION['step1']['total']).set_position(('center', MARGIN))
    description = mpy.TextClip(
        'Count the number of notes (inclusive) ignoring accidentals',
        font=FONT,
        fontsize=FONT_SIZE['body'],
        color='black',
    ) \
        .set_duration(duration['total'] - duration['heading']) \
        .set_start(duration['heading']) \
        .set_position(('center', MARGIN + PADDING['h1']))
    return mpy.CompositeVideoClip([
        heading,
        description,
    ], size=SIZE)

def background():
    duration = DURATION['title'] + DURATION['step1']['total']
    return mpy.ColorClip(size=SIZE, color=BACKGROUND).set_duration(duration)

content = mpy.concatenate_videoclips([
    title(),
    step1(),
])
with_bg = mpy.CompositeVideoClip([
    background(),
    content,
])
with_bg.write_videofile('result.mp4', fps=FPS)
