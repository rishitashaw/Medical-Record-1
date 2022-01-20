from sqloperations import *
from emailoperations import *

k=readAudit()
sendLogEmail(k)
print(k)
