"""
This file sets up the DAGS
"""

import sys, os
os.chdir('/home/dark-aengl/robo/mnist/')

# import custom
from processes import process



mnist_process = process()
mnist_dag = mnist_process.get_dag()

