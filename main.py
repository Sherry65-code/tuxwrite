import voice_engine as ve
from colors import COLOR
import dynamics as dy
import sys

# Header
dy.display("TUXWRITE", location=dy.CENTER, bg=COLOR['bg_red'])
print()

# Initialize tux
ve.init()

# Start tux
ve.stt()