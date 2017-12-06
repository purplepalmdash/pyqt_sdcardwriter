import csv

import operator


def sort_by_column(csv_cont, col, reverse=False):
    header = csv_cont[0]
    body = csv_cont[1:]
    if isinstance(col, str):
        col_index = header.index(col)
    else:
        col_index = col
    body = sorted(body,
                  key=operator.itemgetter(col_index),
                  reverse=reverse)
    body.insert(0, header)
    return body


def csv_to_list(csv_file, delimiter=','):
    with open(csv_file, 'r') as csv_con:
        reader = csv.reader(csv_con, delimiter=delimiter)
        return list(reader)

def print_csv(csv_content):
    print(50*'-')
    for row in csv_content:
        row = [str(e) for e in row]
        print('\t'.join(row))
    print(50*'-')


def write_csv(dest, csv_cont):
    """ New CSV file. """
    with open(dest, 'w') as out_file:
        writer = csv.writer(out_file, delimiter=',')
        for row in csv_cont:
            writer.writerow(row)


#csv_cont1 = csv_to_list1('/home/dash/name2.csv')
#csv_cont = csv_to_list('/home/dash/name3.csv')
csv_cont = csv_to_list('/home/dash/name2.csv')

print('\n\n************************************')
print_csv(csv_cont)
print('\n\n************************************')
print('\n\nCSV sorted by column "col3":')
csv_sorted = sort_by_column(csv_cont, 'Name')
print('\n\n************************************')
print_csv(csv_sorted)
print('\n\n************************************')

#print('\n\nOriginal CSV file:')
#print_csv(csv_cont)

#print('\n\nCSV sorted by column "col3":')
#csv_sorted = sort_by_column(csv_cont, 'name')
#print_csv(csv_sorted)
#
#write_csv('/tmp/sorted.csv', csv_sorted)
