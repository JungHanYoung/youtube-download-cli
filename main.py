from PyInquirer import prompt, color_print
from question_format import QUESTION_YOUTUBE_URL, YOUTUBE_URL
from color_print_factory import print_yt, print_warning, print_info
from pytube import YouTube
import threading, time
import re
import os
# from prompt_toolkit import 

loading = False

def main():
    start_print()
    urls = repeat_question(YOUTUBE_URL, QUESTION_YOUTUBE_URL, is_url=True)
    yt_list = repeat_print(urls)
    for yt in yt_list:
        print(yt.title)
    answer = prompt({
        'type': 'confirm',
        'name': 'download',
        'message': '다운로드를 진행하시겠습니까?'
    })['download']
    if answer:
        for yt in yt_list:
            try:
                stream = yt.streams.first()
                stream.download()
            except:
                print_warning('다운로드 실패({})'.format(yt.title))
                continue



def repeat_question(key, question, exit_answer='q', possible_empty=False, **kwargs):

    is_url = kwargs.pop('is_url', False)

    answer_list = []
    question = {
        'type': question['type'],
            'name': question['name'],
            'message': question['message'] + '(`{}` for exit)'.format(exit_answer)
    }
    while True:
        answer = prompt(question)[key]
        if answer == exit_answer:
            break
        if not possible_empty and len(answer) == 0:
            print_warning('내용이 비어있을 수 없습니다.\n')
            continue
        if is_url:
            r = re.compile('https://www.youtube.com/watch\?v=[a-zA-Z0-9]*')
            if r.match(answer) is None:
                print_warning('YouTube URL을 입력하셔야합니다.\n')
                continue
        answer_list.append(answer)
    return answer_list


def repeat_print(list):
    # print('총 {}개의 영상 확인.'.format(len(list)))
    print('총 %i개의 영상 확인' % len(list))
    repeat_loading_print('YouTube 주소에 대한 영상 정보를 가져오는중.')
    yt_list = []
    for item in list:
        yt_list.append(YouTube(item))
    global loading
    loading = False
    return yt_list

def start_print():
    width = os.get_terminal_size().columns
    os.system('clear')
    print_yt('--유튜브 영상 다운로더--'.center(width))
    print()
    print_info('저작권이 붙어있는 영상에 대해서는'.center(width))
    print()
    print_info('다운로드가 불가능하다는 것! 주의하세요!'.center(width))
    print('\n')


def repeat_loading_print(s):
    global loading
    loading = True
    t = threading.Thread(target=repeat_printing, args=(s,))
    t.start()

def repeat_printing(s, timeout=1):
    global loading
    increment = 0
    while True:
        if not loading:
            break
        dot = increment % 3
        space = 3 - dot
        print("{}{}{} - {}/{}".format(s, ("." * dot), (" " * space), ), end="\r")
        time.sleep(timeout)
        increment += 1
    width = os.get_terminal_size().columns
    print(' ' * width)


if __name__ == '__main__':
    main()