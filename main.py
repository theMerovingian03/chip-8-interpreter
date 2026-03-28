from src.cpu import CPU
from src.memory import Memory
from src.display import Display
from src.keyboard import Keyboard
import os
import time

def main():
    memory = Memory()
    display = Display()
    keyboard = Keyboard()
    cpu = CPU(memory=memory, display=display, keyboard=keyboard)

    # List available ROMs
    rom_dir = "roms"
    roms = [f for f in os.listdir(rom_dir) if f.endswith('.ch8')]
    
    if not roms:
        print("No ROMs found in roms/ directory.")
        return

    print("Available ROMs:")
    for i, rom in enumerate(roms):
        print(f"{i+1}. {rom}")
    
    while True:
        try:
            choice = int(input("Select a ROM (number): ")) - 1
            if 0 <= choice < len(roms):
                selected_rom = roms[choice]
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number.")

    rom_path = os.path.join(rom_dir, selected_rom)
    with open(rom_path, 'rb') as f:
        rom_data = f.read()
    memory.load_rom(rom_data)

    print(f"Loaded {selected_rom}. Starting emulator...")

    last_timer = time.time()
    running = True

    while running:
        # Handle events
        running = keyboard.handle_event()

        # Run CPU cycles (adjust number as needed for speed)
        cpu.cycle()

        # Update timers at 60Hz
        now = time.time()
        if now - last_timer >= 1/60:
            if cpu.delay_timer > 0:
                cpu.delay_timer -= 1
            if cpu.sound_timer > 0:
                cpu.sound_timer -= 1
            last_timer = now

        # Render display
        display.render()

        # Small delay to prevent 100% CPU usage
        time.sleep(0.001)

if __name__ == "__main__":
    main()