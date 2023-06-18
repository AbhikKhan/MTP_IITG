import z3

opt = z3.Optimize()
opt.add(z3.Int('x')>5)
opt.minimize(z3.Int('x'))

if opt.check()=='unsat':
    print('Unsat')
else:
    print('Sat')
    res = opt.model()
    print(res)