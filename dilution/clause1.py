import sys
import time
sys.path.append("/home/sukanta/App/z3-master/build")
from z3 import *

s = Optimize()
X1, Y1, x1, y1, s1 = Ints('X1 Y1 x1 y1 s1')
X2, Y2, x2, y2, s2 = Ints('X2 Y2 x2 y2 s2')
X3, Y3, x3, y3, s3 = Ints('X3 Y3 x3 y3 s3')
w21 = Int('w21')
w31, w32 = Ints('w31 w32')


t1, t2 = Ints('t1 t2')
s.add(16*x1 + 1*t1 + 4*t2 == X1)
s.add(Implies((w21 == 0), (t1 == 0)))
s.add(Implies((w21 == 1), (t1 == 1*X2)))
s.add(Implies((w21 == 2), (t1 == 2*X2)))
s.add(Implies((w21 == 3), (t1 == 3*X2)))
s.add(Implies((w31 == 0), (t2 == 0)))
s.add(Implies((w31 == 1), (t2 == 1*X3)))
s.add(Implies((w31 == 2), (t2 == 2*X3)))
s.add(Implies((w31 == 3), (t2 == 3*X3)))

t3 = Int('t3')
s.add(4*x2 + 1*t3 == X2)
s.add(Implies((w32 == 0), (t3 == 0)))
s.add(Implies((w32 == 1), (t3 == 1*X3)))
s.add(Implies((w32 == 2), (t3 == 2*X3)))
s.add(Implies((w32 == 3), (t3 == 3*X3)))

s.add(1*x3 == X3)

t4, t5 = Ints('t4 t5')
s.add(16*y1 + 1*t4 + 4*t5 == Y1)
s.add(Implies((w21 == 0), (t4 == 0)))
s.add(Implies((w21 == 1), (t4 == 1*Y2)))
s.add(Implies((w21 == 2), (t4 == 2*Y2)))
s.add(Implies((w21 == 3), (t4 == 3*Y2)))
s.add(Implies((w31 == 0), (t5 == 0)))
s.add(Implies((w31 == 1), (t5 == 1*Y3)))
s.add(Implies((w31 == 2), (t5 == 2*Y3)))
s.add(Implies((w31 == 3), (t5 == 3*Y3)))

t6 = Int('t6')
s.add(4*y2 + 1*t6 == Y2)
s.add(Implies((w32 == 0), (t6 == 0)))
s.add(Implies((w32 == 1), (t6 == 1*Y3)))
s.add(Implies((w32 == 2), (t6 == 2*Y3)))
s.add(Implies((w32 == 3), (t6 == 3*Y3)))

s.add(1*y3 == Y3)


s.add(x1 + y1 + w21 + w31 == 4)
s.add(x2 + y2 + w32 == 4)
s.add(x3 + y3 == 4)


s.add(w21  <= 4)
s.add(w31 + w32  <= 4)


s.add(And(X1 >= 0, Y1 >= 0, x1 >= 0, x1 <= 3, y1 >= 0, y1 <= 3))
s.add(And(X2 >= 0, Y2 >= 0, x2 >= 0, x2 <= 3, y2 >= 0, y2 <= 3))
s.add(And(X3 >= 0, Y3 >= 0, x3 >= 0, x3 <= 3, y3 >= 0, y3 <= 3))
s.add(And(w21 >= 0, w21 <= 3))
s.add(And(w31 >= 0, w31 <= 3, w32 >= 0, w32 <= 3))
s.add(s3 == 0)
s.add(s2 == s3 )
s.add(s1 == s2 + w31 )
s.add(s1 <= 2)
s.add(And(X1 == 47, Y1 == 17))


sample = s.minimize(x1 + x2 + x3)
buff = s.minimize(y1 + y2 + y3)
startTime = time.time()
print (s.check())
print ("sample = ", sample.value(), "buffer = ", buff.value())
endTime = time.time()
executionTime = endTime - startTime
print ("Execution Time = ",executionTime)
fp = open('op','w')
lst = s.model()
for i in lst:
    fp.write(str(i) + " = " + str(s.model()[i]) + '\n')
