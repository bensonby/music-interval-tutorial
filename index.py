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
FONT_BOX = {
    'timer': (50, 50),
    'note': (20, 30),
    'count': (14, 30),
    'accidental': (12, 20),
}
NUM_EXAMPLES = 3
EXAMPLE_WIDTH = 150 # added padding
EXAMPLE_HEIGHT = 160 # added padding
PADDING = {
    'h1': 60,
    'h2': 30,
    'h3': 20,
    'small': 5,
}
MARGIN = 60
FPS = 15
DURATION = {
    'title': 4,
    'step1': {
        'total': 23,
        'heading': 2,
        'description': 3,
        'example': 6,
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

STYLE = {
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
    'accidental_inactive': {
        'font': FONT,
        'fontsize': FONT_SIZE['h3'],
        'color': 'gray',
        'align': 'WEST',
        'method': 'caption',
        # 'size': # set accordingly
    },
    'note': {
        'font': FONT,
        'fontsize': FONT_SIZE['h2'],
        'color': 'black',
        'align': 'center',
        'method': 'caption',
        'size': FONT_BOX['note'],
    },
    'note_between': {
        'font': FONT,
        'fontsize': FONT_SIZE['h2'],
        'color': 'blue',
        'align': 'center',
        'method': 'caption',
        'size': FONT_BOX['note'],
    },
    'answer': {
        'font': FONT,
        'fontsize': FONT_SIZE['h1'],
        'color': 'red',
    },
    'answer_small': {
        'font': FONT,
        'fontsize': FONT_SIZE['h3'],
        'color': 'red',
    },
}

def flatten(l): # flatten a list
    return [x for sublist in l for x in sublist]

def empty_clip():
    return mpy.TextClip(' ', font=FONT, fontsize=1, color='white')

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
    note_from = mpy.TextClip(INTERVAL_FROM[id][0], **STYLE['note']) \
        .set_duration(duration - 1) \
        .set_start(1) \
        .set_position(('right', 'bottom'))
    note_to = mpy.TextClip(INTERVAL_TO[id][0], **STYLE['note']) \
        .set_duration(duration - 1) \
        .set_start(1) \
        .set_position(('right', 'top'))

    notes_vertical_gap = int((EXAMPLE_HEIGHT - (len(BETWEEN_NOTES[id]) + 2) * FONT_BOX['note'][1]) / (len(BETWEEN_NOTES[id]) + 1))
    between_notes = [
        mpy.TextClip(note, **STYLE['note_between'])
        .set_duration(duration - 2 - (len(BETWEEN_NOTES[id]) - i) * 0.1)
        .set_start(2 + (len(BETWEEN_NOTES[id]) - i) * 0.1)
        .set_position(
            (
                'right',
                FONT_BOX['note'][1] * (i + 1) + notes_vertical_gap * (i + 1),
            )
        )
        for i, note in enumerate(reversed(BETWEEN_NOTES[id]))
    ]
    return mpy.CompositeVideoClip(
        [
            image,
            note_from,
            note_to
        ] + between_notes,
        size=(EXAMPLE_WIDTH, EXAMPLE_HEIGHT),
    )

def create_count(id, duration):
    count = len(BETWEEN_NOTES[id])
    notes_vertical_gap = int((EXAMPLE_HEIGHT - (count + 2) * FONT_BOX['count'][1]) / (count + 1))
    count_numbers = [
        mpy.TextClip(
            str(i),
            font=FONT,
            fontsize=FONT_SIZE['h3'],
            color='red',
            align='center',
            method='caption',
            size=FONT_BOX['count'],
        )
        .set_duration(duration)
        .set_start(2 + count * 0.1 + 0.5 + 0.15 * i)
        .set_position(
            (
                'center',
                FONT_BOX['count'][1] * (count + 2 - i) + notes_vertical_gap * (count + 2 - i),
            )
        )
        for i in range(1, count + 3)
    ]
    return mpy.CompositeVideoClip(count_numbers, size=(FONT_BOX['count'][0], EXAMPLE_HEIGHT))

def create_accidentals(id, duration):
    text_from = INTERVAL_FROM[id][1:]
    text_to = INTERVAL_TO[id][1:]
    width = max(len(text_from), len(text_to)) * FONT_BOX['accidental'][0]
    size = (width, FONT_BOX['note'][1])
    if text_from:
        accidental_from = mpy.TextClip(text_from,
            **STYLE['accidental_inactive'],
            size=size,
        ) \
            .set_duration(duration - 1) \
            .set_start(1) \
            .set_position(('right', 'bottom'))
    else:
        accidental_from = None
    if text_to:
        accidental_to = mpy.TextClip(text_to,
            **STYLE['accidental_inactive'],
            size=size,
        ) \
            .set_duration(duration - 1) \
            .set_start(1) \
            .set_position(('right', 'top'))
    else:
        accidental_to = None
    return mpy.CompositeVideoClip(
        [
            accidental_from or empty_clip(),
            accidental_to or empty_clip(),
        ],
        size=(max(1, width), EXAMPLE_HEIGHT),
    )


def create_answer(id, duration):
    count = len(BETWEEN_NOTES[id])
    return mpy.TextClip(
        NUMBER[id],
        **STYLE['answer'],
    ) \
        .set_duration(duration) \
        .set_start(2 + count * 0.1 + (count + 2) * 0.15 + 1.5) \
        .set_position((
            'center',
            'bottom',
        ))

def create_compound(id, duration):
    if id in [0, 1]:
        return empty_clip()
    count = len(BETWEEN_NOTES[id])
    return mpy.TextClip(
        'Compound',
        **STYLE['answer_small']
    ) \
        .set_duration(duration) \
        .set_start(2 + count * 0.1 + (count + 2) * 0.15 + 1.5) \
        .set_position((
            'center',
            'bottom',
        ))


def main():
    duration = DURATION['step1']
    example_start = duration['heading'] + duration['description']
    examples_duration = NUM_EXAMPLES * duration['example']
    heading = mpy.TextClip(
        'Step 1: Count',
        **STYLE['heading'],
    ) \
        .set_duration(duration['total']) \
        .set_position(('center', MARGIN))
    description = mpy.TextClip(
        'Count the number of notes (inclusive) ignoring accidentals',
        **STYLE['description'],
    ) \
        .set_duration(duration['total'] - duration['heading']) \
        .set_start(duration['heading']) \
        .set_position(('center', MARGIN + PADDING['h1']))

    width_between_examples = int(
        (WIDTH - MARGIN * 2 - NUM_EXAMPLES * EXAMPLE_WIDTH) /
        (NUM_EXAMPLES - 1)
    )
    dur = lambda id: duration['example'] * (NUM_EXAMPLES - id)
    examples = [
        mpy.clips_array([
            [
                create_example(id, dur(id)),
                create_accidentals(id, dur(id)),
                create_count(id, dur(id)),
            ],
            [
                create_answer(id, dur(id)),
                empty_clip(), # dummy clip
                empty_clip(), # dummy clip
            ],
            [
                create_compound(id, dur(id)),
                empty_clip(), # dummy clip
                empty_clip(), # dummy clip
            ],
        ])
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

def timer():
    total = DURATION['title'] + DURATION['step1']['total']
    clips = [
        mpy.TextClip(
            str(i),
            font=FONT,
            fontsize=FONT_SIZE['body'],
            color='black',
            align='center',
            method='caption',
            size=FONT_BOX['timer'],
        )
        .set_duration(1)
        for i in range(total)
    ]
    return mpy.concatenate_videoclips(clips)

def background():
    duration = DURATION['title'] + DURATION['step1']['total']
    return mpy.ColorClip(size=SIZE, color=BACKGROUND).set_duration(duration)

def create_score_image():
    os.system('lilypond -o score -f png -d resolution=160 score/score.ly')
    images =  glob.glob('score/score-page*.png')
    for path in images:
        os.system('convert {} -define png:color-type=2 -trim {}'.format(path, path.replace('/score', '/cropped-score'))) # use colorspace RGB to workaround issue
        # https://github.com/Zulko/moviepy/issues/623

# create_score_image()
content = mpy.concatenate_videoclips([
    title(),
    main(),
])
with_bg = mpy.CompositeVideoClip([
    background(),
    content,
    timer().set_position(('right', 'bottom')),
])
with_bg.write_videofile('result.mp4', fps=FPS)
