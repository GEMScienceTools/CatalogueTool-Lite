def crea_ptable(Data):
    """
    """
    from prettytable import PrettyTable
    # Set table
    p = PrettyTable(["N1","Id01","N2","Id02","dT", "dS","dM","DZ"])

    p.align["Db01"] = 'l'
    p.align["Db02"] = 'l'
    p.align["Id01"] = 'l'
    p.align["Id02"] = 'l'

    p.align["dT"] = 'r'
    p.align["dS"] = 'r'
    p.align["dM"] = 'r'

    # Create table
    for D in Data:
        n1 = '%s' % (D[0])
        id01 = '%s' % (D[1])
        n2 = '%s' % (D[2])        
        id02 = '%s' % (D[3])    
        dt = '%6.2f' % (float(D[4]))
        ds = '%6.2f' % (float(D[5]))
        dm = '%6.2f' % (float(D[6])) 
        dz = '%6.2f' % (float(D[7])) 

        p.add_row([n1,id01,n2,id02,dt,ds,dm,dz])
    print p