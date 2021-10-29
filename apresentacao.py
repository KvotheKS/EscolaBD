from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtGui import QPixmap
import sys
import persistency as PT
import base64
from PIL import Image
import io 

def trim(name):
	name = name.replace(' de ','')
	return unitoascii(name)

def unitoascii(name):
	dct = {
		'á':'a',
		'ã':'a',
		'é':'e',
		'í':'i',
		'ó':'o',
		'ç':'c'
	}
	for i in dct.keys():
		name = name.replace(i,dct[i])
	return name

class Application(QtWidgets.QMainWindow):
	def __init__(self):
		super(Application, self).__init__()
		self.buttons=[]
		self.entries={}
		self.scrolls={}
		self.sexo = None #Workaround um "bug" do qt. Radio buttons sendo destruidos antes do desejado
		self.selectedname=''
		self.selectedtable=''
		self.fotoPath=''
		self.initial()

	def initial(self):
		self.clearWindow()
		uic.loadUi('TelasBD/principal.ui', self)
		escolhas = {'Estudante':self.initEstudante, 
					'Atividade':self.initAtividade, 'Professor':self.initProfessor}
		self.selectedname=''
		self.selectedtable=''
		for i in escolhas.keys():
			self.buttons.append(self.findChild(QtWidgets.QPushButton, 'btt' + i)) # Find the button
			self.buttons[-1].clicked.connect(escolhas[i])
		self.show()

	def initEstudante(self):
		self.initBindows('Estudante')
		
	def initAtividade(self):
		self.initBindows('Atividade', 'AtividadeExtracurricular')

	def initProfessor(self):
		self.initBindows('Professor')

	def initBindows(self, name='', tablename=''):
		self.clearWindow()
		if(self.selectedname==''):
			self.selectedname=name
			self.selectedtable = name if(tablename=='') else tablename
		uic.loadUi('TelasBD/' + self.selectedname + '.ui', self)
		self.resize(self.maximumSize())

		self.stable = self.findChild(QtWidgets.QTableWidget, 'tbl' + self.selectedname)

		buttonTypes = {'Voltar':self.initial,'Inserir':self.Insert, 
					'Atualizar':self.Update, 'Deletar':self.Delete, 
					'Pesquisa':self.Read}
		self.entries[self.selectedname] = self.findChild(QtWidgets.QLineEdit, 'line' + self.selectedname)
		self.scrolls[self.selectedname] = self.findChild(QtWidgets.QComboBox, 'cmb' + self.selectedname)
		self.scrolls[self.selectedname].currentIndexChanged.connect(self.elementSearch)

		if(self.findChild(QtWidgets.QRadioButton, 'rbttFeminino')!=None):
			self.rbttFeminino.toggled.connect(self.SearchSexo)
			self.rbttMasculino.toggled.connect(self.SearchSexo)
			self.rbttFeminino.setEnabled(True)
			self.rbttMasculino.setEnabled(True)
			self.sexo = True
		for i in buttonTypes.keys():
			self.buttons.append(self.findChild(QtWidgets.QPushButton, 'btt' + i))
			self.buttons[-1].clicked.connect(buttonTypes[i])
		self.show()

	def Insert(self):
		self.clearWindow()
		uic.loadUi('TelasBD/cadastro' + self.selectedname + '.ui', self)
		self.resize(self.maximumSize())

		self.buttons = [self.findChild(QtWidgets.QPushButton, 'bttSalvar'),
						self.findChild(QtWidgets.QPushButton, 'bttCancelar')]
		columns = PT.getTableInfo(self.selectedtable)

		self.buttons[0].clicked.connect(self.validateInsert)
		self.buttons[1].clicked.connect(self.initBindows)
		for i in columns:
			self.insWidget(i)
		for i in self.findChildren(QtWidgets.QComboBox)[1:]: # por alguma razao o primeiro elemento eh um combobox que nao existe
			self.insScroll(i)
		self.show()

	def initScroll(self, table, fk):
		for i in PT.selectColumnPair(table):
			if(len(i) == 2):
				self.scrolls[fk].addItem(f'{i[1]}({i[0]})') # nome(pk)
			else:
				self.scrolls[fk].addItem(f'{i[0]}')

	def insScroll(self, scroll):
		name = PT.pluraltosingular(scroll.objectName().replace('cmb', '')) #nome da tabela da fk.
		relation = PT.getTablePK(name) # pk da tabela. todas as fks estao no modelo Tabela_PKTabela ex : Local__Codigo
		fk = name + relation
		self.scrolls[fk] = scroll
		#print(fk)
		self.initScroll(name,fk)

	def insWidget(self, element):
		if('blob' in element[1]):
			self.bttPesquisar.clicked.connect(self.getPhoto) # por alguma razao funciona.
		elif('char(1)' == element[1]):
			self.rbttFeminino.toggled.connect(self.setSexo)
			self.rbttMasculino.toggled.connect(self.setSexo)
			self.sexo = True
		elif('MUL' not in element[2]):
			#print(element[0])
			self.entries[element[0]] = self.findChild(QtWidgets.QLineEdit, 'line' + element[0])

	def setSexo(self):
		rbtt = self.sender()
		if(rbtt.isChecked()):
			#print(self.sexo)
			self.sexo = rbtt.text()

	def validateInsert(self):
		errorsline = {}
		errorscmb = {}
		errorrbtt = None
		errorblob = None
		dct = {}

		for i in self.entries.keys():
	#		print(i)
			temp = PT.validateTypes(self.entries[i].text(), PT.getColumnType(self.selectedtable, i),i)
			if(len(temp)!=0):
				errorsline[i]=temp
		for i in self.scrolls.keys():
			temp = PT.validateFK(self.scrolls[i].currentText(),i,self.selectedtable) # valor <-> tabela no plural
			if(temp != None):
				errorscmb[i]=temp
			else:
				fkval = self.scrolls[i].currentText().split('(')[-1].replace(')','')
				temp = PT.validateNM(i,fkval,self.selectedtable) 
				if(temp != None):
					errorscmb[i]=temp
		pkerr = PT.validatePK(self.selectedtable, self.entries[PT.getTablePK(self.selectedtable)].text())

		if(self.sexo == True):
			errorrbtt = f'Sexo: nenhuma opcao selecionada'

		if('blob' in PT.getTypes(self.selectedtable) and self.fotoPath==''):
			errorblob = "Foto nao selecionada"
		if(len(errorscmb) + len(errorsline) != 0 or
			errorrbtt != None or pkerr != None or errorblob != None):

			msg = QtWidgets.QMessageBox()
			msg.setWindowTitle('Erros')
			msg.setIcon(QtWidgets.QMessageBox.Critical)

			string = ''
			if(pkerr != None):
				string += pkerr + '\n'
			if(errorblob != None):
				string += errorblob + '\n'
			for i in errorsline.keys():
				for j in errorsline[i]:
					string += i + ': ' + j + '\n'	
			for i in errorscmb.keys():
				string += i + ': ' + errorscmb[i] + '\n'	
			if(errorrbtt!=None):
				string += errorrbtt
			msg.setText(string)
			msg.exec_()
		else:
			self.fillDict(dct)
			self.insertdict(dct)
			self.insertNM(dct) # so insere coisas na tabela nXm quando tiver inserido o elemento.
			self.initBindows()

	def fillDict(self,dct):
		for i in self.entries.keys():
			dct[i]= PT.parseValue(self.selectedtable, i ,self.entries[i].text()) #dados extremamente estaveis
		for i in self.scrolls.keys(): # Guardam 
			column = PT.getColumnInfo(self.selectedtable, i)
			if(column != None):
				dct[i]=self.scrolls[i].currentText().split('(')[-1].replace(')','') 
										#dados incertos, podem estar tanto numa tabela nxm, quanto na tabela escolhida

		foto = PT.getTypeColumn(self.selectedtable, 'blob')
	
		if(foto != None):
			dct[foto] = self.fotoPath
		if(self.sexo == 'Feminino'):
			dct['Sexo'] = 'F'
		elif(self.sexo == 'Masculino'):
			dct['Sexo'] = 'M'	

	def insertNM(self,dct):
		
		for i in self.scrolls.keys():
			column = PT.getColumnInfo(self.selectedtable, i)
			if(column == None):
				PT.insertNM(self.selectedtable, 
						dct[PT.getTablePK(self.selectedtable)], i, 
								self.scrolls[i].currentText().split('(')[-1].replace(')','') )
			
	def insertdict(self, dct):
		columns = []
		values = []
		for i in dct.keys():
			columns.append(i)
			values.append(dct[i])
		PT.INSERT(self.selectedtable, columns, values)
		
		
	def Update(self):
		self.clearWindow()
		uic.loadUi('TelasBD/atualizar' + self.selectedname + '.ui', self)
		self.resize(self.maximumSize())

		self.buttons = [self.findChild(QtWidgets.QPushButton, 'bttSalvar'),
						self.findChild(QtWidgets.QPushButton, 'bttCancelar')]
		columns = PT.getTableInfo(self.selectedtable)
		self.buttons[0].clicked.connect(self.validateUpdate)
		self.buttons[1].clicked.connect(self.initBindows)
		for i in columns:
			if(i[0] != PT.getTablePK(self.selectedtable)):
				self.insWidget(i)
		for i in self.findChildren(QtWidgets.QComboBox)[1:]: # por alguma razao o primeiro elemento eh um combobox que nao existe
			if(PT.pluraltosingular(i.objectName().replace('cmb', '')) == self.selectedtable):
				pk = self.insPKScroll(i)
				self.scrolls[pk].currentIndexChanged.connect(self.initInfo)
			else:
				self.insScroll(i)
		self.show()

	def dbToData(self, data, typ):
		if('date' in typ):
			ls = str(data).split('-')
			return f'{ls[2]}/{ls[1]}/{ls[0]}'
		elif('time' in typ):
			ls = str(data).split(':')
			return f'{ls[0]}:{ls[1]}'
		else:
			return str(data)

	def initInfo(self):
		pk = PT.getTablePK(self.selectedtable)
		pkval = self.scrolls[pk].currentText()
		pkval = pkval.split('(')[-1].replace(')','')
		columns = PT.getTableInfo(self.selectedtable)
		registry = PT.getRegistry(self.selectedtable, pk,pkval)

		for i in self.entries.keys(): # todas as lineedits
			for j in range(len(columns)):
				if(columns[j][0] == i and i != pk):
					if(registry[j] == None):
						self.entries[i].setText('')
					else:
						self.entries[i].setText(self.dbToData(registry[j], columns[j][1]))

		for i in self.scrolls.keys(): #todos os relacionamentos 1xn
			if(i != pk):
				for j in range(len(columns)):
					if(columns[j][0] == i and registry[j] != None):
						fkval = registry[j]
						fktable = PT.getTablebyFK(i)
						fkregistry = PT.selectColumnPair(fktable)
						for z in fkregistry:
							if(z[0] == registry[j]):
								if(len(z) == 2):
									idx = self.scrolls[i].findText(f'{z[1]}({z[0]})') # nome(pk)
								else:
									idx = self.scrolls[i].findText(f'{z[0]}')
								self.scrolls[i].setCurrentIndex(idx)

		for i in range(len(columns)): # tipos especiais
			if('blob' in columns[i][1]):
				pixmap = QPixmap()
				pixmap.loadFromData(registry[i])
				self.lblFotoImg.setPixmap(pixmap)
				self.fotoPath=registry[i]
			elif('char(1)' == columns[i][1]):
				if(registry[i] == 'F'):
					self.sexo = 'Feminino'
					self.rbttFeminino.setChecked(True)
				else:
					self.sexo = 'Masculino'
					self.rbttMasculino.setChecked(True)

	def validateUpdate(self):
		errorsline = {}
		errorscmb = {}
		errorrbtt = None
		errorblob = None
		dct = {}

		for i in self.entries.keys(): #sao a mesma coisa do validateInsert soq a PK ta nas comboboxes.
			temp = PT.validateTypes(self.entries[i].text(), PT.getColumnType(self.selectedtable, i),i)
			if(len(temp)!=0):
				errorsline[i]=temp

		for i in self.scrolls.keys():
			if(i == PT.getTablePK(self.selectedtable)): # no update, a pk eh um combobox.
				continue
			pkval = self.scrolls[PT.getTablePK(self.selectedtable)].currentText()
			pkval = pkval.split('(')[-1].replace(')','')
			fkval = self.scrolls[i].currentText()
			fkval = fkval.split('(')[-1].replace(')','')
			temp = PT.validateNM(i,fkval,
				self.selectedtable, pkval) 
			if(temp != None):
				errorscmb[i]=temp

		if(self.sexo == True):
			errorrbtt = f'Sexo: nenhuma opcao selecionada'

		if('blob' in PT.getTypes(self.selectedtable) and self.fotoPath==''):
			errorblob = "Foto nao selecionada"
		if(len(errorscmb) + len(errorsline) != 0 or
			errorrbtt != None or errorblob != None):

			msg = QtWidgets.QMessageBox()
			msg.setWindowTitle('Erros')
			msg.setIcon(QtWidgets.QMessageBox.Critical)

			string = ''

			if(errorblob != None):
				string += errorblob + '\n'

			for i in errorsline.keys():
				for j in errorsline[i]:
					string += i + ': ' + j + '\n'	

			for i in errorscmb.keys():
				string += i + ': ' + errorscmb[i] + '\n'	
			if(errorrbtt!=None):
				string += errorrbtt
			msg.setText(string)
			msg.exec_()
		else:
			self.fillUpdateDict(dct)
			self.updatedict(dct)
			self.initBindows()

	def fillUpdateDict(self,dct):
		for i in self.entries.keys():
			dct[i]= PT.parseValue(self.selectedtable, i ,self.entries[i].text()) #dados extremamente estaveis
		for i in self.scrolls.keys(): # Guardam 
			if(i == PT.getTablePK(self.selectedtable)):
				continue
			column = PT.getColumnInfo(self.selectedtable, i)
			if(column != None):
				dct[i]=self.scrolls[i].currentText().split('(')[-1].replace(')','') 
										#dados incertos, podem estar tanto numa tabela nxm, quanto na tabela escolhida

		foto = PT.getTypeColumn(self.selectedtable, 'blob')
	
		if(foto != None):
			dct[foto] = self.fotoPath
		if(self.sexo == 'Feminino'):
			dct['Sexo'] = 'F'
		elif(self.sexo == 'Masculino'):
			dct['Sexo'] = 'M'	

	def updatedict(self, dct):
		columns = []
		values = []
		pkval = self.scrolls[PT.getTablePK(self.selectedtable)].currentText()
		pkval = pkval.split('(')[-1].replace(')','')
		for i in dct.keys():
			columns.append(i)
			values.append(dct[i])

		PT.UPDATE(self.selectedtable, columns, values, pkval)

	def insPKScroll(self, scroll):
		name = PT.pluraltosingular(scroll.objectName().replace('cmb', '')) #nome da tabela da fk.
		relation = PT.getTablePK(name) # pk da tabela. todas as fks estao no modelo Tabela_PKTabela ex : Local__Codigo
		self.scrolls[relation] = scroll
		self.initScroll(name,relation)
		return relation

	def Delete(self):
		self.clearWindow()
		uic.loadUi('TelasBD/deletar' + self.selectedname + '.ui', self)
		self.resize(self.maximumSize())

		self.buttons = [self.findChild(QtWidgets.QPushButton, 'bttDeleta'),
						self.findChild(QtWidgets.QPushButton, 'bttCancelar')]
		columns = PT.getTableInfo(self.selectedtable)

		self.buttons[0].clicked.connect(self.validateDeletar)
		self.buttons[1].clicked.connect(self.initBindows)
		self.scrolls[PT.getTablePK(self.selectedtable)] = self.cmbProcurar
		self.initScroll(self.selectedtable,PT.getTablePK(self.selectedtable))
		self.show()

	def validateDeletar(self):
		if(self.cmbProcurar.currentText() == ''):
			msg = QtWidgets.QMessageBox()
			msg.setWindowTitle('Erros')
			msg.setIcon(QtWidgets.QMessageBox.Critical)
			msg.setText(f'Nenhum elemento selecionado!')
			msg.exec_()
		else:
			PT.limpar(self.selectedtable, self.cmbProcurar.currentText().split('(')[-1].replace(')',''))
			self.initBindows()

	def Read(self):
		self.stable.setRowCount(0)
		text = trim(self.scrolls[self.selectedname].currentText())
		entry = trim(self.entries[self.selectedname].text())
		typ = PT.getTypes(self.selectedtable)
		columns = PT.getTableInfo(self.selectedtable)
		if(self.sexo != None and self.sexo != True):
			self.sexo = 'F' if self.sexo == 'Feminino' else 'M'
			elements = PT.getRegistries(self.selectedtable, 'Sexo', self.sexo)
		elif(text == '' or entry == ''):
			elements = PT.getRegistries(self.selectedtable)
		else:
			elements = PT.getRegistries(self.selectedtable, text, entry)
		
		for i in range(len(elements)):
			self.stable.insertRow(i)
			for j in range(len(elements[i])):
				item = str(elements[i][j])
				if('blob' in typ[j]):
					item = self.loadBLOB(elements[i][j])
					self.stable.setCellWidget(i,j,item)
				else:
					if(typ[j] == 'char(1)'):
						item = 'Feminino' if item == 'F' else 'Masculino'
					elif(columns[j][2] == 'MUL'):
						fktbl = PT.getTablebyFK(columns[j][0])
						pkfromfk = PT.getTablePK(fktbl)
						print(fktbl,item, columns[j][0])
						items = PT.selectColumnsInRow(fktbl,PT.getRegistry(fktbl,pkfromfk, item))
						if(len(items) == 2):
							item = f'{items[1]}({items[0]})' # nome(pk)
						else:
							item = f'{items[0]}'
					self.stable.setItem(i,j,QtWidgets.QTableWidgetItem(item))

		self.stable.verticalHeader().setDefaultSectionSize(60)
		self.stable.horizontalHeader().setDefaultSectionSize(120)
		
	def loadBLOB(self,data):
		imglbl = QtWidgets.QLabel(self.centralwidget)
		imglbl.setText('')
		imglbl.setScaledContents(True)
		pixmap = QPixmap()
		pixmap.loadFromData(data)
		imglbl.setPixmap(pixmap)
		return imglbl

	def elementSearch(self):
		text = self.scrolls[self.selectedname].currentText()
		if(text == ''):
			self.entries[self.selectedname].setEnabled(False)
		else:
			self.entries[self.selectedname].setEnabled(True)
		if(self.sexo != None):
			self.sexo = True
			
	def SearchSexo(self):
		rbtt = self.sender()
		if(rbtt.isChecked()):
			self.entries[self.selectedname].setEnabled(False)
			self.scrolls[self.selectedname].setCurrentIndex(-1)
			self.sexo = rbtt.text()

	def getPhoto(self):
		lbl = self.findChild(QtWidgets.QLabel, 'lblFotoImg')
		file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 
         'c:\\',"Image files (*.jpg *.gif *.jpeg *.png)")
		self.fotoPath=file[0]
		pixmap = QPixmap(self.fotoPath)
		pixmap = pixmap.scaled(lbl.size())
		lbl.setPixmap(pixmap)

	def clearWindow(self):
		self.buttons=[]
		self.entries={}
		self.scrolls={}
		self.sexo=None
		self.fotoPath=''
		self.stable = None

app = QtWidgets.QApplication(sys.argv)
window = Application()
app.exec_()
