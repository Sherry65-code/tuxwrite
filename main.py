import voice_engine as ve
from colors import COLOR
import dynamics as dy
import sys


# Header
dy.display("TUXWRITE", location=dy.CENTER, bg=COLOR['bg_red'])
print()

if len(sys.argv) == 1:
    ve.init()
elif sys.argv[1] == "-online":
    ve.init(True)
else:
    sys.exit(-1)

# Start tux
ve.stt()