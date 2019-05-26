from curses import wrapper
import curses
import sys
import math

UP      = 1
DOWN    = -1
LEFT    = 1
RIGHT   = -1

class Screen(object):
    def __init__(self, scrn):
        #stdscr object
        self.screen = scrn

        #Default values
        self.top = 0
        self.data = ["", ""]

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
        
        #Print this data
        self.print_data()

        #Move cursor to start of file1
        self.screen.move(1, 1 + int(curses.COLS/10))

    def take_input(self):
        while True:
            self.screen.refresh()
            ch = self.screen.getch()

            #Options for input
            if ch == curses.KEY_DOWN:
                #Scroll Down
                scroll(self.screen, DOWN)
            elif ch == curses.KEY_UP:
                #Scroll Up
                scroll(self.screen, UP)
            elif ch == curses.KEY_RIGHT:
                #Move cursers right
                move_to(self.screen, RIGHT)
            elif ch == curses.KEY_LEFT:
                #Move cursers left
                move_to(self.screen, LEFT)
            elif ch == ord('q'):
                break
            else:
                #Unknown input
                print("unkown input")

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
        if direction < 0:
            #Scroll down
            print("scroll down")
        elif direction > 0:
            #Scroll up
            print("scroll up")
        else:
            #Bad input
            print("bad input")
        self.top += direction

    def move_to(self, direction):
        if direction < 0:
            #Move to the right
            print("move right")
        elif direction > 0:
            #Move to the left
            print("move left")
        else:
            #Uknown input
            print("uknown input")

    def take_input(self):
        while True:
            self.screen.refresh()
            ch = self.screen.getch()

            #Options for input
            if ch == curses.KEY_DOWN:
                #Scroll Down
                scroll(self.screen, DOWN)
            elif ch == curses.KEY_UP:
                #Scroll Up
                scroll(self.screen, UP)
            elif ch == curses.KEY_RIGHT:
                #Move cursers right
                move_to(self.screen, RIGHT)
            elif ch == curses.KEY_LEFT:
                #Move cursers left
                move_to(self.screen, LEFT)
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
                index = self.top * 12
            else:
                #Assume something broke
                self.print_message("I'm sorry, we lost track of the lines")

            x1 = x1_min
            x2 = x2_min

            byte_chunks = 0

            #Loop until both files are out of bytes OR we printed to the end of the page
            while (ch1 != "" or ch2 != "") and (y1 < curses.LINES):
                if (len(self.data[0]) <= index):
                    ch1 = ""
                else:
                    ch1 = self.data[0][index]

                if (len(self.data[1]) <= index):
                    ch2 = ""
                else:
                    ch2 = self.data[1][index]


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
