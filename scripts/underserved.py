#!/usr/bin/env python3

import sys
import math
from magn import slopes_preT as pt
from magn import include_Rotations as inc_rot


def helper(err):
    if err==0:
        help_msg="""   determine relative distance from regions to natural water sources
                          optional arguments:
                                -l :  ./underserved -l INT,INT #--lim|--limiter INT,INT : limit the matrice size
                                -f : full faux dada
                                -h : help prompt
                            ex:
                                ./underserved -l 8,8   # 8x8 limited region
        """
        print(help_msg)
    elif int(err)==1:
        err_msg="""  err : {} : {} : your limiting boundary failed
                     please try again supplying two integers seperated by a comma
                         -l INT,INT
                         ex.
                              ./underserved -l 8,8
                         or use -h for the help prompt
                """.format(err,sys.argv[2])
        print(err_msg)
    elif int(err)==2:
        err_msg="""  err : {} : {} : bad argument
                          optional arguments:
                                -l :  ./underserved -l INT,INT #--lim|--limiter INT,INT : limit the matrice size
                                -f : full faux dada
                                -h : help prompt
                """.format(err,sys.argv[1])
        print(err_msg)
    else:
        helper(0)
    exit(0)

def f_fromFile():
    #input from file
    mat=[]
    fi=open("../dada/faux_bloc","r")
    for line in fi.readlines():
        line=line.strip()
        j=[]
        for ch in line:
            if ch=="#":
                j.append(0)
            else: #ch=="_"
                j.append(1)
        mat.append(j)
    return mat

def f_limiter(lim,mat):
    #BOILERPLATE_shrink the size of the matrice for testing
    lim_mat=[]
    di=lim[0]
    dj=lim[1]
    for i in mat[:di]:
        lim_j=[]
        for j in i[:dj]:
            lim_j.append(j)
        lim_mat.append(lim_j)
    return lim_mat


def f_limiter_chk(mat):
    #BOILERPLATE_provide cli control of limiter
    l_arg=len(sys.argv)
    if l_arg>1:
        if sys.argv[1]=="-l" and l_arg == 3:
            spl=sys.argv[2].split(",")
            dim=[]
            dim.append(int(spl[0]))
            dim.append(int(spl[1]))
            mat=f_limiter(dim,mat)
    return mat


### stdout >>>
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

### stdout <<<



def quad_bounds(mat,i,j):
    #determines mat bounds based on planar quadrant
    qb=True
    mat_dim=[len(mat)-1,len(mat[0])-1]
    if i<0 or j<0 or j>mat_dim[0] or i>mat_dim[1]:
        qb=False
    return qb


def branch(mat,i,j,magn):
    #searches outward from current position in branching pattern
    mult=1 #vector magnitude multiplier
    all_dir=[]
    all_branch_slopes=inc_rot(pt(magn)[0])
    longest_search=0
    for s_vec in all_branch_slopes:
        mult=1
        found_dist=0
        sl_i=i+(s_vec[0]*(mult))
        sl_j=j+(s_vec[1]*(mult))
        qb=quad_bounds(mat,sl_i,sl_j)
        while qb==True:
            found=chk_waterSource(mat,sl_i,sl_j)
            if found==True:
                svi=(s_vec[0]*(mult))  #vector magnitude from i,j to water source
                svj=(s_vec[1]*(mult))   #vector magnitude from i,j to water source
                found_dist=math.sqrt(svi**2+svj**2)
                all_dir.append(found_dist)
                qb=False
            else:
                mult+=1
                sl_i=i+(s_vec[0]*(mult))
                sl_j=j+(s_vec[1]*(mult))
                qb=quad_bounds(mat,sl_i,sl_j)
                if qb==False:
                    svi=(s_vec[0]*(mult-1)) #use most recent usable multiple
                    svj=(s_vec[1]*(mult-1)) #use most recent usable multiple
                    failed_dist=math.sqrt(svi**2+svj**2)
                    if failed_dist>longest_search:
                        longest_search=failed_dist
    if len(all_dir)==0:
        all_dir.append(longest_search)
    shortest=sorted(all_dir)[0] #shortest distance to water source
    return shortest


def chk_waterSource(mat,i,j):
    found=False
    if mat[j][i]==1:
        found=True
    return found


#faux dada located at ../dada/faux_bloc
def faux(magn):
    mat=f_fromFile()
    mat=f_limiter_chk(mat)
    print("  branch magnitude:",magn)
    print("  dims: {} , {}".format(len(mat),len(mat[0])))

    print("mat:")
    out_mat(True,mat,0)
    und_mat=[]
    for j,_i in enumerate(mat):
        und_j=[]
        for i,_j in enumerate(_i):
            if _j == 1:
                und_j.append(0) # distance to water at water is 0
            else:
                und_j.append(int(branch(mat,i,j,magn)))
        und_mat.append(und_j)
    print("und_mat:")
    out_mat(True,und_mat,11)

def onit():
    branch_magnitude=4
    if len(sys.argv)>1:
        if sys.argv[1]=="-l":
            if len(sys.argv)>2:
                for ea in sys.argv[2].split(","):
                    try:
                        int(ea)
                    except:
                        helper(1.1)
            else:
                helper(1.0)
            faux(branch_magnitude)
        elif sys.argv[1]=="-f":
            faux(branch_magnitude)
        elif sys.argv[1]=="-h":
            helper(0)
        else:
            helper(2)
    else:
        helper(0)

if __name__ == "__main__":
    onit()

#./underserved -l INT,INT #--lim|--limiter INT,INT : limit the matrice size
