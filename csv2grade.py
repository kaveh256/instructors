#!/usr/bin/python

# CAUTION! Requires Python 2.

# Read an Excel file saved as "Comma Separated Values" and write to standard
# output lines that would be the corresponding student records in a DCS grade
# file. The input file name is the single command-line argument:
#
#   csv2grade mygrades.csv
#
# The input lines in the Excel file are assumed to contain these fields,
# separated by tabs: student number, family name, given names, mark, mark....
# There is also very likely a control-M (carriage return) at the end of the
# line; this does not appear in the output.
#
# The assumptions about file format are a simplification of Blackboard's
# format for downloaded files. (See also bb2grade.py.) If you have a similar
# but not identical file format -- for example, with an extra column of some
# kind -- you will probably want to change those assumptions, perhaps simply
# by modifying the line marked "You may want to change this." Watch out,
# however, for other fixes that might be needed.
#
# If the first line of input does not begin with a decimal digit, it is
# probably a line of column labels, so it is silently skipped over. Lines
# containing only white-space are also skipped. Trouble in other lines is
# reported with error messages.

# Jim Clarke, Feb 2011

# Nov 29/12: added 'b' mode to open() call, at Kaveh Ghasemloo's suggestion.
#   It's probably needed sometimes, and probably harmless at other times.

import sys, csv

if len(sys.argv) != 2:
    print >> sys.stderr, 'Usage: csv2grade mygrades.csv [ > stdoutfile]'
    sys.exit(1)

reader = csv.reader(open(sys.argv[1], 'Ub')) # 'U' is universal-newline mode

lineNum = 0
for line in reader:
    lineNum += 1
    if len(line) == 0:
        continue
    
    stunum, family, given = line[:3] # You may want to change this.
    if not stunum[0].isdigit():
        if lineNum == 1:
            continue
        else:
            print >> sys.stderr, 'Line ', lineNum, ' begins with non-digit:'
            print >> sys.stderr, line
            sys.exit(1)
            
    marks = line[3:]
    output_line = stunum + '    ' + family + '  ' + given
    
    for m in marks:
        output_line += '\t' + m
    print output_line
