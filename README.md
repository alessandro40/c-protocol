# c-protocol
c-protocol generates C functions to compose (write) and process (read) packets for byte-oriented network protocol, described in a JSON file (see example.json).

The program is designed to work using:
* little-endian for the packet composition
* `uint8_t` array as buffer for the packet
* `uint*_t` as variable's type

##JSON
For an example of the JSON file, see example.json.

Basically, it is an array of packets (objects) and each packet contains a name (string) and an array of fields (objects). The fields can be fixed (assuming always the same value) or not (the variable to write to/from is passed as argument). 


##Usage

```
python c_protocol.py [-h] [-p | -i] [-o outfile] json

positional arguments:
  json                  file containing the JSON

optional arguments:
  -h, --help            show this help message and exit
  -p, --prototype       create only the prototype of the functions
  -i, --implementation  create only the implementation of the functions
  -o outfile            save output to file
```

##Note
This program has been designed for a specific purpose (see [wall-ev3](http://github.com/alessandro40/wall-ev3)), so there is not much customization available, so far.
