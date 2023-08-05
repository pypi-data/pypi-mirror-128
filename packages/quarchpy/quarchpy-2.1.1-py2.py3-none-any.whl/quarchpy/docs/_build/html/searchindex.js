Search.setIndex({docnames:["CHANGES","index","readme","source/changelog","source/licenses","source/modules","source/quarchpy","source/quarchpy.calibration","source/quarchpy.config_files","source/quarchpy.connection_specific","source/quarchpy.debug","source/quarchpy.device","source/quarchpy.disk_test","source/quarchpy.fio","source/quarchpy.iometer","source/quarchpy.qis","source/quarchpy.qps","source/quarchpy.user_interface","source/quarchpy.utilities","source/readme"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["CHANGES.rst","index.rst","readme.rst","source\\changelog.rst","source\\licenses.rst","source\\modules.rst","source\\quarchpy.rst","source\\quarchpy.calibration.rst","source\\quarchpy.config_files.rst","source\\quarchpy.connection_specific.rst","source\\quarchpy.debug.rst","source\\quarchpy.device.rst","source\\quarchpy.disk_test.rst","source\\quarchpy.fio.rst","source\\quarchpy.iometer.rst","source\\quarchpy.qis.rst","source\\quarchpy.qps.rst","source\\quarchpy.user_interface.rst","source\\quarchpy.utilities.rst","source\\readme.rst"],objects:{"":[[6,0,0,"-","quarchpy"]],"quarchpy.config_files":[[8,1,1,"","get_config_path_for_module"],[8,1,1,"","parse_config_file"]],"quarchpy.connection":[[6,2,1,"","PYConnection"],[6,2,1,"","QISConnection"],[6,2,1,"","QPSConnection"]],"quarchpy.connection_specific":[[9,0,0,"-","connection_QIS"],[9,0,0,"-","connection_QPS"],[9,0,0,"-","connection_ReST"],[9,0,0,"-","connection_Serial"],[9,0,0,"-","connection_TCP"],[9,0,0,"-","connection_Telnet"],[9,0,0,"-","connection_USB"]],"quarchpy.connection_specific.connection_QIS":[[9,2,1,"","QisInterface"]],"quarchpy.connection_specific.connection_QIS.QisInterface":[[9,3,1,"","GetQisModuleSelection"],[9,3,1,"","averageStripes"],[9,3,1,"","avgStringFromPwr"],[9,3,1,"","connect"],[9,3,1,"","convertStreamAverage"],[9,3,1,"","deviceDictSetup"],[9,3,1,"","deviceMulti"],[9,3,1,"","disconnect"],[9,3,1,"","getDeviceList"],[9,3,1,"","getStreamXmlHeader"],[9,3,1,"","interruptList"],[9,3,1,"","isXmlHeader"],[9,3,1,"","qis_scan_devices"],[9,3,1,"","rxBytes"],[9,3,1,"","scanIP"],[9,3,1,"","sendAndReceiveCmd"],[9,3,1,"","sendAndReceiveText"],[9,3,1,"","sendCmd"],[9,3,1,"","sendText"],[9,3,1,"","sortFavourite"],[9,3,1,"","startStream"],[9,3,1,"","startStreamThread"],[9,3,1,"","stopStream"],[9,3,1,"","streamBufferStatus"],[9,3,1,"","streamGetStripesText"],[9,3,1,"","streamHeaderAverage"],[9,3,1,"","streamHeaderFormat"],[9,3,1,"","streamHeaderVersion"],[9,3,1,"","streamInterrupt"],[9,3,1,"","streamRunningStatus"],[9,3,1,"","waitStop"]],"quarchpy.connection_specific.connection_QPS":[[9,2,1,"","QpsInterface"]],"quarchpy.connection_specific.connection_QPS.QpsInterface":[[9,3,1,"","connect"],[9,3,1,"","disconnect"],[9,3,1,"","getDeviceList"],[9,3,1,"","recv"],[9,3,1,"","scanIP"],[9,3,1,"","send"],[9,3,1,"","sendCmdVerbose"]],"quarchpy.connection_specific.connection_ReST":[[9,2,1,"","ReSTConn"]],"quarchpy.connection_specific.connection_ReST.ReSTConn":[[9,3,1,"","close"],[9,3,1,"","sendCommand"]],"quarchpy.connection_specific.connection_Serial":[[9,2,1,"","SerialConn"],[9,1,1,"","serial_read_until"]],"quarchpy.connection_specific.connection_Serial.SerialConn":[[9,3,1,"","close"],[9,3,1,"","sendCommand"]],"quarchpy.connection_specific.connection_TCP":[[9,2,1,"","TCPConn"]],"quarchpy.connection_specific.connection_TCP.TCPConn":[[9,3,1,"","close"],[9,3,1,"","sendCommand"]],"quarchpy.connection_specific.connection_Telnet":[[9,2,1,"","TelnetConn"]],"quarchpy.connection_specific.connection_Telnet.TelnetConn":[[9,3,1,"","close"],[9,3,1,"","sendCommand"]],"quarchpy.connection_specific.connection_USB":[[9,2,1,"","TQuarchUSB_IF"],[9,1,1,"","USB"],[9,2,1,"","USBConn"],[9,1,1,"","getUSBDeviceSerialNo"],[9,1,1,"","importUSB"]],"quarchpy.connection_specific.connection_USB.TQuarchUSB_IF":[[9,3,1,"","BulkRead"],[9,3,1,"","BulkReadEP"],[9,3,1,"","BulkReadEPTout"],[9,3,1,"","BulkReadN"],[9,3,1,"","CheckComms"],[9,3,1,"","ClosePort"],[9,3,1,"","DebugDump"],[9,3,1,"","FetchCmdReply"],[9,3,1,"","FetchCmdReplyTOut"],[9,3,1,"","GetExtendedInfo"],[9,3,1,"","GetIdn"],[9,3,1,"","GetLastError"],[9,3,1,"","GetSerialNumber"],[9,3,1,"","IsPortOpen"],[9,3,1,"","OpenPort"],[9,3,1,"","RunCommand"],[9,3,1,"","SendCommand"],[9,3,1,"","SetTimeout"],[9,3,1,"","VerboseSendCmd"],[9,3,1,"","WriteZeroPacketCmd"],[9,3,1,"","clean_and_flush_stuck_usb_comms"],[9,4,1,"","lockUSBStr"],[9,4,1,"","unlockUSBStr"]],"quarchpy.connection_specific.connection_USB.USBConn":[[9,3,1,"","close"],[9,3,1,"","sendCommand"]],"quarchpy.debug":[[10,0,0,"-","SystemTest"],[10,0,0,"-","upgrade_quarchpy"],[10,0,0,"-","versionCompare"]],"quarchpy.debug.SystemTest":[[10,1,1,"","QuarchSimpleIdentify"],[10,1,1,"","fix_usb"],[10,1,1,"","get_QIS_version"],[10,1,1,"","get_java_location"],[10,1,1,"","get_quarchpy_version"],[10,1,1,"","main"],[10,1,1,"","test_communication"],[10,1,1,"","test_system_info"]],"quarchpy.debug.upgrade_quarchpy":[[10,1,1,"","check_if_update"],[10,1,1,"","main"],[10,1,1,"","updateQuarchpy"]],"quarchpy.debug.versionCompare":[[10,1,1,"","requiredQuarchpyVersion"]],"quarchpy.device":[[11,0,0,"-","device"],[11,1,1,"","getQuarchDevice"],[11,1,1,"","getSerialNumberFromConnectionTarget"],[11,1,1,"","get_connection_target"],[11,1,1,"","listDevices"],[11,1,1,"","qpsNowStr"],[11,2,1,"","quarchArray"],[11,0,0,"-","quarchArray"],[11,2,1,"","quarchDevice"],[11,2,1,"","quarchPPM"],[11,0,0,"-","quarchPPM"],[11,2,1,"","quarchQPS"],[11,0,0,"-","quarchQPS"],[11,2,1,"","quarchStream"],[11,1,1,"","scanDevices"],[11,0,0,"-","scanDevices"],[11,2,1,"","subDevice"],[11,1,1,"","userSelectDevice"]],"quarchpy.device.device":[[11,1,1,"","checkModuleFormat"],[11,1,1,"","getQuarchDevice"],[11,2,1,"","quarchDevice"]],"quarchpy.device.device.quarchDevice":[[11,3,1,"","closeConnection"],[11,3,1,"","getRuntime"],[11,3,1,"","openConnection"],[11,3,1,"","resetDevice"],[11,3,1,"","sendAndVerifyCommand"],[11,3,1,"","sendBinaryCommand"],[11,3,1,"","sendCommand"]],"quarchpy.device.quarchArray":[[11,3,1,"","getSubDevice"],[11,1,1,"","isThisAnArrayController"],[11,2,1,"","quarchArray"],[11,3,1,"","scanSubModules"],[11,2,1,"","subDevice"]],"quarchpy.device.quarchArray.quarchArray":[[11,3,1,"","getSubDevice"],[11,3,1,"","scanSubModules"]],"quarchpy.device.quarchArray.subDevice":[[11,3,1,"","sendCommand"]],"quarchpy.device.quarchDevice":[[11,3,1,"","closeConnection"],[11,3,1,"","getRuntime"],[11,3,1,"","openConnection"],[11,3,1,"","resetDevice"],[11,3,1,"","sendAndVerifyCommand"],[11,3,1,"","sendBinaryCommand"],[11,3,1,"","sendCommand"]],"quarchpy.device.quarchPPM":[[11,2,1,"","quarchPPM"],[11,3,1,"","setupPowerOutput"],[11,3,1,"","startStream"],[11,3,1,"","stopStream"],[11,3,1,"","streamBufferStatus"],[11,3,1,"","streamInterrupt"],[11,3,1,"","streamResampleMode"],[11,3,1,"","streamRunningStatus"],[11,3,1,"","waitStop"]],"quarchpy.device.quarchPPM.quarchPPM":[[11,3,1,"","setupPowerOutput"],[11,3,1,"","startStream"],[11,3,1,"","stopStream"],[11,3,1,"","streamBufferStatus"],[11,3,1,"","streamInterrupt"],[11,3,1,"","streamResampleMode"],[11,3,1,"","streamRunningStatus"],[11,3,1,"","waitStop"]],"quarchpy.device.quarchQPS":[[11,1,1,"","current_milli_time"],[11,1,1,"","current_second_time"],[11,1,1,"","qpsNowStr"],[11,2,1,"","quarchQPS"],[11,2,1,"","quarchStream"],[11,3,1,"","startStream"]],"quarchpy.device.quarchQPS.quarchQPS":[[11,3,1,"","startStream"]],"quarchpy.device.quarchQPS.quarchStream":[[11,3,1,"","addAnnotation"],[11,3,1,"","addComment"],[11,3,1,"","addDataPoint"],[11,3,1,"","channels"],[11,3,1,"","createChannel"],[11,3,1,"","failCheck"],[11,3,1,"","get_custom_stats_range"],[11,3,1,"","get_stats"],[11,3,1,"","hideAllDefaultChannels"],[11,3,1,"","hideChannel"],[11,3,1,"","myChannels"],[11,3,1,"","saveCSV"],[11,3,1,"","showChannel"],[11,3,1,"","stats_to_CSV"],[11,3,1,"","stopStream"],[11,3,1,"","takeSnapshot"]],"quarchpy.device.quarchStream":[[11,3,1,"","addAnnotation"],[11,3,1,"","addComment"],[11,3,1,"","addDataPoint"],[11,3,1,"","channels"],[11,3,1,"","createChannel"],[11,3,1,"","failCheck"],[11,3,1,"","get_custom_stats_range"],[11,3,1,"","get_stats"],[11,3,1,"","hideAllDefaultChannels"],[11,3,1,"","hideChannel"],[11,3,1,"","myChannels"],[11,3,1,"","saveCSV"],[11,3,1,"","showChannel"],[11,3,1,"","stats_to_CSV"],[11,3,1,"","stopStream"],[11,3,1,"","takeSnapshot"]],"quarchpy.device.scanDevices":[[11,1,1,"","filter_module_type"],[11,1,1,"","getSerialNumberFromConnectionTarget"],[11,1,1,"","get_connection_target"],[11,1,1,"","get_user_level_serial_number"],[11,1,1,"","listDevices"],[11,1,1,"","list_USB"],[11,1,1,"","list_network"],[11,1,1,"","list_serial"],[11,1,1,"","lookupDevice"],[11,1,1,"","mergeDict"],[11,1,1,"","scanDevices"],[11,1,1,"","userSelectDevice"]],"quarchpy.device.subDevice":[[11,3,1,"","sendCommand"]],"quarchpy.disk_test":[[12,0,0,"-","AbsDiskFinder"],[12,0,0,"-","DiskTargetSelection"],[12,0,0,"-","iometerDiskFinder"]],"quarchpy.disk_test.AbsDiskFinder":[[12,2,1,"","AbsDiskFinder"]],"quarchpy.disk_test.AbsDiskFinder.AbsDiskFinder":[[12,3,1,"","findDevices"],[12,3,1,"","formatList"],[12,3,1,"","returnDisk"]],"quarchpy.disk_test.DiskTargetSelection":[[12,1,1,"","getDiskTargetSelection"]],"quarchpy.disk_test.iometerDiskFinder":[[12,2,1,"","iometerDiskFinder"]],"quarchpy.disk_test.iometerDiskFinder.iometerDiskFinder":[[12,3,1,"","findDevices"],[12,3,1,"","formatList"],[12,3,1,"","getAvailableDisks"],[12,3,1,"","getAvailableDrives"],[12,3,1,"","remove_values_from_list"],[12,3,1,"","returnDisk"]],"quarchpy.fio":[[13,0,0,"-","FIO_interface"],[13,1,1,"","runFIO"]],"quarchpy.fio.FIO_interface":[[13,1,1,"","adjustTime"],[13,1,1,"","follow"],[13,1,1,"","return_data"],[13,1,1,"","runFIO"],[13,1,1,"","start_fio"],[13,1,1,"","timeNow"]],"quarchpy.iometer":[[14,1,1,"","generateIcfFromConf"],[14,1,1,"","generateIcfFromCsvLineData"],[14,0,0,"-","iometerFuncs"],[14,1,1,"","processIometerInstResults"],[14,1,1,"","readIcfCsvLineData"],[14,1,1,"","runIOMeter"]],"quarchpy.iometer.iometerFuncs":[[14,1,1,"","followResultsFile"],[14,1,1,"","generateIcfFromConf"],[14,1,1,"","generateIcfFromCsvLineData"],[14,1,1,"","processIometerInstResults"],[14,1,1,"","readIcfCsvLineData"],[14,1,1,"","runIOMeter"]],"quarchpy.qis":[[15,1,1,"","closeQis"],[15,1,1,"","isQisRunning"],[15,0,0,"-","qisFuncs"],[15,1,1,"","startLocalQis"]],"quarchpy.qis.qisFuncs":[[15,1,1,"","GetQisModuleSelection"],[15,1,1,"","check_remote_qis"],[15,1,1,"","closeQis"],[15,1,1,"","isQisRunning"],[15,1,1,"","startLocalQis"]],"quarchpy.qps":[[16,1,1,"","GetQpsModuleSelection"],[16,1,1,"","closeQps"],[16,1,1,"","isQpsRunning"],[16,0,0,"-","qpsFuncs"],[16,4,1,"","qpsInterface"],[16,1,1,"","startLocalQps"],[16,1,1,"","toQpsTimeStamp"]],"quarchpy.qps.qpsFuncs":[[16,1,1,"","GetQpsModuleSelection"],[16,1,1,"","closeQps"],[16,1,1,"","isQpsRunning"],[16,1,1,"","legacyAdjustTime"],[16,1,1,"","startLocalQps"],[16,1,1,"","toQpsTimeStamp"]],"quarchpy.run":[[6,1,1,"","main"]],"quarchpy.user_interface":[[17,2,1,"","User_interface"],[17,1,1,"","displayTable"],[17,1,1,"","endTestBlock"],[17,1,1,"","get_check_valid_calPath"],[17,1,1,"","listSelection"],[17,1,1,"","logCalibrationResult"],[17,1,1,"","logSimpleResult"],[17,1,1,"","printText"],[17,1,1,"","progressBar"],[17,1,1,"","requestDialog"],[17,1,1,"","showDialog"],[17,1,1,"","startTestBlock"],[17,1,1,"","userRangeIntSelection"],[17,0,0,"-","user_interface"],[17,1,1,"","validateUserInput"]],"quarchpy.user_interface.User_interface":[[17,4,1,"","instance"]],"quarchpy.user_interface.user_interface":[[17,2,1,"","User_interface"],[17,1,1,"","dictToList"],[17,1,1,"","displayTable"],[17,1,1,"","endTestBlock"],[17,1,1,"","get_check_valid_calPath"],[17,1,1,"","is_user_admin"],[17,1,1,"","listSelection"],[17,1,1,"","logCalibrationResult"],[17,1,1,"","logResults"],[17,1,1,"","logSimpleResult"],[17,1,1,"","niceListSelection"],[17,1,1,"","printText"],[17,1,1,"","progressBar"],[17,1,1,"","quarchSleep"],[17,1,1,"","requestDialog"],[17,1,1,"","setup_logging"],[17,1,1,"","showDialog"],[17,1,1,"","startTestBlock"],[17,1,1,"","storeResult"],[17,1,1,"","userRangeIntSelection"],[17,1,1,"","validateUserInput"]],"quarchpy.user_interface.user_interface.User_interface":[[17,4,1,"","instance"]],"quarchpy.utilities":[[18,0,0,"-","TestCenter"]],"quarchpy.utilities.TestCenter":[[18,1,1,"","beginTestBlock"],[18,1,1,"","endTest"],[18,1,1,"","endTestBlock"],[18,1,1,"","setup"],[18,1,1,"","testPoint"]],quarchpy:[[8,0,0,"-","config_files"],[6,0,0,"-","connection"],[9,0,0,"-","connection_specific"],[10,0,0,"-","debug"],[11,0,0,"-","device"],[12,0,0,"-","disk_test"],[13,0,0,"-","fio"],[14,0,0,"-","iometer"],[15,0,0,"-","qis"],[16,0,0,"-","qps"],[6,0,0,"-","run"],[17,0,0,"-","user_interface"],[18,0,0,"-","utilities"]]},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:attribute"},terms:{"0":[1,9,11,15,16,18],"000000":11,"03":[0,3],"08":[0,3,12,14],"09":[0,3],"1":[1,9,11,15,16,17,18],"10":[1,9,11],"100":[11,17],"11":1,"12":[1,15],"123":9,"127":[9,15,16],"13":[1,12,14,16],"14":1,"15":1,"16":1,"1620817118182":16,"1620817126":16,"168":9,"17":[0,3],"18":1,"19":1,"192":9,"2":[1,2,15,19],"20":1,"2000":11,"2001":4,"2009":4,"2016":4,"2017":4,"2018":[4,12,14],"2020":4,"21":1,"22":1,"23":[0,3],"3":[1,2,4,17,19],"300":9,"4":1,"4096":9,"5":[1,11],"6":1,"7":[1,2,19],"8":[1,2,19],"9":1,"9722":[9,15],"9822":[9,16],"abstract":12,"boolean":[9,18],"case":[0,3,9],"char":[9,16],"class":[0,3,6,9,11,12,15,17],"default":[11,15],"do":11,"export":[0,3],"float":16,"function":[0,3,6,9,10,11,12,14,15,17,18],"import":[0,3],"int":[9,11,16],"new":[0,3,9],"return":[9,10,11,15,16,18],"switch":11,"true":[9,10,11,15,16,17],"while":[0,3],A:4,AND:[4,11],AS:4,BE:4,BUT:4,BY:4,By:15,FOR:4,IF:4,IN:4,IS:4,If:[9,10,11],In:18,NO:4,NOT:4,No:11,OF:4,ON:4,OR:4,SUCH:4,THE:4,TO:4,The:[0,3,4,9,11,17],With:[0,3,11],__init__:[0,3],__version__:[0,3],about:[0,3],abov:4,absolut:11,accept:[11,16],access:[0,3,10,17],ad:[0,3,11],add:11,addannot:11,addcom:11,adddatapoint:11,addit:[0,3,11,15],additionalopt:[9,11,16,17],address:[0,3,9,15],adjusttim:13,advis:4,after:[9,11],alia:16,align:17,all:[0,3,4,9,10,11,18],allign:[0,3],allow:[0,3,6,9,10,11,18],alreadi:9,also:[0,3],alwai:11,an:[0,3,9,10,11,15],andi:[12,14],ani:[0,3,4,11,18],annot:[0,3,11],annotationcolor:11,annotationgroup:11,annotationtim:11,annotationtyp:11,api:[0,2,3,18,19],app:15,appear:[0,3,9,11],applic:[2,6,19],ar:[0,3,4,9,10,11],architectur:[0,3],arg:[6,10,15,16],argstr:10,argument:[0,3,6,13],aris:4,around:[0,3],arrai:[0,3,11],ask:11,assum:16,attempt:11,author:[1,4],auto:[0,3],auto_upd:10,autom:[2,14,19],automat:[2,10,19],avail:[4,10,11],averagestrip:9,avgpwrtwo:9,avgstringfrompwr:9,b:[0,3],backend:9,base:[4,6,9,11,12,14,17,18],basedevic:11,baseunit:11,basic:[2,10,19],becom:[9,11],befor:9,beggin:9,begintestblock:18,being:4,belong:11,better:[0,3],betweencommanddelai:9,binari:4,bit:[0,3],block:[9,18],bool:[10,11,15],both:[0,3,17],bottom:11,bsd:4,buffer:9,bug:[0,3],bugfix:[0,3],build:10,bulkread:9,bulkreadep:9,bulkreadeptout:9,bulkreadn:9,busi:4,c:4,cabl:11,calibr:[0,3,5,6,17],calibration_class:[5,6],calibrationconfig:[5,6],calibrationutil:[5,6],call:[0,3,9,10,11],calpath:17,can:[0,3,9,11,15,17],card:11,carriag:11,caus:[4,9],center:[0,3],cento:[0,3],certain:[0,3],chang:1,changelog:1,channel:11,channelgroup:11,channelnam:11,channelspecifi:11,check:[0,3,10,15],check_if_upd:10,check_remote_qi:15,checkcomm:9,checkmoduleformat:11,chri:4,claus:4,clean:[0,3],clean_and_flush_stuck_usb_comm:9,cleaner:11,cliechti:4,close:[9,11,15],closeconnect:11,closeport:9,closeqi:15,closeqp:16,cmd:[9,11],co:[0,3],code:[0,2,3,4,11,19],color:11,comm:9,command:[0,3,6,9,10,11,15],command_nam:18,command_param:18,command_respons:11,commandstr:11,comment:[0,3],commentcolor:11,commenttim:11,common:17,commun:[0,2,3,18,19],compar:[0,3,10],comparison:[0,3],compat:[0,3,10],complet:11,condit:4,conf:11,config:11,config_fil:[5,6],configpars:[5,6],confpath:14,connect:[0,2,3,5,9,10,11,15,18,19],connection_prefer:11,connection_qi:[5,6],connection_qp:[0,3,5,6,16],connection_rest:[5,6],connection_seri:[5,6],connection_specif:[0,3,5,6,16],connection_tcp:[5,6],connection_telnet:[5,6],connection_usb:[5,6],connectionmessag:9,connectiontarget:11,conntarget:9,consequenti:4,constr:[6,11],contain:[0,3,9,12,14,15],content:5,context:9,continu:15,contract:4,contributor:4,control:[0,3,11],contyp:11,convert:[0,3],convertstreamaverag:9,copyright:4,core:[0,3,11],costa:4,cr:11,creat:[0,3,11],createchannel:11,creation:11,csv:11,csvdata:14,csvfilelin:14,csvfilenam:14,current:[],current_milli_tim:11,current_second_tim:11,currenti:10,custom:[0,3,11],damag:4,data:[4,9,10],datafram:11,datapointtim:11,datavalu:11,datetim:16,daysdhour:11,debug:[0,3,5,6],debug_info:[0,2,3,19],debugdump:9,debugpr:11,debuprint:11,decim:17,defaultuserinput:17,delimit:11,deprec:15,deriv:4,describ:18,descript:[0,3],design:[0,3],desir:17,desiredtyp:17,detect:[0,3],dev:10,develop:[2,19],devic:[0,3,5,6,9,10],device1:10,devicedictsetup:9,devicehelp:[5,6],devicelist:12,devicemulti:9,df:11,dicttolist:17,did:11,didn:[0,3],direct:[4,10],directori:11,disclaim:4,disconnect:9,disk:[0,3,12],displayt:17,dispons:18,distribut:4,dll:[0,3],document:[0,3,4],doe:11,don:9,down:10,drive:[0,3,11],driveinfo:14,driver:[0,2,3,19],each:18,easi:[0,3],effect:18,eg:9,element:17,embed:6,empti:11,enabl:4,end:[9,11,18],end_tim:11,endors:4,endtest:18,endtestblock:[17,18],ensur:[10,12,17],enter:17,enumer:[0,3,11],environ:15,ep:9,error:[0,3,18],even:4,event:4,exampl:[2,10,19],except:11,exectu:10,execut:[11,15,17,18],exemplari:4,exist:10,expect:11,expectedrespons:[9,11],express:4,extratext:11,f:9,fail:9,failcheck:11,fals:[9,10,11,15,17],favouriteonli:[9,11,16],featur:[0,3,10],fedora:[0,3],fetchcmdrepli:9,fetchcmdreplytout:9,ffffff:11,field:[0,3],file:[0,3,8,11],file_nam:[11,13],filemaxmb:[9,11],filenam:[9,11,13,14],filepath:11,fill:17,filllin:17,filter:11,filter_module_typ:11,filterstr:11,finddevic:12,finish:[9,11],fio:[0,3,5,6],fio_interfac:[5,6],fiocallback:13,fiodiskfind:[5,6],first:[12,14],fit:4,fix:[0,3],fix_usb:10,fixtur:11,flag:[0,3,18],flush:9,folder:[0,3],follow:[4,11,13],followresultsfil:14,form:[4,10,18],format:[0,3,6,11],formatlist:12,found:[11,15],found_devic:11,founddevic:9,free:[4,11],from:[0,3,4,6,9,10,11,12,14,18],full:[0,3,9,11],fullwidth:17,fx:[2,19],gener:[0,3,15,18],generateicffromconf:14,generateicffromcsvlinedata:14,get:1,get_check_valid_calpath:17,get_config_path_for_modul:8,get_connection_target:11,get_custom_stats_rang:11,get_java_loc:10,get_qis_vers:10,get_quarchpy_vers:10,get_stat:11,get_user_level_serial_numb:11,getavailabledisk:12,getavailabledr:12,getdevicelist:9,getdisktargetselect:12,getextendedinfo:9,getidn:9,getlasterror:9,getqismoduleselect:[9,15],getqpsmoduleselect:16,getquarchdevic:[0,3,11],getquarchpyvers:[],getruntim:11,getserialnumb:9,getserialnumberfromconnectiontarget:11,getstreamxmlhead:9,getsubdevic:11,getusbdeviceserialno:9,give:11,given:[10,11],gmx:4,gone:[0,3],good:4,graphic:15,grid:11,group:11,groupnam:11,ha:[2,18,19],halt:[2,11,19],handl:11,have:[0,3],hd:[0,3],hdpowermodul:[5,6],header:[0,3],headertext:9,headless:[0,3,15],held:18,help:[0,3,9,11,12],helper:15,here:4,hex:11,hidealldefaultchannel:11,hidechannel:11,high:11,histori:[12,14],hit:15,holder:4,host:[6,9,15,16],hostdriv:12,how:11,howev:4,http:4,icffilepath:14,identif:10,identifi:4,idn_str:8,ignor:11,implement:[0,3,18],impli:4,importusb:9,improv:[0,3,18],incident:4,includ:[0,2,3,4,11,18,19],include_conn_typ:11,index:1,indexreq:17,indirect:4,info:[0,3],inform:[4,11],initi:[0,3,12,14],input:[0,3],inputstr:17,instal:[0,1,3,10,12],instanc:[9,15,17],instead:15,instrument:[0,3],integ:11,integr:[0,3],interac:17,interact:[0,3,17],interfac:[0,3,9,17,18],interface_nam:18,interfacenam:18,intern:[17,18],interrupt:4,interruptlist:9,intlength:17,involv:[0,3],ioment:[0,3],iomet:[0,3,5,6,12],iometerfunc:[5,6],ip:[0,3,9,15],ipaddress:9,ipaddresslookup:11,is_run:15,is_user_admin:17,isportopen:9,isqisrun:[0,3,9,15],isqpsrun:16,issu:[0,3,11],isthisanarraycontrol:11,isxmlhead:9,iter:[17,18],its:[4,10],java:[0,2,3,10,19],just:11,keepqisrun:16,keithley_2460_control:[5,6],kwarg:17,l:17,lairson:4,lan:[0,2,3,19],lan_modul:11,lantimeout:11,latest:[0,2,3,19],launch:[0,3],layer:18,leao:[12,14],left:[9,11],leftov:9,legaci:[0,3],legacyadjusttim:16,level:[0,3],lf:11,liabil:4,liabl:4,librari:[2,4,18,19],licens:[0,1,3],liechti:4,like:[9,11],limit:4,line:[6,10,11,15],linesperfil:11,linux:[0,3],list:[0,3,4,11,15,18],list_driv:[0,3],list_network:11,list_seri:11,list_usb:11,listdevic:[0,3,11],listselect:17,liter:[0,3],live:11,load:[0,3],local:[0,3,10,15],localhost:15,locat:[0,3,10,11],lock:[0,3],lockusbstr:9,log:1,logcalibrationresult:17,loglevel:17,logresult:17,logsimpleresult:17,longer:[0,3],look:9,lookupdevic:11,loss:4,low:[0,3],ltd:[2,4,19],m:[0,2,3,6,19],machin:4,mai:[0,3,4],main:[6,10],major:[0,3],make:[0,3],managernam:14,manual:11,marker:11,match:11,materi:4,maxrang:17,md:[0,3],mdn:[2,19],merchant:4,mergedict:11,messag:[0,3,9,11,17,18],message_text:18,met:[4,10],method:11,millisecond:[11,16],minimum:10,minor:[0,3],minrang:17,minut:11,mismatch:11,mode:[13,15],model:[0,3],modif:4,modifi:4,modul:[0,1,2,3,5,19],module_connect:8,module_str:11,module_type_filt:11,modulestr:11,most:[2,11,19],ms:16,multilin:11,multipl:[0,3,18],must:4,mychannel:11,mysocket:11,mystream:[13,14],n:9,name:[4,11,18],need:[0,3,9],neglig:4,neither:4,nest:18,net:4,network:9,network_modul:11,newdirectori:11,newstrip:9,next:11,nice:[11,17],nicelistselect:17,non:15,none:[8,9,10,11,15,17],nor:4,normal:9,norri:[12,14],note:[2,17,18,19],notic:4,now:[0,3],number:[10,11],numstrip:9,oars:[0,3],object:[0,3,6,9,11,12,17,18],off:[0,3],ok:11,older:[2,19],one:[9,10],onli:[0,2,3,6,18,19],onlin:[0,3],onto:18,open:[0,3,9,10,11],openconnect:11,openport:9,option:[0,2,3,6,9,10,11,13,15,19],order:18,org:4,originobj:11,os:[0,3],other:[4,11,15],otherwis:[4,10,11],ou:11,out:[4,9,11],output_fil:13,outsid:[0,3],over:[0,3,11],overridden:11,own:[0,3],p:13,pack:[0,3],packag:[0,1,2,3,5,19],package_list:10,page:1,pam:[0,3,11],panda:11,param:9,paramet:[9,10,11,15,16,18],pars:6,parse_config_fil:8,parser:[0,3,18],part:[0,3],particular:4,pass:[11,16,18],path:[0,3,11,17],pattern:17,pedro:[12,14],per:11,percetang:11,perform:[0,3,9],permiss:4,permit:4,pip:[0,2,3,10,19],pkg_resourc:[0,3],place:11,platform:[0,3],plot:11,point:18,port:[0,3,6,9,11,15,16],possibl:[4,9],potenti:[0,3],power:[0,3,11],powermodulecalibr:[5,6],ppm:[0,3],practic:[0,3],prefix:17,prepar:10,prerequisit:[0,1,3],present:10,prevent:10,previou:[9,10],primari:11,print:[0,3,10,15],printtext:17,printtoconsol:17,prior:4,problem:[0,3],process:[4,15,18],processiometerinstresult:14,procur:4,product:[4,11],profit:4,progressbar:17,project:[0,3],promot:4,prompt:[0,3,10],provid:[0,3,4,10,17],purpos:[4,12],py:11,pyconnect:6,pypi:[0,3],pyseri:1,python2:[0,3],python:[0,2,3,6,18,19],pyusb:1,pywin32:12,qc:[0,2,3,19],qi:[0,2,3,5,6,9,10,19],qis_scan_devic:9,qisconnect:[6,9,15],qisfunc:[5,6,9],qisinterfac:[0,3,9,15],qp:[0,2,3,5,6,9,10,11,19],qps1:[0,3],qpsconnect:[6,9,16],qpsfunc:[5,6],qpsinterfac:[9,16],qpsnowstr:11,qtl2347:[5,6],quarch:[0,2,3,4,9,10,11,14,17,18,19],quarcharrai:[5,6],quarchdevic:[0,3,10,11],quarchpc3:14,quarchppm:[0,3,5,6],quarchqp:[5,6],quarchsimpleidentifi:10,quarchsleep:17,quarchstream:11,quickli:9,qurchpi:[0,3],rais:11,ran:9,rang:11,rather:[0,3],re:11,read:9,readabl:18,readi:[0,3],readicfcsvlinedata:14,readm:[0,1,3],readuntilcursor:9,recent:11,recommend:[2,19],reconnect:11,recov:11,recv:9,redistribut:4,relat:[2,18,19],releaseondata:[9,11],remainingstrip:9,remot:[0,3,15],remov:[0,3],remove_values_from_list:12,replac:[0,3],report:[0,3,17,18],repositori:[0,3],represent:10,reproduc:4,request:10,requestdialog:17,requir:[2,10,11,19],requiredquarchpyvers:10,requiredvers:10,resampl:[0,3],reserv:4,reset:11,resetdevic:11,resourc:18,respond:15,respons:[0,3,9,11],responseexpect:11,restconn:9,restructur:[0,3],result:[11,17,18],retain:4,return_data:13,returndisk:12,rev:[0,3],rework:[0,3],right:4,rule:[0,3],run:[0,2,3,5,9,10,15,18,19],runcommand:9,runfio:13,runiomet:14,runtim:11,rxbyte:9,safe_to_run:10,sai:9,sampl:[2,11,19],save:[11,17],savecsv:11,scan:[0,2,3,9,15,16,19],scan_devic:11,scan_dictionari:11,scandevic:[5,6],scandictionari:11,scanfilterstr:11,scaninarrai:11,scanip:9,scansubmodul:11,screen:11,script:[0,3,10,11,18],seamlessli:[0,3],search:[0,1,3],second:[11,16],select:[0,3,11,12,15],selectionlist:17,send:[9,11],sendandreceivecmd:9,sendandreceivetext:9,sendandverifycommand:11,sendbinarycommand:11,sendcmd:9,sendcmdverbos:9,sendcommand:[9,11],sendtext:9,sensit:[0,3],sent:9,senttext:9,separ:[0,3,9,11],seper:[0,3,11],serial:[0,2,3,19],serial_read_until:9,serialconn:9,serid:9,server:[0,3],servic:4,set:[0,3,9,11,15,18],settimeout:9,setup:18,setup_log:17,setup_respons:18,setuppoweroutput:11,shall:4,shinx:[0,3],should:[9,11,15],showchannel:11,showdialog:17,shown:[15,18],shut:10,shutdown:10,signific:[0,3],simpl:[0,2,3,11,18,19],simpli:[0,3],sinc:[0,3,15],singl:[0,3],singleton:17,skip:[0,3],skipstatuscheck:9,sleep:9,sleeplength:17,smart:[0,3],snapshot:[0,3,11],sock:9,socket:9,softwar:4,some:11,sortfavourit:9,sourc:[0,3,4],space:[0,3],spdx:4,spec:18,special:4,specif:[0,3,4,6,9,11],specifi:[0,3,9,10,11,15],stack:11,standard:[2,17,18,19],start:[1,11,15,18],start_fio:13,start_tim:11,startlocalqi:[0,3,15],startlocalqp:16,startstream:[9,11],startstreamthread:9,starttestblock:17,startup:15,stat:[0,3,11],statement:[0,3],statist:11,stats_to_csv:11,stdin:18,stdout:18,sting:11,stop:[11,15],stopstream:[9,11],storeresult:17,str:[9,10,11,15,18],stream:[0,3,11],streamaverag:[9,11],streambufferstatu:[9,11],streamcom:11,streamdata:11,streamgetstripestext:9,streamheaderaverag:9,streamheaderformat:9,streamheadervers:9,streaminterrupt:[9,11],streamnam:[9,11],streamresamplemod:11,streamrunningstatu:[9,11],strict:4,string:[0,3,9,10,11,18],structur:[0,3],stub:[0,3],stuck:9,studio:[0,3],style:17,sub:[0,3,11],subdevic:11,submodul:5,subnet:[0,3],subpackag:5,substitut:4,success:[9,11,18],successfulli:11,suffix:17,suppli:15,support:[0,3,10,17],switchbox:[0,3],syntax:[0,3],system:[10,15],systemtest:[0,3,5,6],systentest:[0,3],t:[0,3,9],tab:[0,3],tabledata:17,tablehead:17,take:11,takesnapshot:11,talk:[0,3,9],target:12,target_conn:11,targetdevic:9,tcp:[0,3],tcpconn:9,technic:11,technolog:[2,4,19],telnetconn:9,termin:[0,3,10,11,15,17,18],terminalwidth:17,test:[0,2,3,10,11,17,18,19],test_commun:10,test_respons:18,test_system_info:10,testcent:[5,6,17],testnam:[14,18],testpoint:18,text:[11,17],than:[0,3,15],the_list:12,thefil:[13,14],thei:[0,3,10],theori:4,thi:[0,2,3,4,6,9,10,11,12,14,15,17,18,19],through:[0,3],thrown:11,tidi:[0,3],time:[0,3,11,16],timenow:13,timeout:[0,3,9,11,15,16],timestamp:[13,16],titl:[11,17],titlecolor:11,tl:[0,3],too:9,tool:[2,14,19],top:11,toqpstimestamp:16,tort:4,total:17,tquarchusb_if:9,trace:11,tri:9,trigger:[9,11],txt:11,type:[0,3,10,11,15,18],ubuntu:[0,3],udp:[0,3],ui:[0,3,17],unabl:9,underli:11,unit:[0,3],unlockusbstr:9,until:[9,11,15],up:[0,3,11,18],upcom:[0,3],updat:[0,3,10],updateperiod:17,updatequarchpi:10,upgrad:[2,10,19],upgrade_quarchpi:[5,6],uptim:[0,3],us:[0,2,3,4,6,9,10,11,12,14,15,18,19],usb:[0,2,3,9,19],usbconn:9,usbfix:[0,3],useprefix:11,user:[0,3,15,17,18],user_data:13,user_interfac:[5,6],usercallback:14,userrangeintselect:17,userselectdevic:11,userstr:17,util:[0,3,5,6],v1:[0,3],val:12,valid:[0,3,16],validateuserinput:17,valu:[0,3,11,15,16],valueerror:11,vari:18,variabl:9,variou:[0,3],verbosesendcmd:9,verifi:11,version:[0,2,3,9,10,12,14,15,19],versioncompar:[5,6],versionnumb:10,via:[0,2,3,19],view:11,wa:[0,3,11],wai:[0,3,4,11],wait:[0,3,11],waitstop:[9,11],wander:4,want:[0,3,9],warn:[0,3,9],warranti:4,we:11,welcom:9,when:[0,3,9,11],where:[0,3],whern:11,whether:[4,11],which:[0,3,9,11],white:[0,3],wide:11,window:[0,3],wire:[0,3],within:[0,3,10,15],without:[0,3,4],wmi:[0,3,12],work:[0,2,3,10,12,14,19],worri:[0,3],would:[9,11],wrapper:[0,3,11],write:11,writezeropacketcmd:9,written:4,x00:9,x01:9,x02:9,x03:9,x04:9,x6:[0,3],x:[2,11,19],xx:11,xxxdxx:11,xxxx:11,y:11,you:[0,3,9,11],your:[0,3],ypo:11,zeroconf:[2,19]},titles:["Changelog (Quarchpy)","Welcome to quarchpy\u2019s documentation!","Quarchpy - Readme","Changelog (Quarchpy)","LICENSES","quarchpy","quarchpy package","quarchpy.calibration package","quarchpy.config_files package","quarchpy.connection_specific package","quarchpy.debug package","quarchpy.device package","quarchpy.disk_test package","quarchpy.fio package","quarchpy.iometer package","quarchpy.qis package","quarchpy.qps package","quarchpy.user_interface package","quarchpy.utilities package","Quarchpy - Readme"],titleterms:{"0":[0,3],"1":[0,3],"10":[0,3],"11":[0,3],"12":[0,3],"13":[0,3],"14":[0,3],"15":[0,3],"16":[0,3],"18":[0,3],"19":[0,3],"2":[0,3],"20":[0,3],"21":[0,3],"22":[0,3],"3":[0,3],"4":[0,3],"5":[0,3],"6":[0,3],"7":[0,3],"8":[0,3],"9":[0,3],absdiskfind:12,author:[2,19],calibr:7,calibration_class:7,calibrationconfig:7,calibrationutil:7,chang:[0,3],changelog:[0,3],config_fil:8,configpars:8,connect:6,connection_qi:9,connection_qp:9,connection_rest:9,connection_seri:9,connection_specif:9,connection_tcp:9,connection_telnet:9,connection_usb:9,content:[1,6,7,8,9,10,11,12,13,14,15,16,17,18],debug:10,devic:11,devicehelp:7,disk_test:12,disktargetselect:12,document:1,drivetestconfig:12,drivetestcor:12,dtscomm:12,dtsglobal:12,fio:13,fio_interfac:13,fiodiskfind:13,get:[2,19],hdpowermodul:7,hostinform:12,hotplugtest:12,indic:1,instal:[2,19],iomet:14,iometerdiskfind:12,iometerfunc:14,keithley_2460_control:7,licens:4,log:[0,3],lspci:12,modul:[6,7,8,9,10,11,12,13,14,15,16,17,18],packag:[4,6,7,8,9,10,11,12,13,14,15,16,17,18],powermodulecalibr:7,powertest:12,prerequisit:[2,19],pyseri:4,pyusb:4,qi:15,qisfunc:15,qp:16,qpsfunc:16,qtl2347:7,quarcharrai:11,quarchpi:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19],quarchppm:11,quarchqp:11,readm:[2,19],run:6,s:1,sasfunc:12,scandevic:11,start:[2,19],submodul:[6,7,8,9,10,11,12,13,14,15,16,17,18],subpackag:[6,9],systemtest:10,tabl:1,testcent:18,testlin:12,upgrade_quarchpi:10,user_interfac:17,usertestexampl:12,util:18,versioncompar:10,welcom:1}})