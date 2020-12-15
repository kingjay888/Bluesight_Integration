# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 22:26:02 2020

@author: JAYAKRISHNAJANAKIRAM

READ ME
"""
Prerequisite: 
    Install Python 3.9 and the dependency modules as below:
        requests, pandas, xlrd, csv, os, shutil, sys, datetime, time, logging
    Script Config file:
        SquadConfig.py file copied to the dir as the parent dir where script to be executed
    Internet Connectivity to connect to the bluesight Application

Config File:
    The config file defines the Input for the script, and the variables to be defined are as follows:
        Path         : Dir from which the Script would be executed
        URL          : The bluesight application URL to be accessed
        SquadID      : Squad ID 
        SquadName    : Squad Name
        Squadlist    : list the squads as Squad 1,2...n
        Source       : The Input file from the IPC tools
        SwimlaneName : Swimlane assigned for the squad in bluesight
        TokenID      : Token generated to login to the API in bluesight
        Headers      : update the TokenID in the headers
        Status       : Status of the IPC tickets
        Workgroup    : Workgroup defined for the Squad classification
        
Script execution:
    The Source file <(filename_yyyymmdd_hh).xlsx> file must be copied into the <Path> defined in the config file.
    Schedule the script in the windows scheduler or linux crontask
    
Logfile:
    The log file location are as follows:
        Summary logfile: (Path/<ddmmyyyy>/summary/IP_LogSummary_yyyymmdd_hhmm.log)
        Create Success : (Path/<ddmmyyyy>/log/create_success_yyyymmdd_hhmm.log)
        Create Error   : (Path/<ddmmyyyy>/log/create_error_yyyymmdd_hhmm.log)
        Update Success : (Path/<ddmmyyyy>/log/update_success_yyyymmdd_hhmm.log)
        Update Error   : (Path/<ddmmyyyy>/log/update_error_yyyymmdd_hhmm.log)

    
    

