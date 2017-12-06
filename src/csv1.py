#!/usr/bin/env python
#-*- coding:utf-8 -*-
import csv

def main():
    with open('/home/dash/name1.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print ' '.join(row)
            #print ', '.join(row)

if __name__ == '__main__':
    main()