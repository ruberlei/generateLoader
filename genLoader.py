#-- -----------------------------------------------------------------------------------
#-- File Name    : genLoader.py
#-- Author       : Ruberlei Cardoso Bento
#-- Description  : Generate Loader scripts.
#-- Call Syntax  : genLoader.py filename.csv
#-- Last Modified: 21/11/2023 
#-- -----------------------------------------------------------------------------------

import sys
import pandas as pd
import unidecode
import numpy as np
 
fileName = sys.argv[1]
fileNameBase = fileName.replace(" ", "_")[:-4]

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

    createTable = ("""set echo on
set timing on
set serveroutput on size unlimited
declare v_count number;
begin
    select count(1) into v_count from user_tables where table_name = upper('@tableName');
    if v_count = 0 then
        execute immediate 'create table @tableName (@columns)';
    else
        dbms_output.put_line('Table exists');
    end if;
end;
/
exit;""")
    
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
    sh = "#!/bin/bash\n"
    sh = sh + generateSqlPlusExec(fileNameBase+'.sql')
    sh = sh + '\n' + generateLoaderExec()
    writeFile(sh, fileNameBase + '.sh')

def writeFile(content, fileName):
    file = open(fileName, "w",encoding='utf-8') # write mode
    file.write(content)
    file.close()

def genFiles():
    createTable()
    generateSh()
    generateLoader(fileName)
    
genFiles() 