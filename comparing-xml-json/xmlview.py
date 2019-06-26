#!/usr/bin/env python3

import sys
import xml.dom.minidom

args = sys.argv[1:]
txt = open(args[0]).read() if args else sys.stdin.read()
print(xml.dom.minidom.parseString(txt).toprettyxml())