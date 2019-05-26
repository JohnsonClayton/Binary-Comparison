#Created by Clayton Johnson => github.com/JohnsonClayton
#Partly inspired by example => github.com/mingrammer/python-curses-scroll-example

from curses import wrapper
import curses
import sys
import math


class Screen(object):
    #Maps for the change in (y, x)
    UP      = [-1, 0]
    DOWN    = [1, 0]
    LEFT    = [0, -1]
    RIGHT   = [0, 1]

    def __init__(self, scrn):
        #stdscr object
        self.screen = scrn

        #Default values
        self.top = 0
        self.bottom = 0
        self.data = ["", ""]
        self.highlights = []

        self.screen.clear()

    def set_files(self, file1, file2):
        #File names
        self.filename1 = file1
        self.filename2 = file2
    
    def run(self):
        self.init_screen()
        self.take_input()

    def init_screen(self):
        self.draw_boundaries()
        self.print_file_names()
        
        #Load up files
        self.data[0] = self.to_hex_string(self.read_file(self.filename1))
        self.data[1] = self.to_hex_string(self.read_file(self.filename2))

        #Initialize colors
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

        #Set bottom
        self.set_bottom_val()
        
        #Print this data
        self.print_data()

        #Move cursor to beginning of file1
        self.reset_cursor()


    def set_bottom_val(self):
        lines1 = int(len(self.data[0]) / 12) + 1
        lines2 = int(len(self.data[1]) / 12) + 1
        self.bottom = lines1 if lines1 > lines2 else lines2
        #self.screen.addstr(0, 0, "{}".format(self.bottom))

    def draw_boundaries(self):
        #Draw lines separating the two files
        mid_col = int(curses.COLS/2)
        quarter_col = int(curses.COLS/10)
        threequarter_col = int(9*curses.COLS/10)
        for y in range(0, curses.LINES):
            self.screen.addch(y, quarter_col, curses.ACS_VLINE)
            self.screen.addch(y, mid_col, curses.ACS_VLINE)
            self.screen.addch(y, threequarter_col, curses.ACS_VLINE)


    def draw_message_box(self, x_min, x_max, y_min, y_max):
        for x in range(x_min, x_max):
            self.screen.addch(y_min, x, curses.ACS_HLINE)
            self.screen.addch(y_max, x, curses.ACS_HLINE)
        for y in range(y_min + 1, y_max):
            self.screen.addch(y, x_min - 1, curses.ACS_VLINE)
            self.screen.addch(y, x_max, curses.ACS_VLINE)

    def print_message(self, msg):
        x_min = int(curses.COLS/2) - 20
        x_max = int(curses.COLS/2) + 20
        width = x_max - x_min

        #Height of the box depends on the length of the message provided
        lines = math.ceil(len(msg) / width + 1)

        y_min = int(curses.LINES/2) - int(math.ceil(int(lines) / 2)) - 1    #I'm sorry for this
        y_max = int(curses.LINES/2) + int(math.ceil(int(lines) / 2)) + 1

        assert(width > 0)

        self.draw_message_box(x_min, x_max, y_min, y_max)
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
                    self.screen.addstr(y, x_min + 2, substr)
                elif len(substr) == text_width:
                    if substr[-1] != ' ' and (len(msg) - len(substr)) != 0:
                        substr += '-'
                    self.screen.addstr(y, x_min + 2, substr)
                    msg = msg[text_width:]
                    y = y + 1
                else:
                    if substr[-1] != ' ' and msg[text_width] != ' ':
                        substr += '-'
                    self.screen.addstr(y, x_min + 2, substr)
                    msg = msg[text_width:]
                    y = y + 1
        else:
            self.screen.addstr(y_min + 2, x_min + 2, msg)

        self.screen.move(0,0)
        self.screen.getch()


    def print_file_names(self):
        #This is where I officially threw readability out the window
        self.screen.addstr(curses.LINES - 1, 1 + int(curses.COLS/10), self.filename1, curses.A_REVERSE)
        self.screen.addstr(curses.LINES - 1, 1 + int(curses.COLS/2), self.filename2, curses.A_REVERSE)

    def to_hex_string(self, data):
        vals = []
        for ch in data:
            val = hex(ord(ch))[2:]
            if len(val) < 2:
                val = '0' + val
            vals.append(val)

        return vals

    def read_file(self, filename):
        #There need to be some protections to scrub filename's input prior to this step!
        data = ""
        with open(filename, "r") as file_obj:
            data = file_obj.read()
        return data


    def scroll(self, direction):
        if self.top >= 0 and self.top <= self.bottom:
            self.top += direction[0]
            self.print_data()

    def remove_highlight(self, y, x):
        #Removes the given coordinates from highlight list
        for pos in self.highlights: #This could be more efficient
            if pos[0] == y and pos[1] == x:
                self.highlights.remove(pos)
                val = self.screen.getstr(y, x)
                self.screen.addstr(y, x, val)

    def add_highlight(self, y, x):
        #Adds given coordinates to highlight list
        self.highlights.append([y, x])

    def do_move_cursor(self, prev_y, prev_x, next_y, next_x):
        #self.remove_highlight(prev_y, prev_x + 43)
        #self.add_highlight(next_y, next_x + 43)
        self.screen.move(next_y, next_x)

    def move_cursor(self, direction):
        #Update the cursor position based on the direction vector handed over
        pos = curses.getsyx()
        next_pos = [pos[0] + direction[0], pos[1] + direction[1]]
        if next_pos[1] < 0 or next_pos[1] >= curses.COLS/2 or next_pos[0] > self.bottom:
            #Trying to go offscreen left or right with x's
            curses.beep()
        elif next_pos[0] < 1:
            #Scroll
            self.scroll(self.UP)
            self.screen.move(pos[0], pos[1])
        elif next_pos[0] >= curses.LINES - 1:
            #Scroll
            self.scroll(self.DOWN)
            self.screen.move(pos[0], pos[1])
        else:
            #self.screen.move(next_pos[0], next_pos[1])
            self.do_move_cursor(pos[0], pos[1], next_pos[0], next_pos[1])

    def reset_cursor(self):
        self.screen.move(1, 1 + int(curses.COLS/10))

    def update_screen(self):
        #Redraw all the highlighted characters
        y = 0
        for pos in self.highlights:
            val = self.screen.getstr(pos[0], pos[1])
            self.screen.addstr(pos[0], pos[1], val, curses.A_REVERSE)
            self.screen.move(pos[0], pos[1] - 43)
            #self.screen.addstr(y, 0, "{}".format(pos))

        self.screen.refresh()

    def take_input(self):
        while True:
            self.update_screen()
            ch = self.screen.getch()

            #Options for input
            if ch == curses.KEY_DOWN:
                #Move Cursor Down
                self.move_cursor(self.DOWN)
            elif ch == curses.KEY_UP:
                #Move Cursor Up
                self.move_cursor(self.UP)
            elif ch == curses.KEY_RIGHT:
                #Move cursor right
                self.move_cursor(self.RIGHT)
            elif ch == curses.KEY_LEFT:
                #Move cursor left
                self.move_cursor(self.LEFT)
            elif ch == ord('q'):
                break
            else:
                #Uknown input
                print("unkown input")

    def print_data(self):
        
        #Positional defaults
        x1_min = int(curses.COLS / 10) + 1
        x1_max = int(curses.COLS / 2) - 2
        x2_min = int(curses.COLS / 2) + 1
        y1 = 1
        y2 = y1

        #Default char/index values
        ch1 = " "
        ch2 = ch1

        if len(self.data[0]) > 0 and len(self.data[1]) > 0:

            #We need to base index off `top`
            if self.top >= 0:
                #Find how many lines we skip printing
                    #self.screen.addstr(0, 0, "top: {}".format(self.top))
                    #self.screen.addstr(1, 0, "btm: {}".format(self.bottom))
                index = self.top * 12
            else:
                #Assume something broke
                index = 0
                self.top = 0
                #self.print_message("I'm sorry, we lost track of the lines")

            x1 = x1_min
            x2 = x2_min

            byte_chunks = 0

            #Loop until both files are out of bytes OR we printed to the end of the page
            while (ch1 != "" or ch2 != "") and (y1 < curses.LINES - 1):
                if (len(self.data[0]) <= index):
                    ch1 = ""
                else:
                    ch1 = self.data[0][index]

                if (len(self.data[1]) <= index):
                    ch2 = ""
                else:
                    ch2 = self.data[1][index]

                #Highlight if the bytes are different
                if (ch1 != ch2):
                    self.screen.addstr(y1, x1, ch1, curses.color_pair(1))
                    self.screen.addstr(y1, x1 + 2, " ")
                    self.screen.addstr(y2, x2, ch2, curses.color_pair(1))
                    self.screen.addstr(y2, x2 + 2, " ")
                else:
                    self.screen.addstr(y1, x1, ch1 + " ")
                    self.screen.addstr(y2, x2, ch2 + " ")

                #Update for next position
                x1 += 3
                x2 += 3

                byte_chunks += 1
                if byte_chunks % 4 == 0 and x1 < x1_max:
                    #Add additional space
                    self.screen.addstr(y1, x1, " ")
                    self.screen.addstr(y2, x2, " ")
                    x1 += 3
                    x2 += 3
                elif x1 >= x1_max:
                    x1 = x1_min
                    x2 = x2_min
                    y1 += 1
                    y2 += 1

                index += 1

        else:
            #Something has gone horribly wrong
            self.print_message("ERROR: Something has gone horribly wrong. I'm sorry.")


def main(stdscr):
    screen_instance = Screen(stdscr)

    #If 2 files provided, intialize 
    if len(sys.argv) >= 3:
        screen_instance.set_files(sys.argv[1], sys.argv[2])
        screen_instance.run()
    else:
    #Else, print error
        screen_instance.print_message("ERROR: Two files are required to compare them. Press any key to exit")

    stdscr.refresh()

wrapper(main)
