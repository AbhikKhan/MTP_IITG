import sys
import time
sys.path.append("/home/sukanta/App/z3/bin")
from z3 import *

def getSolver(r11, r12):
    s=Optimize()
    R11, R12, x11, x12 = Ints('R11 R12 x11 x12')
    R21, R22, x21, x22 = Ints('R21 R22 x21 x22')
    R31, R32, x31, x32 = Ints('R31 R32 x31 x32')
    R41, R42, x41, x42 = Ints('R41 R42 x41 x42')
    w21 = Int('w21')
    w31, w32 = Ints('w31 w32')
    w41, w42, w43 = Ints('w41 w42 w43')


    t1, t2, t3 = Ints('t1 t2 t3')
    s.add(64*x11 + 1*t1 + 4*t2 + 16*t3 == R11)
    s.add(Implies((w21 == 0), (t1 == 0)))
    s.add(Implies((w21 == 1), (t1 == 1*R21)))
    s.add(Implies((w21 == 2), (t1 == 2*R21)))
    s.add(Implies((w21 == 3), (t1 == 3*R21)))
    s.add(Implies((w21 == 4), (t1 == 4*R21)))
    s.add(Implies((w31 == 0), (t2 == 0)))
    s.add(Implies((w31 == 1), (t2 == 1*R31)))
    s.add(Implies((w31 == 2), (t2 == 2*R31)))
    s.add(Implies((w31 == 3), (t2 == 3*R31)))
    s.add(Implies((w31 == 4), (t2 == 4*R31)))
    s.add(Implies((w41 == 0), (t3 == 0)))
    s.add(Implies((w41 == 1), (t3 == 1*R41)))
    s.add(Implies((w41 == 2), (t3 == 2*R41)))
    s.add(Implies((w41 == 3), (t3 == 3*R41)))
    s.add(Implies((w41 == 4), (t3 == 4*R41)))

    t4, t5, t6 = Ints('t4 t5 t6')
    s.add(64*x12 + 1*t4 + 4*t5 + 16*t6 == R12)
    s.add(Implies((w21 == 0), (t4 == 0)))
    s.add(Implies((w21 == 1), (t4 == 1*R22)))
    s.add(Implies((w21 == 2), (t4 == 2*R22)))
    s.add(Implies((w21 == 3), (t4 == 3*R22)))
    s.add(Implies((w21 == 4), (t4 == 4*R22)))
    s.add(Implies((w31 == 0), (t5 == 0)))
    s.add(Implies((w31 == 1), (t5 == 1*R32)))
    s.add(Implies((w31 == 2), (t5 == 2*R32)))
    s.add(Implies((w31 == 3), (t5 == 3*R32)))
    s.add(Implies((w31 == 4), (t5 == 4*R32)))
    s.add(Implies((w41 == 0), (t6 == 0)))
    s.add(Implies((w41 == 1), (t6 == 1*R42)))
    s.add(Implies((w41 == 2), (t6 == 2*R42)))
    s.add(Implies((w41 == 3), (t6 == 3*R42)))
    s.add(Implies((w41 == 4), (t6 == 4*R42)))

    t7, t8 = Ints('t7 t8')
    s.add(16*x21 + 1*t7 + 4*t8 == R21)
    s.add(Implies((w32 == 0), (t7 == 0)))
    s.add(Implies((w32 == 1), (t7 == 1*R31)))
    s.add(Implies((w32 == 2), (t7 == 2*R31)))
    s.add(Implies((w32 == 3), (t7 == 3*R31)))
    s.add(Implies((w32 == 4), (t7 == 4*R31)))
    s.add(Implies((w42 == 0), (t8 == 0)))
    s.add(Implies((w42 == 1), (t8 == 1*R41)))
    s.add(Implies((w42 == 2), (t8 == 2*R41)))
    s.add(Implies((w42 == 3), (t8 == 3*R41)))
    s.add(Implies((w42 == 4), (t8 == 4*R41)))

    t9, t10 = Ints('t9 t10')
    s.add(16*x22 + 1*t9 + 4*t10 == R22)
    s.add(Implies((w32 == 0), (t9 == 0)))
    s.add(Implies((w32 == 1), (t9 == 1*R32)))
    s.add(Implies((w32 == 2), (t9 == 2*R32)))
    s.add(Implies((w32 == 3), (t9 == 3*R32)))
    s.add(Implies((w32 == 4), (t9 == 4*R32)))
    s.add(Implies((w42 == 0), (t10 == 0)))
    s.add(Implies((w42 == 1), (t10 == 1*R42)))
    s.add(Implies((w42 == 2), (t10 == 2*R42)))
    s.add(Implies((w42 == 3), (t10 == 3*R42)))
    s.add(Implies((w42 == 4), (t10 == 4*R42)))

    t11 = Int('t11')
    s.add(4*x31 + 1*t11 == R31)
    s.add(Implies((w43 == 0), (t11 == 0)))
    s.add(Implies((w43 == 1), (t11 == 1*R41)))
    s.add(Implies((w43 == 2), (t11 == 2*R41)))
    s.add(Implies((w43 == 3), (t11 == 3*R41)))
    s.add(Implies((w43 == 4), (t11 == 4*R41)))

    t12 = Int('t12')
    s.add(4*x32 + 1*t12 == R32)
    s.add(Implies((w43 == 0), (t12 == 0)))
    s.add(Implies((w43 == 1), (t12 == 1*R42)))
    s.add(Implies((w43 == 2), (t12 == 2*R42)))
    s.add(Implies((w43 == 3), (t12 == 3*R42)))
    s.add(Implies((w43 == 4), (t12 == 4*R42)))

    s.add(1*x41 == R41)
    s.add(1*x42 == R42)


    s.add(x11 + x12  + w21 + w31 + w41 == 4)
    s.add(x21 + x22  + w32 + w42 == 4)
    s.add(x31 + x32  + w43 == 4)
    s.add(x41 + x42  == 4)


    s.add(w21  <= 4)
    s.add(w31 + w32  <= 4)
    s.add(w41 + w42 + w43  <= 4)


    s.add(And(R11 >= 0, R12 >= 0, x11 >= 0, x11 <= 3, x12 >= 0, x12 <= 3))
    s.add(And(R21 >= 0, R22 >= 0, x21 >= 0, x21 <= 3, x22 >= 0, x22 <= 3))
    s.add(And(R31 >= 0, R32 >= 0, x31 >= 0, x31 <= 3, x32 >= 0, x32 <= 3))
    s.add(And(R41 >= 0, R42 >= 0, x41 >= 0, x41 <= 3, x42 >= 0, x42 <= 3))
    s.add(And(w21 >= 0, w21 <= 3))
    s.add(And(w31 >= 0, w31 <= 3, w32 >= 0, w32 <= 3))
    s.add(And(w41 == 0, w42 >= 0, w42 <= 3, w43 >= 0, w43 <= 3))

    s.add(If(w21 == 3, w31 == 0, And(w31 >= 0, w31 <= 3)))
    s.add(If(w32 == 3, w42 == 0, And(w42 >= 0, w42 <= 3)))


    s.add(And(R11 == r11, R12 == r12))

    return s


for i in range(1, 128):
    fp = open(f'/home/sparrow/Desktop/IITG/MTP/Codes/MTP_IITG/output/op{i}','w')
    start = time.time()
    s = getSolver(256-i, i)
    if s.check() == unsat:
        print ('unsat')
    else:
        print ('sat')
        lst = s.model()
        for i in lst:
            fp.write(str(i) + " = " + str(s.model()[i]) + '\n')
