import random

def generate_random_bitstream(filename, length):
    with open(filename, 'w') as f:
        bits = ''.join(random.choice('01') for _ in range(length))
        f.write(bits)

if __name__ == "__main__":
    generate_random_bitstream('Z.txt', 1000)  # generuje 1000-bitowy ciąg
