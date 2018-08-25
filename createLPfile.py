#generate the nodes of source, transit, destination
X = int(input('The amount of source nodes:'))
Y = int(input('The amount of transit nodes:'))
Z = int(input('The amount of destination nodes:'))
N = 3

print('Source nodes : {}\ntransit nodes : {}\nDestination node : {}'.format(X, Y, Z))
print('---------------------')


def DV_contraint():
    '''return the demand volume constraint: 
    Xikj = hij
    which Xikj means the sum of load between source i to destination j'''
    DV = []
    demand_equation = []
    for i in range(1, X + 1):
        for j in range(1, Z + 1):
            dv = []
            for k in range(1, Y + 1):
                dv.append("x{}{}{}".format(i, k, j))
            DV = ' + '.join(dv) + ' = {}'.format(i + j)
            demand_equation.append(DV)
    demand_constraint = '\n'.join(demand_equation)
    return demand_constraint


def ST_capp_constraint():
    '''return the cappacity constraint from source to transit node'''
    ST = []
    capp1_equation = []
    for i in range (1, X + 1):
        for k in range (1, Y +1):
            st = []
            for j in range(1, Z+1):
                st.append('x{}{}{}'.format(i, k, j))
            ST = ' + '.join(st) + ' - c{}{} <= 0'.format(i, k)
            capp1_equation.append(ST)
    capp1_constraint = '\n'.join(capp1_equation)
    return capp1_constraint


def TD_capp_constraint():
    '''return the cappacity constraint from transit node to dest node'''
    TD = []
    capp2_equation = []
    for k in range(1, Y+1):
        for j in range(1, Z+1):
            td = []
            for i in range(1, X+1):
                td.append('x{}{}{}'.format(i, k, j))
            TD = ' + '.join(td) + ' - d{}{} <= 0'.format(k, j)     
            capp2_equation.append(TD)
    capp2_constraint = '\n'.join(capp2_equation)
    return capp2_constraint


def TN_constraint():
    '''return the constraint of load of transit nodes which should be minimize'''
    TN = []
    tn_equation = []
    for k in range(1, Y + 1):
        tn = []
        for j in range(1, Z + 1):
            for i in range(1, X + 1):
                tn.append('x{}{}{}'.format(i, k, j))
        TN = ' + '.join(tn) + ' - r <= 0'.format(k, j)     
        tn_equation.append(TN)
    tn_constraint = '\n'.join(tn_equation)
    return tn_constraint


def BV_constriant():
    '''return the binary variables constraint: 
    Uikj = Nk 
    which Uikj means the sum of used paths and Nk = N in this problem'''
    BV = []
    binary_equation = []
    for i in range(1, X + 1):
        for j in range(1, Z + 1):
            bv = []
            for k in range(1, Y + 1):
                bv.append("u{}{}{}".format(i, k, j))
            BV = ' + '.join(bv) + ' = {}'.format(N)
            binary_equation.append(BV)
    binary_constraint = '\n'.join(binary_equation)
    return binary_constraint
 
 
def DF_constraint():
    '''return the demand flow constraint:
    Nk * Xikj = hij * Uikj'''
    DF = []
    flow_equation = []
    for i in range(1, X + 1):
        for j in range(1, Z + 1):
            for k in range(1, Y + 1):
                DF = '{} x{}{}{} - {} u{}{}{} = 0'.format(N, i, k, j, i + j, i, k, j)
                flow_equation.append(DF)
    demand_flow_constraint = '\n'.join(flow_equation)
    return demand_flow_constraint

                
def Bounds_variable():
    '''return the bounds of demand variable : Xikj of this problem'''
    bound_x = []
    bound_unequation_x = []
    for i in range(1, X + 1):
        for j in range(1, Z + 1):
            for k in range(1, Y + 1):
                bound_x = '0 <= x{}{}{}'.format(i, k, j)
                bound_unequation_x.append(bound_x)
    Bounds_x = '\n'.join(bound_unequation_x)
    return Bounds_x


def binary_constraint():
    '''return binary constraints'''
    bc = ''
    for i in range(1, X+1):
        for k in range(1, Y+1):
            for j in range(1, Z+1):
                bc += 'u{}{}{}\n'.format(i,k,j)
    return bc


def createLP():
    '''create a LP file for this problem'''
    f = open(filename, 'w')
    content = \
    '''Minimize
    r
Subject to
demand volume: \n{}
srouce to tranfer node capp1: \n{}
transit to destination node capp2: \n{}
transit nodes: \n{}
binary variables: \n{}
demand flow: \n{}
Bounds
{}
0 <= r
Binaries
{}
End'''.format(demand_volume, ST_capacity,
              TD_capacity, transit_nodes, binary_variables, demand_flow, bounds_x, binaries)
    f.write(content)
    f.close


def set_filename():
    '''return the filename : XYZ.lp which Y belongs to {3, 4, 5, 6, 7}'''
    filename = '{}{}{}.lp'.format(X, Y, Z)
    return filename


demand_volume = DV_contraint()
ST_capacity = ST_capp_constraint()
TD_capacity = TD_capp_constraint()
transit_nodes = TN_constraint()
binary_variables = BV_constriant()
demand_flow = DF_constraint()
bounds_x = Bounds_variable()
binaries = binary_constraint()
filename = set_filename()


createLP()
