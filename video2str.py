import cv2
from PIL import Image, ImageFont, ImageDraw
import numpy as np

save_video_path = './video/video.avi'
process_video_path = './video/2019特效最逼真科幻片，每帧经费都在燃烧，看完才发现不是实景.mp4'

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:oa+>!:+. ")


# ascii_char = list("MNHQ$OC67+>!:-. ")
# ascii_char = list("MNHQ$OC67)oa+>!:+. ")

# 将像素转换为ascii码
def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ''
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


# 将txt转换为图片
def image2str(file_name):
    im = Image.open(file_name).convert('RGB')
    # gif拆分后的图像，需要转换，否则报错，由于gif分割后保存的是索引颜色
    raw_width = im.width
    raw_height = im.height
    width = int(raw_width / 6)
    height = int(raw_height / 15)
    im = im.resize((width, height), Image.NEAREST)

    txt = ""
    colors = []
    for i in range(height):
        for j in range(width):
            pixel = im.getpixel((j, i))
            colors.append((pixel[0], pixel[1], pixel[2]))
            if (len(pixel) == 4):
                txt += get_char(pixel[0], pixel[1], pixel[2], pixel[3])
            else:
                txt += get_char(pixel[0], pixel[1], pixel[2])
        txt += '\n'
        colors.append((255, 255, 255))

    im_txt = Image.new("RGB", (raw_width, raw_height), (255, 255, 255))
    dr = ImageDraw.Draw(im_txt)
    # font = ImageFont.truetype(os.path.join("fonts","汉仪楷体简.ttf"),18)
    font = ImageFont.load_default().font
    x = y = 0
    # 获取字体的宽高
    font_w, font_h = font.getsize(txt[1])
    font_h *= 1.37  # 调整后更佳
    # ImageDraw为每个ascii码进行上色
    for i in range(len(txt)):
        if (txt[i] == '\n'):
            x += font_h
            y = -font_w
        dr.text((y, x), txt[i], fill=colors[i])
        y += font_w

    im_txt.save('.image2str_tmp~.jpg')


videoCapture = cv2.VideoCapture()
videoCapture.open(process_video_path)

fps = int(videoCapture.get(cv2.CAP_PROP_FPS))
frames = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
frameH = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
frameW = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
# fps是帧率，意思是每一秒刷新图片的数量，frames是一整段视频中总的图片数量。
print("fps=", fps, "frames=", frames, 'size=', (frameW, frameH))

video = cv2.VideoWriter(save_video_path, 0, fps, (frameW, frameH))

for i in range(1280):
    tmp_path = '.image_tmp~.jpg'
    ret, frame = videoCapture.read()
    cv2.imwrite(tmp_path, frame)
    image2str(tmp_path)
    video.write(cv2.imread('.image2str_tmp~.jpg'))
    print('process {}%'.format(round(i / frames, 4)))
cv2.destroyAllWindows()
video.release()
