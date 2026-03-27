from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def hex_to_bytes(hex_str: str):
    hex_str = hex_str.lower()
    hex_chars = "0123456789abcdef"
    byte_arr = bytearray()
    
    if len(hex_str)%2 != 0:
        hex_str = "0" + hex_str

    for i in range(0, len(hex_str), 2):
        char_high = hex_str[i]
        char_low = hex_str[i+1]

        val_high = hex_chars.find(char_high)
        val_low = hex_chars.find(char_low)

        if val_high == -1 | val_low == -1:
            raise ValueError(f"Invalid Char {char_high} or {char_low} at {i}")
        
        byte = val_high*16 + val_low
        byte_arr.append(byte)
    
    return byte_arr

def bytes_to_base64(byte_arr: bytearray):
    b64_str = ""
    b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    for i in range(0, (len(byte_arr)//3) * 3, 3):
        B1 = byte_arr[i]
        B2 = byte_arr[i+1]
        B3 = byte_arr[i+2]
    
        B_combined = (B1<<16) | (B2<<8) | (B3)

        I1 = (B_combined>>18) & 63
        I2 = (B_combined>>12) & 63
        I3 = (B_combined>>6) & 63
        I4 = (B_combined) & 63

        b64_str += b64_chars[I1]
        b64_str += b64_chars[I2]
        b64_str += b64_chars[I3]
        b64_str += b64_chars[I4]

    if (len(byte_arr)%3 == 1):
        B = byte_arr[-1] << 4
        I1 = (B>>6) & 63
        I2 = (B) & 63

        b64_str += b64_chars[I1]
        b64_str += b64_chars[I2]
        b64_str += "=="
        
    elif (len(byte_arr)%3 == 2):
        B1 = byte_arr[-2]
        B2 = byte_arr[-1]

        B_combined = ((B1<<8) | B2) << 2

        I1 = (B_combined>>12) & 63
        I2 = (B_combined>>6) & 63
        I3 = (B_combined) & 63

        b64_str += b64_chars[I1]
        b64_str += b64_chars[I2]
        b64_str += b64_chars[I3]
        b64_str += "="

    return b64_str

def bytes_to_hex(byte_arr: bytearray):
    hex_arr = []
    hex_chars = "0123456789abcdef"

    for i in range(0, len(byte_arr)):
        byte = byte_arr[i]
        val_high = byte>>4
        val_low = byte & 15

        hex_arr.append(hex_chars[val_high])
        hex_arr.append(hex_chars[val_low])

    hex_str = "".join(hex_arr)
    return hex_str

def XOR_bytes(first_byte_arr: bytearray, second_byte_arr: bytearray):
    ORed_arr = bytearray()
    for i in range(0, len(first_byte_arr)):
        ORed_arr.append(first_byte_arr[i] | second_byte_arr[i])

    NANDed_arr = bytearray()
    for i in range(0, len(first_byte_arr)):
        NANDed_arr.append((~(first_byte_arr[i] & second_byte_arr[i])) & 255)

    XORed_arr = bytearray()
    for i in range(0, len(first_byte_arr)):
        XORed_arr.append(ORed_arr[i] & NANDed_arr[i])

    return XORed_arr

def score_text(string: str):
    score = 0
    frequency_list = [ ' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'd', 'l', 'u', 
    'c', 'm', 'f', 'y', 'w', 'g', 'p', 'b', 'v', 'k', 'x', 'q', 'j', 'z']

    for char in string.lower():
        if char in frequency_list:
            score += (len(frequency_list) - frequency_list.index(char))
        else:
            score-=30

    return score

def score_text_list(key_list):
    for key, message in key_list.items():
        message_score = score_text(message[0])
        key_list[key][1] = message_score
    return key_list

def repeat_XOR(byte_arr, key):
    XORed_bytes = bytearray()
    key_len = len(key)
    
    for i in range(0, len(byte_arr)):
        XORed_bytes.append((byte_arr[i] ^ key[i%key_len]))

    return XORed_bytes

def base64_to_bytes(b64_string: str):
    b64_chars = {
    'A': 0,  'B': 1,  'C': 2,  'D': 3,  'E': 4,  'F': 5,  'G': 6,  'H': 7,
    'I': 8,  'J': 9,  'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15,
    'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23,
    'Y': 24, 'Z': 25, 'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31,
    'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36, 'l': 37, 'm': 38, 'n': 39,
    'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47,
    'w': 48, 'x': 49, 'y': 50, 'z': 51, '0': 52, '1': 53, '2': 54, '3': 55,
    '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61, '+': 62, '/': 63}
    b64_arr = bytearray()

    for i in range(0, len(b64_string)-4, 4):
        I1 = b64_chars[b64_string[i]]
        I2 = b64_chars[b64_string[i+1]]
        I3 = b64_chars[b64_string[i+2]]
        I4 = b64_chars[b64_string[i+3]]

        B_Combined = (I1<<18) | (I2<<12) | (I3<<6) | (I4)
        
        B1 = (B_Combined>>16) & 255
        B2 = (B_Combined>>8) & 255
        B3 = B_Combined & 255

        b64_arr.extend([B1, B2, B3])

    if b64_string[-2:] == "==":
        I1 = b64_chars[b64_string[-4]]
        I2 = b64_chars[b64_string[-3]]

        B_Combined = (I1<<6) | (I2)
        byte = B_Combined>>4
        b64_arr.append(byte)
    
    elif b64_string[-1] == "=":
        I1 = b64_chars[b64_string[-4]]
        I2 = b64_chars[b64_string[-3]]
        I3 = b64_chars[b64_string[-2]]

        B_Combined = ((I1<<12) | (I2<<6) | (I3)) >>2

        B1 = (B_Combined>>8) & 255
        B2 = B_Combined & 255

        b64_arr.extend([B1, B2])
    
    else:
        I1 = b64_chars[b64_string[-4]]
        I2 = b64_chars[b64_string[-3]]
        I3 = b64_chars[b64_string[-2]]
        I4 = b64_chars[b64_string[-1]]

        B_Combined = (I1<<18) | (I2<<12) | (I3<<6) | (I4)

        B1 = (B_Combined>>16) & 255
        B2 = (B_Combined>>8) & 255
        B3 = B_Combined & 255

        b64_arr.extend([B1, B2, B3])

    return b64_arr

def hamming_distance(string1:str, string2:str):
    ham_dist = 0

    diff = XOR_bytes(string1, string2)
    
    for byte in diff:
        ham_dist += byte.bit_count()

    return ham_dist

def generate_XORed_messages(byte_arr):
    key_list = {}
    for i in range(0, 256):
        decrypted_list = []

        for j in range(0, len(byte_arr)):
            XORed_byte = byte_arr[j]^i
            decrypted_list.append(chr(XORed_byte))

        decrypted_text = "".join(decrypted_list)
        key_list[i] = [decrypted_text, 0]
    return key_list

def rank_messages(key_list):
    best_message = None
    best_key = None
    best_score = float('-inf') 

    for key, message in key_list.items():
        current_key = key
        current_message = message[0]
        current_score = message[1]

        if current_score>best_score:
            best_key = current_key
            best_message = current_message
            best_score = current_score
    return best_key, best_message, best_score

def find_key_of_repeat_XOR(transposed_bytes, keysize):
    key = []
    for i in range(0, keysize):
        byte_arr = transposed_bytes[i]

        keylist = generate_XORed_messages(byte_arr)
        scored_list = score_text_list(keylist)
        ranked_message = rank_messages(scored_list)

        key.append(ranked_message[0])
    return key

def transpose_arr(arr, step: int):
    transposed_arrs = []

    for i in range(0, step):
        transposed_arr = []

        if i==0:
            iter_len = ( (len(arr) // (step)) *step )
        else:
            iter_len = ( (len(arr) // (i)) *i )

        for i_byte in range(i, iter_len, step):
            transposed_arr.append(arr[i_byte])
        
        transposed_arrs.append(transposed_arr)
    
    return transposed_arrs

def find_keysize_repeat_XOR(bytearr: bytearray, min_key_len: int, max_key_len: int):
    keysizes = {}

    for keysize in range(min_key_len, max_key_len):
        sum = 0
        num = 0 
        for byte_len in range(0, ( (len(bytearr) // (keysize*2)) *keysize ), keysize*2):
            dist = hamming_distance(
                bytearr[byte_len:(byte_len+keysize)], 
                bytearr[(byte_len+keysize):(byte_len+keysize*2)])
            sum += dist/keysize
            num += 1
        avg = sum/num
        keysizes[keysize] = avg

    return keysizes

def decrypt_AES_ECB(key: bytearray, data: bytearray):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data

def detect_AES_ECB(bytes_list: [bytearray]):
    best_score = -1
    detected_line = None

    for bytes_line in bytes_list:
        divided_chunks = []
        unique_chunks = set()
        for i in range(0, len(bytes_line), 16):
            divided_chunks.append(bytes_line[i:(i+16)])

        for chunk in divided_chunks:
            unique_chunks.add(bytes(chunk))
        
        score = len(divided_chunks) - len(unique_chunks)

        if score>best_score:
            best_score = score
            detected_line = bytes_line
    
    return best_score, detected_line

def pad_PKCS7(bytes_arr: bytearray, block_size: int):
    remaining_bytes = block_size - (len(bytes_arr) % block_size)

    for _ in range(0, remaining_bytes):
        bytes_arr.append(remaining_bytes)
   
    return bytes_arr