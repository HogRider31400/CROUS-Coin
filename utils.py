
def get_int(zh,N):
    qlen = N.bit_length()//8
    if(len(zh) > qlen):
        zh = zh[:(qlen)]

    z = int.from_bytes(zh,byteorder='big')%N
    return z