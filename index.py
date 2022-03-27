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
    'title': 3,
}
DURATION_TOTAL = 15
FPS = 8
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

def create_description():
    '1. Count: Count the number of notes (inclusive) ignoring accidentals'
    '2. Scale: Write down the major scale of the lower note'
    '3. Compare the major scale note with the top note'

    '1 is unison | 8 is octave | Add "Compound" for more than 8'
    'Gbb is same as F | A# is same as Bb'
    '1458 is perfect | diminished -> perfect -> augmented\n'
    '2367 is major | diminished -> minor -> major -> augmented'

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
    # main(),
])
with_bg = mpy.CompositeVideoClip([
    background(),
    content,
    timer().set_position(('right', 'bottom')),
])
with_bg.write_videofile('result.mp4', fps=FPS)
