import os
import glob
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
    'h3': 18,
    'body': 20,
}
EXAMPLE_IMAGE_WIDTH = 114
EXAMPLE_IMAGE_HEIGHT = 120 # added padding
PADDING = {
    'h1': 60,
    'h2': 30,
    'h3': 20,
    'small': 5,
}
MARGIN = 60
FPS = 5
DURATION = {
    'title': 4,
    'step1': {
        'total': 20,
        'heading': 2,
        'description': 3,
        'example': 5,
    },
}
# EXAMPLES
INTERVAL_FROM = ['D', 'Gbb', 'A#']
INTERVAL_TO = ['F', 'Db', 'G']
BETWEEN_NOTES = [
    ['E'],
    ['A', 'B', 'C'],
    ['B', 'C', 'D', 'E', 'F'],
]
NUMBER = ['3rd', '5th', '7th']

def flatten(l): # flatten a list
    return [x for sublist in l for x in sublist]

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
    examples_duration = duration['total'] - duration['heading'] - duration['description']
    examples_start = duration['heading'] + duration['description']
    heading = mpy.TextClip(
        'Step 1: Count',
        font=FONT,
        fontsize=FONT_SIZE['h1'],
        color='black'
    ).set_duration(duration['total']).set_position(('center', MARGIN))
    description = mpy.TextClip(
        'Count the number of notes (inclusive) ignoring accidentals',
        font=FONT,
        fontsize=FONT_SIZE['body'],
        color='black',
    ) \
        .set_duration(duration['total'] - duration['heading']) \
        .set_start(duration['heading']) \
        .set_position(('center', MARGIN + PADDING['h1']))
    example_images = [
        mpy.ImageClip('score/cropped-score-page{}.png'.format(id + 1))
        .set_duration(examples_duration - id * duration['example'])
        .set_start(examples_start + id * duration['example'])
        .set_position((int(WIDTH / 3 * id) + PADDING['h2'], 'center'))
        for id in [0, 1, 2]
    ]
    example_text_from = [
        mpy.TextClip(
            INTERVAL_FROM[id],
            font=FONT,
            fontsize=FONT_SIZE['h2'],
            color='black',
        )
        .set_duration(examples_duration - id * duration['example'] - 1)
        .set_start(examples_start + id * duration['example'] + 1)
        .set_position((
            int(WIDTH / 3 * id) + EXAMPLE_IMAGE_WIDTH + PADDING['h2'],
            int(HEIGHT / 2 + EXAMPLE_IMAGE_HEIGHT / 2) - PADDING['h3']
        ))
        for id in [0, 1, 2]
    ]
    example_text_to = [
        mpy.TextClip(
            INTERVAL_TO[id],
            font=FONT,
            fontsize=FONT_SIZE['h2'],
            color='black',
        )
        .set_duration(examples_duration - id * duration['example'] - 1)
        .set_start(examples_start + id * duration['example'] + 1)
        .set_position((
            int(WIDTH / 3 * id) + EXAMPLE_IMAGE_WIDTH + PADDING['h2'],
            int(HEIGHT / 2 - EXAMPLE_IMAGE_HEIGHT / 2) - PADDING['h3']
        ))
        for id in [0, 1, 2]
    ]
    between_notes = [[
            mpy.TextClip(
                note,
                font=FONT,
                fontsize=FONT_SIZE['h3'],
                color='blue',
            )
            .set_duration(examples_duration - id * duration['example'] - 2
                - (len(BETWEEN_NOTES[id]) - i) * 0.2)
            .set_start(examples_start + id * duration['example'] + 2
                + (len(BETWEEN_NOTES[id]) - i) * 0.2)
            .set_position((
                int(WIDTH / 3 * id) + EXAMPLE_IMAGE_WIDTH + PADDING['h2'] + PADDING['small'],
                int(HEIGHT / 2 - EXAMPLE_IMAGE_HEIGHT / 2) - PADDING['h3']
                + int(EXAMPLE_IMAGE_HEIGHT * (i + 1) / (len(BETWEEN_NOTES[id]) + 1))
                + PADDING['small']
            ))
            for i, note in enumerate(reversed(BETWEEN_NOTES[id]))
        ]
        for id in [0, 1, 2]
    ]
    numbers = [
        mpy.TextClip(
            NUMBER[id],
            font=FONT,
            fontsize=FONT_SIZE['h1'],
            color='red',
        )
        .set_duration(examples_duration - id * duration['example'] - 3)
        .set_start(examples_start + id * duration['example'] + 3)
        .set_position((
            int(WIDTH / 3 * id + EXAMPLE_IMAGE_WIDTH / 2 ),
            int(HEIGHT / 2 + EXAMPLE_IMAGE_HEIGHT / 2) + PADDING['h1'],
        ))
        for id in [0, 1, 2]
    ]
    return mpy.CompositeVideoClip(
        [
            heading,
            description,
        ] + example_images
        + example_text_from
        + example_text_to
        + flatten(between_notes)
        + numbers,
        size=SIZE,
    )

def background():
    duration = DURATION['title'] + DURATION['step1']['total']
    return mpy.ColorClip(size=SIZE, color=BACKGROUND).set_duration(duration)

def create_score_image():
    os.system('lilypond -o score -f png -d resolution=160 score/score.ly')
    images =  glob.glob('score/score-page*.png')
    for path in images:
        os.system('convert {} -define png:color-type=2 -trim {}'.format(path, path.replace('/score', '/cropped-score'))) # use colorspace RGB to workaround issue
        # https://github.com/Zulko/moviepy/issues/623

create_score_image()
content = mpy.concatenate_videoclips([
    title(),
    step1(),
])
with_bg = mpy.CompositeVideoClip([
    background(),
    content,
])
with_bg.write_videofile('result.mp4', fps=FPS)
