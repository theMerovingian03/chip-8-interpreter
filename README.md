# Python CHIP-8 Interpreter

### What is the CHIP-8?
CHIP-8 is an interpreted programming language, developed by Joseph Weisbecker on his 1802 microprocessor.
It wasinitially used on the COSMAC VIP and Telmac 1800, which were 8-bit microcomputers made in the mid-1970s.
CHIP-8 was designed to be easy to program for and to use less memory than other programming languages like BASIC. (Wikipedia)

---

### Installation
1. Recommended Python version: `3.12`, to avoid possible compatibility issues with SDL2
2. Clone using `git clone https://github.com/theMerovingian03/chip-8-interpreter.git`
3. `cd chip-8-interpreter`
4. Create virtual env `py -3.12 -m venv myenv`
5. Activate virtual env `myenv\Scripts\activate`
6. Run: `pip install -r requirements.txt`

---

### How do I run it?
Simply run the `main.py` file in the `chip-8-interpreter` directory. It'll show you a detailed menu so you can choose which programs (ROMs) you want to see running.

---

### Controls:

#### Pong (Two plaers):
* `1`: Move left paddle UP
* `Q`: Move left paddle DOWN
* `4`: Move right paddle UP
* `R`: Move right paddle DOWN

#### Space Invaders (Single Player):
* `W`: Start game
* `Q`: Move left
* `E`: Move right
* `W`: Shoot

---

### Sources
* Tobias V.I Langhoff's blog (https://tobiasvl.github.io/blog/write-a-chip-8-emulator/)
* Wikipedia (https://en.wikipedia.org/wiki/CHIP-8)