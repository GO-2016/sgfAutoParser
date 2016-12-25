import numpy as np

def numpy_transform(a):
	b=a;
	b=np.argsort(-b)
	c=[]
	y=[]
	x=[]
	for i in range (0,20,1):
		c.append(a[b[i]])#top 20
		y.append(int(b[i]/19))#top 20's line'
		x.append(b[i]%19)#top 20's column'
	return c,y,x
