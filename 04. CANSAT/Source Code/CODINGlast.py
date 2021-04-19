# -*- coding:utf-8 -*-
from pylab import plot,show,axis,legend
import copy
import math
import matplotlib.pyplot as plt
import numpy as np

# 측정계수
avwind0001 = [10904.45, 10974.73, 11045.18, 11115.80, 11186.59, 11257.56, 11328.69, 11400.00, 11471.48, 11543.14, 11614.96, 11686.97, 11759.15, 11831.5, 11904.04, 11976.74, 12049.63, 12122.7, 12195.95, 12269.37, 12342.98, 12416.77, 12490.74, 12564.89, 12639.23, 12713.75, 12788.46, 12863.36, 12938.43]
# len=29
avwind0002 = [10974.73, 11045.18, 11115.80, 11186.59, 11257.56, 11328.69, 11400.00, 11471.48, 11543.14]
# len=9
avwind0003 = [27488.42, 27720.59, 27837.21, 27954.19, 28071.54, 28189.26, 28307.34, 28425.78, 28544.6, 29023.62]
# len=10

#선형 근사식


#이차 근사식



#수학 연산
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
	if len(mat)==1:
		for i in range(0,len(mat[0])):
			temp9=copy.deepcopy(mat)
			sum+=temp9[0][i]**2
	elif len(mat[0])==1:
		for j in range(0,len(mat)):
			temp9=copy.deepcopy(mat)
			sum+=temp9[j][0]**2
	return math.sqrt(sum)


#행렬 연산

def matMake(column,row,C):
	if C=='x':
		matrix=[[]*row for i in range(column)]
	else:
		matrix=[[C]*row for i in range(column)]
	return matrix
	
def matxC(C,matrix3):
	column=len(matrix3)
	row=len(matrix3[0])
	temp=copy.deepcopy(matrix3)
	for i in range(0,column):
		for j in range(0,row):
			temp[i][j]*=C
	return temp
	
def matxM(mat1,mat2):
	column=len(mat1)
	row=len(mat2[0])
	mid=len(mat2)
	temp2=matMake(column,row,0)
	
	for i in range(0,column):
		for j in range(0,row):
			sum=0
			for k in range(0,mid):
				sum+=mat1[i][k]*mat2[k][j]
			temp2[i][j]=sum
	return temp2
	
def matTranspose(matrix2):
	temp3=copy.deepcopy(matrix2)
	column=len(temp3)
	row=len(temp3[0])
	temp4=matMake(row,column,0)
	for i in range(0,row):
		for j in range(0,column):
			temp4[i][j]=temp3[j][i]
	return temp4
	
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
	coft=matMake(3,3,0)
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
	
def convMat(pitch,roll,yaw):
	conv2=matxM(matxM(convAxis(roll,"x"),convAxis(pitch,"y")),convAxis(yaw,"z"))
	return conv2
	
def convMat2(pitch,roll,yaw):
	conv3=matxM(matxM(convAxis(yaw,"z"),convAxis(pitch,"y")),convAxis(roll,"x"))
	return conv3
	
def axisVec(x,y,z):
	M2=matInv3x3(convMat(x,y,z))
	xyzcomma=matxM(matInv3x3(M2),[[1,0,0],[0,1,0],[0,0,1]])
	return xyzcomma

def cosBetVec(mat1,mat2):	#두 벡터간의 코사인값
	sum4=0
	for i in range(0,len(mat1)):
		temp10=copy.deepcopy(mat1)
		temp11=copy.deepcopy(mat2)
		sum4+=temp10[i][0]*temp11[i][0]	#내적
	if size(mat1)==0 or size(mat2)==0:
		return 0
	else:
		return sum4/(size(mat1)*size(mat2))	#내적/크기

#근사

def functionApprox(datax,datay,degree):	#degree=차수
	length=len(datax)
	rawmat=matMake(degree+1,degree+2,0)
	
	for i in range(0,degree+1):
		for j in range(0,degree+1):
			for n in range(0,length):
				rawmat[i][j]+=(datax[n]**(i+j))
		for m in range(0,length):
			rawmat[i][degree+1]+=(datay[m]*(datax[m]**(i)))
		
	ans=[]
	temp99=matRREF(rawmat)
	for l in range(0,degree+1):
		ans.append(temp99[l][degree+1])
	return ans		#[0차차수,1차차수,2차차수..]
	
	
	
#확인	

cho=raw_input("Test for t/T, Real for r/R : ")
if cho=="T" or cho=="t":
	key=True
elif cho=="R" or cho=="r":
	key=False
	print"Not Ready Yet"

#초기화
windgiven=0

gap=1
row=0
windvec=[[0],[1],[0]]

flex=[[],[],[]]	#[flex01,flex02,flex03]
wind=[[],[],[]] #[wind01,wind02,wind03]

axis=[[],[],[]]	#[axis01,axis02,axis03]
coslist=[[],[],[]] #[cosx,cosy,cosz]

windspdlist=[]

#실행

if key:
	while gap<=11:
		windoriginvec=[[0],[0],[0]]
		windoriginspd=0			#초기화
		
		data_windraw=raw_input().split()		#데이터 받기
		for i in range(0,len(data_windraw)):
			data_windraw[i]=float(data_windraw[i])
		
		if len(data_windraw)==0:	#공란 재기
			gap+=1
			continue
			
		else:
			windgiven=data_windraw[6]					#초기 데이터 분류
			for i in range(0,3):
				axis[i].append(data_windraw[i])
				flex[i].append(data_windraw[i+3])
			
			axisvec=axisVec(axis[0][row],axis[1][row],axis[2][row])
			for j in range(0,3):			#데이터 변환
				coslist[j].append(cosBetVec(windvec,matTranspose([axisvec[j]])))
				wind[j].append((coslist[j][row]**2)*windgiven)
				windoriginspd+=(wind[j][row])
			
			windoriginvec=matxM(convMat2(axis[0][row],axis[1][row],axis[2][row]),[[wind[0][row]],[wind[1][row]],[wind[2][row]]])
			windspdlist.append(windoriginspd)
			
			# print ""
			# print "flex : ",flex
			# print "wind : ",wind
			# print "axis : ",axis
			# print "coslist : ",coslist
			# print "axisvec : ",axisvec
			# print ""
			# print "original wind speed : ",windoriginspd,"m/s"
			# print "original wind vector : ",matxC(1.0/(size(windoriginvec)),windoriginvec)
			# print "wind vector given : ",windvec
			# print ""
			# print "풍속 오차율 : ",round((windgiven-windoriginspd)/windgiven,5)*100,"%"
			# print "풍향 오차 : ",math.degrees(math.acos(cosBetVec(windvec,windoriginvec))),"deg"
			row+=1
		
aaa=copy.deepcopy(axis)
			
# 계수 리스트

apcs=[[],[],[]]	#[[b,a,c,b,a],[b,a,c,b,a]..]
for axis in range(0,3):
	for deg in range(1,3):
		apcs[axis].append(functionApprox(flex[axis],wind[axis],deg))
		
# 축 범위
maxx=[]
maxy=[]
for axis in range(0,3):
	maxx.append(int(max(flex[axis]))+1)
	maxy.append(int(max(wind[axis]))+1)
maxx=max(maxx)
maxy=max(maxy)

		
# 근사 함수
xlist=[[],[],[]]	
ylist_linar=[[],[],[]]
ylist_quadra=[[],[],[]]
	
for axis in range(0,3):
	xlist[axis]=range(0,maxx)
	ylist_linar[axis]=[apcs[axis][0][0]+apcs[axis][0][1]*v for v in xlist[axis]]
	ylist_quadra[axis]=[apcs[axis][1][0]+apcs[axis][1][1]*vv+apcs[axis][1][2]*(vv**2) for vv in xlist[axis]]
	



	
# 그리기 : MPH - m/s
plt.figure()	

plt.subplot(331)
plt.axis([0,maxx,0,maxy])
plt.plot(flex[0],wind[0],'o')
plt.plot(xlist[0],ylist_linar[0],label='linar approx',linewidth=0.5)
plt.plot(xlist[0],ylist_quadra[0],label='quadratic approx',linewidth=0.5)
plt.xlabel('MPH')
plt.ylabel('m/s')
plt.title('x axis')
plt.legend()

plt.subplot(332)
plt.axis([0,maxx,0,maxy])
plt.plot(flex[1],wind[1],'o')
plt.plot(xlist[1],ylist_linar[1],label='linar approx',linewidth=0.5)
plt.plot(xlist[1],ylist_quadra[1],label='quadratic approx',linewidth=0.5)
plt.xlabel('MPH')
plt.ylabel('m/s')
plt.title('y axis')
plt.legend()

plt.subplot(333)
plt.axis([0,maxx,0,maxy])
plt.plot(flex[2],wind[2],'o')
plt.plot(xlist[2],ylist_linar[2],label='linar approx',linewidth=0.5)
plt.plot(xlist[2],ylist_quadra[2],label='quadratic approx',linewidth=0.5)
plt.xlabel('MPH')
plt.ylabel('m/s')
plt.title('z axis')
plt.legend()


tries=[]
n=1
while n <= len(wind[0]) :
	tries.append(n)
	n+=1

	
plt.subplot(312)
plt.axis([0,len(tries),0,max(windspdlist)+0.5])
plt.plot(tries,windspdlist)
plt.xlabel('th try')
plt.ylabel('calculated wind speed')
plt.grid()

plt.subplot(313)
plt.axis([0,len(tries),-180,180])
plt.plot(tries,aaa[0],label='roll')
plt.plot(tries,aaa[1],label='pitch')
plt.plot(tries,aaa[2],label='yaw')
plt.xlabel('th try')
plt.ylabel('degree')
plt.title('Axes Data')
plt.legend()

plt.show()


