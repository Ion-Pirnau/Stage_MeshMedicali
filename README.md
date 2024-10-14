# Stage_MeshMedicali
La [cartella] è così sviluppata

[CODE] contiene:

mainBrain.py : programma main

FunctionforProcess : Contiene tutte funzioni necessarie per processare la mesh

Process_Mesh - processing_functions.py : classe contenente le funzioni da FunctionforProcess per processare la mesh, classe usata da mainBrain.py per operare sulla mesh

FunzioniUtili - Utils.py : contiene un set di funzioni utilizzate da FunctionforProcess ed Process_Mesh
    
[INPUT_SOURCE OUTPUT_SOURCE]  : contenente i file che devono essere processati (INPUT_SOURCE) e i risultati ottenuti (OUTPUT_SOURCE)
    
PROBLEMA di Pymesh: l'installazione non avviene correttamente.

FIXED RIMOZIONE COMPONENTI NON CONNESSE: nel file png che ho inserito, andando a modificare la n_decimation si riesce a ottenere una mesh senza componenti connesse.



[TIME EXECUTION]:

remove_zero_area_faces : circa 3.97 sec

rimozione_not_connected_componente : circa 2.79 sec

scaling : circa 0.23 sec

repair_mesh : circa 4.62 sec
