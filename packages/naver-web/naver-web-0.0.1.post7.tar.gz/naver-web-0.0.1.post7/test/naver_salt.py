import random
memory = []


def generate():
    hash = random.getrandbits(128).to_bytes(16, 'big').hex()
    memory.append(hash)
    print("Memory {}".format(memory))
    print("Len {}".format(len(hash)))
    print("hash value: {}".format(hash))
    return hash

if __name__ == '__main__':
    generate() 
    