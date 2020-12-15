# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 20:57:32 2020

@author: JAYAKRISHNA JANAKIRAMAN (jayakrishna@my.ibm.com)

Script to read the excel file from IPC tools and create or update cards in bluesight

"""

"""
Import the Required Python Modules to support the script execution

"""
import requests
import SquadConfig
import pandas as pd
import xlrd, csv
import os, shutil, sys
from datetime import datetime
import time
import logging

"""
Assign Variables defined in the SquadConfig file

"""
path = SquadConfig.Path
url = SquadConfig.URL
sid = SquadConfig.SquadID
slist = SquadConfig.Squadlist
sname = SquadConfig.SquadName
swln = SquadConfig.SwimlaneName
tokid = SquadConfig.TokenID
headers = SquadConfig.Headers
status = SquadConfig.Status
sfile = SquadConfig.Source
# archive = SquadConfig.Archive
wgrp = SquadConfig.Workgroup
maindir = os.path.join(path, datetime.now().strftime('%d%m%Y'))
logdir = os.path.join(maindir, 'log')
sourcedir = os.path.join(maindir, 'source')
sumdir = os.path.join(maindir, 'summary')

"""
Create the Required directories to archive the log and source files

"""
def createdir():
    
    if not os.path.exists(maindir):
        os.mkdir(maindir)
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    if not os.path.exists(sourcedir):
         os.mkdir(sourcedir)
    if not os.path.exists(sumdir):
        os.mkdir(sumdir)
        
createdir()

"""
Enable logging for the script execution

"""
ts = time.time()
lgtime = datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M')
sttime = datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
start_time = datetime.now()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.handlers.RotatingFileHandler(os.path.join(sumdir, 'IP_LogSummary_{}.log'.format(lgtime)))
formatter    = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

if (logger.hasHandlers()):
    logger.handlers.clear()

logger.addHandler(file_handler)

if not os.path.isfile(sfile):
    
    logger.info('***********************************************************************************************************')
    logger.info('The Source File Does not exist')
    logger.info('***********************************************************************************************************')
    sys.exit(0)
   
create_success = os.path.join(logdir, 'create_success_{}.log'.format(lgtime))
with open(create_success, 'a'):
    os.utime(create_success)
create_error = os.path.join(logdir, 'create_error_{}.log'.format(lgtime))
with open(create_error, 'a'):
    os.utime(create_error)
update_success = os.path.join(logdir, 'update_success_{}.log'.format(lgtime))
with open(update_success, 'a'):
    os.utime(update_success)
update_error = os.path.join(logdir, 'update_error_{}.log'.format(lgtime))
with open(update_error, 'a'):
    os.utime(update_error)

logger.info('***********************************************************************************************************')
logger.info('Batch Job   Run DateTime (START) :=' + str(start_time) + '\n')
logger.info('++++++++++++++++++ Source File Summary ++++++++++++++++++' + '\n')
logger.info('Source File Name               := ' + sfile)
logger.info('Squad Bluesight Endpoint URL   := ' + url)
logger.info('Squad Bluesight API Token Used := ' + tokid)
logger.info('Squad ID                       := ' + str(sid))
logger.info('Squad Name                     := ' + str(sname))

"""
Function to Read the source file and create csv files

"""     
def csv_from_excel():
    
    workbook = xlrd.open_workbook(sfile)
   
    logger.info('No.of Worksheet In Source File := ' + str(workbook.nsheets))
    logger.info('Ticket Types Processed         := ' + str(swln) + '\n')
    logger.info('++++++++++++++++++ IPCR Records Summary ++++++++++++++++++' + '\n')
        
    for i in range(0, workbook.nsheets):
        sheet = workbook.sheet_by_index(i)
        sheet_name = sheet.name        
        with open( '{}.csv'.format(sheet_name), 'w') as csvfile:
                wr = csv.writer(csvfile, lineterminator='\n', delimiter=',', quoting=csv.QUOTE_MINIMAL)
                row_bucket = []
                
                for rownum in range(0, sheet.nrows):
                        col_bucket = []
                        if rownum == 0:
                                continue
                        if rownum == 1:
                                row_bucket.append(sheet.row_values(rownum))                               
                                continue
                        for colnum in range(sheet.ncols):
                                _type = sheet.cell_type(rownum, colnum)
                                _value = sheet.cell_value(rownum, colnum)
                                if colnum in [0,1]:
                                        col_bucket.append(str(_value))
                                        continue
                                if not _type == xlrd.XL_CELL_DATE:
                                        col_bucket.append(_value)                
                                else:
                                        _dt = xlrd.xldate_as_tuple(_value, workbook.datemode)
                                        _col = datetime(_dt[0], _dt[1], _dt[2], _dt[3], _dt[4], _dt[5])
                                        _in_string = _col.strftime("%m/%d/%Y %H:%M:%S")
                                        col_bucket.append(_in_string)
                        row_bucket.append(col_bucket)
                
                wr.writerows(row_bucket)

csv_from_excel()

"""
Function to Read the Csv files and transform the data into the input data 
to create cards

"""
def massage_input():
    list = swln
    if os.path.isfile('test_card_1_csv'):
        os.remove('test_card_1.csv')
    
 
    with open('test_card_1.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=["title", "swimlaneName", "workstateName", "squadId", "openedAt"])      
        writer.writeheader()
        f.close()
    
    for i in list:        
        df_i = pd.DataFrame(pd.read_csv('{}.csv'.format(i),engine= 'python'))
        ID = df_i.columns[1]              
        if i == 'Service':
            OD = df_i.columns[3]
        else:
            OD = df_i.columns[2]
        
        df_i = df_i.filter([ID, OD, 'Status', 'Description', 'Workgroup'])
        Active = status['Active']
        Backlog = status['Backlog']
        Closed = status['Closed']
        Wait = status['Wait']
                                
        sid_0 = wgrp['Squad1']
        sid_1 = wgrp['Squad2']
    
        df_i.insert(1,"swimlaneName", i, allow_duplicates = False)
        df_i[ID] = df_i[ID].astype(str).replace('\.0', '', regex=True)             
        df_i['Description'] = df_i['Description'].replace(to_replace= r'\\', value='', regex=True)
        df_i['Description'] = df_i['Description'].replace(to_replace= r'"', value='', regex=True)
        df_i['Description'] = df_i['Description'].replace(to_replace= r' ', value='_', regex=True)
        df_i['openedAt'] = df_i[OD]  
        df_i['workstateName'] = df_i['Status']
        df_i['title'] = df_i[ID].astype(str) + " : " + df_i['Description'].astype(str).apply(lambda x: x[:50])        
        df_i.loc[df_i['Status'].isin(Active), 'workstateType'] = 'Active'
        df_i.loc[df_i['Status'].isin(Backlog), 'workstateType'] = 'Backlog'
        df_i.loc[df_i['Status'].isin(Wait), 'workstateType'] = 'Wait'
        df_i.loc[df_i['Status'].isin(Closed), 'workstateType'] = 'Closed'
        df_i.loc[df_i['Workgroup'].isin(sid_0), 'squadId'] = sid[0]
        df_i.loc[df_i['Workgroup'].isin(sid_1), 'squadId'] = sid[1]
        df_i = df_i.filter(["title", "swimlaneName", "workstateName", "squadId", "openedAt"])
        
        rec_count = len(df_i)
        logger.info('The Total {} Record Processed := '.format(i) + str(rec_count) )
        df_i.to_csv('test_card_1.csv', mode='a', header=False, index=False)

massage_input()

"""
Function to update the cards in Bluesight

"""
def do_when_found(cid, sln, title, wsn, sc, ec, sqid):
    print('+++ update existing card')
    
    #
    def update_card(cid, sqid, sln, wsn):
        output_data = """{
    "query": "mutation {
      updateCard (
        input: {
          cardIdentifier: \\"%s\\"
            cardAttributes: {
                squadId: %s
                swimlaneName: \\"%s\\"
                workstateName: \\"%s\\"
                }
            }
        )
      {
        card {
          identifier
          
        }
        errors {
          path
          message
        }
      }
    }"
    }"""%(cid, sqid, sln, wsn)
        return output_data
       
    with open(update_success, "a") as of, open(update_error, "a") as ef:             
        catch_output = update_card(cid, sqid, sln, wsn )
        
        rc = requests.post(url, data=catch_output, headers=headers)
        
        log_msg = rc.json()
        data = pd.DataFrame(log_msg['data'])
        card_identifier = (data['updateCard']['card'])
        error = (data['updateCard']['errors'])
          
        if error == None:
            print( sln, title, card_identifier, error)
            of.write(str(sttime) + ':' + str(sln) + ':' + str(title) + str(card_identifier) +'\n')
            
        else:
            print( sln, title, error)
            ef.write(str(sttime) + ' :' + str(sln) + ':' + str(title) + str(error)+'\n')
                    
"""
Function to Create New Cards in Bluesight

"""
def do_when_not_found(title, wsn, sln, opd, sc, ec, sqid):
    print('+++ create new card')
    print(opd)
    def create_card(title, wsn, sln, opd, sqid):
        output_data = """{
            "query": "mutation {
              createCard (
                input: {
                  cardAttributes: {
                    squadId: %s
                    swimlaneName: \\"%s\\"
                    workstateName: \\"%s\\"
                    title: \\"%s\\"
                    openedAt: \\"%s\\"
                  }
                }
              )
              {
                card {
                  identifier
                }
                errors {
                  path
                  message
                }
              }
            }"
            }  
            """%(sqid, sln, wsn, title, opd)
        return output_data
     
    ts = time.time()
   
    sttime = datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')     
        
    with open(create_success, "a") as of, open(create_error, "a") as ef:    
        catch_output = create_card(title, wsn, sln, opd, sqid)
        print(catch_output)
        rc = requests.post(url, data=catch_output, headers=headers)
        
        log_msg = rc.json()
        
        data = pd.DataFrame(log_msg['data'])
        card_identifier = (data['createCard']['card'])
        error = (data['createCard']['errors'])
      
        if card_identifier != None:
            print(sln, title, card_identifier, error)
            of.write(str(sttime) + ':' + str(sln) + ':' + str(title) + str(card_identifier) +'\n')
            
        else:
            print(sln, title, error)
            ef.write(str(sttime) + ':' + str(sln) + ':' + str(title) + str(error)+'\n')
              
    return sc, ec

"""
Function to check the available cards

"""
def get_active_card():    
    
    list = swln
    squad = sid
    for k in squad:
        for i in list:
            get_card_details = """{
          "query": "{
            squad(id:%s) {
              name
              cards (includedOnKanban:true,
                      closed:false,
                      archived:false,
                      cancelled:false,
                      swimlaneName:\\"%s\\",
                      updatedSince: \\"2019-10-10T00:00:00-0300\\") {
                identifier
                title
            }
            }
          }"
        }"""%(k, i)
                         
            rc = requests.post(url, data=get_card_details, headers=headers)
            msg = rc.json()
            data = pd.DataFrame(msg['data'])
            data1 = (data['squad']['cards'])
            
            ld1 = len(data1)
           
            df = pd.read_csv("test_card_1.csv")
            
            flag = False
            sc = 0
            ec = 0
            for index,row in df.iterrows():
                title = row['title']
                sln = row['swimlaneName']
                wsn = row['workstateName']
                opd = row['openedAt']
                sqid = row['squadId']
                
                                          
                if k == str(sqid) and i == sln:
                                             
                    for j in range(0,ld1):
                        data2 = data1[j]
                        cid = data2['identifier']
                        if data2['title'] == title and i == sln and k == str(sqid):
                            do_when_found(cid, sln, title, wsn, sc, ec, sqid)
                            flag = True
                            break
                    
                    if flag == False:
                        do_when_not_found(title, wsn, sln, opd, sc, ec, sqid)
                       
                flag = False
            
get_active_card()

upd_success_count = len(open(update_success).readlines(  ))
upd_error_count = len(open(update_error).readlines(  ))
new_success_count = len(open(create_success).readlines(  ))
new_error_count = len(open(create_error).readlines(  ))

logger.info('\n' + '++++++++++++++++++ BlueSight Record Insert Summary ++++++++++++++++++' + '\n')
logger.info('Total Record NEW     (SUCCESS) := ' + str(new_success_count))
logger.info('Total Record NEW       (ERROR) := ' + str(new_error_count))
logger.info('Total Record UPDATE  (SUCCESS) := ' + str(upd_success_count))
logger.info('Total Record UPDATE    (ERROR) := ' + str(upd_error_count))
logger.info('\n' + '++++++++++++++++++ Log File Summary ++++++++++++++++++' + '\n')
logger.info('Success Log File Name (New)    := ' + create_success )
logger.info('Success Log File Name (Update) := ' + update_success )
logger.info('Error Log File Name (New)      := ' + create_error )
logger.info('Error Log File Name (New)      := ' + update_error + '\n')

end_time = datetime.now()

logger.info('Batch Job Run DateTime (END)   := ' + str(end_time) )
logger.info('TOTAL Run Time (Batch Job)     :=  {}'.format(end_time - start_time) + '\n')

logger.info('***********************************************************************************************************')

"""
Archive the Source file

"""
def move_source():
    sourcefiles = os.listdir(path)
    for files in sourcefiles:
        if files.endswith('.xlsx'):
            shutil.move(os.path.join(path,files) , os.path.join(sourcedir,files))
        if files.endswith('.csv'):
            os.remove(files)

move_source()

file_handler.close()
                     