from curses import wrapper
import curses
import sys
import math

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
    width = x_max - x_min

    #Height of the box depends on the length of the message provided
    lines = math.ceil(len(msg) / width + 1)

    y_min = int(curses.LINES/2) - int(math.ceil(int(lines) / 2)) - 1    #I'm sorry for this
    y_max = int(curses.LINES/2) + int(math.ceil(int(lines) / 2)) + 1

    assert(width > 0)

    draw_message_box(stdscr, x_min, x_max, y_min, y_max)
    #Message needs to be drawn responsive to width of the box
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
                if substr[-1] != ' ' and (len(msg) - len(substr)) != 0:
                    substr += '-'
                stdscr.addstr(y, x_min + 2, substr)
                msg = msg[text_width:]
                y = y + 1
            else:
                if substr[-1] != ' ' and msg[text_width] != ' ':
                    substr += '-'
                stdscr.addstr(y, x_min + 2, substr)
                msg = msg[text_width:]
                y = y + 1
    else:
        stdscr.addstr(y_min + 2, x_min + 2, msg)

    stdscr.move(0,0)


def draw_boundaries(stdscr):
    #Draw lines separating the two files
    mid_col = int(curses.COLS/2)
    quarter_col = int(curses.COLS/10)
    threequarter_col = int(9*curses.COLS/10)
    for y in range(0, curses.LINES):
        stdscr.addch(y, quarter_col, curses.ACS_VLINE)
        stdscr.addch(y, mid_col, curses.ACS_VLINE)
        stdscr.addch(y, threequarter_col, curses.ACS_VLINE)
def print_file_names(stdscr, filename1, filename2):
    stdscr.addstr(curses.LINES - 1, 1 + int(curses.COLS/10), filename1, curses.A_REVERSE)
    stdscr.addstr(curses.LINES - 1, 1 + int(curses.COLS/2), filename2, curses.A_REVERSE)

def read_file(filename):
    #There need to be some protections to scrub filename's input prior to this step!
    data = ""
    with open(filename, "r") as file_obj:
        data = file_obj.read()
    return data

def print_data(stdscr, data):
    stdscr.addstr(0, 0, "File 1: {}")

def init_screen(stdscr):
    draw_boundaries(stdscr)

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    print_file_names(stdscr, filename1, filename2)
    
    #Load up files
    file_data = ["", ""]
    file_data[0] = read_file(filename1)
    print(file_data[0])
    file_data[1] = read_file(filename2)
    
    #Print this data
    print_data(stdscr, file_data)
    

def main(stdscr):
    #Clear screen
    stdscr.clear()

    #If 2 files provided, intialize 
    if len(sys.argv) >= 3:
        init_screen(stdscr)
    #Else, print error
    else:
        print_message(stdscr, "ERROR: Two files are required to compare them. Press any key to exit")

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)
