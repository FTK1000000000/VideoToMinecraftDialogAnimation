import moviepy, cv2

OUT_FILE = '.mcfunction'
TEMPORARY_FILE_PATH = 'bin/temp.jpg'
FRAME_LENGHT = 0.05
WORD = '■'


# bit_amount = (18, 32)
# bit_amount = (36, 64)
bit_amount = (72, 128)
scobread = 'da1'
title = 'ハレ晴レユカイ'
max_frame_number: int

video = moviepy.VideoFileClip('using.mp4')
duration, width, height, fps = \
    video.duration, video.size[0], video.size[1], video.fps
# print(f"duration: {duration}, width: {width}, height: {height}, fps: {fps}")



def parse_frame(number: int, height, width):
    frame = video.to_ImageClip(number * FRAME_LENGHT)
    frame.save_frame(TEMPORARY_FILE_PATH)
    image = cv2.imread(TEMPORARY_FILE_PATH)

    h_keep_ratio, w_keep_ratio = image.shape[0] / height, image.shape[1] / width
    frame = []
    h_range = 0
    for h in range(image.shape[0]):
        h_range += 1
        if h_range == h_keep_ratio:
            h_range = 0

            lines = []
            w_range = 0
            for w in range(image.shape[1]):
                w_range += 1
                if w_range == w_keep_ratio:
                    w_range = 0
                    color = image[h, w]
                    lines.append(color)
            frame.append(lines)
    file.write(generate_base_command(number) + generate_frame_text(frame, number) + '\n')

def rgb_to_hex(v: list[int]) -> str:
    return '#{:02X}{:02X}{:02X}'.format(v[2], v[1], v[0])

def generate_line_text(line_array: list[list], firset = True) -> str:
    content = ''
    text = WORD
    code = rgb_to_hex(line_array[0])
    color = '"color": "%s"' % code
    
    index = 0
    for one in line_array:
        index += 1
        if len(line_array) > index:
            if rgb_to_hex(line_array[index]) != rgb_to_hex(one):
                content += generate_line_text(line_array[index:], False)
                break
            else:
                text += WORD
    if firset:
        text += '\\n'
    content += '{"text": "%s",' % text + color + '},'
    return content

def generate_frame_text(frame_array: list[list], number: int) -> str:
    text = ''
    for line in frame_array:
        text += generate_line_text(line)
    text = text.rstrip(',')
    content = ('{' +
            '"type": "notice",' +
            '"pause": false,' +
            '"can_close_with_escape": true,' +
            '"after_action": "close",' +
            '"title": "%s — %s / %s",' % (title, number, max_frame_number) +
            '"action": {"label": "Close","action": {"type": "run_command","command": "/trigger %s.close"}},' % scobread +
            '"body": {"type": "plain_message","width": %s,"contents": [%s]}' % (1024, text) +
            '}')
    return content

def generate_base_command(number: int):
    return 'execute if score @s %s.timer matches %s run return run dialog show @s ' % (scobread, number)


file = open('bin/' + scobread + OUT_FILE, 'w', encoding='utf-8')
file.write('scoreboard players add @s %s.timer 1\n' % scobread)

keep_frame_ratio = 60 / fps
keep_range = 0
number = 0
max_frame_number = int(duration / FRAME_LENGHT)
# print(f'frame amount: {max_frame_number}')
for i in range(max_frame_number):
    number += 1
    parse_frame(number, bit_amount[0], bit_amount[1])
file.close()