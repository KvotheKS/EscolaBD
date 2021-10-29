from mysql.connector import *
import re
import datetime

database = connect(host='localhost', user='root', password='Arthur123', database='escola')
dbcur = database.cursor(buffered=True)

def SELECTALL(table):
	table = curateTable(table)
	return f'SELECT * FROM {table}'

def SELECT(table, columns, cond):
	table = curateTable(table)
	strcol = ''
	for i in columns:
		strcol += i + ','
	strcol = strcol[:-1]
	return f'SELECT {strcol} FROM {table} WHERE {cond}'

def SELECTALLW(table, cond):
	table = curateTable(table)
	if(len(cond) > 0):
		return f'SELECT * FROM {table} WHERE {cond}'
	return f'SELECT * FROM {table}'

def SELECTCOL(table, columns):
	table = curateTable(table)
	strcol = ''
	for i in columns:
		strcol += i + ','
	strcol = strcol[:-1]
	return f'SELECT {strcol} FROM {table}'

def INSERT(table, columns, values):
	table = curateTable(table)
	strcol, strval = '',''
	vals = []
	for i in columns:
		strcol += str(i) + ','
	strcol = strcol[:-1]
	for i in range(len(values)):
		sdw = sandwich(values[i], getColumnType(table,columns[i]))
		if('blob' in getColumnType(table,columns[i]) and 'LOAD_FILE' not in sdw):
			vals.append()
			strval += '%s,'
		else:
			strval += sdw + ','
	strval = strval[:-1]
	dbcur.execute(f'INSERT INTO {table} ({strcol}) VALUES({strval})', tuple(vals))
	database.commit()

def UPDATE(table, columns, values, pkval):
	table = curateTable(table)
	strcvs = ''
	vals = []
	pkval = sandwich(pkval, getColumnType(table,getTablePK(table)))
	for i in range(len(columns)):
		sdw = sandwich(values[i], getColumnType(table,columns[i]))
		if('blob' in getColumnType(table,columns[i]) and 'LOAD_FILE' not in sdw):
			vals.append(sdw)
			strcvs += columns[i] + ' = %s,'
		else:
			strcvs += columns[i] + f' = {sdw},'
	print(f'UPDATE {table} SET {strcvs[:-1]} WHERE {getTablePK(table)} = {pkval}', tuple(vals))
	dbcur.execute(f'UPDATE {table} SET {strcvs[:-1]} WHERE {getTablePK(table)} = {pkval}', tuple(vals))
	database.commit()

def sandwich(name, typ):
	if(name == ''):
		return "NULL"
	elif('blob' in typ):
		if(type(name) == bytes):
			return f'{name}'
		return f'LOAD_FILE("{name}")'
	elif('char' in typ or 'date' in typ or 'float' in typ):
		return f'"{name}"'
	elif('time' in typ):
		return f'"{name}' + ':00"'
	else:
		return f'{name}'

def getRegistries(table, column='', value=''):
	if(column != ''):
		dbcur.execute(SELECTALLW(table, f'{column} = {sandwich(value,getColumnType(table,column))}'))
	else:
		dbcur.execute(SELECTALLW(table, ''))
	return dbcur.fetchall()

def getRegistry(table, column='', value=''):
	table = table.replace(table[0], table[0].upper())
	if(column != ''):
		dbcur.execute(SELECTALLW(table, f'{column} = {sandwich(value,getColumnType(table,column))}'))
	else:
		dbcur.execute(SELECTALLW(table, ''))
	return dbcur.fetchone()

def getColumns(table):
	table = curateTable(table)
	dbcur.execute(f'SHOW COLUMNS FROM {table}')
	ls = []
	for i in dbcur.fetchall():
		ls.append(i[0])
	return ls

def getTables():
	tbls = []
	dbcur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema = "Escola"')
	for i in dbcur.fetchall():
		tbls.append(i)
	return tbls

def getTableLike(PK, FK):
	dbcur.execute(f'SELECT table_name FROM information_schema.tables WHERE table_schema = "Escola"')
	ls= dbcur.fetchall()
	pkbool, fkbool = False, False
	for i in ls: # roda em todas as tabelas
		dbcur.execute(f'SHOW FIELDS FROM {i[0]}')
		ls2 = dbcur.fetchall()
		pkbool, fkbool = False, False
		for j in ls2:
			if(PK == j[0]):
				pkbool=True
			if(FK == j[0]):
				fkbool=True
		if(pkbool and fkbool):
			return i[0]

def getTablebyFK(FK):
	dbcur.execute(f'SELECT table_name FROM information_schema.tables WHERE table_schema = "Escola"')
	ls= dbcur.fetchall()
	for i in ls: # roda em todas as tabelas
		dbcur.execute(f'SHOW FIELDS FROM {i[0]}')
		ls2 = dbcur.fetchall()
		for j in ls2: # roda em todas as colunas 
			name = i[0]
			name=name.replace(name[0],name[0].upper(),1)
			if(name + j[0] == FK):
				return name


def getTypes(table):
	table = curateTable(table)
	dbcur.execute(f'SHOW FIELDS FROM {table}')
	ls = []
	for i in dbcur.fetchall():
		ls.append(i[1].decode('ascii'))
	return ls

def getTableInfo(table):
	table = curateTable(table)
	dbcur.execute(f'SHOW FIELDS FROM {table}')
	ls = []
	for i in dbcur.fetchall():
		ls.append([i[0],i[1].decode('ascii'),i[3]]) # nome, tipo, chave
	return ls

def getColumnInfo(table, column):
	table = curateTable(table)
	dbcur.execute(f'SHOW FIELDS FROM {table} WHERE Field = "{column}"')
	temp = dbcur.fetchone()
	if(temp != None):
		return [temp[0],temp[1].decode('ascii'),temp[3]]

def getColumnType(table,column):
	table = curateTable(table)
	dbcur.execute(f'SHOW FIELDS FROM {table} WHERE Field = "{column}"')
	print(table, column)
	return dbcur.fetchone()[1].decode('ascii')

def getTypeColumn(table, typ):
	table = curateTable(table)
	dbcur.execute(f'SHOW FIELDS FROM {table} WHERE Type like "%{typ}"')
	temp = dbcur.fetchone()
	if(temp != None):
		return temp[0]

def getColumnNull(table, column):
	table = curateTable(table)

	dbcur.execute(f'SHOW FIELDS FROM {table} WHERE Field = "{column}"')
	res = dbcur.fetchone()
	if(res != None):
		return res[2]

def getTablePK(table):
	table = curateTable(table)
	dbcur.execute(f'SHOW FIELDS FROM {table}')
	return dbcur.fetchone()[0]

def validateFK(fk,FK,table):
	table = curateTable(table)
	if(fk == ''):
		bl = getColumnNull(table, FK) #se relacionamento for nm, nao esta no escopo dessa funcao
		if(bl == 'NO'):
			return f'Linha nao selecionada'

def validateNM(FK,fk,table, pkval=''):
	if(FK not in getColumns(table)):
		p = re.search('[A-Z]*[a-z]*[_]*', FK).group()
		if(fk == '' and p in notNullNM(table) and pkval==''):
			return f'Linha nao selecionada'
		if(fk != '' and pkval!=''):
			pk = getTablePK(table)
			fkinfo = getTableInfo(getTablebyFK(FK))[0][1] # so a informacao da FK
			pkinfo = getTableInfo(table)[0][1]
			tbl = getTableLike(table + pk,FK) # procura a tabela nXm
			#print(tbl, FK, fk, fkinfo, table+pk, pkval, pkinfo)
			if(tbl != None):
				dbcur.execute(SELECTALLW(tbl,f'{FK} = {sandwich(fk,fkinfo)} and {table+pk} = {sandwich(pkval,pkinfo)}')) # registro na tabela nxm PT.getRegistry(tbl, table + pk, pkval))
				mreg = dbcur.fetchone()
				if(mreg != None):
					return f'Elemento ja selecionado para este registro.'	
				
		

def typetoname(typ):
	dct = {
		'varchar': 'nome',
		'int': 'inteiro',
		'float': 'número racional',
		'date': 'DD/MM/YYYY',
		'time': 'hh:mm'
	}
	return dct[typ]

def validatePK(table, name):
	table = curateTable(table)
	if(len(name)==0):
		return f'Identificador vazio'
	pk = getTablePK(table)
	typ = getColumnType(table,pk)
	exists = dbcur.execute(SELECTALLW(table, f'{pk} = {sandwich(name,typ)}'))
	if(exists != None):
		return f'Elemento com mesmo identificador ja existe'

def validateVarchar(name):
	rg = re.compile('[^\W\d]+[_]*')
	ls = rg.findall(name)

	restr=''
	for i in ls:
		restr += i + ' '
	restr = restr[:-1]
	if(len(ls)==0 or len(restr) != len(name)):
		raise ValueError

def validateDate(data):
	res = re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', data)
	if(res == None):
		raise ValueError

	ls = list(map(lambda x:int(x),data.split('/')))
	if(ls[0] > 31 or ls[1] > 12 or ls[0] == 0 or ls[1] == 0):
		raise ValueError

	td = datetime.date.today()
	datat = datetime.date(ls[2],ls[1],ls[0])
	delta = td-datat
	if(datat > td or delta.days > 36500):
		raise ValueError

def validateTime(time):

	res = re.search('[0-9]{2}:[0-9]{2}', time)
	if(res == None):
		raise ValueError
	ls = list(map(lambda x:int(x),time.split(':')))
	
	if(ls[0] + ls[1]/60 < 6.0):
		raise ValueError


def validateTypes(name, typ, column):
	dct = {
		'varchar': validateVarchar,
		'int':int,
		'float':float,
		'date': validateDate,
		'time': validateTime,
		'blob':lambda :None,
		'char':lambda :None
	}
	errs = []
	try:
		dct[typ.split('(')[0]](name)
	except:
		errs.append(f'Tipo "{typetoname(typ.split("(")[0])}" esperado')
	finally:
		temp = validateSize(name,typ)
		if(temp != None):
			errs.append(temp)
		if('CPF' in column):
			try:
				int(name)
			except:
				errs.append('11 digitos esperados')
			finally:
				if(len(name)!=11):
					errs.append('11 digitos esperados')
		return errs

def validateSize(name, typ):
	if('(' in typ):
		tam = int(typ.split('(')[1].replace(')',''))
		if(len(name) > tam):
			name=name[:tam]
			return f'Tamanho do dado grande demais, diminuido para caber'

def selectColumnPair(table):
	table = curateTable(table)
	columns = [getTablePK(table), interfaceBD(table)]
	if(columns[1]==''):
		columns = columns[:-1]
	dbcur.execute(SELECTCOL(table,columns))
	return dbcur.fetchall()

def selectColumnsInRow(table, reg):
	table = curateTable(table)
	columns = [getTablePK(table), interfaceBD(table)]
	values = []
	tblinfo = getTableInfo(table)
	if(columns[1] == ''):
		columns = columns[:-1]
	for i in range(len(columns)):
		for z in range(len(tblinfo)):
			print(columns[i],tblinfo[z][0])
			if(columns[i]==tblinfo[z][0]):
				values.append(reg[z])
	return values

def curateTable(table):
	if(table == 'Local'):
		return 'Local_'
	elif(table == 'Atividade'):
		return 'AtividadeExtracurricular'
	return table

def interfaceBD(table): #Serve para saber qual eh o atributo a ser visto na hora do read.
	table = curateTable(table)
	dct = {
		'Local':'Categoria',
		'Local_':'Categoria',
		'Departamento': 'Nome',
		'Disciplina': 'Nome',
		'Responsavel': 'Nome',
		'Telefone': 'ResponsavelCPF',
		'Professor': 'Nome',
		'AtividadeExtracurricular': 'Descricao',
		'Turma':'Turno',
		'Estudante': 'Nome',
		'Dependente': '',
		'Itens': '',
		'Despesas': 'Descricao',
		'HistoricoDespesas': '',
		'ProfessorTurma':'',
		'ResponsavelEstudante': '',
		'Notas': ''
	}
	return dct[table]

def pluraltosingular(tables):
	dct = {
		'Professores': 'Professor',
		'Locais': 'Local_',
		'Turmas': 'Turma',
		'Disciplinas': 'Disciplina',
		'Departamentos': 'Departamento',
		'Responsaveis': 'Responsavel',
		'Atividades': 'AtividadeExtracurricular',
		'Estudantes': 'Estudante'
	}
	return dct[tables]

def singulartoplural(table):
	dct = {
		'Professor': 'Professores',
		'Local_': 'Locais',
		'Local': 'Locais',
		'Turma': 'Turmas',
		'Disciplina': 'Disciplinas',
		'Departamento': 'Departamentos',
		'Responsavel': 'Responsaveis',
		'Atividade': 'Atividades'
	}
	return dct[table]

def insertNM(table,pk,FK, fk): # tabela, valor pk, fk, fk val
	table = curateTable(table)
	if(not isNM(table, FK) or fk == ''):
		#print(table, getTablePK(table), FK)
		return

	fk = fk.split('(')[-1].replace(')','') # faz uma limpa, caso o formato da fk seja: blabla (fk)
	tbl = getTableLike(table + getTablePK(table), FK)
	print(tbl, table, pk, FK , fk)
	columns = []
	values = []

	for i in getColumns(tbl):
		if(i == FK):
			columns.append(FK)
			values.append(fk)
		else:
			columns.append(table + getTablePK(table))
			values.append(pk)
	print(tbl,columns, values)
	INSERT(tbl,columns,values)

def isNM(table, fk):
	table = curateTable(table)
	return fk not in getColumns(table)

def notNullNM(table):
	table = curateTable(table)
	dct = {
		'Estudante':['Responsavel'],
		'Professor':['Disciplina'],
		'AtividadeExtracurricular':['Professor']
	}
	return dct[table]

def fkToTable(fk):
	return re.search('[A-Z]+[a-z]+[_]*',fk).group() 

def parseValue(table,column, value):
	typ = getColumnType(table,column)
	if('date' in typ):
		ls = value.split('/')
		return ls[2] + '-' + ls[1] + '-' + ls[0]
	return value

def limpar(table, pkval):
	table = curateTable(table)
	PK = getTablePK(table)
	dbcur.execute(f'DELETE FROM {table} WHERE {PK} = {sandwich(pkval, getColumnType(table,PK))}')
	database.commit()