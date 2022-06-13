list = [0,1,2,3] 
dir_list_final = []
id_arq = []    
for i in range(len(list)):
    id_arq.append(i+1)
    dir_list_final.append(f"{id_arq[i]} - {list[i]}")
print(dir_list_final)
