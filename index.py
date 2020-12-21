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
    'small': 15,
}
FONT_BOX = {
    'timer': (50, 50),
    'note': (20, 30),
    'scale_note': (40, 30),
    'count': (20, 30),
    'accidental': (12, 20),
}
NUM_EXAMPLES = 3
EXAMPLE_WIDTH = 150 # added padding
EXAMPLE_WIDTH_FULL = EXAMPLE_WIDTH + FONT_BOX['count'][0] + FONT_BOX['scale_note'][0] + FONT_BOX['accidental'][0] * 2  # including outside clips`
EXAMPLE_HEIGHT = 160 # added padding
PADDING = {
    'h1': 45,
    'h2': 30,
    'h3': 20,
    'small': 5,
}
MARGIN = 20
FPS = 8
WIDTH_BETWEEN_EXAMPLES = int(
    (WIDTH - MARGIN * 2 - NUM_EXAMPLES * EXAMPLE_WIDTH_FULL) /
    (NUM_EXAMPLES - 1)
)
DURATION = {
    'title': 4,
    'step1': {
        'total': 25,
        'heading': 2,
        'description': 3,
        'example': 6,
    },
    'step2': {
        'total': 15,
        'heading': 2,
        'description': 3,
        'example': 4,
    },
    'step3': {
        'total': 15,
        'heading': 2,
        'description': 3,
    },
}
DURATION_TOTAL = DURATION['title'] + DURATION['step1']['total'] \
    + DURATION['step2']['total'] + DURATION['step3']['total']
DURATION_CONTENT = DURATION_TOTAL - DURATION['title']
# EXAMPLES
INTERVAL_FROM = ['D', 'Gbb', 'A#']
INTERVAL_TO = ['F', 'Db', 'G']
ACCIDENTAL_LENGTH = [0, 2, 1]
BETWEEN_NOTES = [
    ['E'],
    ['A', 'B', 'C'],
    ['B', 'C', 'D', 'E', 'F'],
]
NUMBER = ['3rd', '5th', '7th']
SCALE_NOTES = [
    ['D', 'E', 'F#'],
    ['F', 'G', 'A', 'Bb', 'C'],
    ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
]

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

def create_example(id):
    image = mpy.ImageClip('score/cropped-score-page{}.png'.format(id + 1)) \
        .set_start(0) \
        .set_position((0, 'center'))
    note_from = mpy.TextClip(INTERVAL_FROM[id][0], **STYLE['note']) \
        .set_start(1) \
        .set_position(('right', 'bottom'))
    note_to = mpy.TextClip(INTERVAL_TO[id][0], **STYLE['note']) \
        .set_start(1) \
        .set_position(('right', 'top'))

    notes_vertical_gap = int((EXAMPLE_HEIGHT - (len(BETWEEN_NOTES[id]) + 2) * FONT_BOX['note'][1]) / (len(BETWEEN_NOTES[id]) + 1))
    between_notes = [
        mpy.TextClip(note, **STYLE['note_between'])
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

def create_count(id):
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

def create_accidentals(id):
    text_from = INTERVAL_FROM[id][1:]
    text_to = INTERVAL_TO[id][1:]
    width = ACCIDENTAL_LENGTH[id] * FONT_BOX['accidental'][0]
    size = (width, FONT_BOX['note'][1])
    if text_from:
        accidental_from = mpy.TextClip(text_from,
            **STYLE['accidental_inactive'],
            size=size,
        ) \
            .set_start(1) \
            .set_position(('right', 'bottom'))
    else:
        accidental_from = None
    if text_to:
        accidental_to = mpy.TextClip(text_to,
            **STYLE['accidental_inactive'],
            size=size,
        ) \
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

def create_scale(id):
    count = len(SCALE_NOTES[id])
    # start_offset = example_start + id * duration['step1']['example']
    notes_vertical_gap = int((EXAMPLE_HEIGHT - count * FONT_BOX['scale_note'][1]) / (count - 1))
    scales = [
        mpy.TextClip(
            SCALE_NOTES[id][i],
            font=FONT,
            fontsize=FONT_SIZE['h3'],
            color='green',
            align='center',
            method='caption',
            size=FONT_BOX['scale_note'],
        )
        .set_start(0.5 + 0.15 * i)
        .set_position(
            (
                'center',
                FONT_BOX['note'][1] * (count - i - 1) + notes_vertical_gap * (count - i - 1),
            )
        )
        for i, note in enumerate(SCALE_NOTES[id])
    ]
    return mpy.CompositeVideoClip(
        scales,
        size=(FONT_BOX['note'][0], EXAMPLE_HEIGHT)
    ) \
        .set_end(DURATION_CONTENT) \

def create_answer(id):
    count = len(BETWEEN_NOTES[id])
    return mpy.TextClip(
        NUMBER[id],
        **STYLE['answer'],
    ) \
        .set_start(2 + count * 0.1 + (count + 2) * 0.15 + 1.5) \
        .set_position((
            'center',
            'bottom',
        ))

def create_compound(id):
    if id in [0, 1]:
        return empty_clip()
    count = len(BETWEEN_NOTES[id])
    return mpy.TextClip(
        'Compound',
        **STYLE['answer_small']
    ) \
        .set_start(2 + count * 0.1 + (count + 2) * 0.15 + 1.5) \
        .set_position((
            'center',
            'bottom',
        ))


def create_heading():
    heading1 = mpy.TextClip(
        'Step 1: Count',
        **STYLE['heading'],
    ) \
        .set_duration(DURATION['step1']['total'])
    heading2 = mpy.TextClip(
        'Step 2: Major Scale',
        **STYLE['heading'],
    ) \
        .set_duration(DURATION['step2']['total'])
    heading3 = mpy.TextClip(
        'Step 3: Compare',
        **STYLE['heading'],
    ) \
        .set_duration(DURATION['step3']['total'])
    return mpy.concatenate_videoclips([
        heading1,
        heading2,
        heading3,
    ])

def create_description():
    empty1 = empty_clip().set_duration(DURATION['step1']['heading'])
    empty2 = empty_clip().set_duration(DURATION['step2']['heading'])
    empty3 = empty_clip().set_duration(DURATION['step3']['heading'])
    description1 = mpy.TextClip(
        'Count the number of notes (inclusive) ignoring accidentals',
        **STYLE['description'],
    ) \
        .set_duration(DURATION['step1']['total'] - DURATION['step1']['heading'])
    description2 = mpy.TextClip(
        'Write down the major scale of the lower note',
        **STYLE['description'],
    ) \
        .set_duration(DURATION['step2']['total'] - DURATION['step2']['heading'])
    description3 = mpy.TextClip(
        'Compare the major scale note with the top note',
        **STYLE['description'],
    ) \
        .set_duration(DURATION['step3']['total'] - DURATION['step3']['heading'])
    return mpy.concatenate_videoclips([
        empty1,
        description1,
        empty2,
        description2,
        empty3,
        description3,
    ])

def create_remarks():
    empty1 = empty_clip().set_duration(DURATION['step1']['heading'])
    empty2 = empty_clip().set_duration(DURATION['step2']['heading'])
    empty3 = empty_clip().set_duration(DURATION['step3']['heading'])
    remarks1 = mpy.TextClip(
        '1 is unison | 8 is octave | Add "Compound" for more than 8',
        **STYLE['remarks'],
    ) \
        .set_duration(DURATION['step1']['total'] - DURATION['step1']['heading'])
    remarks2 = mpy.TextClip(
        'Gbb is same as F | A# is same as Bb',
        **STYLE['remarks'],
    ) \
        .set_duration(DURATION['step2']['total'] - DURATION['step2']['heading'])
    remarks3 = mpy.TextClip(
        '1458 is perfect | diminished -> perfect -> augmented\n' +
        '2367 is major | diminished -> minor -> major -> augmented',
        **STYLE['remarks'],
    ) \
        .set_duration(DURATION['step3']['total'] - DURATION['step3']['heading'])
    return mpy.concatenate_videoclips([
        empty1,
        remarks1,
        empty2,
        remarks2,
        empty3,
        remarks3,
    ])

def main():
    duration = DURATION['step1']
    example_start = duration['heading'] + duration['description']
    examples_duration = NUM_EXAMPLES * duration['example']
    examples = [
        mpy.clips_array([
            [
                create_example(id),
                create_accidentals(id),
                create_count(id),
            ],
            [
                create_answer(id),
                empty_clip(), # dummy clip
                empty_clip(), # dummy clip
            ],
            [
                create_compound(id),
                empty_clip(), # dummy clip
                empty_clip(), # dummy clip
            ],
        ])
        .set_position((
            MARGIN + id * (EXAMPLE_WIDTH_FULL + WIDTH_BETWEEN_EXAMPLES),
            int(HEIGHT / 2 - EXAMPLE_HEIGHT / 2)
        ))
        .set_start(example_start + id * duration['example'])
        .set_end(DURATION_CONTENT)
        for id in range(NUM_EXAMPLES)
    ]
    return mpy.CompositeVideoClip(
        [
            create_heading().set_position(('center', MARGIN)),
            create_description().set_position(('center', MARGIN + PADDING['h1'])),
            create_remarks().set_position(('center', MARGIN + PADDING['h1'] + PADDING['h3'])),
        ] + examples
        + [
            create_scale(id)
                .set_start(DURATION['step1']['total'] + id * DURATION['step2']['example'])
                .set_end(DURATION_CONTENT)
                .set_position((
                    MARGIN
                        + id * EXAMPLE_WIDTH_FULL
                        + EXAMPLE_WIDTH
                        + FONT_BOX['count'][0]
                        + ACCIDENTAL_LENGTH[id] * FONT_BOX['accidental'][0]
                        + id * WIDTH_BETWEEN_EXAMPLES,
                    int(HEIGHT / 2 - EXAMPLE_HEIGHT / 2)
                ))
            for id in range(NUM_EXAMPLES)
        ],
        size=SIZE,
    )

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
