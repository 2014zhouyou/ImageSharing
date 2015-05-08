import random
import pickle

def keyGen(num_person):
    file = open("num_person.txt", "wb")
    pickle.dump(num_person, file)
    file.close()
    #gen a key of 64 bit 0 or 1
    keys = []
    for i in range(1, int(num_person) + 1):
        key = []
        for j in range(0,64):
            key.append(random.randint(0,1))
        keys.append(key)
        file = open("key_"+ str(i) + ".txt", "wb")
        pickle.dump(key, file)
        file.close()
    return keys

def keySelect():
    decrypt_keys = []
    file = open("num_person.txt", "rb")
    num_person = pickle.load(file)
    file.close()
    print("Total people: " + str(num_person))
    #determine whether the i-th people give key to decrypt
    for i in range(1, int(num_person) + 1):
        choice = input("Please input the person " + str(i) + " choice: ")
        if choice == 'y':
            file = open("key_" + str(i) + ".txt", "rb")
            key = pickle.load(file)
            file.close()
            decrypt_keys.append(key)
        else:
            decrypt_keys.append([0] * 64)
    return decrypt_keys

if __name__ == "__main__":
    keyGen()


