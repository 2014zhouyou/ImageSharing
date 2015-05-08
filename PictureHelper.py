from PIL import Image
#read the picture into a pixel list
def read_picture(picture_name):
    im = Image.open(picture_name).convert("L")
    len_x = im.size[0]
    len_y = im.size[1]
    px = im.load()
    pixel_number = []
    for x in range(0, len_x):
        for y in range(0, len_y):
            pixel_number.append(px[x, y])

    #stored the size of picture for reshape the image
    pixel_number.append((len_x, len_y))
    return pixel_number

#format the data to be the form of list of list, where the inner list is the length of 64
# (1 to meet if the final list's length < 61)
def format_data(data):
    result = []
    length_of_data = len(data)
    count_flag = 0
    buffer = []
    #the final element is the size
    for i in range(0, length_of_data - 1):
        count_flag += 1
        if count_flag > 8:
            count_flag = 1
            result.append(buffer)
            buffer = []
        temp_string = '{0:08b}'.format(data[i])
        for item in temp_string:
            buffer.append(int(item))
    result.append(buffer)
    #print(len(result[-1]))
    #handle the final one if it is not length 64
    if len(result[-1]) < 64:
        result[-1] += [1] * (64 - len(result[-1]))

    #now we stored the real length of the picture data into the final item of result
    result.append(data[-1])
    return result

#reshape an image
def reshape(result, image_name):
    pixel_data = get_pixel_data(result)
    size_x, size_y = result[-1]
    im = Image.new("L", (size_x, size_y))
    px = im.load()
    count = 0
    for x in range(0, size_x):
        for y in range(0, size_y):
            px[x, y] = pixel_data[count]
            count += 1
    im.save(image_name)

#get the origin pixel data
def get_pixel_data(data):
    len_x , len_y = data[-1]
    result = []
    for i in range(0, len(data) - 1):
        result.extend(turn_to_pixel_number(data[i]))

    result = result[:len_x * len_y]
    return result

#form a list of length 64 to 8 number
def turn_to_pixel_number(data):
    result = []
    count = 0
    temp = ""
    for i in range(0, len(data)):
        count += 1
        temp += str(data[i])
        if count % 8 == 0:
            result.append(int(temp, 2))
            count = 0
            temp = ""
    return result





