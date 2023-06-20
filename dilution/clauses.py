import sys
import time
sys.path.append("/home/sukanta/App/z3-master/build")
from z3 import *

def z3Solver(r11, r12):
    s = Optimize()
    X1, Y1, x1, y1, s1 = Ints('X1 Y1 x1 y1 s1')
    X2, Y2, x2, y2, s2 = Ints('X2 Y2 x2 y2 s2')
    X3, Y3, x3, y3, s3 = Ints('X3 Y3 x3 y3 s3')
    X4, Y4, x4, y4, s4 = Ints('X4 Y4 x4 y4 s4')
    w21 = Int('w21')
    w31, w32 = Ints('w31 w32')
    w41, w42, w43 = Ints('w41 w42 w43')


    t1, t2, t3 = Ints('t1 t2 t3')
    s.add(64*x1 + 1*t1 + 4*t2 + 16*t3 == X1)
    s.add(Implies((w21 == 0), (t1 == 0)))
    s.add(Implies((w21 == 1), (t1 == 1*X2)))
    s.add(Implies((w21 == 2), (t1 == 2*X2)))
    s.add(Implies((w21 == 3), (t1 == 3*X2)))
    s.add(Implies((w31 == 0), (t2 == 0)))
    s.add(Implies((w31 == 1), (t2 == 1*X3)))
    s.add(Implies((w31 == 2), (t2 == 2*X3)))
    s.add(Implies((w31 == 3), (t2 == 3*X3)))
    s.add(Implies((w41 == 0), (t3 == 0)))
    s.add(Implies((w41 == 1), (t3 == 1*X4)))
    s.add(Implies((w41 == 2), (t3 == 2*X4)))
    s.add(Implies((w41 == 3), (t3 == 3*X4)))

    t4, t5 = Ints('t4 t5')
    s.add(16*x2 + 1*t4 + 4*t5 == X2)
    s.add(Implies((w32 == 0), (t4 == 0)))
    s.add(Implies((w32 == 1), (t4 == 1*X3)))
    s.add(Implies((w32 == 2), (t4 == 2*X3)))
    s.add(Implies((w32 == 3), (t4 == 3*X3)))
    s.add(Implies((w42 == 0), (t5 == 0)))
    s.add(Implies((w42 == 1), (t5 == 1*X4)))
    s.add(Implies((w42 == 2), (t5 == 2*X4)))
    s.add(Implies((w42 == 3), (t5 == 3*X4)))

    t6 = Int('t6')
    s.add(4*x3 + 1*t6 == X3)
    s.add(Implies((w43 == 0), (t6 == 0)))
    s.add(Implies((w43 == 1), (t6 == 1*X4)))
    s.add(Implies((w43 == 2), (t6 == 2*X4)))
    s.add(Implies((w43 == 3), (t6 == 3*X4)))

    s.add(1*x4 == X4)

    t7, t8, t9 = Ints('t7 t8 t9')
    s.add(64*y1 + 1*t7 + 4*t8 + 16*t9 == Y1)
    s.add(Implies((w21 == 0), (t7 == 0)))
    s.add(Implies((w21 == 1), (t7 == 1*Y2)))
    s.add(Implies((w21 == 2), (t7 == 2*Y2)))
    s.add(Implies((w21 == 3), (t7 == 3*Y2)))
    s.add(Implies((w31 == 0), (t8 == 0)))
    s.add(Implies((w31 == 1), (t8 == 1*Y3)))
    s.add(Implies((w31 == 2), (t8 == 2*Y3)))
    s.add(Implies((w31 == 3), (t8 == 3*Y3)))
    s.add(Implies((w41 == 0), (t9 == 0)))
    s.add(Implies((w41 == 1), (t9 == 1*Y4)))
    s.add(Implies((w41 == 2), (t9 == 2*Y4)))
    s.add(Implies((w41 == 3), (t9 == 3*Y4)))

    t10, t11 = Ints('t10 t11')
    s.add(16*y2 + 1*t10 + 4*t11 == Y2)
    s.add(Implies((w32 == 0), (t10 == 0)))
    s.add(Implies((w32 == 1), (t10 == 1*Y3)))
    s.add(Implies((w32 == 2), (t10 == 2*Y3)))
    s.add(Implies((w32 == 3), (t10 == 3*Y3)))
    s.add(Implies((w42 == 0), (t11 == 0)))
    s.add(Implies((w42 == 1), (t11 == 1*Y4)))
    s.add(Implies((w42 == 2), (t11 == 2*Y4)))
    s.add(Implies((w42 == 3), (t11 == 3*Y4)))

    t12 = Int('t12')
    s.add(4*y3 + 1*t12 == Y3)
    s.add(Implies((w43 == 0), (t12 == 0)))
    s.add(Implies((w43 == 1), (t12 == 1*Y4)))
    s.add(Implies((w43 == 2), (t12 == 2*Y4)))
    s.add(Implies((w43 == 3), (t12 == 3*Y4)))

    s.add(1*y4 == Y4)


    s.add(x1 + y1 + w21 + w31 + w41 == 4)
    s.add(x2 + y2 + w32 + w42 == 4)
    s.add(x3 + y3 + w43 == 4)
    s.add(x4 + y4 == 4)


    s.add(w21  <= 4)
    s.add(w31 + w32  <= 4)
    s.add(w41 + w42 + w43  <= 4)


    s.add(And(X1 >= 0, Y1 >= 0, x1 >= 0, x1 <= 3, y1 >= 0, y1 <= 3))
    s.add(And(X2 >= 0, Y2 >= 0, x2 >= 0, x2 <= 3, y2 >= 0, y2 <= 3))
    s.add(And(X3 >= 0, Y3 >= 0, x3 >= 0, x3 <= 3, y3 >= 0, y3 <= 3))
    s.add(And(X4 >= 0, Y4 >= 0, x4 >= 0, x4 <= 3, y4 >= 0, y4 <= 3))
    s.add(And(w21 >= 0, w21 <= 3))
    s.add(And(w31 >= 0, w31 <= 3, w32 >= 0, w32 <= 3))
    s.add(And(w41 >= 0, w41 <= 3, w42 >= 0, w42 <= 3, w43 >= 0, w43 <= 3))
    s.add(s4 == 0)
    s.add(s3 == s4 )
    s.add(s2 == s3 + w42 )
    s.add(s1 == s2 + w31 + w41 )
    s.add(s1 <= 2)
    s.add(And(X1 == r11, Y1 == r12))


    sample = s.minimize(x1 + x2 + x3 + x4)
    buff = s.minimize(y1 + y2 + y3 + y4)
    startTime = time.time()
    print (s.check())
    print ("sample = ", sample.value(), "buffer = ", buff.value())
    endTime = time.time()
    executionTime = endTime - startTime
    print ("Execution Time = ",executionTime)
    fp = open(f'/home/sparrow/Desktop/MTP/Codes/MTP_IITG/dilution/outputs/op{r12}','w')
    lst = s.model()
    for i in lst:
        fp.write(str(i) + " = " + str(s.model()[i]) + '\n')

for r in range(1, 128):
    z3Solver(256-r, r)
