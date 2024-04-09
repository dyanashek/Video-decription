import random
import cv2

from gradio_client import Client


client = Client("https://tonyassi-image-story-teller.hf.space/--replicas/liw84/", ssl_verify=False)


def save_random_frame(video_path, output_path):
    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    random_frame_number = random.randint(0, total_frames - 1)

    cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame_number)

    ret, frame = cap.read()

    if ret:
        cv2.imwrite(output_path, frame)

    cap.release()


def describe_image(image_path):
    try:
        result = client.predict(
            image_path,	
            api_name="/predict"
        )
    except:
        result = 'Не удалось описать изображение'

    return result