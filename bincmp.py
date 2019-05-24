from curses import wrapper
import curses
import sys

def draw_message_box(stdscr, x_min, x_max, y_min, y_max):
    for x in range(x_min, x_max):
        stdscr.addch(y_min, x, curses.ACS_HLINE)
        stdscr.addch(y_max, x, curses.ACS_HLINE)
    for y in range(y_min + 1, y_max):
        stdscr.addch(y, x_min - 1, curses.ACS_VLINE)
        stdscr.addch(y, x_max, curses.ACS_VLINE)

def print_message(stdscr, msg):
    x_min = int(curses.COLS/2) - 20
    x_max = int(curses.COLS/2) + 20
    y_min = int(curses.LINES/2) - 5
    y_max = int(curses.LINES/2) + 5

    width = x_max - x_min

    assert(width > 0)

    draw_message_box(stdscr, x_min, x_max, y_min, y_max)
    #Message needs to be drawn responsive to width of the box but this will do for now
    if len(msg) > (x_max - x_min):
        y = y_min+1
        text_width = width - 4
        end_reached = False
        while end_reached != True:
            #Print message dynamically
            substr = msg[:text_width]
            if len(substr) < text_width:
                end_reached = True
                stdscr.addstr(y, x_min + 2, substr)
            elif len(substr) == text_width:
                if substr[-1] != ' ' and msg[text_width] != ' ':
                    substr += '-'
                stdscr.addstr(y, x_min + 2, substr)
                msg = msg[text_width:]
                y = y + 1
            else:
                if substr[-1] != ' ':
                    substr += '-'
                stdscr.addstr(y, x_min + 2, substr)
                msg = msg[text_width:]
                y = y + 1
    else:
        stdscr.addstr(y_min + 2, x_min + 2, msg)


def draw_boundaries(stdscr):
    #Draw lines separating the two files
    mid_col = int(curses.COLS/2)
    quarter_col = int(curses.COLS/10)
    threequarter_col = int(9*curses.COLS/10)
    for y in range(0, curses.LINES):
        stdscr.addch(y, quarter_col, curses.ACS_VLINE)
        stdscr.addch(y, mid_col, curses.ACS_VLINE)
        stdscr.addch(y, threequarter_col, curses.ACS_VLINE)
def print_file_names(stdscr):
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    stdscr.addstr(curses.LINES - 1, 1 + int(curses.COLS/10), filename1, curses.A_REVERSE)
    stdscr.addstr(curses.LINES - 1, 1 + int(curses.COLS/2), filename2, curses.A_REVERSE)

def main(stdscr):
    #Clear screen
    stdscr.clear()

    #If 2 files provided, intialize 
    if len(sys.argv) >= 3:
        draw_boundaries(stdscr)
        print_file_names(stdscr)
    #Else, print error
    else:
        print_message(stdscr, "ERROR: Two files are required to compare them. Hello? Test this is still a test omg we need more testing hows it going be now youre nowhere anymore???")




    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
