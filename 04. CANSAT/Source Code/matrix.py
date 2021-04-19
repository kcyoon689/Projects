# -*- coding:utf-8 -*-
import copy
import math

# 기본 수학량들
ex=[[1,0,0]]
ey=[[0,1,0]]
ez=[[0,0,1]]
	
#행렬 연산
def	matMakeO(column,row):
	matrix=[[0]*row for i in range(column)]
	return matrix

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
	conv2=matxM(matxM(convAxis(pitch,"x"),convAxis(roll,"y")),convAxis(yaw,"z"))
	return conv2

#풍속데이터
# def windOriginal(force,convmat):
	# wind1=matxM(force
length=7
result=[]
data_axis=[[0,0,0]]
data_force=[[0],[0],[0]]

while True:
	data_windraw=raw_input().split()
	length=len(data_windraw)
	if length==0:
		break
	else:
		for i in range(1,4):
			data_axis[0][i-1]=float(data_windraw[i])
		for j in range(4,7):
			data_force[j-4][0]=float(data_windraw[j])
	result.append(matxM(convMat(data_axis[0][0],data_axis[0][1],data_axis[0][2]),data_force))

for i in range(0,len(result)):
	print result[i]