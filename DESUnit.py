import random
#对target循环左移position位
def shift(position, target):
    result = []
    length_of_target = len(target)
    for index in range(0, length_of_target):
        result.append(target[(position + index) % length_of_target])
    return result

#根据choose_table进行置换选择
def choose(choose_table, origin_source):
    result = []
    for index in choose_table:
        result.append(origin_source[index - 1])
    return result

#对两个数据进行按位异或操作
def exclusiveByBit(source1, source2):
    result = []
    for i in range(0, len(source1)):
        if source1[i] == source2[i]:
            result.append(0)
        else:
            result.append(1)
    return result

#the main part of DES algorithm
class DESUnit:
    def __init__(self, input_key, s_box):
        #initial some data, data is correct
        self.origin_key = input_key#origin key to be length of 64, 0 or 1
        self.des_encrypt_key = []
        self.des_decrypt_key = []
        self.halve_key_tableA = [57, 49, 41, 33, 25, 17, 9,
                                 1, 58, 50, 42, 34, 26, 18,
                                 10, 2, 59, 51, 43, 35, 27,
                                 19, 11, 3, 60, 50, 44, 36]#len of 28 初始key的等分表
        self.halve_key_tableB = [63, 55, 47, 39, 31, 23, 15,
                                 7, 62, 54, 46, 38, 30, 22,
                                 14, 6, 61, 53, 45, 37, 29,
                                 21, 13, 5, 28, 20, 12, 4]#len of 28
        self.KEY_SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]#len of 16，每一轮的移位表
        self.final_key_table = [14, 17, 11, 24, 1, 5, 3, 28,
                                15, 6, 21, 10, 23, 19, 12, 4,
                                26, 8, 16, 7, 27, 20, 13, 2,
                                41, 52, 31, 37, 47, 55, 30, 40,
                                51, 45, 33, 48, 44, 49, 39, 56,
                                34, 53, 46, 42, 50, 36, 29, 32] #len of 48, key的选择表
        self.IP_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
                          60, 52, 44, 36, 28, 20, 12, 4,
                          62, 54, 46, 38, 30, 22, 14, 6,
                          64, 56, 48, 40, 32, 24, 16, 8,
                          57, 49, 41, 33, 25, 17, 9, 1,
                          59, 51, 43, 35, 27, 19, 11, 3,
                          61, 53, 45, 37, 29, 21, 13, 5,
                          63, 55, 47, 39, 31, 23, 15, 7]#数据的初始置换表len of 64
        self.ENCRYPT = 'encrypt'
        self.DECRYPT = 'decrypt'
        self.EXTEND_TABLE = [32, 1, 2, 3, 4, 5, 4, 5,
                             6, 7, 8, 9, 8, 9, 10, 11,
                             12, 13, 12, 13, 14, 15, 16, 17,
                             16, 17, 18, 19, 20, 21, 20, 21,
                             22, 23, 24, 25, 24, 25, 26, 27,
                             28, 29, 28, 29, 30, 31, 32, 1]#len of 48，数据的拓展置换表
        if s_box == 'default':
            self.COMPRESS_TABLE = [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
                                0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
                                4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
                                15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
                               [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
                                3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
                                0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
                                13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
                               [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
                                13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
                                13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
                                1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
                               [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
                                13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
                                10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
                                3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
                               [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
                                14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
                                4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
                                11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
                               [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
                                10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
                                9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
                                4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
                               [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
                                13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
                                1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
                                6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
                               [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
                                1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
                                7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
                                2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
        else:
            self.COMPRESS_TABLE = s_box
        self.DATA_REPLACEMENT_TABLE = [16, 7, 20, 21, 29, 12, 28, 17,
                                     1, 15, 23, 26, 5, 18, 31, 10,
                                     2, 8, 24, 14, 32, 27, 3, 9,
                                     19, 13, 30, 6, 22, 11, 4, 25]
        self.IP_REVERSE_TABLE = [40, 8, 48, 16, 56, 24, 64, 32,
                                  39, 7, 47, 15, 55, 23, 63, 31,
                                  38, 6, 46, 14, 54, 22, 62, 30,
                                  37, 5, 45, 13, 53, 21, 61, 29,
                                  36, 4, 44, 12, 52, 20, 60, 28,
                                  35, 3, 43, 11, 51, 19, 59, 27,
                                  34, 2, 42, 10, 50, 18, 58, 26,
                                  33, 1, 41, 9, 49, 17, 57, 25]

    #compute the key use to encrypt and decrypt
    #stored result in a two dimentional array
    def compute_key(self):
        #step one:halve the key
        key_partA = choose(self.halve_key_tableA, self.origin_key)
        key_partB = choose(self.halve_key_tableB, self.origin_key)

        for i in range(0, 16):
            #step two:shift
            key_partA = shift(self.KEY_SHIFT_TABLE[i], key_partA)
            key_partB = shift(self.KEY_SHIFT_TABLE[i], key_partB)
            combine_key_partAB = key_partA + key_partB

            #step three:select key
            final_key = choose(self.final_key_table, combine_key_partAB)
            #print("in compute key：len(final_key) = " + str(len(final_key)))

            #step four:stored and iterate
            self.des_encrypt_key.append(final_key)

        self.des_decrypt_key = list(self.des_encrypt_key)
        self.des_decrypt_key.reverse()

    def action(self, type, data):
        #check the action decide to encrypt or decrypt
        if type == self.ENCRYPT:
            key = list(self.des_encrypt_key)
        elif type == self.DECRYPT:
            key = list(self.des_decrypt_key)
        else:
            print("Action type not valid")

        #step one:first we assume the data to be a length of 64bit 0 or 1

         #step two :initial replacement
        new_data = choose(self.IP_TABLE, data)
        left_data = new_data[:32]
        right_data = new_data[32:]

        #iterate des
        for round_number in range(0, 16):
            temp_data = left_data
            left_data = list(right_data)
            #step three:extend right_data
            #right data to be a length of 48, divide into eight number of 6 bit
            right_data = choose(self.EXTEND_TABLE, right_data)
            right_data = exclusiveByBit(right_data, key[round_number])

            #step four:compress right_data
            #先把列表按照6位划分成8组
            data_group = []
            for i in range(0, 8):
                data_group.append(right_data[6*i:6*(i+1)])

            data_group_number = []
            #把8个列表的值转变成8个数字对应于压缩表的位置
            for i in range(0, 8):
                temp = ""
                for j in range(0, 6):
                    temp += str(data_group[i][j])
                temp1 = int(temp[0] + temp[-1], 2)
                temp2 = int(temp[1:-1], 2)
                data_group_number.append(temp1 * 16 + temp2)

            right_data = []
            for i in range(0, 8):
                #根据数据表压缩转换成二进制
                temp_number_string = '{0:04b}'.format(self.COMPRESS_TABLE[i][data_group_number[i]])
                for j in temp_number_string:
                    right_data.append(int(j))

            #step five:换位置换
            right_data = choose(self.DATA_REPLACEMENT_TABLE, right_data)

            #step six:交换数据
            right_data = exclusiveByBit(right_data, temp_data)

        #step seven:final process
        #transpose left and right:
        temp = left_data
        left_data = right_data
        right_data = temp
        combine_data = left_data + right_data
        encrypted_data = choose(self.IP_REVERSE_TABLE, combine_data)

        return encrypted_data
