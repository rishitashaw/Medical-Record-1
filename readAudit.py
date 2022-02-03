from sqloperations import *
from emailoperations import *

def audit():
  k=readAudit()
  sendLogEmail(k)
  print(k)
