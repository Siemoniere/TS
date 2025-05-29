FLAG = "01111110"
POLYNOMIAL = "100000111"  # CRC-8 (x^8 + x^2 + x + 1), zapisane jako bitstring długości 9 (wielomian + bit najwyższego stopnia)
# Można zmienić na inny wielomian według potrzeby

def xor_bits(a, b):
    # XOR bit po bicie (a i b to stringi bitów tej samej długości)
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

def crc_remainder(input_bits, polynomial=POLYNOMIAL, initial_filler='0'):
    # Oblicza CRC remainder (resztę dzielenia wielomianowego)
    # input_bits - ciąg bitów do sprawdzenia
    # polynomial - wielomian dzielący w postaci bitstringa (np. "100000111")
    # initial_filler - bity zerowe do dopisania na końcu (dla CRC-8 długość to len(polynomial)-1)
    
    n = len(polynomial) - 1
    padded_input = input_bits + initial_filler * n
    padded_input = list(padded_input)

    for i in range(len(input_bits)):
        if padded_input[i] == '1':
            for j in range(len(polynomial)):
                padded_input[i + j] = '0' if padded_input[i + j] == polynomial[j] else '1'

    return ''.join(padded_input[-n:])

def bit_stuffing(data_bits):
    # Wstawia bit '0' po 5 kolejnych '1'
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

def bit_unstuffing(data_bits):
    # Usuwa bit '0' po 5 kolejnych '1'
    unstuffed = []
    count = 0
    i = 0
    while i < len(data_bits):
        bit = data_bits[i]
        unstuffed.append(bit)
        if bit == '1':
            count += 1
            if count == 5:
                i += 1  # pomijamy bit '0' po pięciu '1'
                count = 0
        else:
            count = 0
        i += 1
    return ''.join(unstuffed)

def create_frame(data_bits):
    # Tworzy ramkę: flagi + ramkowanie + CRC
    crc = crc_remainder(data_bits)
    full_data = data_bits + crc
    stuffed_data = bit_stuffing(full_data)
    frame = FLAG + stuffed_data + FLAG
    return frame

def parse_frame(frame):
    # Usuwa flagi, usuwa rozpychanie bitów, sprawdza CRC
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

# === Program ramkujący ===

def encode_file(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        data_bits = f.read().strip()

    frame = create_frame(data_bits)

    with open(output_filename, 'w') as f:
        f.write(frame)

# === Program odwrotny (odramkowujący) ===

def decode_file(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        frame = f.read().strip()

    try:
        data = parse_frame(frame)
    except ValueError as e:
        print("Błąd ramki:", e)
        return

    with open(output_filename, 'w') as f:
        f.write(data)


# === Przykład uruchomienia ===

if __name__ == "__main__":
    # Zamiana Z -> W
    encode_file('Z.txt', 'W.txt')
    # Zamiana W -> Z_kopia
    decode_file('W.txt', 'Z_kopia.txt')
