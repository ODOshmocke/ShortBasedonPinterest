import shutil
from pinscrape import pinscrape
from moviepy.editor import *
import time

def scrape_pinterest_image(topic):
    details = pinscrape.scraper.scrape(f'{topic}', "output", {}, 7)

    if details["isDownloaded"]:
        print(len(details))
    else:
        print("\nNothing to download !!")

def set_image_amount():
    number = 0
    folder_content = os.listdir('output')
    for i in folder_content:
        number += 1
        if number > max_amount_images:
            os.remove(f'output/{i}')

def remove_file():
    for image in os.listdir('output'):
        image_path = f'output/{image}'
        shutil.copy(image_path, 'overallstored')
        os.remove(image_path)

def text(topic, video_start_words, image_amount):

    display_text = []
    word_display_time = 1.5 / len(video_start_words.split())
    start_display_words = 0.5


    for word in video_start_words.split():


        start_display_words += word_display_time

        display_text.append(TextClip(word, fontsize=100, color='white', font="Roboto").set_start(start_display_words).set_duration(word_display_time).set_pos('center'))
        start_display_words += word_display_time

    display_text.append(TextClip(topic, fontsize=100, color='white', font="Roboto").set_start(3.8).set_duration(1).set_pos('center'))

    display_text.append(TextClip(f"in {image_amount} pictures", fontsize=100, color='white', font="Roboto").set_start(4.8).set_duration(1).set_pos('center'))


    return display_text

def image():
    start = 5
    video_amount = 0

    for image in os.listdir('output'):
        try:
            image_path = f'output/{image}'
            compose_list.append((ImageClip(image_path).resize(height=3840, width=2160).set_duration(.5).set_pos('center').set_start(start)))
            start += 0.1
            video_amount += 1
            print(video_amount)
        except: print('help')

    videoduration = start

    return videoduration, video_amount

def write_video_file(topic, video_duration):
    print(topic)
    video_name = f'Best {topic} pictures on pinterest #{topic} #pinterest.mp4'
    final_video = CompositeVideoClip(compose_list).set_duration(video_duration)
    final_video.write_videofile(f'Created videos/{video_name}', codec="h264_nvenc", bitrate="8000k")

def create_video(topic, video_start_words):
    compose_list.append(background_video)
    scrape_pinterest_image(topic)
    time.sleep(1)

    set_image_amount()
    video_duration, image_amount = image()
    [compose_list.append(x) for x in text(topic, video_start_words, image_amount)]
    print(compose_list)
    write_video_file(topic, video_duration)
    remove_file()
    compose_list.clear()



def main():
    start = time.time()
    with open('topics.txt', 'r') as r:
        topic_list = r.read().splitlines()
        print(topic_list)
    for topic in topic_list:
        create_video(topic, video_start_words)
    end = time.time()
    print(end - start)



max_amount_images = 500
background_video_path = 'bg_video/street.mp4'
background_audio = AudioFileClip("audio.mp3").subclip(18, 50)
background_video = VideoFileClip(background_video_path).set_audio(background_audio)
compose_list = []
video_start_words = "best PINTEREST pictures on the topic:"

if __name__ == '__main__':
    main()