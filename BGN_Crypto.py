import random
from functools import partial
from curves.curves import WeierstrassCurve
from fields.primeorder import FiniteFieldPrimeOrder
from fields.extension import FiniteFieldExtension3thPrimitiveRoot
from bgn.keygen import modified_weil_pairing

#Definim variables
q = 2     
r = 3
n = q*r 
p=23

#Definim el camp on es troben tots els punts i la corba el·líptica en aquest camp.
field = FiniteFieldPrimeOrder(prime=p)
curve = WeierstrassCurve(a=0, b=1, field=field)

#Definim els punts de la corba
def Point(x, y, curve):
    return WeierstrassCurve.Point(curve, x, y)

#Definim el camp on es troben tots els punts amb una extensió i la corba el·líptica en aquest camp.
field_Fp2 = FiniteFieldExtension3thPrimitiveRoot(prime=p)
curve_Fp2 = WeierstrassCurve(a=0, b=1, field=field_Fp2)


#Definim un punt S que el necessitarem per l'aparellament de Weil
S = curve_Fp2.point(
    field_Fp2.from_coefficients(0),
    field_Fp2.from_coefficients(1)
)


#Classe que inclou funcions per encriptar, desencriptar, poder sumar punts enciptats i fer multiplicació
class BGN:
    def __init__(self, curve, P, Q, q, r, n, pairing):
        self.curve = curve
        self.P = P
        self.Q = Q
        self.q = q
        self.r = r
        self.n = n
        self.pairing = pairing

    def encrypt(self, m):
        t = random.randint(1, self.n - 1)
        C = m * self.P + t * self.Q
        return C

    def decrypt(self, C):
        P_tilde = self.q * self.P
        C_tilde = self.q * C

        for m in range(self.r):
            if m * P_tilde == C_tilde:
                return m
        
    def add(self, C1, C2):
        t0 = random.randint(1, self.n - 1)
        C = C1 + C2 + t0 * self.Q
        return C

    def mult(self, C1, C2):
        u = random.randint(1, self.n - 1)
        e1 = self.pairing(C1, C2)
        e2 = self.pairing(self.Q, self.Q)
        result = e1 * (e2 ** u)
        return result


#Funció per trobar punts d'ordre n
def punts_amb_ordre(curve, ordre_total):
    Punts = curve.get_all_points()
    O = curve.neutral_element()
    punts_valids = []

    for P in Punts:
        if P == O:
            continue  

        # Comprova si [ordre_total]P == O
        if ordre_total * P != O:
            continue

        # Comprova si és l'ordre mínim
        ordre_minim = True
        for d in range(1, ordre_total):
            if ordre_total % d == 0 and d * P == O:
                ordre_minim = False
                break

        if ordre_minim:
            punts_valids.append(P)

    return punts_valids


punts_ordre_n=punts_amb_ordre(curve, n)
#Triam 2 punts aleatoris d'ordre n
P1, P2 = random.sample(punts_ordre_n, 2)

#P ha de ser d'ordre n
P = Point(x=P1.x, y=P1.y, curve=curve)   
print('Punt P =',P)
Q_tilde = Point(x=P2.x, y=P2.y, curve=curve)
#Q ha de ser d'ordre q (Q=[r]Q' on Q' és d'ordre n)
Q=r*Q_tilde
print('Punt Q =',Q)

pairing = partial(modified_weil_pairing, curve_Fp2, n=n, S=S)

bgn = BGN(curve, P, Q, q,r, n, pairing)

m1 = 2
m2 = 3

C1 = bgn.encrypt(m1)
C2 = bgn.encrypt(m2)

C_sum = bgn.add(C1,C2)

print("Missatge 1:", m1)
print("Missatge 2:", m2)

print("Missatge 1 encriptat =", C1)
print("Missatge 2 encriptat =", C2)
print('Missatge 1 desencriptat =', bgn.decrypt(C1))
print('Missatge 2 desencriptat =', bgn.decrypt(C2))


sum_dec = bgn.decrypt(C_sum)
print("Suma desencriptada:", sum_dec)  


