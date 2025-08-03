# -*- coding: utf-8 -*-
# Copyright (c) 2025
#
# Comaptible with Python 2.7 + and Python 3.x
#
# With this script you can run examples for the Diffie-Hellmann Key exchange
#
# Author:
#   Xenia Bogomolec, xb@quant-x-sec.com
#
################################################################################################
########################################### FUNCTIONS ##########################################
################################################################################################

import binascii, io, os, platform, sys
from datetime import datetime


# global variables
DH_args = {}
required_args = {
    "-p": "prime",
    "-g": "base",
    "-a": "Alice's secret",
    "-b": "Bob's secret",
}


#################################### PYTHON VERSION VARIANTS ##################################

def v_bytes(string):
    return bytes(string, "utf-8") if sys.version_info[0] == 3 else string

def v_input(string):
    return input(string) if sys.version_info[0] == 3 else raw_input(string)


################################## OS RELATED TERMINAL VARIANTS ###############################    

def clearConsole():
    command = "cls" if platform.system().lower().startswith("win") else "clear"
    os.system(command)

def terminalSize():
    if platform.system().lower().startswith("linux"):
        os.system("resize -s 40 120")
        return 120
    elif platform.system().lower().startswith("win"):
        os.system("mode con: cols=120 lines=40")
        return 120
    else: 
        return 80


#################################### DIFFIE-HELLMANN CLASS ####################################

class DiffieHellmann(object):

    start_exchange = 0
    end_exchange = 0
    usage = """

This is a purely mathematical Diffie-Hellman key exchange demonstrator!
It is not valid for serious encryption applications!
Run it like this: 

  python diffieHello.py -p prime -g base -a Alice's secret -b Bob's secret

  1. where prime is a prime number
  2. base is a primitive root modulo p and such g < p
  3. Alice's secret is a number < p
  4. Bob's secret is a number < p
        """

    def start(self, argv):

        if len(argv) == 1:
            print(self.usage)
            sys.exit()

        self.parse_args(argv)
        self.computeDiffie()


    ### build a dictionary of valid arguments 
    def parse_args(self, strings):
        missing_args = set(required_args.keys()) - set(strings)
        if len(missing_args) > 0:
            print("\n")
            for arg in missing_args:
                print("   You forgot to define {}".format(required_args[arg]) )
            sys.exit()
        if len(strings) == 9:
            for string in strings[1:-1]:
                nextString = strings[strings.index(string) + 1]
                if string.startswith("-") and nextString.isdigit():
                    DH_args[string] = int(nextString)
            self.validateArgs()
        else: 
            print(self.usage)
            sys.exit()

    ### prepare arguments for computation
    def validateArgs(self):
        for arg in (set(required_args.keys()) - set(DH_args.keys())):
            print("\n   You forgot to define {}".format(required_args[arg]) )
            sys.exit()
        if self.prime(DH_args["-p"]) == False:
            v_input("\n   {} is not a prime number, enter a new choice for -p which is prime: ".format(DH_args["-p"]))
        if self.primitiveRoot(DH_args["-g"], DH_args["-p"]) == False:
            v_input("\n   {} is not a primitive root of {}, enter a new choice for -g: ".format(DH_args["-g"], DH_args["-p"]))
        for char in ["-g", "-a", "-b"]:
            if DH_args[char] >= DH_args["-p"]:
                v_input("\n   {} should be smaller than {}, enter a new choice for {}: ".format(DH_args[char], DH_args["-p"], required_args[char]))

    ### primality test
    def prime(self, p):
        return not (
            (p < 2) or # 0 and 1
            (p > 2 and p % 2 == 0) or # even numbers > 2
            any(p % x == 0 for x in range(3, int(p ** 0.5) + 1, 2))
        )

    ### A short version of the primality test is:
    # return not (p < 2 or any(p % x == 0 for x in range(2, int(p ** 0.5) + 1)))
    ### keep the long version for an easier understanding

    ### primitive root test
    def primitiveRoot(self, g, p):
        return g**((p-1)/2) % p == -1

    def computeDiffie(self):
        alicePub = (DH_args['-g']**DH_args['-a']) % DH_args['-p']
        bobPub = (DH_args['-g']**DH_args['-b']) % DH_args['-p']
        privateKey1 = (alicePub**DH_args['-b']) % DH_args['-p']
        privateKey2 = (bobPub**DH_args['-a']) % DH_args['-p']
        print("\nAlice's public key is {},\nAlice's public key is {},\nprivate keys are equal: {},".format(str(alicePub), str(bobPub), str(privateKey1 == privateKey2)))
        

if __name__ == '__main__':

    DiffieHellmann().start(sys.argv)



#
#
#                          m    m      \           /      m    m   
#                      m            m   \    n    /   m            m
#                       m              m \  OOO  / m              m
#                         m              m\/ Ö \/m              m
#                            m             mÖÖÖm            m
#                                 m    m    ÖÖÖ    m    m
#                                    m   m   Ö   m   m
#                           m               /Ö\              m
#                       m              |   / Ö \   |             m
#                     m               m   !  Ö  !   m              m
#                      m          m   /   !  Ö  !   \   m          m
#                         m  m            !  Ö  !           m  m
#                                        /   Ö   \
#                                            Ö
#                                            Ö
#                                            Ö
#                                            Ö
#                                            Ö
#
#
