#!/usr/bin/python

"""
Output randomly shuffled lines from FILE.
"""

import random, sys, argparse

class Shuf:
    def __init__(self, input, do_repeat, count, filename = None):
        self.count = count
        self.do_repeat = do_repeat
        self.lines = [ ]  
        self.index = 0
        #'-' tells program to read from standard input
        if filename == "-":
            self.lines = sys.stdin.readlines()
        #check for input file
        elif filename != None:
            file = open(filename, 'r') #create file handle                                                                                                                                  
            self.lines = file.readlines() #reads the file to list of string
            file.close() #close file
        #-i or -e option
        elif input != None:
            self.lines = input
        #read from standard input
        else:
            self.lines = sys.stdin.readlines() 

        if self.count == -9000 and do_repeat == False:
            self.count = len(self.lines)
            
        #shuffle lines
        if self.count != 0 and do_repeat == False:
            self.lines = random.sample(self.lines, self.count)
    
    #The 2 methods below are so this object is iterable
    def __iter__(self):
        return self
    
    def __next__(self):
        if (self.count <= 0 or self.index == len(self.lines)) and self.do_repeat == False:
            raise StopIteration
        #if -r used without a -n then script goes forever
        elif self.do_repeat and self.count == -9000:
            return random.choice(self.lines)
        #Case where -n and -r both used
        elif self.do_repeat and self.count > 0:
            if self.count == self.index:
                raise StopIteration
            self.index += 1 
            return random.choice(self.lines)
        elif self.do_repeat == False and self.count > 0:
            self.count -= 1
            self.index += 1
            return self.lines[self.index - 1]

def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... FILE

Output randomly shuffled lines from FILE."""

    parser = argparse.ArgumentParser()

    parser.add_argument("File",
                        nargs='?',
                        action="store",
                        default=None)
    
    parser.add_argument("-n", "--head-count",
                      action = "store",
                      dest   = "count",
                      default = -9000,  #no significance to this default value, just so I cant check
                      help   = "Output at most count lines")

    parser.add_argument("-r", "--repeat",
                      action = "store_true",
                      dest   = "repeat",
                      default = False,
                      help   = "lines can be repeated in output")

    parser.add_argument("-e", "--echo",
                      action = "store",
                      dest   = "echo",
                      nargs = "+",
                      default = None,
                      help   = "Treat each command-line operand as an input line")
    
    parser.add_argument("-i", "--input-range",
                      action = "store",
                      dest   = "input_range",
                      default = None,
                      help   = "Act as if input came from a file containing the range of unsigned decimal integers lo…hi, one per line")

    args = parser.parse_args()

    input_string = None

    #check for head count
    count = int(args.count)
    if count != -9000 and count < 0:
        parser.error("invalid head count: {0}".format(args.count))
             
    #check for repeat 
    do_repeat = args.repeat

    #check for echo.
    try:
        if args.echo != None:
            temp = args.echo
            input_string = [x + "\n" for x in temp]
    except:
            parser.error("invalid echo input: '{0}'".format(args.echo))

    #Check for input range 
    try:
        if args.input_range != None:
            temp = str(args.input_range)
            input_range = temp.split("-")  #get list containing lower limit and upper limit
            if len(input_range) != 2:
                parser.error("invalid input range: {0}".format(args.input_range))
            lower_limit = int(input_range[0])
            upper_limit = int(input_range[1])
            if (upper_limit < lower_limit):  #check for valid number range
                parser.error("invalid input range: {0}".format(args.input_range))
            else:
                temp_list = [str(i) for i in range(lower_limit, upper_limit + 1)] #create list containing range of numbers
                input_string = [item + '\n' for item in temp_list]
    except:
            parser.error("invalid input range: '{0}'".format(args.input_range))

    filename = args.File;

    shuf = Shuf(input_string, do_repeat, count, filename)
    for lines in shuf:
        sys.stdout.write(lines)


if __name__ == "__main__":
    main()
