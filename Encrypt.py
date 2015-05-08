import KeyHelper
import PictureHelper
import DESUnit
import random
import pickle

def encrypt():
    #prepare data
    num_person = input("Please input the number of the person to share an image:")
    keys = KeyHelper.keyGen(int(num_person))
    image_name = input("Please input the image name:")
    image_data = PictureHelper.read_picture(image_name)
    image_data = PictureHelper.format_data(image_data)

    #encryption
    key_sequence = []
    encryption_image = []
    print("processing...")
    for i in range(0, len(image_data) - 1):
        key_choice = random.randint(1, int(num_person))
        key_sequence.append(key_choice)
        des = DESUnit.DESUnit(keys[key_choice - 1], "default")
        des.compute_key()
        encryption_image.append(des.action("encrypt", image_data[i]))
    encryption_image.append(image_data[-1])

    PictureHelper.reshape(encryption_image,"en_" + image_name)

    #stored key sequence
    file = open("key_sequence.txt", "wb")
    pickle.dump(key_sequence,file)
    file.close()

if __name__ == "__main__":
    encrypt()





