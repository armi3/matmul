import numpy as np
import sys, time
import pandas as pd
from threading import Thread
import logging
import traceback


def geUserInput():
  if len(sys.argv) == 5:
    try:
      matA = np.loadtxt(open(sys.argv[1], "rb"), delimiter=",")
      matB = np.loadtxt(open(sys.argv[2], "rb"), delimiter=",")
      if int(sys.argv[3]) >= 1:
        poolSize = int(sys.argv[3])
      outputFilename = sys.argv[4]
      return matA, matB, poolSize, outputFilename
    except Exception as e:
      print("\nERROR: An exception ocurred. Check your arguments.\n")
      logging.error(traceback.format_exc())

  else:
    print("\nERROR: The multiplier takes exactly 4 arguments but {} where given. Example: \n\n\t matmul.py file1.csv file2.csv pool_size (min = 1 thread) output.out\n".format(str(len(sys.argv))))
  exit()


def checkDimensions(matA, matB):
  print("\n🔎  Checking matrices dimensions...")
  l = m1 = m2 = m = n = 0
  print("matA shape = {}".format(matA.shape))
  print("matB shape = {}".format(matB.shape))
  
  l = matA.shape[0]
  m1 = matA.shape[1]
  m2 = matB.shape[0]
  n = matB.shape[1]
  
  if m1 == m2:
    print("\n👍  The matrices are multipliable...")
    m = m1
    if l == m == n:
      print("👍  The matrices are of the same dimentions, too!")
      return l, m, n
  else:
    print("\n👎  The matrices aren't multipliable...")
  print("\n👎  But they have different dimentions...")
  exit()


def matmul(matA, matB, start, end):
  global matC
  n = matA.shape[0]
  for i in range(start, end):
    for j in range(n):
      for k in range(n):
        matC[i][j] += int(matA[i][k] * matB[k][j])
        print("matmul, i = {}, j = {}, matC[i][j] = {}".format(i, j, matC[i][j]))


def parallelMatmul(matA, matB, matC, poolSize):
  threadHandle = []
  n = matA.shape[0]

  for j in range(0, poolSize):
    thread = Thread(target = matmul, args=(matA, matB, int((n/poolSize) * j), int((n/poolSize) * (j+1))))
    threadHandle.append(thread)
    thread.start()   
  
  for j in range(0, poolSize):
    threadHandle[j].join()


if __name__=="__main__":
  matA, matB, poolSize, outputFilename = geUserInput()
  print("\nmatA =\n", matA)
  print("\nmatB =\n", matB)
  print("\n🧵  Pool size = ", poolSize)

  matA = matA.astype(int)
  matB = matB.astype(int)

  l, m, n = checkDimensions(matA, matB)
  
  global matC
  matC = np.zeros((n, n))
  matC = matC.astype(int)
  
  startTime = time.time()
  parallelMatmul(matA, matB, matC, poolSize)
  endTime = time.time()
  print("\nElapsed time = {} seconds.".format(str(startTime - endTime)))
  
  try:
    #np.savetxt(outputFilename, matC, delimiter=',')
    pd.DataFrame(matC).to_csv(outputFilename, header=None, index=None)
    print("\n👍  Output file saved!")
  except Exception as e:
    print("\n👎  Exception saving matC to output file.")
    logging.error(traceback.format_exc())

