import pandas as pd
import unidecode
import numpy as np
 
#https://stackoverflow.com/questions/50339065/how-to-get-maximum-length-of-each-column-in-the-data-frame-using-pandas-python
#df2 = df[[x for x in df if df[x].dtype == 'object']]
#max_length_in_each_col = df2.applymap(lambda x: len(x)).max()
#print(max_length_in_each_col)


fileName = 'randomperson.csv'
fileNameBase = fileName[:-4]

df = pd.read_csv(fileName)

def getColumnDtypes(dataTypes):
    dataList = []
    for x in dataTypes:
        if(x == 'int64'):
            dataList.append('number')
        elif (x == 'float64'):
            dataList.append('float')
        elif (x == 'bool'):
            dataList.append('boolean')
        else:
            dataList.append('varchar2')
    return dataList

def createTable():
    createTable = "set echo on\n"
    createTable = createTable + "set timing on\n"
    createTable = createTable + "set serveroutput on size unlimited\n"
    createTable = createTable + 'create table @tableName (@columns);\n'
    createTable = createTable + 'exit;'
    
    columns = ''

    columnDataType = getColumnDtypes(df.dtypes)
    
    measurer = np.vectorize(len)
    res1 = measurer(df.values.astype(str)).max(axis=0)
    
    for i in range(len(df.columns)):
        columns = columns + ''.join(letter for letter in df.columns[i].lower() if letter.isalnum()) + ' ' + columnDataType[i] + '('+ str(res1[i])  + '), '
  
    columns = unidecode.unidecode(columns[:-2])
        
    createTable = createTable.replace('@columns', columns)
    createTable = createTable.replace('@tableName', unidecode.unidecode(fileNameBase))
    writeFile(createTable, fileNameBase+'.sql') 

def generateLoader(fileName):
    columns =""
    genLoader =  "options (direct=true, errors=0, rows=100000, skip=1)\n"
    genLoader += "load data\n"
    genLoader += "infile '"  + fileName + "'\n"
    genLoader += "badfile '" + fileNameBase + ".bad'\n"
    genLoader += "append into table " +  fileNameBase + "\n"
    genLoader += "fields terminated by ','\n"
    genLoader += '''optionally enclosed by '"'\n'''
    genLoader += "date      format 'DD/MM/YYYY HH24:MI:SS'\n"
    genLoader += "trailing nullcols\n"
    genLoader += "(\n"
    for i in range(len(df.columns)):
        columns = columns + ''.join(letter for letter in df.columns[i].lower() if letter.isalnum()) + ',\n'
  
    genLoader += unidecode.unidecode(columns[:-2])
    genLoader += "\n)\n"           
    writeFile(genLoader, fileNameBase+'.ctl') 
    
def generateSqlPlusExec(sqlCommand):
    connectString = 'sqlplus HR/HR@192.168.0.22:1521/pdb @' + sqlCommand
    return connectString
    
def generateLoaderExec():
    generateLoaderSQL = 'sqlldr HR/HR@192.168.0.22:1521/pdb control='+fileNameBase+'.ctl ' + 'log=' + fileNameBase + '.log'
    return generateLoaderSQL

def generateSh():
    sh = '#!/bin/bash\n'
    sh = sh + generateSqlPlusExec(fileNameBase+'.sql')
    sh = sh + '\n' + generateLoaderExec()
    writeFile(sh, fileNameBase + '.sh')

def writeFile(content, fileName):
    file = open(fileName, "w",encoding='utf-8')  # write mode
    file.write(content)
    file.close()

def genFiles():
    createTable()
    generateSh()
    generateLoader(fileName)
    
genFiles()




