import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)
parent = os.path.dirname(current)
sys.path.append(parent)
