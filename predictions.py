# This file is the Prediction module which is able to calculate altitude
# and speed predictions before and during the flight


class EconMachEquationsA320():
    def __init__(self):
        self.eq0 = self.eq3degrees(-8.333e-8, 8.3452e-5, -2.7071e-2, 3.5750)
        self.eq20 = self.eq3degrees(-3.5354e-8, 3.1169e-5, -8.3997e-3, 1.4107)
        self.eq40 = self.eq3degrees(-2.5253e-8, 1.7857e-5, -3.2892e-3, 8.3507e-1)
        self.eq60 = self.eq3degrees(5.4714e-8, -5.9286e-5, 2.1181e-2, -1.7028)
        self.eq100 = self.eq3degrees(5.8923e-9, -6.2771e-6, 2.1476e-3, 5.6153e-1)

    def eq3degrees(self, a, b, c, d):
        return lambda x : a*x**3 + b*x**2 + c*x + d

    def compute_ECON_MACH(self, CI, FL):
        # compute ECON MACH, depending on cost index and flight level
        # CI and FL inputs are only considered as integers
        if CI >= 100 : CI=100
        diff_min = 100
        for nom_CI in [0, 20, 40, 60, 100]:
            diff = CI - nom_CI
            if abs(diff) < diff_min:
                diff_min = diff
                CI_used = nom_CI
        print("CI_used=", CI_used)
        print("CI=", CI)
        if CI_used == 0: ratio = (1 + CI/20)
        else : ratio = CI/CI_used
        return round(ratio*eval('self.eq'+str(CI_used)+'('+str(FL)+')'), 3)

    def examples(self):
        print("CI=0, FL=350 : ECON_MACH=", self.compute_ECON_MACH(0, 350))
        print("CI=0, FL=310 : ECON_MACH=", self.compute_ECON_MACH(0, 310))
        print("CI=40, FL=290 : ECON_MACH=", self.compute_ECON_MACH(40, 290))
        print("CI=100, FL=370 : ECON_MACH=", self.compute_ECON_MACH(100, 370))
        print("CI=200, FL=370 : ECON_MACH=", self.compute_ECON_MACH(100, 370))


eqs = EconMachEquationsA320()
eqs.examples()
