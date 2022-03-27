import os
import glob
import moviepy.editor as mpy

COLOR = {
    'white': [255, 255, 255],
    'black': [0, 0, 0],
    'red': [255, 0, 0],
}
WIDTH = 1080
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
BACKGROUND = COLOR['white']
FONT = 'Noto-Sans-CJK-HK'
FONT_SIZE = {
    'h1': 32,
    'h2': 24,
    'h3': 18,
    'body': 20,
    'small': 15,
}
FONT_BOX = {
    'timer': (50, 50),
    'note': (20, 30),
    'scale_note': (40, 30),
    'count': (20, 30),
    'accidental': (12, 20),
}
MARGIN = 20
DURATION = {
    'title': 2,
}
DURATION_TOTAL = 5
FPS = 2
STYLE = {
    'empty': {
        'font': FONT,
        'fontsize': 1,
        'color': 'white',
    },
    'heading': {
        'font': FONT,
        'fontsize': FONT_SIZE['h1'],
        'color': 'black'
    },
    'description': {
        'font': FONT,
        'fontsize': FONT_SIZE['body'],
        'color': 'black',
    },
    'remarks': {
        'font': FONT,
        'fontsize': FONT_SIZE['small'],
        'color': 'gray',
    },
}

def flatten(l): # flatten a list
    return [x for sublist in l for x in sublist]

def empty_clip():
    return mpy.TextClip(' ', **STYLE['empty'])

def empty_clip_with_size(size):
    return mpy.TextClip(' ',
        **STYLE['empty'],
        method='caption',
        size=size,
    )

def title():
    return mpy.CompositeVideoClip([mpy.TextClip(
        'Identify an interval in 3 simple steps',
        font=FONT,
        fontsize=FONT_SIZE['h1'],
        color='black',
        ).set_duration(DURATION['title']).set_position('center'),
    ], size=SIZE)

def text_heading(text, index):
    return mpy.TextClip(
        text,
        method='caption',
        size=(800, 70),
        align='West',
        font=FONT,
        fontsize=FONT_SIZE['h1'],
        color='black',
    ).set_duration(DURATION_TOTAL).set_position((0, index * 130))

def text_description(text, index):
    if index == 2:
        y = index * 130 + 60
    else:
        y = index * 130 + 40
    return mpy.TextClip(
        text,
        method='caption',
        size=(800, 70),
        align='West',
        font=FONT,
        fontsize=FONT_SIZE['body'],
        color='black',
    ).set_duration(DURATION_TOTAL).set_position((15, y))

def text_remark(text, index):
    if index == 3:
        y = 2 * 130 + 110
    else:
        y = index * 130 + 80
    if index >= 2:
        y = y + 40

    return mpy.TextClip(
        text,
        method='caption',
        size=(800, 50),
        align='West',
        font=FONT,
        fontsize=FONT_SIZE['small'],
        color='black',
    ).set_duration(DURATION_TOTAL).set_position((15, y))

def description():
    headings = [
        'Step 1. Count',
        'Step 2. Scale',
        'Step 3. Compare',
    ]
    descriptions = [
        'Count the number of notes (inclusive) ignoring accidentals [denoted as n]',
        'Find the n-th note in the major scale of the lower note',
        'Compare this n-th note with the upper note. Same note means PERFECT/MAJOR. Adjust by semi-tone difference:',
    ]

    remarks = [
        '1 is unison // 8 is octave // Add "Compound" for more than an octave',
        'Enharmonic spelling does not matter, i.e. treat E# as F',
        'n=1/4/5/8:    diminished   <-   PERFECT   ->   augmented',
        'n=2/3/6/7:    diminished   <-   minor   <-   MAJOR   ->   augmented',
    ]
    headings_clips = [text_heading(h, index) for (index, h) in enumerate(headings)]
    descriptions_clips = [text_description(d, index) for (index, d) in enumerate(descriptions)]
    remarks_clips = [text_remark(d, index) for (index, d) in enumerate(remarks)]
    return mpy.CompositeVideoClip([
        headings_clips[0],
        descriptions_clips[0],
        remarks_clips[0],
        headings_clips[1],
        descriptions_clips[1],
        remarks_clips[1],
        headings_clips[2],
        descriptions_clips[2],
        remarks_clips[2],
        remarks_clips[3],
    ], size=SIZE)
        # ).set_duration(DURATION['title']) # .set_position('center')

def timer():
    clips = [
        mpy.TextClip(
            '{}:{:02d} '.format(str(int(i / 60)), i % 60),
            font=FONT,
            fontsize=FONT_SIZE['body'],
            color='black',
            align='EAST',
            method='caption',
            size=FONT_BOX['timer'],
        )
        .set_duration(1)
        for i in range(DURATION_TOTAL)
    ]
    return mpy.concatenate_videoclips(clips)

def background():
    return mpy.ColorClip(size=SIZE, color=BACKGROUND).set_duration(DURATION_TOTAL)

def create_score_image():
    os.system('lilypond -o score -f png -d resolution=160 score/score.ly')
    images =  glob.glob('score/score-page*.png')
    for path in images:
        os.system('convert {} -define png:color-type=2 -trim {}'.format(path, path.replace('/score', '/cropped-score'))) # use colorspace RGB to workaround issue
        # https://github.com/Zulko/moviepy/issues/623

def main():
    pass

content = mpy.concatenate_videoclips([
    title(),
    mpy.CompositeVideoClip([
        description().set_position((40, 220)),
    ], size=SIZE),
])
with_bg = mpy.CompositeVideoClip([
    background(),
    content,
    timer().set_position(('right', 'top')),
])
with_bg.write_videofile('result.mp4', fps=FPS)
