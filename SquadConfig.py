from datetime import datetime
import time

Path = 'C:/Jay_Doc/Python/Automation'
URL = 'https://singapore.bluesight.io/graphql'
SquadID = ['323','446']
Squadlist = ['Squad1', 'Squad2']
SquadName = ['my_test_python_script' , 'my_test_python_script_1']
ts = time.time()
sourcefiletime = datetime.fromtimestamp(ts).strftime('%Y%m%d_%H')                                           
Source = 'Incident_V2_{}.xlsx'.format(sourcefiletime)
SwimlaneName = ['Incident', 'Service', 'Change Request', 'Problem']
TokenID = "'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0MywiY3VycmVudF90aW1lIjoiMjAyMC0xMC0xNlQxNzo1ODozNS4zNTIrMDg6MDAifQ.4Pdfx7GO-Br3ciQzQugNZUpJmCNXwWuB_8bAztkk4mQ'"
Headers = {'Content-Type' : 'application/json', 'Bluesight-API-Token' : 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0MywiY3VycmVudF90aW1lIjoiMjAyMC0xMC0xNlQxNzo1ODozNS4zNTIrMDg6MDAifQ.4Pdfx7GO-Br3ciQzQugNZUpJmCNXwWuB_8bAztkk4mQ'}
Status = {'Active' : ['Assigned', 'Approved', 'In Progress', 'RCA Submitted', 'In-Progress', 'Resolved', 'Build', 'Implemented', 'Objected', 'Customer Approved', 'RCA Approved', 'Reviewed', 'Pre Authorization' ],
          'Backlog' : ['New', 'Requested', 'Initial Authorization', 'Draft', 'Estimate Provided', 'Testing',  
                       'RCA Approved', 'Referred back for RCA',  'Referred back to pre authorizer'],
          'Wait' : ['Waiting for Acceptance Test', 'Pending for Approval', 'Pending', 'On-Hold', 'Pending Further Review', 'Waiting for Customer Approval'],  
          'Closed' : ['Closed', 'Implemented', 'Cancelled', 'Rejected', 'Canceled']}

Workgroup = {'Squad1' : ['IBM On Site Support Team', 'IBM SAP Basis Team', 'IBM Service Desk Team', 'Application Team - SAP ABAP', 'Chandra Asri Network Team HO', 'Chandra Asri Network Team SO'],
             'Squad2' : ['IBM Server Team', 'IBM Network Team', 'Application Team - SAP PM SMI', 'Application Team - SAP MM SMI', 'Application Team - SAP PM SO']}