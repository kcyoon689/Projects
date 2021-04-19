# -*- coding:utf-8 -*-
from pylab import plot,show,axis,legend
import copy
import math
import matplotlib.pyplot as plt
import numpy as np

# 기본 수학량들 / 기본 측정계수들
ex=[[1,0,0]]
ey=[[0,1,0]]
ez=[[0,0,1]]
ex2=[[1],[0],[0]]
ey2=[[0],[1],[0]]
ez2=[[0],[0],[1]]

avwind0001 = [10904.45, 10974.73, 11045.18, 11115.80, 11186.59, 11257.56, 11328.69, 11400.00, 11471.48, 11543.14, 11614.96, 11686.97, 11759.15, 11831.5, 11904.04, 11976.74, 12049.63, 12122.7, 12195.95, 12269.37, 12342.98, 12416.77, 12490.74, 12564.89, 12639.23, 12713.75, 12788.46, 12863.36, 12938.43]
# len=29
avwind0002 = [10974.73, 11045.18, 11115.80, 11186.59, 11257.56, 11328.69, 11400.00, 11471.48, 11543.14]
# len=9
avwind0003 = [27488.42, 27720.59, 27837.21, 27954.19, 28071.54, 28189.26, 28307.34, 28425.78, 28544.6, 29023.62]
# len=10

# def windx_quadratic(bend):
	# return -5.35127+0.063962*((743961-62.5371*bend)**(0.5))

# def windy_quadratic(bend):
	# return 6.91912-0.0618259*((49.1684*bend-543420)**(0.5))
	
# def windz_quadratic(bend):
	# return 3-2.27992+0.253715*((110750-3.94143*bend)**(0.5))

# def wind_quadratic(x,y,z):
	# return [windx_quadratic(x),windy_quadratic(y),windz_quadratic(z)]


def average(list):
	temp7=copy.deepcopy(list)
	sum2=0
	if len(list)==0:
		return 0
	else:
		for i in range(0,len(list)):
			sum2+=temp7[i]
		return sum2/len(list)
	
def standardDeviation(list):
	temp8=copy.deepcopy(list)
	avg=average(temp8)
	sum3=0
	for i in range(0,len(list)):
		sum3+=(avg-list[i])**2
	return sum3/len(list)
	
def size(mat):
	sum=0
	for i in range(0,len(mat[0])):
		temp9=copy.deepcopy(mat)
		sum+=temp9[0][i]**2
	return math.sqrt(sum)
	

#행렬 연산
def	matMakeO(column,row):
	matrix=[[0]*row for i in range(column)]
	return matrix
	
def matMakeNone(column,row):
	matrix2=[[]*row for i in range(column)]
	return matrix2

def matMakeC(length,C):
	if length==0:
		return []
	else:
		matrix3=[[C]*length for i in range(length)]
		return matrix3[0]

def matxC(cons,mat):
	column=len(mat)
	row=len(mat[0])
	for i in range(0,column):
		for j in range(0,row):
			mat[i][j]*=cons
	return mat

def matxM(mat1,mat2):
	column=len(mat1)
	row=len(mat2[0])
	mid=len(mat2)
	temp=matMakeO(column,row)
	
	for i in range(0,column):
		for j in range(0,row):
			sum=0
			for k in range(0,mid):
				sum+=mat1[i][k]*mat2[k][j]
			temp[i][j]=sum
	return temp
	
def matTranspose(mat):
	temp6=copy.deepcopy(mat)
	column=len(temp6)
	row=len(temp6[0])
	mat3=matMakeO(row,column)
	for i in range(0,row):
		for j in range(0,column):
			mat3[i][j]=temp6[j][i]
	return mat3

def matMinor3x3(mat,a,b):
	temp1=copy.deepcopy(mat)
	for i in range(0,3):
		del temp1[i][b-1]
	del temp1[a-1]
	return detM2x2(temp1)	

def detM2x2(mat):
	det=mat[0][0]*mat[1][1]-mat[0][1]*mat[1][0]
	return det

def detM3x3(mat):
	detm=0
	for i in range(0,3):
			temp3=copy.deepcopy(mat)
			detm+=mat[i][0]*((-1)**(i))*matMinor3x3(temp3,i+1,1)
	return detm

def matInv3x3(mat):
	temp5=copy.deepcopy(mat)
	coft=matMakeO(3,3)
	det2=detM3x3(temp5)
	for i in range(0,3):
		for j in range(0,3):
			temp4=copy.deepcopy(mat)
			coft[i][j]=((-1)**(i+j))*matMinor3x3(temp4,i+1,j+1)
	inverse=matxC((1.0/det2),matTranspose(coft))
	return inverse

def matRearr(mat):
	temp=copy.deepcopy(mat)
	temp2=copy.deepcopy(mat)
	row=len(temp)
	i=0
	while temp[0][0]==0:
		if temp[i][0]!=0:
			temp[0]=temp2[i]
			temp[i]=temp2[0]
			break
		i+=1
	return temp

def matREF(mat):
	temp=copy.deepcopy(matRearr(mat))
	row=len(temp)
	column=len(temp[0])
	i=0
	while i<row-1:
		for j in range(1,row-i):
			a=temp[i+j][i]/float(temp[i][i])
			for k in range(0,column):
				temp[i+j][k]-=a*temp[i][k]
		i+=1
	return temp

def matRREF(mat):
	temp=copy.deepcopy(matREF(mat))
	row=len(temp)
	column=len(temp[0])
	i=row-1
	zz=0
	while i>=0:
		for j in range(1,row-zz):
			a=temp[i-j][i]/float(temp[i][i])
			for k in range(0,column):
				temp[i-j][k]-=a*temp[i][k]
		i-=1
		zz+=1
	for l in range(0,row):
		b=temp[l][l]
		for m in range(0,column):
			temp[l][m]/=b
	return temp

#변환행렬
def convAxis(theta,axis):
	cos1=math.cos(math.radians(theta))
	sin1=math.sin(math.radians(theta))
	if axis=="x":
		conv1=[[1,0,0],[0,cos1,sin1],[0,-sin1,cos1]]
	elif axis=="y":
		conv1=[[cos1,0,-sin1],[0,1,0],[sin1,0,cos1]]
	else:
		conv1=[[cos1,sin1,0],[-sin1,cos1,0],[0,0,1]]
	return conv1

def convAxis2(theta,axis):
	cos1=(math.cos(math.radians(theta)))**2
	sin1=(math.sin(math.radians(theta)))**2
	if axis=="x":
		conv1=[[1,0,0],[0,cos1,sin1],[0,-sin1,cos1]]
	elif axis=="y":
		conv1=[[cos1,0,-sin1],[0,1,0],[sin1,0,cos1]]
	else:
		conv1=[[cos1,sin1,0],[-sin1,cos1,0],[0,0,1]]
	return conv1

def convMat(pitch,roll,yaw):
	conv2=matxM(matxM(convAxis(roll,"x"),convAxis(pitch,"y")),convAxis(yaw,"z"))
	return conv2

def convMat2(pitch,roll,yaw):
	conv2=matxM(matxM(convAxis2(roll,"x"),convAxis2(pitch,"y")),convAxis2(yaw,"z"))
	return conv2

def axisVec(x,y,z):
	M2=matTranspose(convMat(x,y,z))
	xyzcomma=matxM(M2,[[1,0,0],[0,1,0],[0,0,1]])
	return matTranspose(xyzcomma)

def cosBetVec(mat1,mat2):
	sum4=0
	for i in range(0,len(mat1[0])):
		temp10=copy.deepcopy(mat1)
		temp11=copy.deepcopy(mat2)
		sum4+=temp10[0][i]*temp11[0][i]
	if size(mat1)==0 or size(mat2)==0:
		return 0
	else:
		return sum4/(size(mat1)*size(mat2))

# 초기화
length=7
data_axis=[[0,0,0]]
data_force=[[0],[0],[0]]
bendx=[[],[],[],[],[],[],[],[]]	#bendx[absolute_wind]=[[convert_wind1,flex1],[convert_wind2,flex2]....]
bendy=[[],[],[],[],[],[],[],[]]
bendz=[[],[],[],[],[],[],[],[]]
windconvxyz=[[],[],[]]
flexlist=[[],[],[]]
meter=0
idk=1

# data_axis2=[[],[],[]]
# data_flex2=[[],[],[]]
# avg_axis=[[],[],[],[],[],[],[],[]]
# avg_flex=[[],[],[],[],[],[],[],[]]

#실행
while meter<=7 and idk<=8:
	data_windraw=raw_input().split()	#(pitch,roll,yaw,flex1,flex2,flex3,wind)
	length=len(data_windraw)
	windconvxyz=[[],[],[]]
	if length==0:
		# for j in range(0,3):
			# avg_axis[meter].append(average(data_axis2[j]))
			# avg_flex[meter].append(average(data_flex2[j]))
		meter+=1
		if meter==8:
			meter=0
		idk+=1
		# data_axis2=[[],[],[]]
		# data_flex2=[[],[],[]]
		continue
	else:
		for i in range(0,3):
			data_axis[0][i]=float(data_windraw[i])
		for j in range(3,6):
			data_force[j-3][0]=float(data_windraw[j])
		# for k in range(0,3):
			# data_axis2[i].append(float(data_windraw[i]))
			# data_flex2[i].append(float(data_windraw[i+3]))
		
		wind2=[[float(data_windraw[6])],[0],[0]]
	
		cosx=cosBetVec(wind2,[axisVec(data_axis[0][0],data_axis[0][1],data_axis[0][2])[0]])
		cosy=cosBetVec(wind2,[axisVec(data_axis[0][0],data_axis[0][1],data_axis[0][2])[1]])
		cosz=cosBetVec(wind2,[axisVec(data_axis[0][0],data_axis[0][1],data_axis[0][2])[2]])
		
		bendx[meter].append([wind2[0][0]*((cosx)**2),data_force[0][0]])
		bendy[meter].append([wind2[0][0]*((cosy)**2),data_force[1][0]])
		bendz[meter].append([wind2[0][0]*((cosz)**2),data_force[2][0]])



# avflex01=[]
# avflex02=[]
# avflex03=[]	

# for i in range(0,8):
	# for j in range(0,len(bendx[i])):
		# if avflex01.count(bendx[i][j][1])==0:
			# avflex01.append(bendx[i][j][1])
		# avwind01.append(bendx[i][j][0])
	# for k in range(0,len(bendy[i])):
		# if avflex02.count(bendy[i][k][1])==0:
			# avflex02.append(bendy[i][k][1])
		# avwind02.append(bendy[i][k][0])
	# for l in range(0,len(bendz[i])):
		# if avflex03.count(bendz[i][l][1])==0:
			# avflex03.append(bendz[i][l][1])
		# avwind03.append(bendz[i][l][0])

avwind01=matMakeNone(len(avwind0001),1)
avwind02=matMakeNone(len(avwind0002),1)
avwind03=matMakeNone(len(avwind0003),1)

for i in range(0,8):
	for j in range(0,len(bendx[i])):
		avwind01[avwind0001.index(bendx[i][j][1])].append(bendx[i][j][0])
	for k in range(0,len(bendy[i])):
		avwind02[avwind0002.index(bendy[i][k][1])].append(bendy[i][k][0])
	for l in range(0,len(bendz[i])):
		avwind03[avwind0003.index(bendz[i][l][1])].append(bendz[i][l][0])
		
x1=[]
y1=[]
x2=[]
y2=[]
x3=[]
y3=[]
# xav1=[]
# yav1=[]
# xav2=[]
# yav2=[]
# xav3=[]
# yav3=[]
for bb in range(0,len(avwind01)):
	x1.extend(matMakeC(len(avwind01[bb]),avwind0001[bb]))
	y1.extend(avwind01[bb])
for cc in range(0,len(avwind02)):
	x2.extend(matMakeC(len(avwind02[cc]),avwind0002[cc]))
	y2.extend(avwind02[cc])
for zz in range(0,len(avwind03)):
	x3.extend(matMakeC(len(avwind03[zz]),avwind0003[zz]))
	y3.extend(avwind03[zz])
	
# for i in range(0,8):
	# xav1.append(avg_flex[i][0])
	# xav2.append(avg_flex[i][1])
	# xav3.append(avg_flex[i][2])
	
# for j in range(0,8):
	# yav1.append(average(y1))
	# yav2.append(average
	# yav3

idk001=0
idk002=0
idk003=0
idk004=0
idk005=0
for aaa in range(0,len(x1)):
	idk001+=x1[aaa]**2
	idk002+=x1[aaa]
	idk003+=x1[aaa]*y1[aaa]
	idk004+=1
	idk005+=y1[aaa]

ans01=matRREF([[idk001,idk002,idk003],[idk002,idk004,idk005]])
linar_a=ans01[0][2]
linar_b=ans01[1][2]

xxx=range(int(min(x1)),int(max(x1)))
yyy=[(linar_a*v)+linar_b for v in xxx]

# 1 2 3 a 
# 2 3 4 b
# 3 4 5 c
idk101=0
idk102=0
idk103=0
idk104=0
idk105=0
idk10a=0
idk10b=0
idk10c=0
for bbb in range(0,len(x1)):
	idk101+=1
	idk102+=x1[bbb]
	idk103+=x1[bbb]**2
	idk104+=x1[bbb]**3
	idk105+=x1[bbb]**4
	idk10a+=y1[bbb]
	idk10b+=y1[bbb]*x1[bbb]
	idk10c+=y1[bbb]*(x1[bbb]**2)

ans02=matRREF([[idk101,idk102,idk103,idk10a],[idk102,idk103,idk104,idk10b],[idk103,idk104,idk105,idk10c]])

print "linar approximate :",linar_a,"x +",linar_b


quadratic_c=ans02[0][3]
quadratic_b=ans02[1][3]
quadratic_a=ans02[2][3]

print "quadratic approximate :",quadratic_c,"x^2 +",quadratic_b,"x +",quadratic_a
xxxx=range(int(min(x1)),int(max(x1)))
yyyy=[(quadratic_a*(vv**2))+(quadratic_b*vv)+quadratic_c for vv in xxxx]

plt.plot(xxx,yyy,label='linar approximate')
plt.plot(xxxx,yyyy,label='quadratic approximate')



plt.plot(x1,y1,'ro',label='Flex01_conv')
plt.plot(x2,y2,'bo',label='Flex02_conv')
# plt.plot(x3,y3,'go',label='Flex03_conv')
# plt.plot(xav1,yav1,label='Flex01_raw')
# plt.plot(xav2,yav2,label='Flex02_raw')
plt.legend()
plt.show()



for j in range(0,len(avwind0001)):
	if len(avwind01[j])!=0:
		print "Flex 01 저항:",avwind0001[j],"	풍속의 범위:",min(avwind01[j]),"~",max(avwind01[j]),"		평균 풍속:",average(avwind01[j]),"	데이터 수:",len(avwind01[j])
print ""
for k in range(0,len(avwind0002)):
	if len(avwind02[k])!=0:
		print "Flex 02  저항:",avwind0002[k],"	풍속의 범위:",min(avwind02[k]),"~",max(avwind02[k]),"			평균 풍속:",average(avwind02[k]),"	데이터 수:",len(avwind02[k])
print ""
for l in range(0,len(avwind0003)):
	if len(avwind03[l])!=0:
		print "Flex 03 저항:",avwind0003[l],"	풍속의 범위:",min(avwind03[l]),"~",max(avwind03[l]),"			평균 풍속:",average(avwind03[l]),"	데이터 수:",len(avwind03[l])