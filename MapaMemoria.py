class MapaMemoria:
	def __init__(self, inicio_int, inicio_float, inicio_string, inicio_bool,limite):
		"""MapaMemoria define un bloque de memoria para los scopes de variables:
				1) Globales
				2) Locales
				3) Temporales
				4) Constantes
			Los atributos que recibe son:
				inicio_int: que es la direccion de inicio para las variables enteras
				inicio_float: que es la direccion de inicio de las variables flotantes
				inicio_string: que es la direccion de inicio de las variables string
				limite: que es la direccion final del bloque de memoria
			Las propiedades que tiene son:
				int: que es una lista de dos elementos [direccion de inicio, cantidad actual]
				float: que es una lista de dos elementos [direccion de inicio, cantidad actual]
				string: que es una lista de dos elementos [direccion de inicio, cantidad actual]
				limite: que es la ultima direccion de memoria del bloque actual
		"""
		self.int = [ inicio_int, 0 ]
		self.float = [ inicio_float, 0 ]
		self.string = [ inicio_string, 0 ]
		self.bool= [inicio_bool,0]
		self.limite = limite

	def add_int(self, cont=1):
		''' comment '''
		if ( self.int[0] + self.int[1] + cont ) < self.float[0]:
			self.int[1] += cont
			return ( self.int[0] + self.int[1] - cont )
		else:
			print 'STACKOVERFLOW: stack pointer exceeded the stack bound.'

	def add_float(self, cont=1):
		''' comment '''
		if ( self.float[0] + self.float[1] + cont ) < self.string[0]:
			self.float[1] += cont
			return ( self.float[0] + self.float[1] - cont )
		else:
			print 'STACKOVERFLOW: stack pointer exceeded the stack bound.'

	def add_string(self, cont=1):
		''' comment '''
		if ( self.string[0] + self.string[1] + cont ) < self.bool[0]:
			self.string[1] += cont
			return ( self.string[0] + self.string[1] - cont )
		else:
			print 'STACKOVERFLOW: Stack pointer exceeded the stack bound.'

	def add_bool(self, cont=1):
		''' comment '''
		if ( self.bool[0] + self.bool[1] + cont ) < self.limite:
			self.bool[1] += cont
			return ( self.bool[0] + self.bool[1] - cont )
		else:
			print 'STACKOVERFLOW: Stack pointer exceeded the stack bound.'

	def add_type(self,tipo,cant):
		''' comment '''
		if tipo== 'string':
		   return self.add_string(1)
		elif tipo=='int':
		   return self.add_int(1)
		elif tipo=='float':
		   return self.add_float(1)
		elif tipo=='bool':
			return self.add_bool(1)
		elif tipo=='arrfloat':
		   return self.add_float(int(cant))
		elif tipo=='arrint':
		   return self.add_int(int(cant))

