from __future__ import print_function
import argparse
import json
import sys

def prototype_read(pkt, indent, f_out):
    """"Write the prototype of foo_read()"""
    print('void read_{}(uint8_t *pkt'.format(pkt["name"]), end='', file=f_out)
    for field in pkt['fields']:
        if 'value' not in field:
            print(', {} *{}'.format(field["type"], field["name"]), end='', file=f_out)
    print(')', end='', file=f_out)

def prototype_write(pkt, indent, f_out):
    """"Write the prototype of foo_write()"""
    print('void write_{}(uint8_t *pkt'.format(pkt["name"]), end='', file=f_out)
    for field in pkt['fields']:
        if 'value' not in field:
            print(', {} {}'.format(field["type"], field["name"]), end='', file=f_out)
    print(')', end='', file=f_out)

def field_read(variable, offset, size, indent, f_out):
    """"Write the code to read a field of the packet"""
    print('{}*{} = *((uint8_t *) pkt + {});'.format(indent, variable, offset), file=f_out)
    if size > 1:
        for i in range(1, size):
            print('{}*{} += (*((uint8_t *) pkt + {}) << {});'.format(indent, variable, offset + i, 8*i), file=f_out)

def field_write(variable, offset, size, indent, f_out):
    """"Write the code to write a field of the packet"""
    if size is 1:
        print('{}*((uint8_t *) (pkt + {})) = {};'.format(indent, offset, variable), file=f_out)
    else:
        print('{}*((uint8_t *) (pkt + {})) = {} & 0xFF;'.format(indent, offset, variable), file=f_out)
        for i in range(1, size):
            print('{}*((uint8_t *) (pkt + {})) = ({} >> {}) & 0xFF;'.format(
                indent, offset + i, variable, 8*i), file=f_out)

def packet_read(pkt, indent, f_out):
    """"Write the function to read a packet"""
    prototype_read(pkt, indent, f_out)
    print('\n{', file=f_out)
    offset = 0
    for field in pkt['fields']:
        if 'value' not in field:
            field_read(field['name'], offset, field['size'], indent, f_out)
        offset += field['size']
    print('}', file=f_out)

def packet_write(pkt, indent, f_out):
    """"Write the function to write a packet"""
    prototype_write(pkt, indent, f_out)
    print('\n{', file=f_out)
    offset = 0
    for field in pkt['fields']:
        if 'value' not in field:
            field_write(field['name'], offset, field['size'], indent, f_out)
        else:
            field_write(field['value'], offset, field['size'], indent, f_out)
        offset += field['size']
    print('}', file=f_out)

def create_implementation(prot, indent, f_out):
    """"Write the implementation of the functions"""
    print('/* File automatically generated */\n', file=f_out)
    print('#include <stdint.h>', file=f_out)

    for pkt in prot:
	print('', file=f_out)
        packet_read(pkt, indent, f_out)
	print('', file=f_out)
        packet_write(pkt, indent, f_out)

def create_prototypes(prot, indent, f_out):
    """"Write the prototype of the functions"""
    print('/* File automatically generated */\n', file=f_out)
    print('#include <stdint.h>', file=f_out)

    for pkt in prot:
	print('', file=f_out)
        prototype_read(pkt, indent, f_out)
	print(';', file=f_out)
	prototype_write(pkt, indent, f_out)
	print(';', file=f_out)

def main_fn():
    parser = argparse.ArgumentParser(description='generate C functions to compose and process byte-oriented network protocol.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--prototype", help="create only the prototype of the functions", action="store_true")
    group.add_argument("-i", "--implementation", help="create only the implementation of the functions", action="store_true")
    parser.add_argument('-o', help="save output to file", metavar='outfile')
    parser.add_argument('filename', metavar='json',
                   help='file containing the JSON') 
    args = parser.parse_args()

    f_in = open(args.filename, 'r')
    if args.o:
        f_out = open(args.o, 'w')
    else:
        f_out = sys.stdout

    try:
        prot = json.loads(f_in.read())
    except ValueError:
        print('Decode of JSON failed', file=stderr)
        return

    indent = 4*' '

    if args.prototype:
        create_prototypes(prot, indent, f_out)
    elif args.implementation:
	create_implementation(prot, indent, f_out)
    else:
        create_prototypes(prot, indent, f_out)
	create_implementation(prot, indent, f_out)

if __name__ == "__main__":
    main_fn()
