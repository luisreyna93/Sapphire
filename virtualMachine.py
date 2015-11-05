
import json
import pprint

pp = pprint.PrettyPrinter()
global_dic={}
local_dic={}
temp_dic={}
const_dic={}
stack=[]

def get(q1):
	if q1/4000 < 1:
		return local_dic[q1][0]
	elif q1/8000 < 1:
		return global_dic[q1][0]
	elif q1/12000 < 1:
		return const_dic[q1][0]
	else:
		return temp_dic[q1][0]
def suma(q1,q2,q3):
	temp_dic[q3]=[float(get(q1))+float(get(q2))]

def resta(q1,q2,q3):
	temp_dic[q3]=[float(get(q1))-float(get(q2))]

def mult(q1,q2,q3):
	temp_dic[q3]=[float(get(q1))*float(get(q2))]

def div(q1,q2,q3):
	temp_dic[q3]=[float(get(q1))/float(get(q2))]

def asig(q1,q2,q3):
	if q3/4000 < 1:
		local_dic[q3]=get(q1)
	elif q3/8000 < 1:
		global_dic[q3]=get(q1)
	elif q3/12000 < 1:
		const_dic[q3]=get(q1)
	else:
		temp_dic[q3]=get(q1)

def prints(q1,q2,q3):
	print get(q3)

def goto(q1,q2,q3):
	count=float(q3)

def gotof(q1,q2,q3):
	if q1: count=q3

methods = {
	'+': suma,
	'-': resta,
	'/': div,
	'*': mult,
	'=': asig,
	'<': suma,
	'>': resta,
	'<>': suma,
	'<=': resta,
	'>=': suma,
	'==': resta,
	'era': resta,
	'param': suma,
	'gosub': resta,
	'gotof': gotof,
	'goto': goto,
	'line': suma,
	'rect': resta,
	'teapot': suma,
	'triangle': resta,
	'cube': suma,
	'color': resta,
	'arc': suma,
	'circle': resta,
	'width': suma,
	'print': prints,}

with open('obj.json') as df:
	data=json.load(df)
const_dic=data['constants']
const_dic = {v: k for k, v in const_dic.items()}
q= data['quadruples']
#q=[['*',11000,11001,1],['/',11000,11000,2]]
count = 0
while count<len(q):
	quad= q[count]
	print quad
	methods[quad[0]](quad[1],quad[2],quad[3]) 
	count= count +1



pp.pprint(local_dic)
pp.pprint(temp_dic)
exit(-1)