import numpy
import matplotlib.pyplot
import cv2


KEYS = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

charset = ['.', '!', '~', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+']

orders = numpy.zeros(len(charset))

def numsofone_in_charbytes(text):
    
    offset = ord(text)
    
    with open("./ASC16", "rb") as ASC16:
        location = offset*16
        ASC16.seek(location)
        retbytes = ASC16.read(16)
    
    count = 0
    for i in range(len(retbytes)):
        
        for j in range(len(KEYS)):
            if KEYS[j] & retbytes[i]:
                count += 1
    return count

for s in range(len(charset)):
    orders[s] = numsofone_in_charbytes(charset[s])
print(orders)


s = numpy.argsort(orders)
print(s)

charsetnew = []
for i in range(len(charset)):
    charsetnew.append(charset[s[i]])
print(charsetnew)


def trim_pic(img):
    shape = numpy.shape(img)
    
    if shape[0] < 16 or shape[1] < 8:
        return None
    height = shape[0]//16
    width = shape[1]//8
    print(height)
    print(width)
    trimed_pic = img[:height*16, :width*8]
    return trimed_pic


def pool16_8(img):
    
    shape = numpy.shape(img)
    row = shape[0] // 16
    cow = shape[1] // 8
    avgpixel = numpy.zeros((row,cow), dtype=float)
    for i in range(row):
        for j in range(cow):
            
            t = 0.0
            for t1 in range(16):
                for t2 in range(8):
                   t += img[t1+i*16, t2+j*8]
            avgpixel[i, j] = t/(16*8)
    return avgpixel


def cvt2char(avgpixel, charset):
    
    chars = len(charset)
    race = 255.0/chars
    shape = numpy.shape(avgpixel)
    retcharmatrix = []
    rowchar = []
    for i in range(shape[0]):
        for j in range(shape[1]):
            
            s = avgpixel[i, j] // race
           
            rowchar.append(charset[int(s)])
        retcharmatrix.append(rowchar[:])
        rowchar.clear()
    return retcharmatrix

def rgb2gray(rgb):
    return numpy.dot(rgb[..., :3], [0.299, 0.587, 0.114])






srcimg = matplotlib.pyplot.imread("D:\Practise Python\pixel_art\jUX3yTZdns2mAiQI.jpg")

grayimg = rgb2gray(srcimg)

trimedimg = trim_pic(grayimg)

pooledimg = pool16_8(trimedimg)

charpic = cvt2char(pooledimg, charsetnew)


for r in charpic:
    for c in r:
        print(c, end='')
    print()










'''
t = []
rect_list = []
for i in range(16):
    rect_list.append([])



print(rect_list)


text = ""
# ??????text???gb2312??????
gb2312 = text.encode('gb2312')
print(gb2312)
# ???gb2312?????????????????????????????????hex_str???bytes????????????
hex_str = binascii.b2a_hex(gb2312)
print(type(hex_str))
# ??????UTF-8????????????????????????
result = str(hex_str, encoding='utf-8')

# eval()???????????????????????????????????????????????????????????????
# ????????????????????????????????????????????????
area = eval('0x'+result[:2]) - 0xA0
# ????????????????????????????????????????????????
index = eval('0x'+result[2:]) - 0xA0

offset = (94*(area-1) + (index-1)) * 32
front_rect = None

# ??????HZK16??????????????????
with open("./HZK16", "rb") as f:
    # ??????text????????????
    f.seek(offset)
    # ???????????????
    font_rect = f.read(32)


for k in range(len(font_rect) // 2):
    ?????????????????????,??????16???
    row_list = rect_list[k]
    for j in range(2):
        for i in range(8):
            asc = font_rect[k*2+j]
            flag = asc & KEYS[i]
            row_list.append(flag)

for row in rect_list:
    for i in row:
        if i:
            print('0', end=' ')
        else:
            print('.', end=' ')
    print()
'''

