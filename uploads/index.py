import numpy as np
print("3(17):create numpy program to find index")
array1=np.array([[1,2,3],[4,5,6],[7,8,9]])
array2=np.array([4,5,6])
index=np.where(np.all(array1==array2,axis=1)[])
print("array1:",array1)
print("array2:",array2)
print("index:",index)
      
      
