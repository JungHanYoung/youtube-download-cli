from PyInquirer import prompt, color_print
from question_format import QUESTION_YOUTUBE_URL, YOUTUBE_URL, QUESTION_CONFIRM_DOWNLOAD, CONFIRM_DOWNLOAD
from color_print_factory import print_yt, print_warning, print_info
from pytube import YouTube
import threading, time, cursor
import re
import os
# from prompt_toolkit import 

loading = False
yt_list = []
filesize = 0
file_title = ''

def main():
    start_print()
    urls = repeat_question(YOUTUBE_URL, QUESTION_YOUTUBE_URL, is_url=True)
    yt_list = prefetch_youtube_urls(urls)
    for yt in yt_list:
        print(yt.title)
    answer = prompt(QUESTION_CONFIRM_DOWNLOAD)[CONFIRM_DOWNLOAD]
    if answer:
        cursor.hide()
        for yt in yt_list:
            try:
                stream = yt.streams.first()
                global filesize
                global file_title
                if len(stream.title) > 15:
                    file_title = stream.title[:15]
                else:
                    file_title = stream.title
                filesize = stream.filesize
                stream.download(filename=file_title)
            except:
                print_warning('다운로드 실패({})'.format(yt.title))
                continue
        cursor.show()


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


def prefetch_youtube_urls(list):
    # print('총 {}개의 영상 확인.'.format(len(list)))
    print('총 %i개의 영상 확인' % len(list))
    repeat_loading_print('YouTube 주소에 대한 영상 정보를 가져오는중.')
    yt_list = []
    for item in list:
        try:
            yt_list.append(YouTube(item, on_progress_callback=progress_function))
        except:
            continue
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
        print("{}{}{}".format(s, ("." * dot), (" " * space)), end="\r")
        time.sleep(timeout)
        increment += 1
    width = os.get_terminal_size().columns
    print(' ' * width)


def progress_function(stream, chunk, file_handle, bytes_remaining):
    iteration = filesize - bytes_remaining
    printProgressBar(iteration, filesize, prefix=file_title + '\t', length=50, fill='#')


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + ' ' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


if __name__ == '__main__':
    main()