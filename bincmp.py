from curses import wrapper
import curses

def draw_boundaries(stdscr):
    #Draw lines separating the two files
    mid_col = int(curses.COLS/2)
    quarter_col = int(curses.COLS/10)
    threequarter_col = int(9*curses.COLS/10)
    for y in range(0, curses.LINES-1):
        stdscr.addch(y, quarter_col, curses.ACS_VLINE)
        stdscr.addch(y, mid_col, curses.ACS_VLINE)
        stdscr.addch(y, threequarter_col, curses.ACS_VLINE)

def main(stdscr):
    #Clear screen
    stdscr.clear()

    draw_boundaries(stdscr)


    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
