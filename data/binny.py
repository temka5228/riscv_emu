from sys import argv

def main(argv, argc):
    if argc < 3:
        raise Exception("Not enough parameters")
    else:
        print(argv[1], argv[2])
        convertor(argv[1], argv[2])

def convertor(fnin, fnout):
    with open(fnin, 'r') as fin:
        with open(fnout, 'wb') as fout:
            hex_str = ''.join(line.strip() for line in fin)
            binary_data = bytes.fromhex(hex_str)
            fout.write(binary_data)
if __name__ == '__main__':
    main(argv, len(argv))