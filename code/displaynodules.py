import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
filename='subset0/subset0/1.3.6.1.4.1.14519.5.2.1.6279.6001.105756658031515062000744821260.mhd'
itkimage = sitk.ReadImage(filename)
OR=itkimage.GetOrigin()
print(OR)
SP=itkimage.GetSpacing()
print(SP)
numpyImage = sitk.GetArrayFromImage(itkimage)

def show_nodules(ct_scan, nodules,Origin,Spacing,radius=20, pad=2, max_show_num=4): 
    show_index = []
    for idx in range(nodules.shape[0]): 
        if idx < max_show_num:
            if abs(nodules[idx, 0]) + abs(nodules[idx, 1]) + abs(nodules[idx, 2]) + abs(nodules[idx, 3]) == 0:
                continue

            x, y, z = int((nodules[idx, 0]-Origin[0])/SP[0]), int((nodules[idx, 1]-Origin[1])/SP[1]), int((nodules[idx, 2]-Origin[2])/SP[2])
        print(x, y, z)
        data = ct_scan[z]
        radius=int(nodules[idx, 3]/SP[0]/2)
        #pad = 2*radius
        data[max(0, y - radius):min(data.shape[0], y + radius),
        max(0, x - radius - pad):max(0, x - radius)] = 3000 
        data[max(0, y - radius):min(data.shape[0], y + radius),
        min(data.shape[1], x + radius):min(data.shape[1], x + radius + pad)] = 3000 
        data[max(0, y - radius - pad):max(0, y - radius),
        max(0, x - radius):min(data.shape[1], x + radius)] = 3000 
        data[min(data.shape[0], y + radius):min(data.shape[0], y + radius + pad),
        max(0, x - radius):min(data.shape[1], x + radius)] = 3000 

        if z in show_index: 
            continue
        show_index.append(z)
        plt.figure(idx)
        plt.imshow(data, cmap='gray')

    plt.show()

b = np.array([[-116.2874457,21.16102581,-124.619925,10.88839157],[-111.1930507,-1.264504521,-138.6984478,17.39699158],[73.77454834,37.27831567,-118.3077904,8.648347161]])
show_nodules(numpyImage,b,OR,SP)