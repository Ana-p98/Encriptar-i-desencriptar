import random
from BGN_Crypto import construir_bgn

#Funció per fer operacions amb els missatges de dues llistes encriptats
def difs_emmascarades_agrupat(bgn, Cx_list, y_list):
    #Xifram els missatges de la segona llista
    Cy_list = [bgn.encrypt(y) for y in y_list]
    out = []
    for Cx in Cx_list:
        bucket = []
        for Cy in Cy_list:
            #Feim la resta dels dos missatges encriptats
            D = bgn.sub(Cx, Cy)                
            k = random.randint(1, bgn.r - 1)   
            #Multiplicamos la resta per un escalar aleatori
            Dk = bgn.scalar_mult(D, k)          
            bucket.append(Dk)
        out.append(bucket)
    return out


def main():
    #Triam els valors de q i r
    q = 2
    r = 11   
    
    bgn, dades = construir_bgn(q, r)
    print(f"p = {dades['p']}, n = {q*r}")
    print("P =", dades["P"])
    print("Q =", dades["Q"])
    
    #Triam dues llistes qualsevols
    llista1 = [9,3,6,1,8,4]     
    llista2 = [4,2,3,5,6,7,10]             
    
    #llista1 xifra la seva llista i l'envia a llista2
    llista1_enc = [bgn.encrypt(x) for x in llista1]
    print("Llista 1 encriptada:", llista1_enc)
    
    #llista2 procesa tots els missatges que han arribat i amb la clau pública xifra els
    #seus elements i fa operacions per poder retornar-li a lista1
    grouped = difs_emmascarades_agrupat(bgn, llista1_enc, llista2)
    
    #llista1 desencripta el que li passa llista2 i troba el element que tenen en comú
    match_idx = []
    for i, bucket in enumerate(grouped):
        dec = [bgn.decrypt(C) for C in bucket]
        if any(v == 0 for v in dec):
            match_idx.append(i)
    
    print("Elements de llista1 que coincideix amb llista2:", [llista1[i] for i in match_idx])

if __name__ == "__main__":
    main()
