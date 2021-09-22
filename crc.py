"""
crc.py
This program is a simple implementation of 
cyclic redundancy check (CRC) taught in EIE2050
"""

global debug
debug = 1   # enable printing calculation process

# GF(2) xor arithmetic of bit strings
def str_xor(a, b):
    # initialize result
    result = ""
    
    # Traverse all bits, if bits are
    # same, then XOR is 0, else 1
    for i in range(0, len(b)):
        if a[i] == b[i]:
            result += '0'
        else:
            result += '1'
    
    result = result.lstrip('0')

    if len(result) == 0:  
        # 2 strings are the same
        return '0'
    else:
        return result


def solve(data, Gcode):
    
    Dlen = len(data)
    Glen = len(Gcode)
    cnt = Glen
    temp = data[:cnt]

    # 
    if debug:
        print(data)
        print(Gcode+'|'*(Dlen-Glen))
        print('-'*Glen+'|'*(Dlen-Glen))
    # 
    
    while cnt < len(data):
        
        temp = str_xor(temp, Gcode)

        if Dlen - cnt <= Glen - len(temp):
            temp += data[cnt:]
            # 
            if debug:
                print(' '*(Dlen-len(temp)), end='')
                print(temp)
            #
            while len(temp) < Glen:
                temp = '0' + temp 
            break

        space = cnt - len(temp)
        while len(temp) < Glen:
            temp += data[cnt]
            cnt += 1

        # 
        if debug:
            print(' '*space+temp+'|'*(Dlen-space-Glen))
            print(' '*space+Gcode+'|'*(Dlen-space-Glen))
            print(' '*space+'-'*Glen+'|'*(Dlen-space-Glen))            
        # 
    
    return temp


def encode(data, Gcode):
    # Append 0s to the data
    data += '0'*len(Gcode)
    result = solve(data, Gcode)
    return result


def decode(data, Gcode):
    result = solve(data, Gcode)
    return result, result.lstrip('0') == ''
    

# Driver code
if __name__ == '__main__':
    # data = "11010011"
    # gcode = "1010"
    data = input("Data to be transmitted: ")
    gcode = input("Generator code: ")
    print()

    key = encode(data, gcode)
    msg = data+key

    print("Check sum is", key)
    print("The transmitted CRC is", msg)
    print()

    res, flag = decode(msg, gcode)

    print("Remainder is", res)
    if flag:
        print("No error!")
    else:
        print("Error detected！")
