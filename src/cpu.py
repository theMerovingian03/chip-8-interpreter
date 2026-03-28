from typing import List
from memory import Memory
from display import Display

class CPU:
    def __init__(self, memory: Memory, display: Display):
        self.V: List[int] = [0]*16      # General purpose registers
        self.I: int = 0                 # Index register
        self.stack: List[int] = [0]*16  # Call stack
        self.PC: int = 0x200            # Program counter
        self.SP: int = 0                # Stack pointer
        self.delay_timer: int = 0       # Delay timer
        self.sound_timer: int = 0       # Sound timer
        self.memory = memory            # Memory
        self.display = display          # Display

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
        if opcode == 0x00E0:
            self._clear_screen()
        elif first == 0x1:
            self._jump_to_nnn(NNN)
        elif first == 0x6:
            self._set_vx_to_nn(X, NN)
        elif first == 0x7:
            self._add_vx_to_nn(X, NN)
        elif first == 0xA:
            self._set_index_to_nnn(NNN)
        elif first == 0xD:
            self._display(X, Y, N)
        else:
            print(f"Unknown OPCODE!: {opcode}")


    def cycle(self):
        opcode = self.fetch()
        self.decode(opcode)
        

    # Handlers
    def _clear_screen(self):
        self.display.clear()

    def _jump_to_nnn(self, NNN: int):
        self.PC = NNN

    def _set_vx_to_nn(self, X: int, NN: int):
        self.V[X] = NN

    def _add_vx_to_nn(self, X: int, NN: int):
        self.V[X] = (self.V[X] + NN) & 0xFF

    def _set_index_to_nnn(self, NNN: int):
        self.I = NNN

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
                     


if __name__ == "__main__":
    import time
    import sdl2
    import sdl2.ext
    memory = Memory()
    display = Display()

    rom_path = r".\roms\ibm_logo.ch8"
    with open(rom_path, 'rb') as f:
        rom = f.read()
    memory.load_rom(rom)
    cpu = CPU(memory=memory, display=display)

    running = True
    while running:
        cpu.cycle()

        # handle window events
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False

        display.render()

        time.sleep(1/500)
