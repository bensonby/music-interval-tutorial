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
NUM_EXAMPLES = 3
EXAMPLE_WIDTH = 140 # added padding
EXAMPLE_HEIGHT = 160 # added padding
PADDING = {
    'h1': 60,
    'h2': 30,
    'h3': 20,
    'small': 5,
}
MARGIN = 60
FPS = 10
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

def create_example(id, duration):
    image = mpy.ImageClip('score/cropped-score-page{}.png'.format(id + 1)) \
        .set_duration(duration) \
        .set_start(0) \
        .set_position((0, 'center'))
    example_text_from = mpy.TextClip(
        INTERVAL_FROM[id],
        font=FONT,
        fontsize=FONT_SIZE['h2'],
        color='black',
    ) \
        .set_duration(duration - 1) \
        .set_start(1) \
        .set_position(('right', 'bottom'))
    example_text_to = mpy.TextClip(
        INTERVAL_TO[id],
        font=FONT,
        fontsize=FONT_SIZE['h2'],
        color='black',
    ) \
    .set_duration(duration - 1) \
    .set_start(1) \
    .set_position(('right', 'top'))
    between_notes = [
        mpy.TextClip(
            note,
            font=FONT,
            fontsize=FONT_SIZE['h3'],
            color='blue',
        )
        .set_duration(duration - 2 - (len(BETWEEN_NOTES[id]) - i) * 0.2)
        .set_start(2 + (len(BETWEEN_NOTES[id]) - i) * 0.2)
        .set_position(
            (
                'right',
                int(EXAMPLE_HEIGHT / (len(BETWEEN_NOTES[id]) + 3) * (i + 1.5))
                # original it is len + 2, and i + 1
                # changed the values for layout adjustment
            )
        )
        for i, note in enumerate(reversed(BETWEEN_NOTES[id]))
    ]
    number = mpy.TextClip(
        NUMBER[id],
        font=FONT,
        fontsize=FONT_SIZE['h1'],
        color='red',
    ) \
    .set_duration(duration - 3) \
    .set_start(3) \
    .set_position((
        'center',
        'bottom',
    ))
    return mpy.CompositeVideoClip(
        [
            image,
            example_text_from,
            example_text_to,
        ] + between_notes
        + [
            number,
        ],
        size=(EXAMPLE_WIDTH, EXAMPLE_HEIGHT),
    )

def step1():
    duration = DURATION['step1']
    example_start = duration['heading'] + duration['description']
    examples_duration = NUM_EXAMPLES * duration['example']
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

    width_between_examples = int((WIDTH - MARGIN * 2 - NUM_EXAMPLES * EXAMPLE_WIDTH) / (NUM_EXAMPLES - 1))
    examples = [
        create_example(id, duration['example'] * (NUM_EXAMPLES - id))
        .set_position((
            MARGIN + id * (EXAMPLE_WIDTH + width_between_examples),
            int(HEIGHT / 2 - EXAMPLE_HEIGHT / 2)
        ))
        .set_start(example_start + id * duration['example'])
        .set_duration(examples_duration - id * duration['example'])
        for id in range(NUM_EXAMPLES)
    ]
    return mpy.CompositeVideoClip(
        [
            heading,
            description,
        ] + examples,
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
