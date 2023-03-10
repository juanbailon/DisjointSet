import argparse
from typing import List


## ------------- AJUSTES PARA UNSAR COMMAND LINE ARGUMENTS  ------------ ##
parser = argparse.ArgumentParser()
parser.add_argument("input_files_paths", type=str, help="instructions input file", nargs='+')
parser.add_argument("-o", "--output", type=str, help="program output file", default="output.txt", nargs='?')
CLI_args = parser.parse_args()


## --------------- SOLUCION AL PROBLEMA PLANTEO DE LOS DEPARTAMENTOS --------------- ##

class DisjointSet:

    def __init__(self, n:int):
        """ Creates an instance of DisjointSet whit n starting sets """
        self.parents = [i for i in range(n)]
        self.size = [1 for i in range(n)]

    def find(self, i:int)->int:
        """ finds the root of the set where belongs given element """
        root = i
        while (self.parents[root] != root):
            root = self.parents[root]

        self.compress_path(i, root)

        return root

    def compress_path(self, i:int, root:int)->None:   
        """ makes the elements that are in the path from the given element
            to the set's root point straight  to the root 
        """     
        while(i != root):
            self.parents[i], i = root, self.parents[i]  
    
    def same_set(self, i:int, j:int)->bool:
        """ if the two given elements are part of the same set returns True, otherwise False """
        return self.find(i) == self.find(j)


    def unify(self, i:int, j:int)->None: 
        """ unies two sets so that they become one set """     
        if(self.same_set(i, j)):        
            return
            
        root1 = self.find(i)
        root2 = self.find(j)
            
        if(self.size[root1] > self.size[root2]):         
            self.size[root1] += self.size[root2]
            self.size[root2] = 0
            self.parents[root2] = root1 
            #this step following is not mandatory, but it helps with futere find() operaions so that they takes less time     
            self.compress_path(j, root1)
        else:        
            self.size[root2] += self.size[root1]        
            self.size[root1] = 0        
            self.parents[root1] = root2        
            self.compress_path(i, root2)                


    def unify_range(self, i:int, j:int)->None:
        """ unies all the sets that are within the given range """
        if(self.same_set(i, j)):        
            return

        for k in range(i, j+1):
            self.unify(i, k)



def deparments(N:int, Q:int, OPS:List[int])->List[bool]:
    """ N: number of deparments in the company
        Q: total number of queries
        OPS: list containing the type of querie and the two elements on which the action will be executed

        Creates a DisjointSet object whit N starting elements, and then ejecutes the actions especify
        by each querie with the two elements/sets given in the querie.
        The function return a list with the results of all the queries which query type is equal to 3 
     """
    if(type(OPS)!=list):
        raise TypeError(f'OPS type {type(OPS)} is NOT a list')
    if(Q != len(OPS)):
        raise ValueError('Second parameter Q should be iqueal to the OPS list size')

    results = []
    ds = DisjointSet(N)
    # print(ds.parents)
    # print(ds.size)
    # print('------------------')

    for queary in OPS:
        q_type = queary[0]
        d1 = queary[1]-1
        d2 = queary[2]-1

        if(q_type == 1):            
            ds.unify(d1, d2)
        elif(q_type == 2):            
            ds.unify_range(d1, d2)
        elif(q_type == 3):            
            flag = ds.same_set(d1, d2)
            results.append(flag)
        else:
            raise ValueError('first element of the queary should be an integer between this range [1,3]')
  
    # print(ds.parents)
    # print(ds.size)
    return results


###  TEST  ###
quearies = [
    [3, 2, 5],
    [1, 2, 5],
    [3, 2, 5],
    [2, 4, 7],
    [2, 1, 2],
    [3, 1, 7]
]
assert deparments(8, 6, quearies) == [False, True, True], 'Prueba de escritorio fallo' 



## -------------- LECTURA Y ESCRITURA DE ARCHIVOS txt ----------------- ##

def read_commands_file(file_path):
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    instructions = [command.strip().split() for command in lines ]

    return instructions



def write_output_file(file_path, results, mode):
    with open(file_path, mode) as f:
        for value in results:
            f.write(str(value)+"\n")

        if( len(CLI_args.input_files_paths) > 1 ):
            f.write("----------------------- \n")



def get_commands_list(instructions):
    for sub_list in instructions:
        for i  in range(len(sub_list)):
            sub_list[i] = int(sub_list[i])

    return instructions



## -------------- INICIO DE EJECUCION DEL PROGRAMA ----------------- ##

input_files = CLI_args.input_files_paths
output_file = CLI_args.output

mode = "w+"
for i in range(len(input_files)):
    instructions = read_commands_file(input_files[i])
    commands = get_commands_list(instructions)

    N = commands[0][0]
    Q = commands[0][1]
    my_queries = commands[1:]

    results = deparments(N, Q, my_queries)

    mode = "w+" if i==0 else "a+"
    write_output_file(output_file, results, mode)

    


