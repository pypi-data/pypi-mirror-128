#!/usr/bin/python

'''a LIBrary implementing TGMK (Tebi-Gibi-Mebi-Kibi), a human-readable 1024-base integer representation, suitable for bits and bytes

A "TGMK literal" is a string made by:

    • zero or more leading blanks
    • an optional ('+' or '-') "sign"
    • one or more "1024-base-digits", each made by:
        • a "coefficient", an unsigned decimal integer constant, as '0', '1' or '10000'
        • a "scale factor", a letter in 'KMGTPEZYkmgtpezy')
    • zero or more trailing blanks

Letters have the following well-known meanings:

    ╔══════╤══════╤════╤══════════════════╤═══════╤═════════════════════════╗
    ║LETTER│PREFIX│LOG2│      LOG10       │LOG1024│          VALUE          ║
    ╟──────┼──────┼────┼──────────────────┼───────┼─────────────────────────╢
    ║K/k   │kibi- │  10│ 3.010299956639812│      1│                     1024║
    ║M/m   │mebi- │  20│ 6.020599913279624│      2│                  1048576║
    ║G/g   │gibi- │  30│ 9.030899869919436│      3│               1073741824║
    ║T/t   │tebi- │  40│12.041199826559248│      4│            1099511627776║
    ║P/p   │pebi- │  50│ 15.05149978319906│      5│         1125899906842624║
    ║E/e   │exbi- │  60│ 18.06179973983887│      6│      1152921504606846976║
    ║Z/z   │zebi- │  70│21.072099696478684│      7│   1180591620717411303424║
    ║Y/y   │yobi- │  80│24.082399653118497│      8│1208925819614629174706176║
    ╚══════╧══════╧════╧══════════════════╧═══════╧═════════════════════════╝

Only the last 1024-base-digit may lack the letter, meaning unities.

Scale factor letters must appear left to right in strictly decreasing order:

    • '3m5k7' is ok, its value is 3 * 1024 ** 2 + 5 * 1024 + 7 = 3150855
    • '5k3m7' is wrong
    • '5k3k7' is wrong too

In coefficients one or more leading zeros are allowed, while commas are not:

    • '04096m' is ok
    • '4,096m' is wrong

A TGMK literal is "normalized" if:

    • no leading or trailing blanks are present
    • sign is '-' for negative numbers, absent for zero or positive numbers
    • coefficients are between 1 and 1023, with no leading zeros, with two exceptions:
        • normalized TGMK literal for zero is '0'
        • for very large numbers the coefficient preceding 'Y' can get any value
    • scale factor letters are always uppercase

TGMK format is implemented by two functions, tgmk2int() and int2tgmk(), both allowing
str or int arguments. So, if s is a str containing a TGMK literal (normalized
or not) and i is an int, then:

    • tgmk2int(s) returns s converted to int
    • tgmk2int(i) returns i unchanged
    • int2tgmk(i) returns i converted to a str in normalized TGMK format
    • int2tgmk(s) returns s translated as a str in normalized TGMK format
    
Usage:

    >>> from libtgmk import tgmk2int, int2tgmk
'''

__version__ = '0.4.1'

# functions

def tgmk2int(x='0'):
    '''x can be str or int, if x is str then it must be a TGMK literal (normalized or not),
and is converted from TGMK format into int:

    >>> tgmk2int('-3000k1)
    -3072001

else if x is int then is returned unchanged:

    >>> tgmk2int(-3000 * 1024 - 1)
    -3072001

If argument is not given then result is 0.
'''
    if isinstance(x, int):
        return x
    elif not isinstance(x, str):
        raise TypeError(f'invalid argument type for tgmk2int(): must be str or int')
    else:
        tgmk = x.upper().strip()
        if tgmk in {'','+','-'}:
            raise ValueError(f'invalid TGMK literal for tgmk2int(): {x!r}')
        tgmk, minus = (tgmk[1:], tgmk[0] == '-') if tgmk[0] in '+-' else (tgmk, False)
        last, num, digit = 999, 0, 0
        for jchar, char in enumerate(tgmk):
            this = '0123456789KMGTPEZY'.find(char)
            if this < 0:
                raise ValueError(f'invalid TGMK literal for tgmk2int(): {x!r}')
            elif this <= 9:
                digit = digit * 10 + this
            elif last <= this:
                raise ValueError(f'invalid TGMK literal for tgmk2int(): {x!r}')
            else:
                last = this
                num += digit * 1024 ** (this - 9)
                digit = 0
        return -(num + digit) if minus else num + digit
        
def int2tgmk(x=0):
    '''x can be int or str, if x is int then it's converted into normalized TGMK format:

    >>> int2tgmk(-3000 * 1024 - 1)
    '-2M952K1'

else if x is str then it must be a TGMK literal (normalized or not) and it's converted
from TGMK into int and back from int into TGMK normalized format:

    >>> int2tgmk('-3000k1')
    '-2M952K1'

If argument is not given then result is '0'.
'''
    if isinstance(x, str):
        try:
            return int2tgmk(tgmk2int(x))
        except ValueError:
            raise ValueError(f'invalid TGMK literal for int2tgmk(): {x!r}')
    elif not isinstance(x, int):
        raise TypeError('int2tgmk(): argument must be int or str')
    elif -1024 < x < 1024:
        return str(x)
    else:
        num, sign = (-x, '-') if x < 0 else (x, '')
        tgmk = ''
        for char in ['','K','M','G','T','P','E','Z','Y']:
            num, mod = (0, num) if char == 'Y' else divmod(num, 1024)
            if mod:
                tgmk = str(mod) + char + tgmk
            if num == 0:
                return sign + tgmk
