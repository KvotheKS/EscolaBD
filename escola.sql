CREATE DATABASE ESCOLA;
USE ESCOLA;

CREATE TABLE Local_(Codigo INT NOT NULL, Categoria VARCHAR(45) NOT NULL, Descricao VARCHAR(45), PRIMARY KEY(Codigo));

CREATE TABLE Departamento(Codigo INT NOT NULL, Nome VARCHAR(45) NOT NULL, PRIMARY KEY(Codigo));

CREATE TABLE Disciplina(Codigo INT NOT NULL, Nome VARCHAR(45) NOT NULL, CargaHoraria INT NOT NULL, PRIMARY KEY(Codigo)); 
                        
CREATE TABLE Responsavel(CPF VARCHAR(15) NOT NULL, NOME VARCHAR(45) NOT NULL, EstadoCivil VARCHAR(30), PRIMARY KEY(CPF));

CREATE TABLE Telefone(Fone VARCHAR(20) NOT NULL, ResponsavelCPF VARCHAR(15) NOT NULL, PRIMARY KEY(Fone),
				      FOREIGN KEY (ResponsavelCPF) REFERENCES Responsavel(CPF));

CREATE TABLE Professor(Matricula INT NOT NULL, Nome VARCHAR(45) NOT NULL, Salario FLOAT NOT NULL, DataContratacao DATE NOT NULL, 
					 DataNascimento DATE NOT NULL, Formacao VARCHAR(45) NOT NULL, FOTO MEDIUMBLOB NOT NULL,
                     DisciplinaCodigo INT, DepartamentoCodigo INT NOT NULL, PRIMARY KEY(MATRICULA),
                     FOREIGN KEY(DisciplinaCodigo) REFERENCES Disciplina(Codigo),
                     FOREIGN KEY(DepartamentoCodigo) REFERENCES Departamento(Codigo)); -- alo

CREATE TABLE ProfessorDisciplina(ProfessorMatricula INT NOT NULL, DisciplinaCodigo INT NOT NULL,
								 FOREIGN KEY (ProfessorMatricula) REFERENCES Professor(Matricula),
                                 FOREIGN KEY (DisciplinaCodigo) REFERENCES Disciplina(Codigo));

CREATE TABLE AtividadeExtracurricular(Codigo INT NOT NULL, Descricao VARCHAR(60) NOT NULL, Horario TIME NOT NULL, 
									  Local_Codigo INT NOT NULL, ProfessorMatricula INT NOT NULL, PRIMARY KEY(Codigo),
                                      FOREIGN KEY (Local_Codigo) REFERENCES Local_(Codigo),
                                      FOREIGN KEY (ProfessorMatricula) REFERENCES Professor(Matricula)); -- alo

CREATE TABLE Turma(Identificacao INT NOT NULL, Turno VARCHAR(45) NOT NULL, Local_Codigo INT NOT NULL,
				   PRIMARY KEY(Identificacao),
                   FOREIGN KEY (Local_Codigo) REFERENCES Local_(Codigo));

CREATE TABLE Estudante(Matricula INT NOT NULL, Nome VARCHAR(45) NOT NULL, Sexo CHAR NOT NULL, DataNascimento DATE NOT NULL, 
					   Mensalidade FLOAT NOT NULL, Foto MEDIUMBLOB NOT NULL, TurmaIdentificacao INT NOT NULL, PRIMARY KEY(Matricula),
                       FOREIGN KEY (TurmaIdentificacao) REFERENCES Turma(Identificacao)); -- alo

CREATE TABLE EstudanteAtividadeExtracurricular(EstudanteMatricula INT NOT NULL, AtividadeExtracurricularCodigo INT NOT NULL,
					   FOREIGN KEY (EstudanteMatricula) REFERENCES Estudante(Matricula),
                       FOREIGN KEY (AtividadeExtracurricularCodigo) REFERENCES AtividadeExtracurricular(Codigo));

CREATE TABLE Dependente(Nome VARCHAR(45) NOT NULL, Parentesco VARCHAR(45) NOT NULL, DataNascimento DATE NOT NULL,
						ProfessorMatricula INT NOT NULL, PRIMARY KEY(Nome),
                        FOREIGN KEY (ProfessorMatricula) REFERENCES Professor(Matricula));

CREATE TABLE Itens(Nome VARCHAR(60) NOT NULL, Quantidade INT NOT NULL, DescricaoAdicional VARCHAR(45), 
					Ilustracao MEDIUMBLOB, Local_Codigo INT NOT NULL, PRIMARY KEY(Nome),
                    FOREIGN KEY (Local_Codigo) REFERENCES Local_(Codigo)); -- Mudar Ilustracao para BLOB?

CREATE TABLE Despesas(Id INT NOT NULL, Descricao VARCHAR(60) NOT NULL, Valor FLOAT NOT NULL, Data_ DATE NOT NULL, 
					  DepartamentoCodigo INT NOT NULL, PRIMARY KEY(Id),
					  FOREIGN KEY (DepartamentoCodigo) REFERENCES Departamento(Codigo));
                      
CREATE TABLE HistoricoDespesas(MesAno DATE NOT NULL, GastoMensal FLOAT NOT NULL, -- Mesano eh um DATE que vai ser guardado por default como YYYY/MM/01, para acessar so o YM, usar funcao.
							   DepartamentoCodigo INT NOT NULL, PRIMARY KEY(MesAno), 
                               FOREIGN KEY (DepartamentoCodigo) REFERENCES Departamento(Codigo)); 
                                
CREATE TABLE ProfessorTurma(ProfessorMatricula INT NOT NULL, TurmaIdentificacao INT NOT NULL, 
							FOREIGN KEY(ProfessorMatricula) REFERENCES Professor(Matricula),
                            FOREIGN KEY(TurmaIdentificacao) REFERENCES Turma(Identificacao));

CREATE TABLE ResponsavelEstudante(ResponsavelCPF VARCHAR(15) NOT NULL, EstudanteMatricula INT NOT NULL, 
								 FOREIGN KEY (ResponsavelCPF) REFERENCES Responsavel(CPF),
                                 FOREIGN KEY (EstudanteMatricula) REFERENCES Estudante(Matricula));

CREATE TABLE Notas(Bimestre INT NOT NULL, Prova FLOAT NOT NULL, Teste FLOAT NOT NULL, 
					Projeto FLOAT NOT NULL, Atividades FLOAT NOT NULL, EstudanteMatricula INT NOT NULL, 
                    DisciplinaCodigo INT NOT NULL, PRIMARY KEY(Bimestre),
                    FOREIGN KEY (EstudanteMatricula) REFERENCES Estudante(Matricula),
                    FOREIGN KEY (DisciplinaCodigo) REFERENCES Disciplina(Codigo));
                    
INSERT INTO Local_ VALUES(1, "Sala", "de aula");
INSERT INTO Local_ VALUES(3, "Laboratório", "de física");
INSERT INTO Local_ VALUES(2, "Sala", "de aula");
INSERT INTO Local_ VALUES(4, "Auditório", NULL);
INSERT INTO Local_ VALUES(5, "Quadra", "externa");

INSERT INTO Departamento VALUES(1, "Exatas");
INSERT INTO Departamento VALUES(5, "Ciências Naturais");
INSERT INTO Departamento VALUES(3, "Artes");
INSERT INTO Departamento VALUES(4, "Ciências Humanas");
INSERT INTO Departamento VALUES(2, "Linguagens");

INSERT INTO Disciplina VALUES(1, "Matemática", 220);
INSERT INTO Disciplina VALUES(2, "Língua Portuguesa", 240);
INSERT INTO Disciplina VALUES(4, "História", 180);
INSERT INTO Disciplina VALUES(3, "Física", 180);
INSERT INTO Disciplina VALUES(5, "Inglês", 160);

INSERT INTO Responsavel VALUES("111.222.333-44", "Alfonso Perreira Silva", "Casado");
INSERT INTO Responsavel VALUES("222.333.444-55", "Gertrudes Santos Perreira Silva", "Casado");
INSERT INTO Responsavel VALUES("333.444.555-66", "Maria Aparecida Costa", "Viúva");
INSERT INTO Responsavel VALUES("444.555.666-77", "Bruna Alves Nascimento", "Solteiro");
INSERT INTO Responsavel VALUES("555.666.777-88", "Oscar Carvalho Costa", "Divorciado");

INSERT INTO Telefone VALUES("94929-5229", "111.222.333-44");
INSERT INTO Telefone VALUES("92005-4477", "222.333.444-55");
INSERT INTO Telefone VALUES("95438-2170", "444.555.666-77");
INSERT INTO Telefone VALUES("3299-4544", "444.555.666-77");
INSERT INTO Telefone VALUES("93505-9256", "555.666.777-88");