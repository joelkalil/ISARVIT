# Easy Cryptography #

keyCeaser = 10

# 65 - 90 = A - Z
# 97 - 122 = a - z
def ceaserEncrypt(data, key):
    if key > 26:
        key = key % 26
    dataEncrypt = ''
    for i in range(len(data)):
        if not data[i] == ' ':
            if data[i] >= 65 and data[i] <= 90:    
                dataEncrypt += chr(ord(data[i]) + key)
        else:
            dataEncrypt += data[i]
    data[i] >= 97 and data[i] <= 122:
    return dataEncrypt

def ceaserDecrypt(data, key):
    dataDecrypt = ''
    for i in range(len(data)):
        if not data[i] == ' ':
            dataDecrypt += chr(ord(data[i]) - key)
        else:
            dataDecrypt += data[i]

    return dataDecrypt

