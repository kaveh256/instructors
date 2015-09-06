#!/usr/bin/python
#
# Copyright Feb. 2011, Jim Clarke,
# University of Toronto, Department of Computer Science
# http://www.cdf.toronto.edu/~clarke/grade/
#
# Read an Excel file saved as "Comma Separated Values" and write to standard
# output lines that would be the corresponding student records in a DCS grade
# file. The input file name is the single command-line argument:
#
#   csv2grade mygrades.csv
#
# The input lines in the Excel file are assumed to contain these fields,
# separated by tabs:
#   student_number, lastname, firstname, mark, mark, ...
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
import sys, csv

if len(sys.argv) != 2:
    sys.stderr.write('Usage: csv2grade.py mygrades.csv [ > outfile]')
    sys.exit(1)

# Open the input file.
# 'U' is for universal-newline mode.
# For Python 3.x use text mode. For Python 2.x use binary mode.
reader = csv.reader(open(sys.argv[1], 'U'))

for line in reader:
    # Skip empty lines.
    if len(line) == 0:
        continue

    # You may want to change this.
    student_num, status, lastname, firstname = line[:4]
    if status == '':
        status = ' '

    if not student_num[0].isdigit():
        if reader.line_num == 1:
            continue
        else:
            sys.stderr.write('Line ' + str(reader.line_num) +
                             ' begins with non-digit:\n' + str(line))
            sys.exit(1)

    # Convert old student numbers to 10 digit student numbers.
    if len(student_num) == 9:
        student_num = '0' + student_num

    # The student's information: sn, status, lastname, firstname
    output_line = student_num + ' ' + status + '  ' + '_'.join(lastname.split(
    )) + ' ' + '_'.join(firstname.split())

    # The student's marks.
    for mark in line[4:]:
        output_line += '\t' + mark

    # Finish the line.
    output_line += '\n'

    # Write the line to the output.
    sys.stdout.write(output_line)
