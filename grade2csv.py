#!/usr/bin/python
#
# Copyright May 2011, Jim Clarke,
# University of Toronto, Department of Computer Science
# http://www.cdf.toronto.edu/~clarke/grade/
#
# Read a file in the DCS standard grades format and write the student
# marks to a "Comma Separated Values" file to be read by a
# spreadsheet application.
#
# Significant data ignored include (1) the entire header and
# (2) lines containing comments about students. The purpose of
# this program is to produce files that can be used to submit marks
# to a system such as the Engineering marks reception process, so
# those data are not needed, though you may want to do some fixing
# based on the omitted items.
#
# Comments within student marks should be removed before running this
# program. They will be left in, and the spreadsheet will be probably
# consider those cells as badly formatted.
#
# The drop and other flags are copied but not used.
#
# The grades file is not checked for validity. Use glint first.
#
# The input file name is the one required command-line argument:
#
#   grade2csv.py gradefile.grade
#
# You must use the -9 option if your grades file has 9-digit student
# numbers (instead of 10-digit). If you don't, the output .csv file
# will be mangled:
#
#   grade2csv.py -9 gradefile.grade

import sys, csv

student_number_len = 10

if len(sys.argv) == 3 and sys.argv[1] == '-9':
    student_number_len = 9
    filename = sys.argv[2]
elif len(sys.argv) == 2:
    filename = sys.argv[1]
    if filename == '-9':
        print >> sys.stderr, \
            'Usage: grade2csv [-9] gradesfile.grade [ > stdoutfile]'
        sys.exit(1)
else:
    print >> sys.stderr, \
        'Usage: grade2csv [-9] gradesfile.grade [ > stdoutfile]'
    sys.exit(1)

# Open the input file.
infile = open(filename)

# Skip the header.
lineNum = 0
while infile.readline() != '\n':
    lineNum += 1

# Make the csv output file.
writer = csv.writer(sys.stdout)

# Read the student data lines and output them as CSV.
while True:
    line = infile.readline()
    if line == '':
        break  # We're done.
    lineNum += 1

    # Delete trailing newline.
    if line[-1] != '\n':
        print >> sys.stderr, "No newline at end of line", lineNum
    line = line[:-1]

    # Break into parts: ID, then marks.
    marks = line.split('\t')
    ID = marks[0]
    marks = marks[1:]

    # Isolate the identifying information, skipping comment lines.
    if len(ID) < student_number_len + 1:
        print >> sys.stderr, "Too-short line at line", lineNum
        continue
    if ID[student_number_len] == '*':
        continue
    if len(ID) < student_number_len + 6:  # two characters for name!
        print >> sys.stderr, "Too-short line at line", lineNum
        continue
    stunum = ID[:student_number_len]
    flags = ID[student_number_len:student_number_len + 4]
    name = ID[student_number_len + 4:]

    # Make a single list out of the student data.
    output = [stunum, flags, name]
    output += marks
    writer.writerow(output)
