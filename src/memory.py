from typing import List
FONT_SET: List[int] = [
    0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
    0x20, 0x60, 0x20, 0x20, 0x70, # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
    0x90, 0x90, 0xF0, 0x10, 0x10, # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
    0xF0, 0x10, 0x20, 0x40, 0x40, # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90, # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
    0xF0, 0x80, 0x80, 0x80, 0xF0, # C
    0xE0, 0x90, 0x90, 0x90, 0xE0, # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
    0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]

class Memory:
    def __init__(self, capacity: int = 4096):
        """Initializes memory of given capacity bytes"""
        self.capacity = capacity
        self.memory: bytearray = bytearray(4096)
        self.load_fonts()

    def load_fonts(self):
        start_address = 0x050
        for offset, byte in enumerate(FONT_SET):
            self.write(start_address + offset, byte)
        
    def read(self, address: int) -> int:
        """Reads memory at given address (0-4095)"""
        if address < 0 or address >= self.capacity:
            print(f"[MEMORY_ERROR] Could not access memory at address {address} invalid!")
            raise IndexError
        return self.memory[address]
    
    def write(self, address: int, value: int) -> None:
        """Writes value to given address"""
        if address < 0 or address >= self.capacity:
            print(f"[MEMORY_ERROR] Could not write to memory at address {address} invalid!")
            raise IndexError
        if value < 0 or value > 255:
            print(f"[MEMORY_ERROR] Could not write {value} to memory at address {address} invalid!")
            raise ValueError
        self.memory[address] = value

    def load_rom(self, rom_bytes: bytes) -> None:
        """Loads a ROM"""
        start_address = 0x200

        if start_address + len(rom_bytes) > self.capacity:
            raise MemoryError("[MEMORY_ERROR] ROM exceeds memory capacity")

        for offset, byte in enumerate(rom_bytes):
            self.write(start_address + offset, byte)

if __name__ == "__main__":
    rom_path = r".\roms\ibm_logo.ch8"
    memory = Memory()
    with open(rom_path, 'rb') as f:
        rom = f.read()
    memory.load_rom(rom)

    for adr in range(512, 644):
        value = memory.read(adr)
        print(hex(value))