
import json
import pprint
from SapphireSemantics import errors
from copy import deepcopy
import sys
import OpenGL
from math import *
from OpenGL.GL import *     
from OpenGL.GLU import *    
from OpenGL.GLUT import *
pp = pprint.PrettyPrinter()
global_dic={}
local_dic={}
local_dic_aux={}
temp_dic={}
const_dic={}
arr_dic={} #dictionary para saber el limite del arreglo
stack=[] #Stack para guardar las memorias 
params=[] #parametros de cada funcion
linewidth=10 #variable para draw_line
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
	stack.append([count,deepcopy(local_dic),deepcopy(temp_dic)])
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
	global temp_dic
	global count
	fun=stack.pop()
	count=fun[0]
	local_dic=fun[1]
	temp_dic=fun[2]

def draw_line(q1,q2,q3):
	var1=get(q1[0])
	var2=get(q1[1])
	var3=get(q1[2])
	var4=get(q1[3])
	print 'asas'
	print linewidth
	glLineWidth(200);
	glBegin(GL_LINES); 
	glVertex2f(float(var1), float(var2));
	glVertex2f(float(var3), float(var4));
	glEnd();
def rect(q1,q2,q3):
	var1=float(get(q1[0]))
	var2=float(get(q1[1]))
	var3=float(get(q1[2]))
	var4=float(get(q1[3]))
	glBegin(GL_QUADS)                                  # start drawing a rectangle
	glVertex2f(var1, var2)                                   # bottom left point
	glVertex2f(var1, var3)                           # bottom right point
	glVertex2f(var3, var4)                  # top right point
	glVertex2f(var3, var2)                          # top left point
	glEnd()
def teapot(q1,q2,q3):
	var1=float(get(q1[0]))
	var2=float(get(q1[1]))
	var3=float(get(q1[2]))
	var4=float(get(q1[3]))
	glPushMatrix()
	glTranslated(var1, var2, var3)
	glRotated(rota, 0.0, 1.0, 0.0)
	glColor3f(var1, var2, var3)
	glutWireTeapot(var4)
	glPopMatrix()
	glutSwapBuffers()

def triangle(q1,q2,q3):
	var1=float(get(q1[0]))
	var2=float(get(q1[1]))
	var3=float(get(q1[2]))
	var4=float(get(q1[3]))
	glBegin(GL_TRIANGLES)                                  # start drawing a rectangle
	glVertex2f(var1, var2)                           # bottom right point
	glVertex2f(var1+var3, var2)                  # top right point
	glVertex2f(var1+(var3/2), var2+var4)                          # top left point
	glEnd()
def cube(q1,q2,q3):
	var1=float(get(q1[0]))
	var2=float(get(q1[1]))
	var3=float(get(q1[2]))
	var4=float(get(q1[3]))
	glPushMatrix()
	glTranslated(var1, var2, var3)
	glRotated(0, 0.0, 1.0, 0.0)
	glColor3f(var1, var2, var3)
	glutWireCube (var4);
	glPopMatrix()
	glutSwapBuffers()

def color(q1,q2,q3):
	var1=float(get(q1[0]))
	var2=float(get(q1[1]))
	var3=float(get(q1[2]))
	glColor3f(var1, var2, var3)

def circle(q1,q2,q3):
	var1=float(get(q1[0]))
	var2=float(get(q1[1]))
	var3=float(get(q1[2]))
	posx, posy = var1,var2    
	sides = 32    
	radius = var3    
	glBegin(GL_POLYGON)    
	for i in range(100):    
	    cosine= radius * cos(i*2*pi/sides) + posx    
	    sine  = radius * sin(i*2*pi/sides) + posy    
	    glVertex2f(cosine,sine)
	glEnd()


def arc(q1,q2,q3):
	var1=float(get(q1[0]))
	var2=float(get(q1[1]))
	var3=float(get(q1[2]))
	var4=float(get(q1[3]))
	PI = 3.14
	step=5.0;
	glBegin(GL_LINE_STRIP)
	angle=var3
	while angle<=var4:
		rad  = PI*angle/180
		x  = var1+100*cos(rad)
		y  = var2+100*sin(rad)
		glVertex(x,y,0.0)
		angle+=step
	glEnd()
def widthLine(q1,q2,q3):
	var1=float(get(q1))
	print var1
	global linewidth
	linewidth=var1


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
	'line': draw_line,
	'rect': rect,
	'teapot': teapot,
	'triangle': triangle,
	'cube': cube,
	'color': color,
	'arc': arc,
	'circle': circle,
	'width': widthLine,
	'print': prints,}
window = 0                                             # glut window number
width, height = 500, 400   
def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 500.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 400)
glutInitWindowPosition(100, 100)
glutCreateWindow("Python OGL Program")
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
glLoadIdentity()                                   # reset position
refresh2d(width, height)                           # set mode to 2d
glColor3f(1.0, 1.0, 1.0)
with open('obj.json') as df:
	data=json.load(df)
const_dic=data['constants']
const_dic = {v: k for k, v in const_dic.items()}
q= data['quadruples']
fill_local_dic('main')
count = 0
while count<len(q):
	quad= q[count]
	#print count
	#print quad
	methods[quad[0]](quad[1],quad[2],quad[3]) 
	count= count +1

print 'Fin de la ejecucion, favor de cerrar la ventana grafica para continuar.'

def draw():                           # set color to white
	glutSwapBuffers() 
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutMainLoop()



draw()
pp.pprint(local_dic)
pp.pprint(temp_dic)
exit(-1)