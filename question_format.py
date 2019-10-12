import questions

YOUTUBE_URL = 'youtube_url'
CONFIRM_DOWNLOAD = 'download'

QUESTION_YOUTUBE_URL = {
    'type': 'input',
    'name': YOUTUBE_URL,
    'message': questions.YOUTUBE,
}

QUESTION_CONFIRM_DOWNLOAD = {
    'type': 'confirm',
    'name': CONFIRM_DOWNLOAD,
    'message': questions.DOWNLOAD
}