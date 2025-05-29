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

def bit_unstuffing(data_bits):
    unstuffed = []
    count = 0
    i = 0
    while i < len(data_bits):
        bit = data_bits[i]
        unstuffed.append(bit)
        if bit == '1':
            count += 1
            if count == 5:
                i += 1  # skip stuffed 0
                count = 0
        else:
            count = 0
        i += 1
    return ''.join(unstuffed)

def parse_frame(frame):
    if not (frame.startswith(FLAG) and frame.endswith(FLAG)):
        raise ValueError("Brak flag ramki")

    content = frame[len(FLAG):-len(FLAG)]
    unstuffed = bit_unstuffing(content)
    data = unstuffed[:- (len(POLYNOMIAL) - 1)]
    crc_received = unstuffed[- (len(POLYNOMIAL) - 1):]

    crc_calc = crc_remainder(data)
    if crc_calc != crc_received:
        raise ValueError("Błąd CRC")

    return data

if __name__ == "__main__":
    frame = sys.stdin.read().strip()
    try:
        data = parse_frame(frame)
        print(data, end='')
    except ValueError as e:
        print("Błąd ramki:", e, file=sys.stderr)
        sys.exit(1)
