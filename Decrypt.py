import KeyHelper
import PictureHelper
import DESUnit
import pickle

def decrypt():
    decrypt_keys = KeyHelper.keySelect()
    print(len(decrypt_keys))
    file = open("key_sequence.txt", "rb")
    key_sequence = pickle.load(file)
    file.close()

    image_name = "en_2.bmp"
    image_data = PictureHelper.read_picture(image_name)
    image_data = PictureHelper.format_data(image_data)

    decryption_image = []
    print("processing...")
    for i in range(0, len(image_data) - 1):
        key = decrypt_keys[key_sequence[i] - 1]
        #print("i = " + str(i))
        #print("key_sequece[i] = " + str(key_sequence[i]))
        des = DESUnit.DESUnit(key, "default")
        des.compute_key()
        decryption_image.append(des.action("decrypt", image_data[i]))
    decryption_image.append(image_data[-1])

    PictureHelper.reshape(decryption_image, "de_" + image_name)

if __name__ == "__main__":
    decrypt()