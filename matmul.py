import random
import math
import numpy as np
import threading
import time


def geUserInput():
  fileA = input("Filename of CSV with matA: ")
  fileB = input("Filename of CSV with matB: ")
  poolSize = input("Thread pool size: ")
  matA = np.loadtxt(open(fileA, "rb"), delimiter=",")
  matB = np.loadtxt(open(fileB, "rb"), delimiter=",")
  print("matA = ", matA)
  print("matB = ", matB)
  


if __name__=="__main__":
  geUserInput()