from curses import wrapper
import curses
import sys
import math

UP      = 1
DOWN    = -1
LEFT    = 1
RIGHT   = -1

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

def to_hex_string(data):
    vals = []
    for ch in data:
        val = hex(ord(ch))[2:]
        if len(val) < 2:
            val = '0' + val
        vals += val
    return vals

def print_data(stdscr, data):
    #stdscr.addstr(0, 0, "File 1: {}".format(data[0]))
    x1_min = int(curses.COLS / 10) + 1
    x1_max = int(curses.COLS / 2) - 2
    x2_min = int(curses.COLS / 2) + 1
    y1 = 1
    y2 = y1

    #data[0] needs to be larger or equal to size of data[1]
    if len(data[0]) >= len(data[1]):
        #Get all even numbers in this search space
        indices1 = []
        for num in range(0, len(data[0])):
            if num % 2 == 0:
                indices1.append(num)

        #Assuming that window space for files is the same...
        x1 = x1_min
        x2 = x2_min
        four_count = 0
        for i in indices1:
            if y1 >= 30:
                #stdscr.addstr(y2, x2, "COLS: {}".format(curses.COLS))
                break

            #Keep them at the same index
            i2 = i

            #If first file is larger, we need to append garbage to end of second to pad 
            if i2 >= len(data[1]):
                data[1].append('')
                data[1].append('')

            #Get data ready to print
            val1 = data[0][i] + data[0][i+1]
            val2 = data[1][i] + data[1][i+1]

            #Print data
            stdscr.addstr(y1, x1, val1 + " ")
            stdscr.addstr(y2, x2, val2 + " ")


            #Update for next position
            x1 += 3
            x2 += 3

            four_count += 1
            if four_count % 4 == 0 and x1 < x1_max:
                stdscr.addstr(y1, x1, " ")
                stdscr.addstr(y2, x2, " ")
                x1 += 3
                x2 += 3
            elif x1 >= x1_max:
                x1 = x1_min
                x2 = x2_min
                y1 += 1
                y2 += 1
    else:
        #data[1] is larger than data[0], so we need to account for that
        #Get all even numbers in this search space
        indices1 = []
        for num in range(0, len(data[1])):
            if num % 2 == 0:
                indices1.append(num)

        #Assuming that window space for files is the same...
        x1 = x1_min
        x2 = x2_min
        four_count = 0
        for i in indices1:
            #Check height to ensure we don't error out
            if y1 >= curses.COLS:
                break

            #Keep them at the same index
            i2 = i

            #If first file is larger, we need to append garbage to end of second to pad 
            if i2 >= len(data[0]):
                data[0].append('')
                data[0].append('')

            #Get data ready to print
            val1 = data[0][i] + data[0][i+1]
            val2 = data[1][i] + data[1][i+1]

            #Print data
            stdscr.addstr(y1, x1, val1 + " ")
            stdscr.addstr(y2, x2, val2 + " ")

            #Update for next position
            x1 += 3
            x2 += 3

            four_count += 1
            if four_count % 4 == 0 and x1 < x1_max:
                stdscr.addstr(y1, x1, " ")
                stdscr.addstr(y2, x2, " ")
                x1 += 3
                x2 += 3
            elif x1 >= x1_max:
                x1 = x1_min
                x2 = x2_min
                y1 += 1
                y2 += 1



def init_screen(stdscr):
    draw_boundaries(stdscr)

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    print_file_names(stdscr, filename1, filename2)
    
    #Load up files
    file_data = ["", ""]
    file_data[0] = to_hex_string(read_file(filename1))
    file_data[1] = to_hex_string(read_file(filename2))
    
    #Print this data
    print_data(stdscr, file_data)
    
def scroll(direction):
    if direction < 0:
        #Scroll down
        print("scroll down")
    elif direction > 0:
        #Scroll up
        print("scroll up")
    else:
        #Bad input
        print("bad input")

def move_to(direction):
    if direction < 0:
        #Move to the right
        print("move right")
    elif direction > 0:
        #Move to the left
        print("move left")
    else:
        #Uknown input
        print("uknown input")

def take_input(stdscr):
    while True:
        stdscr.refresh()
        ch = stdscr.getch()

        #Options for input
        if ch == curses.KEY_DOWN:
            #Scroll Down
            scroll(DOWN)
        elif ch == curses.KEY_UP:
            #Scroll Up
            scroll(UP)
        elif ch == curses.KEY_RIGHT:
            #Move cursers right
            move_to(RIGHT)
        elif ch == curses.KEY_LEFT:
            #Move cursers left
            move_to_(LEFT)
        elif ch == ord('q'):
            break
        else:
            #Uknown input
            print("unkown input")


def main(stdscr):
    #Clear screen
    stdscr.clear()

    #If 2 files provided, intialize 
    if len(sys.argv) >= 3:
        init_screen(stdscr)
        take_input(stdscr)
    #Else, print error
    else:
        print_message(stdscr, "ERROR: Two files are required to compare them. Press any key to exit")

    stdscr.refresh()

wrapper(main)
