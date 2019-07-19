import cv2
from PIL import Image
import numpy as np
import subprocess
import multiprocessing


output_name = 'What if You Swallowed the Most Venomous Snake Ever'.replace(' ', '_')
save_video_path = './video/{}.avi'.format(output_name)
process_video_path = '/home/sun/Videos/What if You Swallowed the Most Venomous Snake Ever.mp4'

def getWav():
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn ./music/{}.wav".format(process_video_path, output_name)
    subprocess.call(command, shell=True)


def add_zimu(ass_path):
    '''
    ffmpeg -i  output.mp4 -vf ass=1.ass video.mp4
    :return:
    '''
    command = "ffmpeg -i  {} -vf ass={} {}.mp4".format(ass_path, save_video_path, output_name)
    subprocess.call(command, shell=True)


def addmusic2video(music_path, video_path):
    '''
    ffmpeg -i .\output.mp3 -i .\output.mp4 output2.mp4
    :return:
    '''
    command = "ffmpeg -i {} -i {} {}_add_music.mp4".format(music_path, video_path, output_name)
    subprocess.call(command, shell=True)


def image2handler(image):
    a = np.asarray(image.convert('L')).astype('float')
    depth = 20.  # (0-100)
    grad = np.gradient(a)  # 取图像灰度的梯度值
    grad_x, grad_y = grad  # 分别取横纵图像梯度值
    grad_x = grad_x * depth / 100.
    grad_y = grad_y * depth / 100.
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A

    vec_el = np.pi / 2.2  # 光源的俯视角度，弧度值
    vec_az = np.pi / 4.  # 光源的方位角度，弧度值
    dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对x 轴的影响
    dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对y 轴的影响
    dz = np.sin(vec_el)  # 光源对z 轴的影响

    b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
    b = b.clip(0, 255)

    im = Image.fromarray(b.astype('uint8'))  # 重构图像
    return im


def run():
    videoCapture = cv2.VideoCapture()
    videoCapture.open(process_video_path)

    fps = int(videoCapture.get(cv2.CAP_PROP_FPS))
    frames = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    frameH = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frameW = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
    # fps是帧率，意思是每一秒刷新图片的数量，frames是一整段视频中总的图片数量。
    print("fps=", fps, "frames=", frames, 'size=', (frameW, frameH))

    video = cv2.VideoWriter(save_video_path, 0, fps, (frameW, frameH))

    for i in range(frames):
        ret, frame = videoCapture.read()
        frame_image = Image.fromarray(frame.astype('uint8')) # frame to image
        handler_image = image2handler(frame_image)
        cv2_img = cv2.cvtColor(np.asarray(handler_image), cv2.COLOR_RGB2BGR) # pil to cv2
        video.write(cv2_img)
        print('process {}%'.format(round(i / frames, 4)*100))
    cv2.destroyAllWindows()
    video.release()

import time
def worker(msg, inti):
    print ("#######start {0}########".format(inti))
    msg[inti] = time.time()
    time.sleep(1)
    print ("#######end   {0}########".format(inti))

def multiprocess_run():
    manager = multiprocessing.Manager()
    d = manager.dict()
    d['a'] = 'c'
    pool = multiprocessing.Pool(processes=3)
    for i in range(1, 10):
        pool.apply_async(func=worker, args=(d,))
    pool.close()
    pool.join()     #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print ("main end")

if __name__ == '__main__':
    # run()
    print(save_video_path)
    addmusic2video('/home/sun/Videos/audio.wav', save_video_path)
