CREATE DATABASE ESCOLA;
USE ESCOLA;

CREATE TABLE Local_(Codigo INT NOT NULL, Categoria VARCHAR(45) NOT NULL, Descricao VARCHAR(45), PRIMARY KEY(Codigo));

CREATE TABLE Departamento(Codigo INT NOT NULL, Nome VARCHAR(45) NOT NULL, PRIMARY KEY(Codigo));

CREATE TABLE Disciplina(Codigo INT NOT NULL, Nome VARCHAR(45) NOT NULL, CargaHoraria INT NOT NULL, PRIMARY KEY(Codigo)); 
                        
CREATE TABLE Responsavel(CPF VARCHAR(15) NOT NULL, NOME VARCHAR(45) NOT NULL, EstadoCivil VARCHAR(30), PRIMARY KEY(CPF));

CREATE TABLE Telefone(Fone VARCHAR(20) NOT NULL, ResponsavelCPF VARCHAR(15) NOT NULL, PRIMARY KEY(Fone),
				      FOREIGN KEY (ResponsavelCPF) REFERENCES Responsavel(CPF) ON DELETE CASCADE);

CREATE TABLE Professor(Matricula INT NOT NULL, Nome VARCHAR(45) NOT NULL, Salario FLOAT NOT NULL, DataContratacao DATE NOT NULL, 
					 DataNascimento DATE NOT NULL, Formacao VARCHAR(45) NOT NULL, FOTO MEDIUMBLOB NOT NULL,
                     DepartamentoCodigo INT NOT NULL, PRIMARY KEY(MATRICULA),
                     FOREIGN KEY(DepartamentoCodigo) REFERENCES Departamento(Codigo) ON DELETE CASCADE); -- alo

CREATE TABLE ProfessorDisciplina(ProfessorMatricula INT NOT NULL, DisciplinaCodigo INT NOT NULL,
								 FOREIGN KEY (ProfessorMatricula) REFERENCES Professor(Matricula) ON DELETE CASCADE,
                                 FOREIGN KEY (DisciplinaCodigo) REFERENCES Disciplina(Codigo) ON DELETE CASCADE);

CREATE TABLE AtividadeExtracurricular(Codigo INT NOT NULL, Descricao VARCHAR(60) NOT NULL, Horario TIME NOT NULL, 
									  Local_Codigo INT NOT NULL, ProfessorMatricula INT NOT NULL, PRIMARY KEY(Codigo),
                                      FOREIGN KEY (Local_Codigo) REFERENCES Local_(Codigo) ON DELETE CASCADE,
                                      FOREIGN KEY (ProfessorMatricula) REFERENCES Professor(Matricula) ON DELETE CASCADE); -- alo

CREATE TABLE Turma(Identificacao INT NOT NULL, Turno VARCHAR(45) NOT NULL, Local_Codigo INT NOT NULL,
				   PRIMARY KEY(Identificacao),
                   FOREIGN KEY (Local_Codigo) REFERENCES Local_(Codigo) ON DELETE CASCADE);

CREATE TABLE Estudante(Matricula INT NOT NULL, Nome VARCHAR(45) NOT NULL, Sexo CHAR NOT NULL, DataNascimento DATE NOT NULL, 
					   Mensalidade FLOAT NOT NULL, Foto MEDIUMBLOB NOT NULL, TurmaIdentificacao INT NOT NULL, PRIMARY KEY(Matricula),
                       FOREIGN KEY (TurmaIdentificacao) REFERENCES Turma(Identificacao) ON DELETE CASCADE); -- alo

CREATE TABLE EstudanteAtividadeExtracurricular(EstudanteMatricula INT NOT NULL, AtividadeExtracurricularCodigo INT NOT NULL,
					   FOREIGN KEY (EstudanteMatricula) REFERENCES Estudante(Matricula) ON DELETE CASCADE,
                       FOREIGN KEY (AtividadeExtracurricularCodigo) REFERENCES AtividadeExtracurricular(Codigo) ON DELETE CASCADE);

CREATE TABLE Dependente(Nome VARCHAR(45) NOT NULL, Parentesco VARCHAR(45) NOT NULL, DataNascimento DATE NOT NULL,
						ProfessorMatricula INT NOT NULL, PRIMARY KEY(Nome),
                        FOREIGN KEY (ProfessorMatricula) REFERENCES Professor(Matricula) ON DELETE CASCADE);

CREATE TABLE Itens(Nome VARCHAR(60) NOT NULL, Quantidade INT NOT NULL, DescricaoAdicional VARCHAR(45), 
					Ilustracao MEDIUMBLOB, Local_Codigo INT NOT NULL, PRIMARY KEY(Nome),
                    FOREIGN KEY (Local_Codigo) REFERENCES Local_(Codigo) ON DELETE CASCADE); -- Mudar Ilustracao para BLOB?

CREATE TABLE Despesas(Id INT NOT NULL, Descricao VARCHAR(60) NOT NULL, Valor FLOAT NOT NULL, Data_ DATE NOT NULL, 
					  DepartamentoCodigo INT NOT NULL, PRIMARY KEY(Id),
					  FOREIGN KEY (DepartamentoCodigo) REFERENCES Departamento(Codigo) ON DELETE CASCADE);
                                
CREATE TABLE ProfessorTurma(ProfessorMatricula INT NOT NULL, TurmaIdentificacao INT NOT NULL, 
							FOREIGN KEY(ProfessorMatricula) REFERENCES Professor(Matricula) ON DELETE CASCADE,
                            FOREIGN KEY(TurmaIdentificacao) REFERENCES Turma(Identificacao) ON DELETE CASCADE);

CREATE TABLE ResponsavelEstudante(ResponsavelCPF VARCHAR(15) NOT NULL, EstudanteMatricula INT NOT NULL, 
								 FOREIGN KEY (ResponsavelCPF) REFERENCES Responsavel(CPF) ON DELETE CASCADE,
                                 FOREIGN KEY (EstudanteMatricula) REFERENCES Estudante(Matricula) ON DELETE CASCADE);

CREATE TABLE Notas(Bimestre INT NOT NULL, Prova FLOAT NOT NULL, Teste FLOAT NOT NULL, 
					Projeto FLOAT NOT NULL, Atividades FLOAT NOT NULL, EstudanteMatricula INT NOT NULL, 
                    DisciplinaCodigo INT NOT NULL, FOREIGN KEY (EstudanteMatricula) REFERENCES Estudante(Matricula) ON DELETE CASCADE,
                    FOREIGN KEY (DisciplinaCodigo) REFERENCES Disciplina(Codigo) ON DELETE CASCADE);
                    
INSERT INTO Local_ VALUES(1, "Sala", "de aula");
INSERT INTO Local_ VALUES(3, "Laboratório", "de física");
INSERT INTO Local_ VALUES(2, "Sala", "de estudo");
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
INSERT INTO Disciplina VALUES(5, "Artes Visuais", 160);

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

INSERT INTO Professor VALUES(101, "Jussara Alencar Alves", 2500.00, "2020-07-12", "1980-05-30", "Matemática Licenciatura", "", 1);
INSERT INTO Professor VALUES(202, "Emerson Nascimento Ferreira", 3000.00, "2008-02-18", "1970-03-01", "Artes Cênicas", "", 3);
INSERT INTO Professor VALUES(303, "Rodrigo Perreira Santos", 2800.00, "2012-10-24", "1975-11-27", "História Licenciatura", "", 4);
INSERT INTO Professor VALUES(404, "Bruno Alves Lima", 2800.00, "2012-04-10", "1982-03-15", "Literatura Licenciatura", "", 2);
INSERT INTO Professor VALUES(505, "Vanessa Silva Castro", 2500.00, "2021-05-11", "1985-09-20", "Educação Física", "", 4);

INSERT INTO ProfessorDisciplina VALUES(101, 1);
INSERT INTO ProfessorDisciplina VALUES(101, 3);
INSERT INTO ProfessorDisciplina VALUES(303, 4);
INSERT INTO ProfessorDisciplina VALUES(404, 2);
INSERT INTO ProfessorDisciplina VALUES(202, 5);

INSERT INTO AtividadeExtracurricular VALUES(10, "Clube de Esporte", "14:00:00", 5, 505);
INSERT INTO AtividadeExtracurricular VALUES(20, "Clube de Esporte", "18:00:00", 5, 505);
INSERT INTO AtividadeExtracurricular VALUES(30, "Clube de Teatro", "18:00:00", 4, 202);
INSERT INTO AtividadeExtracurricular VALUES(40, "Línguas Estrangeiras", "15:00:00", 2, 404);
INSERT INTO AtividadeExtracurricular VALUES(50, "Revisão para Vestibular", "15:00:00", 1, 101);

INSERT INTO Turma VALUES(1, "Matutino", 1);
INSERT INTO Turma VALUES(2, "Vespertino", 1);
INSERT INTO Turma VALUES(3, "Matutino", 2);
INSERT INTO Turma VALUES(4, "Vespertino", 2);
INSERT INTO Turma VALUES(5, "Matutino", 4);

INSERT INTO Estudante VALUES(111, "João Pedro Carvalho Costa", 'M', "2003-10-25", 1700.00, "", 1);
INSERT INTO Estudante VALUES(222, "Maria Clara Andrade dos Santos", 'F', "2015-05-12", 1200.00, "", 2);
INSERT INTO Estudante VALUES(333, "Pedro Alves Costa", 'M', "2002-07-19", 1700.00, "", 1);
INSERT INTO Estudante VALUES(444, "Lucas Perreira Silva", 'M', "2015-05-18", 1200.00, "", 2);
INSERT INTO Estudante VALUES(555, "Larissa Perreira Silva", 'F', "2003-02-28", 1700.00, "", 1);

INSERT INTO EstudanteAtividadeExtracurricular VALUES(111, 50);
INSERT INTO EstudanteAtividadeExtracurricular VALUES(111, 20);
INSERT INTO EstudanteAtividadeExtracurricular VALUES(222, 10);
INSERT INTO EstudanteAtividadeExtracurricular VALUES(333, 30);
INSERT INTO EstudanteAtividadeExtracurricular VALUES(333, 40);

INSERT INTO Dependente VALUES("Bruno Alencar Alves", "Filho", "2005-10-23", 101);
INSERT INTO Dependente VALUES("Pedro Alencar Alves", "Filho", "2015-07-26", 101);
INSERT INTO Dependente VALUES("Ana Clara Silva Perreira Santos", "Esposa", "1982-07-13", 303);
INSERT INTO Dependente VALUES("Maria Eduarda Silva Castro", "Filha", "2003-11-01", 505);
INSERT INTO Dependente VALUES("Leonardo Alencar Alves", "Marido", "1983-08-02", 505);

INSERT INTO Itens VALUES("Cadeira", 30, "de Madeira", NULL, 1);
INSERT INTO Itens VALUES("Mesa", 15, "de Plástico", NULL, 2);
INSERT INTO Itens VALUES("Bola", 10, "de Basquete", NULL, 5);
INSERT INTO Itens VALUES("Balança", 5, NULL, NULL, 3);
INSERT INTO Itens VALUES("Quadro", 1, "Negro", NULL, 1);

INSERT INTO Despesas VALUES(11, "Luz", 500.00, "2021-10-29", 4);
INSERT INTO Despesas VALUES(22, "Manutenção de Salas", 250.00, "2021-10-12", 4);
INSERT INTO Despesas VALUES(33, "Água", 340.00, "2021-09-29", 4);
INSERT INTO Despesas VALUES(44, "Obras", 480.00, "2021-09-05", 4);
INSERT INTO Despesas VALUES(55, "Novos Recursos", 600.00, "2021-09-08", 4);

INSERT INTO ProfessorTurma VALUES(101, 1);
INSERT INTO ProfessorTurma VALUES(202, 2);
INSERT INTO ProfessorTurma VALUES(101, 4);
INSERT INTO ProfessorTurma VALUES(303, 3);
INSERT INTO ProfessorTurma VALUES(404, 5);

INSERT INTO ResponsavelEstudante VALUES("111.222.333-44", 444);
INSERT INTO ResponsavelEstudante VALUES("222.333.444-55", 555);
INSERT INTO ResponsavelEstudante VALUES("333.444.555-66", 111);
INSERT INTO ResponsavelEstudante VALUES("444.555.666-77", 333);
INSERT INTO ResponsavelEstudante VALUES("555.666.777-88", 222);

INSERT INTO Notas VALUES(1, 10.0, 8.5, 9.8, 10.0, 111, 3);
INSERT INTO Notas VALUES(2, 10.0, 7.0, 9.0, 9.9, 111, 1);
INSERT INTO Notas VALUES(1, 8.5, 9.5, 9.5, 8.5, 222, 3);
INSERT INTO Notas VALUES(2, 10.0, 9.5, 9.0, 9.5, 222, 4);
INSERT INTO Notas VALUES(1, 10.0, 10.0, 10.0, 10.0, 333, 2);

CREATE VIEW Media_Notas AS
SELECT E.Nome as Aluno, D.Nome as Disciplina, Bimestre, ROUND((Prova + Teste + Projeto + Atividades)/4, 2) as MediaNotas
FROM Estudante as E, Disciplina as D, Notas as N
WHERE DisciplinaCodigo = Codigo and EstudanteMatricula = Matricula;

SELECT * FROM Media_Notas;

CREATE VIEW Salario_Total AS
SELECT D.Codigo as Depto, ROUND(SUM(P.Salario), 2) as Salario_Custo
FROM Departamento as D, Professor as P
WHERE Codigo =  DepartamentoCodigo
GROUP BY DepartamentoCodigo;

SELECT * FROM Salario_Total;

DELIMITER ||

CREATE PROCEDURE AumentoSalarial (IN CodDept INT)
BEGIN
	DECLARE GastoSalario FLOAT;
    DECLARE DespesasAtuais FLOAT;
    DECLARE DespesasPassadas FLOAT;
    DECLARE Percentual FLOAT;
    
    SELECT Salario_Custo INTO GastoSalario
    FROM Salario_Total
    WHERE Depto = CodDept;
    
    SELECT SUM(Valor) INTO DespesasAtuais
    From Departamento, Despesas
    WHERE Codigo = CodDept AND EXTRACT(YEAR_MONTH FROM Data_) = EXTRACT(YEAR_MONTH FROM CURRENT_DATE());
    
    SELECT SUM(Valor) INTO DespesasPassadas
    FROM Departamento, Despesas
    WHERE Codigo = CodDept AND EXTRACT(YEAR_MONTH FROM Data_) = EXTRACT(YEAR_MONTH FROM DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH));
    
    SELECT GastoSalario + DespesasAtuais INTO DespesasAtuais;
    SELECT GastoSalario + DespesasPassadas INTO DespesasPassadas;
    SELECT DespesasAtuais / DespesasPassadas INTO Percentual;
    
    IF Percentual < 1 THEN
		UPDATE Professor
        SET Salario = Salario + Salario*0.2
        WHERE DepartamentoCodigo = CodDept;
	END IF;
END ||

DELIMITER ;

SELECT * FROM Professor;

CALL AumentoSalarial(4);

SELECT * FROM Professor;