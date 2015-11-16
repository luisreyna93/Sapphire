
import json
import pprint

pp = pprint.PrettyPrinter()
global_dic={}
local_dic={}
temp_dic={}
const_dic={}
arr_dic={} #dictionary para saber el limite del arreglo
stack=[]
def get(q1):
	try:
		if q1/4000 < 1:
			return local_dic[q1][0]
		elif q1/8000 < 1:
			return global_dic[q1][0]
		elif q1/12000 < 1:
			return const_dic[q1][0]
		else:
			return temp_dic[q1][0]
	except:
		print "Variable sin valor"
		exit(-1)
def suma(q1,q2,q3):
	global temp_dic
	temp_dic[q3]=[float(get(q1))+float(get(q2))]
	print temp_dic

def resta(q1,q2,q3):
	global temp_dic
	temp_dic[q3]=[float(get(q1))-float(get(q2))]

def mult(q1,q2,q3):
	global temp_dic
	temp_dic[q3]=[float(get(q1))*float(get(q2))]
	print temp_dic

def div(q1,q2,q3):
	global temp_dic
	temp_dic[q3]=[float(get(q1))/float(get(q2))]

def asig(q1,q2,q3):
	#todo: agregar funcionalidad para arreglo
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
	print get(q3)

def goto(q1,q2,q3):
	global count
	count=int(q3)-1

def gotof(q1,q2,q3):
	global count
	if q1: count=q3


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
	global temp_dic
	if float(get(q1))>float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	print temp_dic

def less(q1,q2,q3):
	global temp_dic
	if float(get(q1))<float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	print temp_dic
	
def diff(q1,q2,q3):
	global temp_dic
	if float(get(q1))!=float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	print temp_dic
def lessEqual(q1,q2,q3):
	global temp_dic
	if float(get(q1))<=float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	print temp_dic
def greaterEqual(q1,q2,q3):
	global temp_dic
	if float(get(q1))>=float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	print temp_dic

def equal(q1,q2,q3):
	global temp_dic
	if float(get(q1))==float(get(q2)):
		temp_dic[q3]=True
	else: 
		temp_dic[q3]=False
	print temp_dic
def era(q1,q2,q3):
	#todo: guardar los datos de la funcion actual y cargar la nueva

def ver(q1,q2,q3):
	if not (get(q1)>=q2 and get(q1)<=q3):
		print errors['ARR_OVERFLOW'] #todo: agregar errores de arr overflow
		exit(-1)
def param(q1,q2,q3):
	#todo: agregar parametros al stack 

def gosub(q1,q2,q3):
	#todo: poner los parametor del stack de params para definir en el nuevo memoria
	count=q1

def 
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



pp.pprint(local_dic)
pp.pprint(temp_dic)
exit(-1)