#!/usr/bin/env python3

import sys
import math
import numpy as np

def helper(err):
    if err==0:
        helper_msg="""
            build a matrix casting outwardly redundant slopes to 0
            ./magn.py INT  # INT : number of rings in matrix
            ex.
                ./magn.py 17
        """
        print(helper_msg)
    elif err==1:
        err_msg="""
            err : {} : {} : bad argument
                please supply only one INT as an argument
                ex.
                    ./magn.py 17
                or -h for the help dialogue:
                    ./magn.py -h
            """.format(err,sys.argv[1])
        print(err_msg)
    elif err==2:
        err_msg="""
            err : {} : {} : bad argument
            maximum vector magnitude must be greater than 2
            ex.
                ./magn.py 4
        """.format(err,sys.argv[1])
        print(err_msg)
    else:
        helper(0)
    exit(0)

### std_out functions >>>

def out_al(bnd,ar):
  #stdout print statement evenly displays list elements
  #based on the length of the first element
  # add to any elements until all elements are the same length as the first
  ml=len(str(bnd))
  sar=""
  for i in ar:
    si=" "*(ml-len(str(i)))+str(i)
    sar=sar+" "+str(si)
  return sar


def out_mat(verbose,mat,bound):
    #stdout print matrix with evenly spaced elements
    print()
    if verbose==True:
        for _axis in mat:
           print(out_al(bound,_axis))


def out_lbl_vchk(verbose,outs):
    #stdout values with labels for debugging
    if verbose==True:
      print("\n")
      cnt=0
      l=len(outs)
      while cnt<l:
        print(" "*2+str(outs[cnt])+":",outs[cnt+1])
        cnt+=2

### std_out functions <<<


### matrix functions >>>
def slopes_preT(lvl):
    verbose=False

    slopes=[0,1]
    vec_slopePreTranslate=[[0,1],[1,1]]
    redundant=[]

    for i in range(2,lvl+2,1):
        for dim in range(0,i+1,1):
            dims=[i,dim]
            slope=dims[1]/dims[0]
            if slope not in slopes:
                slopes.append(slope)
                vec_slopePreTranslate.append(dims)
            else:
                redundant.append(dims)
    return [vec_slopePreTranslate,redundant,slopes]



def full_mat(bound):
    verbose=True
    mat=np.array([[1,1,1]])
    mat_onit=[[1,0,1],[1,1,1]]
    for ea in mat_onit:
        cat=np.array([ea])
        mat=np.concatenate((mat,cat))
    for ea in range(2,bound,1):
        mat=np.insert(mat, 0, ea, axis=0)
        mat=np.insert(mat, len(mat), ea, axis=0)
        mat=np.insert(mat, 0, ea, axis=1)
        mat=np.insert(mat, len(mat[0]), ea, axis=1)
    return mat


def include_Rotations(to_rot):
    rot_list=[] #list of rotations
    #          i,j sign 1|-1
    #rot_list.append([0,0,0]) #[[0,1],[1,1] #onit
    rot_list.append([1,0,0]) #[[1,0],[1,1]
    rot_list.append([0,1,0]) #[[0,1],[-1,1]
    rot_list.append([1,1,0]) #[[1,0],[-1,1]

    rot_list.append([0,1,1]) #[[1,0],[1,1]
    rot_list.append([0,0,1]) #[[0,1],[-1,1]
    rot_list.append([1,0,1]) #[[1,0],[-1,1]

    rot=np.array([[to_rot[0][1],to_rot[0][0]]])
    for r in rot_list:
        if r[0]==0:
            r00=0
            r01=1
        else:
            r00=1
            r01=0
        if r[1]==0:
           r1=1
        else:
            r1=-1
        if r[2]==0:
            r2=1
        else:
            r2=-1
        for ea in to_rot:
            cat=np.array([[r1*ea[r00],r2*ea[r01]]])
            rot=np.concatenate((rot,cat))
    to_rot=np.concatenate((to_rot,rot))
    return to_rot


def mat_setReduTo0(mat,redu):
    hlf=int((len(mat)-1)/2) #0 indice square
    for ea in redu:
        i=hlf+ea[0]
        j=hlf-ea[1]
        mat[j,i]=0
    return mat


def build_mat(bound):
    verbose=True

    mat=full_mat(bound)

    pt=slopes_preT(bound-2) #-2 due to origin and 1s
    preT=pt[0]   # LST of LST   : list of pre translation slope vectors
    redu=pt[1]   # LST of LST   : list of redundant sloped vectors
    slopes=pt[2] # LST of FLOAT : list of slopes as FLOAT
    out_lbl_vchk(verbose,["slopes",slopes,"redundant",redu,"vec_slopePreTranslate",preT])

    redu=include_Rotations(redu)
    mat=mat_setReduTo0(mat,redu)
    return mat

### matrix functions <<<
def tst():
    bound=4
    s_pt=slopes_preT(bound-2)[0]
    uniq_slopes=include_Rotations(s_pt)
    numb=len(uniq_slopes)
    print("all rotation slopes:",uniq_slopes)
    print("number of rotslopes:",numb)
    out_mat(True,uniq_slopes,2)
    print("p_t:")
    out_mat(True,s_pt,2)
    print("pass tst:",numb==36) #36 for bound of 4
    exit(0)

def onit():
    if len(sys.argv)>1:
        if sys.argv[1]=="-h":
            helper(0)
        elif sys.argv[1]=="-tst":
            tst()
        try:
            bound=int(sys.argv[1])
        except:
            helper(1)
        if bound<3:
            helper(2)
    else:
        helper(0)

    mat=build_mat(bound)
    out_mat(True,mat,bound)

    print("\n\n..01x17")

if __name__=="__main__":
    onit()

#./magn.py  #returns vectors with unique slopes based on distance from origin
