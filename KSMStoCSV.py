#! /usr/bin/python
# -*- coding: utf-8 -*-
# This script converts the XML generated from 'SMS Backup and Restore' to CSV
# The file I'm testing this with is a 19.1mb XML file that includes MMS
import xml.etree.ElementTree as ET
import csv
import os.path
import sys


def main(filename, csvfilename):
    tree = ET.parse(filename)
    root = tree.getroot()

    fields = []

    for child in root:
        fields.append([child.tag, child.attrib])

    # Get the SMS and MMS field names
    smsheader = fields[0][1].keys()
    mmsheader = fields[-1][1].keys()

    # Create SMS and MMS CSV filenames
    smsfile = os.path.join(os.path.dirname(csvfilename),
                           'SMS' + os.path.basename(csvfilename))
    mmsfile = os.path.join(os.path.dirname(csvfilename),
                           'MMS' + os.path.basename(csvfilename))

    # Write the SMS entries to a CSV file
    with open(smsfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(smsheader)
        for x in fields:
            rowtowrite = []
            if x[0] == 'sms':
                for y in smsheader:
                    rowtowrite.append(x[1][y].encode('ascii', 'ignore'))
                writer.writerow(rowtowrite)

    # Write the MMS entries to a CSV file
    with open(mmsfile, 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(mmsheader)
        for x in fields:
            rowtowrite = []
            if x[0] == 'mms':
                for y in mmsheader:
                    rowtowrite.append(x[1][y])
                writer.writerow(rowtowrite)

if __name__ == '__main__':
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        main(sys.argv[1], sys.argv[2])
    else:
        print "KSMStoCSV.py XMLFile CSVFile"
        print "  XMLFile needs to be the XML file you want to parse."
        print "  CSVFile is the name of the CSV file(s) to be created."
        sys.exit()
