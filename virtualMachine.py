
import json
import pprint
from SapphireSemantics import errors
from copy import deepcopy
pp = pprint.PrettyPrinter()
global_dic={}
local_dic={}
local_dic_aux={}
temp_dic={}
const_dic={}
arr_dic={} #dictionary para saber el limite del arreglo
stack=[] #Stack para guardar las memorias 
params=[] #parametros de cada funcion
def get(q1):
	try:
		if isinstance(q1, list):
			q1= get(q1[0])
		if q1 in global_dic:
			return global_dic[q1]

		if q1/4000.0 < 1:
			return local_dic[q1]
		elif q1/8000.0 < 1:
			return global_dic[q1]
		elif q1/12000.0 < 1:
			return const_dic[q1]
		elif q1/16000.0 <1:
			return temp_dic[q1]
		else:
			return global_dic[q1]
	except:
		print "Variable sin valor"
		pp.pprint(local_dic)
		pp.pprint(temp_dic)
		pp.pprint(const_dic)
		pp.pprint(global_dic)
		exit(-1)
def suma(q1,q2,q3):
	try:
		global temp_dic
		temp_dic[q3]=float(get(q1))+float(get(q2))
	except:
		pp.pprint(local_dic)
		pp.pprint(temp_dic)
		pp.pprint(const_dic)
		pp.pprint(global_dic)
		exit(-1)

	#print temp_dic

def resta(q1,q2,q3):
	global temp_dic
	temp_dic[q3]=float(get(q1))-float(get(q2))

def mult(q1,q2,q3):
	global temp_dic
	temp_dic[q3]=float(get(q1))*float(get(q2))
	#print temp_dic

def div(q1,q2,q3):
	global temp_dic
	temp_dic[q3]=float(get(q1))/float(get(q2))

def asig(q1,q2,q3):
	#todo: agregar funcionalidad para arreglo
	if isinstance(q3, list):
		q3= get(q3[0])
	if q3/4000 < 1:
		global local_dic
		local_dic[q3]=get(q1)
	elif q3/8000 < 1:
		global global_dic
		global_dic[q3]=get(q1)
	elif q3/12000 < 1:
		global const_dic
		const_dic[q3]=get(q1)
	else:
		global temp_dic
		temp_dic[q3]=get(q1)

def prints(q1,q2,q3):
	print 'print---------'
	print get(q3)

def goto(q1,q2,q3):
	global count
	count=int(q3)-1

def gotof(q1,q2,q3):
	global count
	if not temp_dic[q1]:
		count=q3-1


def fill_local_dic(name):
	local_aux= data['funcs'][name]['localVars']
	for key in local_aux:
		value= local_aux[key]
		if 'arr' in value['type']:
			aux=0
			arr_dic[value['memdir']]=value['size']
			while value['size']==aux+1:
				local_dic[value['memdir']+aux]= None
				aux=aux+1
		else:
			local_dic[value['memdir']]= None
def greater(q1,q2,q3):
	if float(get(q1))>float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	#print temp_dic

def less(q1,q2,q3):
	global temp_dic
	if float(get(q1))<float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	#print temp_dic
	
def diff(q1,q2,q3):
	global temp_dic
	if float(get(q1))!=float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	#print temp_dic
def lessEqual(q1,q2,q3):
	global temp_dic
	if float(get(q1))<=float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	#print temp_dic
def greaterEqual(q1,q2,q3):
	global temp_dic
	if float(get(q1))>=float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	#print temp_dic

def equal(q1,q2,q3):
	global temp_dic
	if float(get(q1))==float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	#print temp_dic
def era(q1,q2,q3):
	global stack
	global local_dic
	stack.append([count,deepcopy(local_dic)])
	#local_dic={}
	#fill_local_dic(q2)
	global params
	params=data['funcs'][q2]

def ver(q1,q2,q3):
	if not (int(get(q1))>=q2 and int(get(q1))<=q3):
		print errors['ARR_OVERFLOW'] 
		exit(-1)
	global q
	global count
	count= count +1
	quad= q[count]
	global temp_dic
	temp_dic[quad[3]]=int(get(quad[1]))+int(quad[2])

def param(q1,q2,q3):
	global local_dic_aux
	x=list(reversed(params['params']))[q3-1]
	local_dic_aux[params['localVars'][x[0]]['memdir']]=get(q1)

	
def gosub(q1,q2,q3):
	global count
	last=stack.pop()
	last[0]=count
	stack.append(last)
	count=q1-1
	global local_dic
	global local_dic_aux
	local_dic=local_dic_aux
	
def ret(q1,q2,q3):
	global global_dic
	global_dic[q1]=get(q3)

def retorno(q1,q2,q3):
	global local_dic
	global count
	fun=stack.pop()
	count=fun[0]
	local_dic=fun[1]
	
methods = {
	'+': suma,
	'-': resta,
	'/': div,
	'*': mult,
	'=': asig,
	'<': less,
	'>': greater,
	'<>': diff,
	'<=': lessEqual,
	'>=': greaterEqual,
	'==': equal,
	'era': era,
	'ver': ver,
	'param': param,
	'return': ret,
	'retorno' :retorno,
	'gosub': gosub, #todo: implementar cambiar local_dict 
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
fill_local_dic('main')
count = 0
while count<len(q):
	quad= q[count]
	print count
	print quad
	methods[quad[0]](quad[1],quad[2],quad[3]) 
	count= count +1

print 'TERMINOOOOOOOOO------'

pp.pprint(local_dic)
pp.pprint(temp_dic)
exit(-1)