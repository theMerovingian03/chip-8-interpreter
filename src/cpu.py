from typing import List, Any
from memory import Memory
from keyboard import Keyboard
from display import Display
import random

class CPU:
    def __init__(self, memory: Memory, display: Display, keyboard: Keyboard):
        self.V: List[int] = [0]*16      # General purpose registers
        self.I: int = 0                 # Index register
        self.stack: List[int] = [0]*16  # Call stack
        self.PC: int = 0x200            # Program counter
        self.SP: int = 0                # Stack pointer
        self.delay_timer: int = 0       # Delay timer
        self.sound_timer: int = 0       # Sound timer
        self.memory = memory            # Memory
        self.display = display          # Display
        self.keyboard = keyboard        # Keyboard

        self.prev_keys: List[int] = [0] * 16 # To prevent debounce
        self.waiting_for_key: bool = False
        self.wait_register: Any = None

    def cycle(self):

        if self.waiting_for_key:
            for key in range(16):
                if self.keyboard.is_pressed(key) and not self.prev_keys[key]:
                    self.V[self.wait_register] = key
                    self.waiting_for_key = False
                    break

            self.prev_keys = self.keyboard.keys.copy()
            return
        
        opcode = self.fetch()
        self.decode(opcode)

    def fetch(self) -> int:
        byte1 = self.memory.read(self.PC)
        byte2 = self.memory.read(self.PC + 1)
        self.PC += 2

        opcode: int = (byte1 << 8) | byte2
        return opcode
    
    def decode(self, opcode: int) -> None:
        first: int = opcode >> 12
        X: int     = (opcode & 0x0F00) >> 8
        Y: int     = (opcode & 0x00F0) >> 4
        N: int     = opcode & 0x000F
        NN: int    = opcode & 0x00FF
        NNN: int   = opcode & 0x0FFF

        # Dispatch
        if first == 0x0:
            self.handle_0_group(opcode)
        elif first == 0x1:
            self._jump_to_nnn(NNN)
        elif first == 0x2:
            self._call_nnn(NNN)
        elif first == 0x3:
            self._skip_vx_nn_equal(X, NN)
        elif first == 0x4:
            self._skip_vx_nn_nequal(X, NN)
        elif first == 0x5:
            self._skip_vx_vy_equal(X, Y)
        elif first == 0x6:
            self._set_vx_to_nn(X, NN)
        elif first == 0x7:
            self._add_vx_to_nn(X, NN)
        elif first == 0x8:
            self.handle_8_group(X, Y, N)
        elif first == 0x9:
            self._skip_vx_vy_nequal(X, Y)
        elif first == 0xA:
            self._set_index_to_nnn(NNN)
        elif first == 0xB:
            self._pc_to_v0_plus_nnn(NNN)
        elif first == 0xC:
            self._random_to_vx_and_nn(X, NN)
        elif first == 0xD:
            self._display(X, Y, N)
        elif first == 0xE:
            self.handle_e_group(X, NN)
        else:
            print(f"Unknown OPCODE!: {opcode}")
        

    # Handlers

    # 0x1NNN
    def _jump_to_nnn(self, NNN: int):
        self.PC = NNN

    # 0x2NNN
    def _call_nnn(self, NNN: int):
        if self.SP >= 16:
            raise Exception("Stack overflow")
        self.stack[self.SP] = self.PC
        self.SP += 1
        self.PC = NNN

    # 0x3XNN
    def _skip_vx_nn_equal(self, X: int, NN: int):
        if self.V[X] == NN:
            self.PC += 2

    # 0x4XNN
    def _skip_vx_nn_nequal(self, X: int, NN: int):
        if self.V[X] != NN:
            self.PC += 2

    # 0x5XY0
    def _skip_vx_vy_equal(self, X: int, Y: int):
        if self.V[X] == self.V[Y]:
            self.PC += 2

    # 0x6XNN
    def _set_vx_to_nn(self, X: int, NN: int):
        self.V[X] = NN

    # 0x7NN
    def _add_vx_to_nn(self, X: int, NN: int):
        self.V[X] = (self.V[X] + NN) & 0xFF

    # 0x9XY0
    def _skip_vx_vy_nequal(self, X: int, Y: int):
        if self.V[X] != self.V[Y]:
            self.PC += 2

    # 0xANNN
    def _set_index_to_nnn(self, NNN: int):
        self.I = NNN

    # 0xBNNN
    def _pc_to_v0_plus_nnn(self, NNN: int):
        self.PC = (self.V[0] + NNN) & 0xFFF

    # 0xCXNN
    def _random_to_vx_and_nn(self, X: int, NN: int):
        self.V[X] = random.getrandbits(8) & NN

    # DXYN
    def _display(self, X: int, Y: int, N: int):
        x_coord = self.V[X] & 63
        y_coord = self.V[Y] & 31
        self.V[0xF] = 0

        for row in range(N):
            sprite_byte = self.memory.read(self.I + row)

            for col in range(8):
                bit = (sprite_byte >> (7 - col)) & 1

                if bit == 1:
                    px = (x_coord + col) & 63
                    py = (y_coord + row) & 31

                    collision = self.display.toggle_pixel(px, py)
                    if collision:
                        self.V[0xF] = 1

    # Group handlers              
    def handle_0_group(self, opcode: int):        
        # 00E0
        if opcode == 0x00E0:
            self.display.clear()
        # 00EE
        elif opcode == 0x00EE:
            self.SP = -1
            self.PC = self.stack[self.PC]

    def handle_8_group(self, X: int, Y: int, N: int):
        # 8XY0
        if N == 0x0:
            self.V[X] = self.V[Y]
        elif N == 0x1:
            self.V[X] |= self.V[Y]
        elif N == 0x2:
            self.V[X] &= self.V[Y]
        elif N == 0x3:
            self.V[X] ^= self.V[Y]
        elif N == 0x4:
            # Handle carry
            result = self.V[X] + self.V[Y]
            self.V[0xF] = 1 if result > 255 else 0
            self.V[X] = result & 0xFF
        elif N == 0x5:
            # Handle underflow
            self.V[0xF] = 1 if self.V[X] > self.V[Y] else 0
            self.V[X] = (self.V[X] - self.V[Y]) & 0xff
        elif N == 0x6:
            self.V[0xF] = self.V[X] & 0x1
            self.V[X] >>= 1
        elif N == 0x7:
            self.V[0xF] = 1 if self.V[Y] > self.V[X] else 0
            self.V[X] = (self.V[Y] - self.V[X]) & 0xFF
        elif N == 0xE:
            self.V[0xF] = (self.V[X] & 0x80) >> 7
            self.V[X] = (self.V[X] << 1) & 0xFF
        else:
            print(f"Unknown 8-group opcode: {N}")

    def handle_e_group(self, X: int, NN: int):
        key = self.V[X]

        # 0xEX9E
        if NN == 0x9E:
            if self.keyboard.is_pressed(key):
                self.PC += 2
        # 0xEXA1
        elif NN == 0xA1:
            if not self.keyboard.is_pressed(key):
                self.PC += 2

    def handle_f_group(self, X: int, NN: int):

        # 0xFX07
        if NN == 0x07:
            self.V[X] = self.delay_timer
        
        # 0xFX0A
        elif NN == 0x0A:
            self.wait_register = X
            self.waiting_for_key = True

        # 0xFX15
        elif NN == 0x15:
            self.delay_timer = self.V[X]
        
        # 0xFX18
        elif NN == 0x18:
            self.sound_timer = self.V[X]

        # 0xFX1E
        elif NN == 0x1E:
            self.I = (self.I + self.V[X]) & 0xFFF

        # 0xFX29
        elif NN == 0x29:
            self.I = 0x050 + ((self.V[X] & 0xF) * 5)

        # 0xFX33
        elif NN == 0x33:
            # Get V[X]
            num: int = self.V[X]
            units: int = num % 10
            tens: int = (num // 10) % 10
            hundreds: int = num // 100

            self.memory.write(self.I, hundreds)
            self.memory.write(self.I + 1, tens)
            self.memory.write(self.I + 2, units)

        elif NN == 0x55:
            for i in range(X + 1):
                self.memory.write(self.I + i, self.V[i])

        elif NN == 0x65:
            for i in range(X + 1):
                self.V[i] = self.memory.read(self.I + i)

        else:
            print(f"Unknown opcode: {NN:02X}")

if __name__ == "__main__":
    import time
    memory = Memory()
    display = Display()
    keyboard = Keyboard()

    rom_path = r".\roms\ibm_logo.ch8"
    with open(rom_path, 'rb') as f:
        rom = f.read()
    memory.load_rom(rom)
    cpu = CPU(memory=memory, display=display, keyboard=keyboard)
    last_timer = time.time()
    running = True

    while running:
        cpu.cycle()

        now = time.time()

        if now - last_timer >= 1/60:
            if cpu.delay_timer > 0:
                cpu.delay_timer -= 1
            if cpu.sound_timer > 0:
                cpu.sound_timer -= 1
            last_timer = now

        running = keyboard.handle_event()

        display.render()

        time.sleep(1/500)
