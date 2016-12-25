import numpy as np

def numpy_transform(numpy_array):
	numpy_array_tmp=numpy_array;
	numpy_array_tmp=np.argsort(-numpy_array_tmp)
	top20_value=[]
	top20_line=[]
	top20_column=[]
	for i in range (0,20,1):
		top20_value.append(numpy_array[numpy_array_tmp[i]])#top 20
		top20_line.append(int(numpy_array_tmp[i]/19))#top 20's line'
		top20_column.append(numpy_array_tmp[i]%19)#top 20's column'
	return top20_value,top20_line,top20_column
