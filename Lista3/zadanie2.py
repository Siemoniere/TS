import random
import time

class Medium:
    def __init__(self, length):
        self.length = length
        self.cells = [None] * length

    def reset(self):
        self.cells = [None] * self.length

    def propagate(self, signals):
        # signals: dict {pos: id_stacji}
        new_cells = [None] * self.length
        for pos, st_id in signals.items():
            # sygnał dociera do pos
            if new_cells[pos] is None:
                new_cells[pos] = set()
            new_cells[pos].add(st_id)
            # propagacja do sąsiadów
            for neighbor in [pos-1, pos+1]:
                if 0 <= neighbor < self.length:
                    if new_cells[neighbor] is None:
                        new_cells[neighbor] = set()
                    new_cells[neighbor].add(st_id)

        # Zamiana set -> id_stacji lub 'collision'
        for i, val in enumerate(new_cells):
            if val is None:
                self.cells[i] = None
            elif len(val) == 1:
                self.cells[i] = val.pop()
            else:
                self.cells[i] = 'collision'

    def is_busy(self):
        # Medium jest zajęte, jeśli w którymkolwiek miejscu jest sygnał (nie None)
        return any(cell is not None for cell in self.cells)

    def has_collision(self):
        # Czy gdzieś jest kolizja?
        return any(cell == 'collision' for cell in self.cells)

    def __str__(self):
        # Wyświetlenie medium — np. '.' puste, 'C' kolizja, cyfrki id stacji
        result = ''
        for c in self.cells:
            if c is None:
                result += '.'
            elif c == 'collision':
                result += 'X'
            else:
                result += str(c)
        return result


class Station:
    def __init__(self, st_id, position):
        self.st_id = st_id
        self.position = position
        self.state = 'idle'  # idle, waiting, sending, backoff
        self.backoff_time = 0
        self.send_time = 0
        self.max_send_time = 5  # jak długo wysyłać ramkę
        self.collision_detected = False

    def sense_medium(self, medium):
        # Sprawdź czy medium jest wolne w miejscu stacji i sąsiadach
        busy = False
        for pos in [self.position, self.position - 1, self.position + 1]:
            if 0 <= pos < medium.length:
                if medium.cells[pos] is not None:
                    busy = True
        return busy

    def step(self, medium):
        if self.state == 'idle':
            # Zamiar wysłania - sprawdzamy medium
            if not self.sense_medium(medium):
                self.state = 'sending'
                self.send_time = self.max_send_time
                self.collision_detected = False
                print(f"Stacja {self.st_id} zaczyna nadawanie")
            else:
                self.state = 'waiting'
        elif self.state == 'waiting':
            if not self.sense_medium(medium):
                self.state = 'sending'
                self.send_time = self.max_send_time
                self.collision_detected = False
                print(f"Stacja {self.st_id} zaczyna nadawanie po oczekiwaniu")
        elif self.state == 'sending':
            # Nadaje swój sygnał
            self.send_time -= 1
            if medium.cells[self.position] == 'collision':
                self.collision_detected = True
                self.state = 'backoff'
                self.backoff_time = random.randint(1, 4)
                print(f"Stacja {self.st_id} wykryła kolizję, czeka {self.backoff_time} kroków")
            elif self.send_time == 0:
                self.state = 'idle'
                print(f"Stacja {self.st_id} zakończyła nadawanie")
        elif self.state == 'backoff':
            self.backoff_time -= 1
            if self.backoff_time <= 0:
                self.state = 'idle'

    def transmit_signal(self):
        # Jeśli nadaje, sygnał na pozycji stacji, inaczej brak sygnału
        if self.state == 'sending':
            return self.position, self.st_id
        else:
            return None


def simulate_csma_cd(num_stations=3, medium_length=20, steps=50):
    medium = Medium(medium_length)
    # Rozmieszczamy stacje losowo, unikamy kolizji pozycji
    positions = random.sample(range(medium_length), num_stations)
    stations = [Station(i, pos) for i, pos in enumerate(positions)]

    print("Pozycje stacji:", [(s.st_id, s.position) for s in stations])

    for t in range(steps):
        print(f"Krok {t}:")
        # Każda stacja decyduje, co robi
        for s in stations:
            s.step(medium)

        # Zbieramy sygnały ze stacji nadających
        signals = {}
        for s in stations:
            tx = s.transmit_signal()
            if tx is not None:
                pos, st_id = tx
                signals[pos] = st_id

        # Propagujemy sygnały po medium
        medium.propagate(signals)

        # Pokazujemy stan medium i stacji
        print("Medium: ", medium)
        for s in stations:
            print(f"Stacja {s.st_id} [{s.position}]: {s.state}")
        print("-" * 40)
        time.sleep(0.1)  # opcjonalnie spowolnienie


if __name__ == "__main__":
    simulate_csma_cd()
