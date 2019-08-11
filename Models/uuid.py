import random as r

def generate_uuid():
    random_string = ''
    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uuid_format = [4, 4, 4]
    for n in range(len(uuid_format)):
        for i in range(0,uuid_format[n]):
            random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
        if n != len(uuid_format)-1:
            random_string += '-'

    return random_string