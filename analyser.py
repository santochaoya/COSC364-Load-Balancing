import subprocess
import time
import json

def CPLEX(filename):
    '''run CPLEX to solve the problem of given lp file'''
    #args1 = ['/Users/mac/Desktop/364/a2/cplex', '-c', 'read /Users/mac/Desktop/364/a2/' + filename, 'optimize',
            #'display solution variable -']
    args1 = ['/Users/zelta/Desktop/cplex', '-c', 'read /Users/zelta/Desktop/' + filename, 'optimize',
            'display solution variable -']
        
    time1 = time.time()
    process1 = subprocess.Popen(args1, stdout = subprocess.PIPE)

    output, error = process1.communicate()
    time2 = time.time()
    execution_time = time2 - time1
       
   # print('Execution_time: '+str("%.5f" % (execution_time))+'seconds')
    result = output.decode("utf-8").split()
    
    start = result.index("Incumbent")
    load = {}
    links = []
    link_count = 0
    cappacities = {}
    cappacities = {'max':[0,[]]}
    max_cappacity = 0.0
    for i in range(1,8):
        load[i] = float(0)
    for n in result[start:]:
        if n.startswith('x'):
            transit_node = int(n[2])
            x_index = result.index(n)
            load[transit_node] += float(result[x_index+1])
        if (n.startswith('c') or n.startswith('d')) and len(n) == 3:
            capp_index = result.index(n)
            cappacity = float(result[capp_index+1])
            if cappacity > 0:
                link_count += 1
                links.append(n)
            if cappacity == max_cappacity:
                cappacities['max'][1].append(n)            
            if cappacity > max_cappacity:
                max_cappacity = cappacity
                cappacities['max'][0] = max_cappacity
                cappacities['max'][1]= [n]
                                                    
    result = 'Execution_time: '+str("%.5f" % (execution_time))+'seconds\n'+'Load on transit nodes: '+json.dumps(load)+'\n'+'Maximum cappacity: '+json.dumps(cappacities)+'\nNon-zero capacity link count: '+str(link_count)+'\nNon-zero capacity links: '+' '.join(links)                                  
    return result
    


def main():

    '''filename = 'X4Z'   
    result = CPLEX(filename+'.lp')
    f=open(filename+'_analyser.txt','w')
    f.write(result)
    f.close()'''
    
    #print(result)
    
    for n in range(3, 8):
        filename = '7{}7.lp'.format(n)
        print(filename)
        result = CPLEX(filename)
        f = open(filename + '_analyser.txt','w')
        f.write(result)
        f.close()

main()