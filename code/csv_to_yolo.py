import csv
import numpy as np
import os

def csv_to_yolo(csv_file,destination_folder):
    if not os.path.exists(destination_folder+'\data'):
        os.makedirs(destination_folder+'\data')
        classes_names = []
    file_names = []
    data = csv.reader(open(csv_file))
    for l in data:
        file_names.append(l[4])
        classes_names.append(l[0])
    classes_names = np.unique(classes_names)
    classes = {k: v for v, k in enumerate(classes_names)}
    f=open(destination_folder+"/data/"+ 'classes.names','a')
    for i in classes_names:
        f.write(str(i))
        f.write('\n')
    f.close()
    for name in np.unique(file_names):
        file = open(destination_folder+'/data/'+str(name[:-4])+".txt",'a')
        for l in csv.reader(open(csv_file)):
            if(l[4]==name):
                file.write(str(classes[l[0]]))
                file.write(' ')
                file.write(l[1])
                file.write(' ')
                file.write(l[2])
                file.write(' ')
                file.write(l[3])
                file.write(' ')
                file.write('\n')
    file.close()
    
csv_to_yolo('data/luna16/csv/evaluationScript/annotations/annotations.csv', 
            'data/luna16/txt/evaluationScript')