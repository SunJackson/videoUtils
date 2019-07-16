import cv2
from PIL import Image
import numpy as np

save_video_path = './video/video.avi'
process_video_path = './video/2019特效最逼真科幻片，每帧经费都在燃烧，看完才发现不是实景.mp4'


def image2handler(image):
    # a = np.asarray(Image.open(image_path).convert('L')).astype('float')
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
    print('process {}%'.format(round(i / frames, 4)))
cv2.destroyAllWindows()
video.release()
