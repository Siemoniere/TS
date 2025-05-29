import sys

FLAG = "01111110"
POLYNOMIAL = "100000111"

def crc_remainder(input_bits, polynomial=POLYNOMIAL, initial_filler='0'):
    n = len(polynomial) - 1
    padded_input = input_bits + initial_filler * n
    padded_input = list(padded_input)

    for i in range(len(input_bits)):
        if padded_input[i] == '1':
            for j in range(len(polynomial)):
                padded_input[i + j] = '0' if padded_input[i + j] == polynomial[j] else '1'

    return ''.join(padded_input[-n:])

def bit_stuffing(data_bits):
    stuffed = []
    count = 0
    for bit in data_bits:
        stuffed.append(bit)
        if bit == '1':
            count += 1
            if count == 5:
                stuffed.append('0')
                count = 0
        else:
            count = 0
    return ''.join(stuffed)

def create_frame(data_bits):
    crc = crc_remainder(data_bits)
    full_data = data_bits + crc
    stuffed_data = bit_stuffing(full_data)
    frame = FLAG + stuffed_data + FLAG
    return frame

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Użycie: python3 program1.py Z.txt", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, 'r') as f:
        data_bits = f.read().strip()

    frame = create_frame(data_bits)
    print(frame, end='')
