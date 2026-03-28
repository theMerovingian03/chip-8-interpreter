import sdl2
import sdl2.ext

WIDTH  = 64
HEIGHT = 32
SCALE  = 10

class Display:
    def __init__(self) -> None:
        sdl2.ext.init()
        self.window = sdl2.ext.Window("CHIP-8", size=(WIDTH * SCALE, HEIGHT * SCALE))
        self.window.show()
        self.renderer = sdl2.ext.Renderer(self.window)
        self.pixels = [0]*(WIDTH * HEIGHT)

    def clear(self):
        """Sets all pixels in framebuffer to 0"""
        for i in range(len(self.pixels)):
            self.pixels[i]=0

    def toggle_pixel(self, x: int, y: int):
        """XOR a pixel and return True if collision occurs"""
        x %= WIDTH
        y %= HEIGHT

        index = y * WIDTH + x
        collision = self.pixels[index] == 1
        self.pixels[index] ^= 1
        return collision
    
    def render(self):
        """Render framebuffer to window"""
        # Set background color (black)
        self.renderer.color = (0, 0, 0)
        self.renderer.clear()

        # Set draw color (white)
        self.renderer.color = (255, 255, 255)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.pixels[y * WIDTH + x]:
                    rect = sdl2.SDL_Rect(
                        x * SCALE,
                        y * SCALE,
                        SCALE,
                        SCALE
                    )
                    self.renderer.fill(rect)
        self.renderer.present()