__author__ = "Abdullahil Kafi"
__copyright__ = "Copyright (C) 2022 Abdullahil Kafi"
__license__ = "KHZG Projekt UKMD"
__version__ = "1.0"

import csv
import pathlib
import random
import codecs
import os
import fileinput

counter = 0
final_sql = []
final_altersql = []
for path in pathlib.Path("C:\Some Files\FD-Files\\").iterdir():    #taking the file input if needed it can also be given as a string from the user
    if path.is_file():
        filename = os.path.basename(path)

        with open(path, errors="ignore") as f:  #encoding is problematic with the data we have! so it's better to ignore error
            #print(f.readline())
            namelist = []
            nameOfTable = ''
            columns = []
            columntype = []
            primaryKey = []
            nullValue = []
            foreignKey = []
            comments = []
            nameOfTable = filename
            tableComments = ''
            for words in f.readlines():
                if words.startswith('%TABLE' or '%STRUCT'):
                    for name in words.split():
                        namelist.append(name)
                    ind_com = 0
                    for i in namelist:
                        if i.__contains__(filename):
                            ind_com = namelist.index(i)
                        else:
                            continue
                    if len(namelist) == ind_com + 1:
                        tableComments = namelist[-1]
                    else:
                        tableComments = namelist[-2] + ' ' +namelist[-1]




                elif words.startswith('%'):
                    continue
                elif words.startswith('#'):
                    continue
                else:
                    #print(words)
                    ahalist = []
                    for word in words.split():
                        ahalist.append(word)
                    if(len(ahalist) != 0):
                        if(ahalist[0] == ':'):
                            continue
                        else:
                            nameoftable_string = ahalist[0]

                            chunksla = nameoftable_string.split(':')
                            nameoftablee = chunksla[0]
                            columns.append(chunksla[0])
                            for item in ahalist:
                                if item.find('FX') > -1:
                                    columntype.append('INT')
                                elif item.find('CH') > -1:
                                    columntype.append('CHAR')
                                elif item.find('TS') > -1:
                                    columntype.append('TIMESTAMP')
                                elif item.find('DA') > -1:
                                    columntype.append('DATE')
                                elif item.find('CL') > -1:
                                    columntype.append('CHAR')
                                elif item.find('BIT') > -1:
                                    #print(nameOfTable)
                                    columntype.append('CHAR')
                                elif item.find('BL') > -1:
                                    columntype.append('TEXT')
                                elif item.find('SEQ') > -1:
                                    columntype.append('CHAR')

                            if ahalist.__contains__(':P:N:C' or ':P:N:B' or ':P' or ':N' or ':P:N' or ':N:B' or ':N:C'):
                                if(primaryKey.__contains__('PRIMARY KEY')):
                                    primaryKey.append('UNIQUE')
                                else:
                                    primaryKey.append('PRIMARY KEY')
                                nullValue.append('NOT NULL')
                            else:
                                primaryKey.append('')
                                nullValue.append('')
                            if (':FK' or ':FV') in ahalist:
                                var = ahalist.index(':FK' or ':FV')
                                referencekey = ahalist[var + 1]
                                remove = '()'
                                newstring = referencekey
                                for i in remove:
                                    newstring = newstring.replace(i, '')
                                chunks = newstring.split(',')

                                foreignKey.append('ALTER TABLE ' + filename + ' ADD' + ' ' + 'FOREIGN KEY' + ' ' + '('+nameoftablee+')' + ' '+  'REFERENCES ' + chunks[0]+'('+ ahalist[0]+');')
                            else:
                                foreignKey.append('')
                            index_hash = 0
                            for i in ahalist:
                                if i.__contains__('#'):
                                    index_hash = ahalist.index(i)
                                    if (index_hash+1 == (len(ahalist)-1)):
                                        if ahalist[index_hash+1].__contains__("'"):
                                            ahalist[index_hash+1] = ahalist[index_hash+1].replace("'", "")

                                        comments.append(ahalist[index_hash + 1])
                                    else:
                                        if ahalist[-1].__contains__("'"):
                                            ahalist[-1] = ahalist[-1].replace("'", "")

                                        if ahalist[-2].__contains__("'"):
                                            ahalist[-2] = ahalist[-2].replace("'", "")

                                        comments.append(ahalist[-2] + '' + ahalist[-1])
                                else:
                                    continue


        def preprocessing(types, primary, nullvalue, foreignkey):
            newtypes = [elem.replace(':', '') for elem in types]
            newprimary= [elem.replace(':', '') for elem in primary]
            newnullvalue = [elem.replace(':', '') for elem in nullvalue]
            newforeignKey = [elem.replace(':', '') for elem in foreignkey]

            return newtypes, newprimary, newnullvalue, newforeignKey

        def generateCSV(columns, types, primary, nullValue, foreignkey, tablename, comments):
            rows = [types, primary, nullValue, foreignkey, comments]
            path = 'C:\Some Files\CSV Files\\'+ tablename+'.csv'

            with open(path, 'w') as f:
                write = csv.writer(f)
                write.writerow(columns)
                write.writerows(rows)

        def generateSql(tablename, columnName, columntype, primary, null, foreignkey, comment, tableComment):

            sql = []



            stringnew = ''
            stringprimary = ''

            for i in range(len(columnName)):
                stringnew = columnName[i] + ' ' + columntype[i] + ' ' + null[i] + ' ' + 'comment ' + '\'' + comment[i] + '\''
                sql.append(stringnew)
            for i in range(len(columnName)):
                if(primary[i] == 'PRIMARY KEY'):
                    stringprimary = primary[i] + ' (' + columnName[i] + ')'
                    sql.append(stringprimary)
                elif(primary[i] == 'UNIQUE'):
                    stringprimary = primary[i] + ' (' + columnName[i] + ')'
                    sql.append(stringprimary)

            tableComment = 'COMMENT = ' + '\''+tableComment+'\''


            compiled =', \n'.join([str(item) for item in sql])
            #print(compiled)
            final_String = 'CREATE TABLE ' + tablename + ' (' \
                           + compiled + \
                           ')'
            final_String = final_String + ' ' + tableComment + ';'
            return final_String




        def generateAlterTable(foreignKey):
            frkey = []
            for i in foreignKey:
                if i.__contains__('ALTER TABLE'):
                    frkey.append(i)

            summed = '\n'.join([str(item) for item in frkey])
            return summed


        #generateCSV(columns, columntype, primaryKey, nullValue, foreignKey, nameOfTable, comments)
        sqlquery = generateSql(nameOfTable, columns, columntype, primaryKey, nullValue, foreignKey, comments, tableComments)

        altertable = generateAlterTable(foreignKey)
        final_sql.append(sqlquery)
        final_altersql.append(altertable)

def createFinal(final):
    finalss = ('\n').join(str(item) for item in final)
    with open('C:\Some Files\SQl\\sqlQuery.sql', 'w', encoding='utf8') as f:
        f.write(finalss)
    f.close()
    print('Done With The File Creation')

createsql = createFinal(final_sql)



print('Succesfully done with all files')