#!/usr/bin/env python3

from magn import *


def plae_multi_bound_comparison(bnd):
    #create a matrix labeling elements as integers from the center
    verbose=True


    rets=[]
    for bound in range(3,bnd,1):
        mat=build_mat(bound)
        ret=plae_mat_evaluate(mat,bound)
        rets.append(ret)

    _i=[]  #indice
    zs=[]  #zeros
    df=[]  #diffs
    z8=[]  #(zeros-1)/8
    d8=[]  #diffs/8
    l2=[]  #math.log(diff,2)
    for ei,ret in enumerate(rets):
        _i.append(ei+3)
        zs.append(ret[0])
        df.append(ret[1])
        z8.append(ret[2])
        d8.append(ret[3])
        l2.append(ret[4])

    out_lbl_vchk(verbose,["0s",zs,"df",df,"z8",z8,"d8",d8,"l2",l2])

    l2_m1=[]
    for ei,ea in enumerate(l2):
        if ea==int(ea):
            l2_m1.append(ei+3)

    out_lbl_vchk(verbose,["l2_m1",l2_m1])

### results ####################
    #                       (0s-1) % 8 == 0  dif % 8 == 0
    #bnd=2  #err: bound >=2  (0s-1)/8 +    d/8    +
    #bnd=3   #0:  9, dif: 16       1   1     2     2
    #bnd=4   #0: 17, dif: 32       2   2     4     2
    #bnd=5   #0: 33, dif: 48       4   1     6     4
    #bnd=6   #0: 41, dif: 80       5   4     10    2
    #bnd=7   #0: 73, dif: 96       9   1     12    6
    #bnd=8   #0: 81, dif:144      10   4     18    6
    #bnd=9   #0:113, dif:176      14   3     22    6
    #bnd=10  #0:137, dif:224      17         28
    #bnd=11  #0:000, dif:000      00  0      00   0
################################

def plae_mat_evaluate(mat,bound):
    verbose=True
    unique, counts = np.unique(mat, return_counts=True)
    uc=dict(zip(unique,counts))

    out_lbl_vchk(verbose,["unique",unique,"counts",counts,"uc",uc,"bound",bound])

    total=((bound-1)*2+1)**2
    tot_chk=0
    for ea in uc:
        tot_chk+=uc[ea]
    dif=total-counts[0]
    lg2=math.log(dif,2)
    cnt0=int(counts[0])
    out_lbl_vchk(verbose,["tot",total,"=?=tot_chk",tot_chk,"0",cnt0,"dif",dif,"(0s-1)/8",(cnt0-1)/8,"dif/8",dif/8,"lg2",lg2])
    return [cnt0,dif,int((cnt0-1)/8),int(dif/8),lg2]

def plae_analysis():
    verbose=True
    plae_multi_bound_comparison(17)

def onit():
    plae_analysis()

if __name__=="__main__":
    onit()

#./plae_analysis
