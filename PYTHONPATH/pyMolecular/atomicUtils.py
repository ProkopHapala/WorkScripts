#!/usr/bin/python

import numpy as np
import elements

def loadAtoms(fname):
    xyzs   = [] 
    Zs     = []
    enames = []
    with open(fname, 'r') as f:
        for line in f:
            wds = line.split()
            if wds >= 4:
                try:
                    xyzs.append( ( float(wds[1]), float(wds[2]), float(wds[3]) ) )
                    try:
                        iz    = int(wds[0]) 
                        Zs    .append(iz)
                        enames.append( elements.ELEMENTS[iz] )
                    except:
                        ename = wds[0]
                        enames.append( ename )
                        Zs    .append( elements.ELEMENT_DICT[ename][0] )
                except:
                    print "cannot interpet line: ", line
                    continue
    xyzs = np.array( xyzs )
    Zs   = np.array( Zs, dtype=np.int32 )
    return xyzs,Zs,enames

def loadXYZmovie(fname):
    frames = []
    with open(fname, 'r') as f:
        il = 0
        while True:
            try:
                line = f.readline(); il+=1; #print ">>",line,
                n = int(line)
            except:
                break
            line = f.readline(); il+=1; #print ">>",line,
            xyzs   = [] 
            Zs     = []
            enames = []
            for i in range(n):
                line = f.readline(); il+=1;
                #print line,
                wds = line.split()
                if len(wds)<4 : print il," : ",line
                xyzs.append( ( float(wds[1]), float(wds[2]), float(wds[3]) ) )
                try:
                    iz    = int(wds[0]) 
                    Zs    .append(iz)
                    enames.append( elements.ELEMENTS[iz] )
                except:
                    ename = wds[0]
                    enames.append( ename )
                    Zs    .append( elements.ELEMENT_DICT[ename][0] )
            xyzs = np.array( xyzs )
            Zs   = np.array( Zs, dtype=np.int32 )
            frames.append( (xyzs, Zs, enames) )
    return frames

def toXYZ( f, enames, xyzs ):
    f.write("%i\n" %len(enames))
    f.write("# comment\n" )
    for i,ename in enumerate(enames):
        f.write("%s %f %f %f\n" %(ename,xyzs[i,0],xyzs[i,1],xyzs[i,2]) )
    #f.write("\n")

def saveXyz( fname, enames, xyzs ):
    with open(fname, 'w') as f:
        toXYZ( f, enames, xyzs )

def saveBas( fname, Zs, xyzs ):
    with open(fname, 'w') as f:
        f.write("%i\n" %len(Zs))
        for i,Z in enumerate(Zs):
            f.write("%i %f %f %f\n" %(Z,xyzs[i,0],xyzs[i,1],xyzs[i,2]) )

def findAllBonds( atoms, Rcut=3.0, RvdwCut=0.7 ):
    bonds     = []
    bondsVecs = []
    ps     = atoms[:,1:]
    iatoms = np.arange( len(atoms), dtype=int )
    Rcut2 = Rcut*Rcut
    for i,atom in enumerate(atoms):
        p    = atom[1:]
        dp   = ps - p
        rs   = np.sum( dp**2, axis=1 )
        for j in iatoms[:i][ rs[:i] < Rcut2 ]:
            ei = int( atoms[i,0] )
            ej = int( atoms[j,0] )
            Rcut_ij =  elements.ELEMENTS[ ei ][7] + elements.ELEMENTS[ ej ][7]
            #print ( i, j, ei, ej, Rcut_ij )
            rij =  np.sqrt( rs[j] )
            if ( rij < ( RvdwCut * Rcut_ij ) ):
                bonds.append( (i,j) )
                bondsVecs.append( ( rij, dp[j]/rij ) )
    return bonds, bondsVecs

def neighs( natoms, bonds ):
    neighs = [{} for i in range(natoms) ]
    for ib, b in enumerate(bonds):
        i = b[0]; j = b[1]; 
        neighs[i][j] = ib
        neighs[j][i] = ib
    return neighs

def findTypeNeigh( atoms, neighs, typ, neighTyps=[(1,2,2)] ):
    typ_mask = ( atoms[:,0] == typ )
    satoms   = atoms[typ_mask]
    iatoms   = np.arange(len(atoms),dtype=int)[typ_mask]
    selected = []
    for i,atom in enumerate(satoms):
        iatom = iatoms[i]
        #for jatom in neighs[ iatom ]:
        #    jtyp = atoms[jatom,0]
        count = {}
        for jatom in neighs[ iatom ]:
            jtyp = atoms[jatom,0]
            count[jtyp] = count.get(jtyp, 0) + 1
        for jtyp, (nmin,nmax) in neighTyps.items():
            n = count.get(jtyp,0)
            if( (n>=nmin)and(n<=nmax) ):
                selected.append( iatom )
    return selected

def getAllNeighsOfSelected( selected, neighs, atoms, typs={1} ):
    result = {}
    for iatom in selected:
        for jatom in neighs[ iatom ]:
            if( atoms[jatom,0] in typs ):
                if jatom in result:
                    result[jatom].append( iatom )
                else:
                    result[jatom] = [iatom]
    return result 

def findPairs( select1, select2, atoms, Rcut=2.0 ):    
    ps = atoms[select2,1:]
    Rcut2 = Rcut*Rcut
    pairs = []
    select2 = np.array( select2 )
    for iatom in select1:
        p = atoms[iatom,1:]
        rs = np.sum( (ps - p)**2, axis=1 )
        for jatom in select2[ rs < Rcut2 ]:
            pairs.append( (iatom,jatom) )
    return pairs

def findPairs_one( select1, atoms, Rcut=2.0 ):    
    ps = atoms[select1,1:]
    Rcut2 = Rcut*Rcut
    pairs = []
    select1 = np.array( select1 )
    for i,iatom in enumerate(select1):
        p = atoms[iatom,1:]
        rs = np.sum( (ps - p)**2, axis=1 )
        #print ( i, iatom, rs )
        for jatom in select1[:i][ rs[:i] < Rcut2 ]:
            pairs.append( (iatom,jatom) )
    return pairs  

def pairsNotShareNeigh( pairs, neighs ):
    pairs_ = []
    for pair in pairs:
        ngis = neighs[ pair[0] ]
        ngjs = neighs[ pair[1] ]
        share_ng = False
        for ngi in ngis:
            if ngi in ngjs:
                share_ng = True
                break
        if not share_ng:
            pairs_.append( pair )
    return pairs_    

def makeRotMat( fw, up ):
    fw   = fw/np.linalg.norm(fw)
    up   = up - fw*np.dot(up,fw)
    up   = up/np.linalg.norm(up)
    left = np.cross(fw,up)
    left = left/np.linalg.norm(left) 
    return np.array([left,up,fw])

def groupToPair( p1, p2, group, up, up_by_cog=False ):
    center = (p1+p2)*0.5
    fw  = p2-p1;    
    if up_by_cog:
        up  = center - up
    rotmat = makeRotMat( fw, up )
    ps  = group[:,1:]
    #ps_ = ps
    #print( "ps=", ps )
    #print ( rotmat )
    #ps_ = np.transpose( np.dot( rotmat, np.transpose(ps) ) )
    ps_ = np.dot( ps, rotmat ) 
    #print( "ps_=", ps_ )
    group[:,1:] = ps_ + center
    return group

def groupToAtom( p, fw, up, group ):
    rotmat      = makeRotMat( fw, up )
    print "========="
    print fw, up
    print rotmat
    ps          = group[:,1:]
    ps_         = np.dot( ps, rotmat ) 
    group[:,1:] = ps_ + p
    return group    

def replacePairs( pairs, atoms, group, up_vec=(np.array((0.0,0.0,0.0)),1) ):
    replaceDict = {}
    for ipair,pair in enumerate(pairs):
        for iatom in pair:
            replaceDict[iatom] = 1
            #if( iatom in replaceDict ):
            #    replaceDict[iatom].append(ipair)
            #else:
            #    replaceDict[iatom] = [ipair]
    atoms_ = []
    for iatom,atom in enumerate( atoms ):
        if(iatom in replaceDict): continue
        atoms_.append(atom)
    for pair in pairs:
        group_ = groupToPair( atoms[pair[0],1:], atoms[pair[1],1:], group.copy(), up_vec[0], up_vec[1] )
        #print( "group = ", group )
        for atom in group_:
            atoms_.append( atom )
        #break
    return atoms_

def findNearest( p, ps, rcut=1e+9 ):
	rs = np.sum( (ps - p)**2, axis=1 )
	imin = np.argmin(rs)
	if rs[imin]<(rcut**2):
	    return imin
	else: 
	    return -1 

def countTypeBonds( atoms, ofAtoms, rcut ):
    bond_counts = np.zeros(len(atoms), dtype=int )
    ps = ofAtoms[:,1:]
    for i,atom in enumerate(atoms):
        p = atom[1:]
        rs = np.sum( (ps - p)**2, axis=1 )
        bond_counts[i] = np.sum( rs < (rcut**2) )
    return bond_counts
	
def findBondsTo( atoms, typ, ofAtoms, rcut ):
    found     = []
    foundDict = {}
    ps = ofAtoms[:,1:] 
    for i,atom in enumerate(atoms):
        if atom[0]==typ:
            p = atom[1:]
            ineigh = findNearest( p, ps, rcut )
            if ineigh >= 0:
                foundDict[i] = len(found)
                found.append( (i, p - ps[ineigh]) )
    return found, foundDict
	
def replace( atoms, found, to=17, bond_length=2.0, radial=0.0, prob=0.75 ):
    replace_mask = np.random.rand(len(found)) < prob
    for i,foundi in enumerate(found):
        if replace_mask[i]:
            iatom = foundi[0]
            bvec  = foundi[1]
            rb    = np.linalg.norm(bvec)
            bvec *= ( bond_length - rb )/rb
            #if radial > 0:
            #    brad = atoms[iatom,1:]
            #    brad = brad/np.linalg.norm(brad)
            #    cdot = np.dot( brad, bvec )
            #    bvec = (1-radial)*bvec + brad*radial/cdot
            atoms[iatom,0]   = to
            atoms[iatom,1:] += bvec  
    return atoms
    
def replaceGroup( atoms, found, foundDict, group=['17'], Ups=(0.0,0.0,0.0), bond_length=2.0, radial=0.0, prob=0.75 ):
    if not isinstance(Ups, np.ndarray):
        Ups = np.array( [ atoms[foundi[0],1:]-Ups for foundi in found ] )
    replace_mask = np.random.rand(len(found)) < prob     
    atoms_ = []
    for iatom,atom in enumerate( atoms ):
        if(iatom in foundDict ): continue
        atoms_.append(atom)
    for i,foundi in enumerate(found):
        if replace_mask[i]:
            iatom = foundi[0]
            bvec  = foundi[1]
            rb    = np.linalg.norm(bvec)
            bvec *= ( bond_length - rb )/rb
            #mat  = makeRotMat( bvec, Ups[i] )
            pos   = atoms[iatom,1:]
            #print pos
            group_= groupToAtom( pos+bvec, bvec, Ups[i], group.copy() )
            for atom in group_:
                atoms_.append( atom )
    return atoms_

def prepareReplaceGroups( replaces ):
    group_dct={}
    #print replaces
    for val in replaces.values():
        val[2] = np.array(val[2]); val[2] /= np.linalg.norm( val[2] )
        val[3] = np.array(val[3]); val[2] /= np.linalg.norm( val[2] )
        print val[2],val[3]
        if not val[0] in group_dct:
            print "loading group: ", val[0]
            group_dct[val[0]]  = np.genfromtxt( val[0], skip_header=1 )
            #group_dct[val[0]]  = ( au.loadAtoms(item[1]) ,)
    return group_dct
    
def replaceAtomTypes( atoms, replaces, group_dct ):   
    atoms_ = []
    for iatom,atom in enumerate( atoms ):
        if( atom[0] in replaces ):
            repl               = replaces[atom[0]]
            group_atoms        = group_dct[repl[0]].copy()
            group_atoms[:,1:]  = group_atoms[:,repl[4]]
            group_atoms[:,1:] -= group_atoms[repl[1],1:] 
            group_= groupToAtom( atom[1:], repl[2], repl[3], group_atoms )
            #group_ = group_atoms
            for atom in group_:
                atoms_.append( atom )
        else:
            atoms_.append(atom)
    return atoms_

def pbc_tile( xyzs, lvec, enames=None, Zs=None, n=(2,2,2), n0=(0,0,0) ):
    xyzs_=[]
    for ia in range(n0[0],n[0]):
        for ib in range(n0[1],n[1]):
            for ic in range(n0[2],n[2]):
                xyzs_   .append( xyzs + (lvec[0]*ia + lvec[1]*ib + lvec[2]*ic)[np.newaxis,:] )
    xyzs_ = np.concatenate( xyzs_ )
    ntot = (n[0]-n0[0])*(n[1]-n0[1])*(n[2]-n0[2])
    Zs_=None; enames_=None
    if enames is not None: enames_ = enames*   ntot
    if Zs     is not None: Zs_     = np.tile(Zs,ntot)
    return xyzs_,Zs_,enames_ 

def pbc_roll( xyzs, lvec, d=(0.5,0.5,0.5) ):
    ilvec = np.linalg.inv( lvec )
    abcs  = np.dot( xyzs, ilvec ) 
    abcs[:,0]  = np.mod( abcs[:,0]+d[0], 1.0 )
    abcs[:,1]  = np.mod( abcs[:,1]+d[1], 1.0 )
    abcs[:,2]  = np.mod( abcs[:,2]+d[2], 1.0 )
    xyzs_ = np.dot( abcs, lvec )
    return xyzs_ 

def saveAtoms( atoms, fname, xyz=True ):
    fout = open(fname,'w')
    fout.write("%i\n"  %len(atoms) )
    if xyz==True : fout.write("\n") 
    for i,atom in enumerate( atoms ):
        #print( i, atom )
        fout.write("%i %f %f %f\n"  %( atom[0], atom[1], atom[2], atom[3] ) )
    fout.close() 
        
#def loadCoefs( characters=['s','px','py','pz'] ):
def loadCoefs( characters=['s'] ):
    dens = None
    coefs = []
    for char in characters:
        fname  = 'phi_0000_%s.dat' %char
        print( fname )
        raw = np.genfromtxt(fname,skip_header=1)
        Es  = raw[:,0]
        cs  = raw[:,1:]
        sh  = cs.shape
        print( "shape : ", sh )
        cs  = cs.reshape(sh[0],sh[1]//2,2)
        d   = cs[:,:,0]**2 + cs[:,:,1]**2
        coefs.append( cs[:,:,0] + 1j*cs[:,:,1] )
        if dens is None:
            dens  = d 
        else:
            dens += d
    return dens, coefs, Es


def findCOG( ps, byBox=False ):
    if(byBox):
        xmin=ps[:,0].min(); xmax=ps[:,0].max();
        ymin=ps[:,1].min(); ymax=ps[:,1].max();
        zmin=ps[:,2].min(); zmax=ps[:,2].max();
        return np.array( (xmin+xmax, ymin+ymax, zmin+zmax) ) * 0.5
    else:
        cog = np.sum( ps, axis=0 )
        cog *=(1.0/len(ps))
        return cog

def histR( ps, dbin=None, Rmax=None, weights=None ):
    rs = np.sqrt(np.sum((ps*ps),axis=1))
    bins=100
    if dbin is not None:
        if Rmax is None:
            Rmax = rs.max()+0.5
        bins = np.linspace( 0,Rmax, int(Rmax/(dbin))+1 )
    print( rs.shape, weights.shape )
    return np.histogram(rs, bins, weights=weights)



    
