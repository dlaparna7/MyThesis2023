import numpy as np
from operator_matrices import *
import math
from helperfuncs import *
from testcases import *


def construct_rhsd(nrj_size_list, allnearest, uvwh, f, xyz, allD, ghost):
    n_p = len(uvwh)
    rhsd = np.empty(3)
    it = 0
    termA = np.zeros(3, dtype = np.float64)
    termB = np.zeros(3, dtype = np.float64)
    termC = np.zeros(3, dtype = np.float64)
    termCx = np.zeros(n_p, dtype = np.float64)
    termCy = np.zeros(n_p, dtype = np.float64)
    termCz = np.zeros(n_p, dtype = np.float64)

    Ru = np.zeros(n_p, dtype = np.float64)
    Rv = np.zeros(n_p, dtype = np.float64)
    Rw = np.zeros(n_p, dtype = np.float64)
    Rh = np.zeros(n_p, dtype = np.float64)

    #g = 9.80616
    #f = 1.4e-3
    g = 1.5454e-8

    #need to get neighborhood Dnx, Dny, Dnz (saved sequentially for each point)
    def get_Dnxyz_from_allD(allD, it, k):

         #gives the length of nrj for the index point id
        
        itx = int(it+k)
        
        Dnx = allD[it: itx, 0]
        Dny = allD[it: itx, 1]
        Dnz = allD[it: itx, 2]
        nearest = allnearest[it:itx]

        return Dnx, Dny, Dnz, nearest

    # need to get neighborhood uvwh (saved at each point)
    def get_uvwh_r(uvwh,nearest):
        uvwh_r = np.empty([len(nearest),4])
        for n in range(len(nearest)):
            uvwh_r[n,0] = uvwh[int(nearest[n]),0]
            uvwh_r[n,1] = uvwh[int(nearest[n]),1]
            uvwh_r[n,2] = uvwh[int(nearest[n]),2]
            uvwh_r[n,3] = uvwh[int(nearest[n]),3]


        return uvwh_r

    def getpxyz(xyz):

        px = np.zeros(3)
        py = np.zeros(3)
        pz = np.zeros(3)

        x = xyz[0]
        y = xyz[1]
        z = xyz[2]

        px[0] = (1 - (x ** 2))
        px[1] = (0 - (x * y))
        px[2] = (0 - (x * z))

        py[0] = (0 - (x * y))
        py[1] = (1 - (y ** 2))
        py[2] = (0 - (y * z))

        pz[0] = (0 - (x * z))
        pz[1] = (0 - (y * z))
        pz[2] = (1 - (z ** 2))


        return px[np.newaxis,:], py[np.newaxis,:], pz[np.newaxis,:]
    l = 0
    # Calculating RHS values for each of the internal points
    for i in range(n_p):
        if not ghost[i]:

            k = int(nrj_size_list[l]) #Check the requirement of int typecasting here
            l= l+1
            Dnx, Dny, Dnz, nearest = get_Dnxyz_from_allD(allD, it,k)
        #print("nearest:", nearest)
            uvwh_r = get_uvwh_r(uvwh, nearest)

            u = uvwh_r[:, 0]
            v = uvwh_r[:, 1]
            w = uvwh_r[:, 2]
            h = uvwh_r[:, 3]

        # u.(Dnx.u_r) + v.(Dny.u_r) + w.(Dnz. u_r)
            termA[0] = (uvwh[i,0]*(np.dot(np.transpose(Dnx),u)) +
                 uvwh[i,1]*(np.dot(np.transpose(Dny),u)) +
                 uvwh[i,2]*(np.dot(np.transpose(Dnz),u)))

            termA[1] = (uvwh[i, 0] * (np.dot(np.transpose(Dnx), v)) +
                       uvwh[i, 1] * (np.dot(np.transpose(Dny), v)) +
                       uvwh[i, 2] * (np.dot(np.transpose(Dnz), v)))

            termA[2] = (uvwh[i, 0] * (np.dot(np.transpose(Dnx), w)) +
                    uvwh[i, 1] * (np.dot(np.transpose(Dny), w)) +
                    uvwh[i, 2] * (np.dot(np.transpose(Dnz), w)))

            it = it + k

        #f. [3,1]
            termB[0] = f[i]*(xyz[i,1]*uvwh[i,2] - xyz[i,2] *uvwh[i,1])
            termB[1] = f[i]*(xyz[i,2]*uvwh[i,0] - xyz[i,0] *uvwh[i,2])
            termB[2] = f[i]*(xyz[i,0]*uvwh[i,1] - xyz[i,1] *uvwh[i,0])

        #g.[Dnx Dny Dnz]. h

            termCx= Dnx
            termCy= Dny
            termCz= Dnz
        
            term_c = np.row_stack([termCx,termCy,termCz])
            termC = np.dot(term_c,h)

            rhsd[0] = termA[0] + (termB[0]) + g*(termC[0])
            rhsd[1] = termA[1] + (termB[1]) + g*(termC[1])
            rhsd[2] = termA[2] + (termB[2]) + g*(termC[2])

            rhsd[:,np.newaxis]


        #Get px, py, pz at the node where we are calculating
            px, py, pz = getpxyz(xyz[i])

            Rh[i] = ( uvwh[i, 0]*(np.dot(Dnx,h)) + uvwh[i, 1]*(np.dot(Dny,h)) + uvwh[i, 2]*(np.dot(Dnz,h)) + uvwh[i,3]*(np.dot(Dnx,u) + np.dot(Dny,v)+ np.dot(Dnz,w)))

            Ru[i] = -np.dot(px, rhsd)
            Rv[i] = -np.dot(py, rhsd)
            Rw[i] = -np.dot(pz, rhsd)
    
        #print("result of construct rhsd:", Ru[i], Rv[i], Rw[i], Rh[i])

    return Ru, Rv, Rw, Rh

def set_initial_conditions(uvwh, xyz, n_p, ghost,lonlat):
    
    N = len(uvwh)
    f = np.zeros(N)
    Omega = 7.292e-5;
    angle = 0.0
       
    #lam = np.zeros(len(xyz))
    #th = np.zeros(len(xyz))

    lam = np.radians(lonlat[:,0])
    th = np.radians(lonlat[:,1])

    x = xyz[:,0]
    y = xyz[:,1]
    z = xyz[:,2]
    
    v_lon = np.zeros(N)
    v_lat = np.zeros(N)
    h = np.zeros(N)

    for n in range(N):
        if not ghost[n]: #calculating all internal values     
            v_lon[n], v_lat[n], h[n], f[n] = test2_fun(lam[n],th[n])
            

        else:
            v_lon[n] = v_lat[n] = h[n] = 0.0
            f[n] = 0.0

            #print("vlon and vlat: ", v_lon[n,0], v_lat[n,0])

    uvw = gvec2cvec_sphere(v_lon, v_lat, lam, th,ghost)
            #uvw, h = test6_fun(lam[n],th[n])
            
    for n in range(n_p):
        if not ghost[n]:
            uvwh[n,0] = uvw[n,0]
            uvwh[n,1] = uvw[n,1]
            uvwh[n,2] = uvw[n,2]
            uvwh[n,3] = h[n]

        else:
            uvwh[n,0] = 0
            uvwh[n,1] = 0
            uvwh[n,2] = 0
            uvwh[n,3] = 0

        
    #print("uvwh and f: ", uvwh)

    return uvwh,f


