
semantic_cube= {
	('int', '+', 'int') : 'int',
	('int', '-', 'int') : 'int',
	('int', '*', 'int') : 'int',
	('int', '/', 'int') : 'float',
	('int', '=', 'int') : 'int',
	('int', '>', 'int') : 'bool',
	('int', '<', 'int') : 'bool',
	('int', '>=', 'int') : 'bool',
	('int', '<=', 'int') : 'bool',
	('int', '==', 'int') : 'bool',
	('int', '<>', 'int') : 'bool',

	('float', '+', 'float') : 'float',
	('float', '-', 'float') : 'float',
	('float', '*', 'float') : 'float',
	('float', '/', 'float') : 'float',
	('float', '=', 'float') : 'float',
	('float', '>', 'float') : 'bool',
	('float', '<', 'float') : 'bool',
	('float', '>=', 'float') : 'bool',
	('float', '<=', 'float') : 'bool',
	('float', '==', 'float') : 'bool',
	('float', '<>', 'float') : 'bool',

	('string', '==', 'string') : 'bool',
	('string', '<>', 'string') : 'bool',
	('string', '=', 'string') : 'string',

	('int', '+', 'float') : 'float',
	('int', '-', 'float') : 'float',
	('int', '*', 'float') : 'float',
	('int', '/', 'float') : 'float',
	('int', '>', 'float') : 'bool',
	('int', '<', 'float') : 'bool',
	('int', '>=', 'float') : 'bool',
	('int', '<=', 'float') : 'bool',
	('int', '==', 'float') : 'bool',
	('int', '<>', 'float') : 'bool',

	('bool', '&&', 'bool') : 'bool',
	('bool', '||', 'bool') : 'bool',
	('bool', '<', 'bool') : 'bool',
	('bool', '>', 'bool') : 'bool',
	('bool', '<=', 'bool') : 'bool',
	('bool', '>=', 'bool') : 'bool',
	('bool', '==', 'bool') : 'bool',
	('bool', '<>', 'bool') : 'bool',
}