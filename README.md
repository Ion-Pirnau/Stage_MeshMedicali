# Stage_MeshMedicali
La cartella è così sviluppata:
CODE
    |
    mainBrain.py : programma main
    |
    FunctionforProcess
    |                 |
    |                 Contiene tutte funzioni necessarie per processare la mesh
    Process_Mesh
    |           |
    |           processing_functions.py : classe contenente le funzioni da FunctionforProcess per processare la mesh, classe usata da mainBrain.py per operare sulla mesh
    FunzioniUtili 
                 |
                 Utils.py : contiene un set di funzioni utilizzate da FunctionforProcess ed Process_Mesh

INPUT_SOURCE
              : contenente i file che devono essere processati (INPUT_SOURCE) e i risultati ottenuti (OUTPUT_SOURCE)
OUTPUT_SOURCE 
    
