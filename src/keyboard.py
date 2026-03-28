from typing import List, Dict
import sdl2
import sdl2.ext

class Keyboard:
    def __init__(self):
        self.keys: List[int] = [0]*16
        self.keymap: Dict = {
            sdl2.SDLK_1: 0x1,
            sdl2.SDLK_2: 0x2,
            sdl2.SDLK_3: 0x3,
            sdl2.SDLK_4: 0xC,

            sdl2.SDLK_q: 0x4,
            sdl2.SDLK_w: 0x5,
            sdl2.SDLK_e: 0x6,
            sdl2.SDLK_r: 0xD,

            sdl2.SDLK_a: 0x7,
            sdl2.SDLK_s: 0x8,
            sdl2.SDLK_d: 0x9,
            sdl2.SDLK_f: 0xE,

            sdl2.SDLK_z: 0xA,
            sdl2.SDLK_x: 0x0,
            sdl2.SDLK_c: 0xB,
            sdl2.SDLK_v: 0xF,
        }
    
    def handle_event(self) -> bool:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                return False
            
            if event.type == sdl2.SDL_KEYDOWN:
                key = event.key.keysym.sym
                
                if key in self.keymap:
                    self.keys[self.keymap[key]] = 1

            elif event.type == sdl2.SDL_KEYUP:
                key = event.key.keysym.sym

                if key in self.keymap:
                    self.keys[self.keymap[key]] = 0
        return True

    def is_pressed(self, key: int) -> bool:
        return self.keys[key] == 1
    