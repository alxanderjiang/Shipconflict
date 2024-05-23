import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from all_data_process import time2epoch,Process1,getships,wgs84_to_gcj02,conflict_process,prove_distances,get_Dbscan_Groups,get_groups,get_Grouprisk,getarea,csvread,get_Grouprisk_simple

# 主窗口类
class Ui_mainWindow(object):
    
    # ui构造函数
    def setupUi(self, mainWindow):
        
        # 主窗口定义
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1300, 800)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # “实时展示”按钮定义
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1090, 180, 160, 50))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        
        # “实时展示”勾选框定义
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(870, 190, 160, 30))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        
        # “冲突侦测”勾选框定义
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(870, 270, 160, 30))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        
        # "冲突侦测"按纽定义
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1090, 260, 160, 50))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        
        # “动态簇划分”勾选框定义
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(870, 110, 160, 30))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setObjectName("checkBox_3")
        
        # “动态簇划分”按钮定义
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(1090, 100, 160, 50))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        
        # “15min“勾选框定义
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(230, 620, 100, 20))
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setCheckable(True)
        self.checkBox_4.setChecked(False)
        self.checkBox_4.setTristate(False)
        self.checkBox_4.setObjectName("checkBox_4")
        
        # “30min”勾选框定义
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setGeometry(QtCore.QRect(340, 620, 100, 20))
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.checkBox_5.setFont(font)
        self.checkBox_5.setObjectName("checkBox_5")
        
        # “45min”勾选框定义
        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setGeometry(QtCore.QRect(450, 620, 100, 20))
        font = QtGui.QFont()
        font.setPixelSize(20)
        self.checkBox_6.setFont(font)
        self.checkBox_6.setObjectName("checkBox_6")
        
        # “自定义”时间编辑器
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(670, 620, 90, 25))
        self.timeEdit.setObjectName("timeEdit")
        
        # 各文字标签
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 610, 170, 40))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(580, 620, 100, 25))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 670, 191, 31))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        
        # 经纬度范围设置浮点数据编辑器
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(330, 670, 81, 31))
        self.doubleSpinBox.setMinimum(-180.0)
        self.doubleSpinBox.setMaximum(180.0)
        self.doubleSpinBox.setProperty("value", 121.8)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(580, 670, 81, 31))
        self.doubleSpinBox_2.setMinimum(-90.0)
        self.doubleSpinBox_2.setMaximum(90.0)
        self.doubleSpinBox_2.setProperty("value", 29.7)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        
        # 标称文字标签
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(260, 670, 61, 31))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.label_4.setFont(font)
        self.label_4.setIndent(-1)
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(510, 670, 61, 31))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.label_6.setFont(font)
        self.label_6.setIndent(-1)
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 100, 701, 451))
        font = QtGui.QFont()
        font.setPixelSize(14)
        
        # 静态地图显示标签区
        self.label_5.setFont(font)
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("主界面底图.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setWordWrap(False)
        self.label_5.setObjectName("label_5")
        
        # 自定义时间编辑器
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_3.setGeometry(QtCore.QRect(420, 670, 81, 31))
        self.doubleSpinBox_3.setMinimum(-180.0)
        self.doubleSpinBox_3.setMaximum(180.0)
        self.doubleSpinBox_3.setProperty("value", 123.0)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_4.setGeometry(QtCore.QRect(680, 670, 81, 31))
        self.doubleSpinBox_4.setMinimum(-90.0)
        self.doubleSpinBox_4.setMaximum(90.0)
        self.doubleSpinBox_4.setProperty("value", 30.0)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        
        # 标称文字标签
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(870, 320, 381, 51))
        font = QtGui.QFont()
        font.setPixelSize(24)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(100, 10, 870, 70))
        font = QtGui.QFont()
        font.setPixelSize(48)
        font.setBold(False)
        font.setWeight(48)
        font.setKerning(True)
        self.label_8.setFont(font)
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setAutoFillBackground(False)
        self.label_8.setObjectName("label_8")
        
        # 计算结果区表格定义
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(870, 380, 381, 321))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        
        # 主界面中央布局设置
        mainWindow.setCentralWidget(self.centralwidget)
        
        # 主界面菜单设置
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1297, 30))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.menu_5 = QtWidgets.QMenu(self.menu_4)
        self.menu_5.setTabletTracking(True)
        self.menu_5.setObjectName("menu_5")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.action1 = QtWidgets.QAction(mainWindow)
        self.action1.setObjectName("action1")
        self.action2 = QtWidgets.QAction(mainWindow)
        self.action2.setObjectName("action2")
        self.action1_2 = QtWidgets.QAction(mainWindow)
        self.action1_2.setObjectName("action1_2")
        self.action1_3 = QtWidgets.QAction(mainWindow)
        self.action1_3.setObjectName("action1_3")
        self.action2_2 = QtWidgets.QAction(mainWindow)
        self.action2_2.setObjectName("action2_2")
        self.action_15min = QtWidgets.QAction(mainWindow)
        self.action_15min.setObjectName("action_15min")
        self.action_30min = QtWidgets.QAction(mainWindow)
        self.action_30min.setObjectName("action_30min")
        self.action_45min = QtWidgets.QAction(mainWindow)
        self.action_45min.setObjectName("action_45min")
        self.action3 = QtWidgets.QAction(mainWindow)
        self.action3.setObjectName("action3")
        self.dbscanparms=QtWidgets.QAction(mainWindow)
        self.dbscanparms.setText("聚类参数")
        self.menu_2.addAction(self.action1)
        self.menu_2.addAction(self.action2_2)
        self.menu_3.addAction(self.action_15min)
        self.menu_3.addAction(self.action_30min)
        self.menu_3.addAction(self.action_45min)
        self.menu_3.addAction(self.action3)
        self.menu_5.addAction(self.action1_2)
        self.menu_5.addAction(self.action1_3)
        self.menu_4.addAction(self.action2)
        self.menu_4.addAction(self.menu_5.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menu_5.addAction(self.dbscanparms)
        
        # 槽函数,聚类参数手动设置
        self.dbscanparms.triggered.connect(self.get_dbscanparms)
        
        # 槽函数,文件选择
        self.action1.triggered.connect(self.fileselect)
        # 百度地图显示
        self.mapshow=QWebEngineView(self.centralwidget)
        self.mapshow.setGeometry(QtCore.QRect(50, 100, 800, 500))
        url=os.getcwd()+"/Baidumap.html"
        self.mapshow.load(QtCore.QUrl.fromLocalFile(url))
        self.mapshow.setZoomFactor(1.5)
        # 数码显示时间函数
        self.timeshow=QtWidgets.QLCDNumber(self.centralwidget)
        self.timeshow.setFixedSize(400,50)
        self.timeshow.move(850,20)
        self.timeshow.setDigitCount(20)
        self.timeshow.display("{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(1970,1,1,0,0,0))
        # 地图重置
        self.mapresetbt=QtWidgets.QPushButton("地图重置",self.centralwidget)
        self.mapresetbt.setFixedSize(100,30)
        self.mapresetbt.move(750,570)
        self.mapresetbt.clicked.connect(self.resetmap)
        
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
        
        #各按钮槽函数 
        self.pushButton.clicked.connect(self.show_conflictdetect)
        self.pushButton_2.clicked.connect(self.show_group)
        self.pushButton_3.clicked.connect(self.show_realtime)
        
    # 聚类参数设置槽函数
    def get_dbscanparms(self):
        global dbs_eps
        global dbs_minsample
        try:
            dbs_eps,ok=QtWidgets.QInputDialog.getInt(self.centralwidget,"参数输入","聚类半径",dbs_eps)
        except:
            dbs_eps,ok=QtWidgets.QInputDialog.getInt(self.centralwidget,"参数输入","聚类半径",3000)
        try:
            dbs_minsample,ok=QtWidgets.QInputDialog.getInt(self.centralwidget,"请输入核心船舶数量","核心船舶数量",dbs_minsample)
        except:
            dbs_minsample,ok=QtWidgets.QInputDialog.getInt(self.centralwidget,"请输入核心船舶数量","核心船舶数量",2)
    
    # 数据文件选择槽函数
    def fileselect(self):
        global filename
        currPath=os.getcwd().replace('\\','/')
        filename,filetype=QtWidgets.QFileDialog.getOpenFileName(self.centralwidget,"选择数据文件(csv)", currPath, "csv文件 (*.csv)")
    
    # 地图重置
    def resetmap(self):
        self.mapshow.page().runJavaScript("map.centerAndZoom(new BMapGL.Point(122.1, 29.9), 11);")
    
    # 动态群组划分槽函数
    def show_group(self):
        # 数据源确认
        try:
            print(filename)
        except:
            QtWidgets.QMessageBox.critical(self.centralwidget,"文件错误","请在数据源中选取正确的数据文件")
            return
        
        try:            
            # 检验冲突变量是否存在
            print(count)
            QtWidgets.QMessageBox.information(self.centralwidget,"动态簇划分","点击OK开始划分动态簇")
            # 数据准备
            AIS=Process1(filename)
            ships=getships(AIS)
            # 距离度量矩阵
            allDists=prove_distances(ships,posb)
            # 动态群组划分结果
            try:
                pre=get_Dbscan_Groups(len_ships=len(ships),eps=dbs_eps,min_samples=dbs_minsample,allDists=allDists)
            except:
                pre=get_Dbscan_Groups(len_ships=len(ships),eps=3000,min_samples=2,allDists=allDists)
            # 清空地图图标
            self.mapshow.page().runJavaScript("clearmap();")
            # 分色数组(CSS样式表内置)
            colors=["red","olive","black","blue","green","purple","yellow","maroon","navy","fuchsia"]
            # 分簇风险计算与区域绘制
            groups=get_groups(pre)
            for i in range(len(groups)):
                #Si,risk=get_Grouprisk(groups[i],posb,posbmax)
                Si,risk=get_Grouprisk_simple(groups[i],posb,posbmax)
                print("簇{}风险计算完成".format(i))
                print(Si)
                areas,mmsilist=getarea(ships,groups[i])
                self.mapshow.page().runJavaScript("drawgroups({},{},{},{},{},\"{}\");".format(i,Si,risk,areas,mmsilist,colors[i%10]))            
                print("分组划分完成")
            # 绘制分色图标
            for i in range(len(ships)):
                [lon,lat]=wgs84_to_gcj02(ships[i]["lng"],lat=ships[i]["lat"])
                theta=ships[i]["cog"]
                props=list(ships[i].values())
                props.append(posbmax[i])#冲突概率添加到属性列表
                conflict_cp=[]
                for j in range(len(ships)):
                    if(posb[i][j]>0):
                        conflict_cp.append("{},".format(ships[j]["MMSI"]))
                props.append(conflict_cp)#冲突连接船舶对添加到属性列表
                if(pre[i]==-1):
                    cmd="drawship_conflict([{},{}],{},{},\"grey\");".format(lon,lat,theta,props)
                else:
                    cmd="drawship_conflict([{},{}],{},{},\"{}\");".format(lon,lat,theta,props,colors[pre[i]%10])
                self.mapshow.page().runJavaScript(cmd)
                
            # table重绘,添加簇相关内容
            self.tableWidget.setColumnCount(9)
            self.tableWidget.setRowCount(len(sortindex))
            self.tableWidget.setHorizontalHeaderLabels(['簇编号','冲突概率','MMSI','经度','纬度','对地航速','船长','船宽','航向'])
            for i in range(len(sortindex)):
                numi=0
                for j in range(len(groups)):
                    if sortindex[i] in groups[j]:
                        numi=j
                        break
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem( '{}'.format(numi) ) )
                self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem( '{:.2f}'.format(posbmax[sortindex[i]]) ) )
                self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["MMSI"]) ) )
                self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["lng"]) ) )
                self.tableWidget.setItem(i,4,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["lat"]) ) )
                self.tableWidget.setItem(i,5,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["sog"]) ) )
                self.tableWidget.setItem(i,6,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["length"]) ) )
                self.tableWidget.setItem(i,7,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["width"]) ) )
                self.tableWidget.setItem(i,8,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["cog"]) ) )
            self.tableWidget.verticalHeader().sectionClicked.connect(self.rowselect)
            self.tableWidget.cellClicked.connect(self.groupselect)
            
            QtWidgets.QMessageBox.information(self.centralwidget,"动态簇划分","划分完成")
        except NameError:
            QtWidgets.QMessageBox.critical(self.centralwidget,"错误","冲突概率未计算")

    # 冲突侦测槽函数
    def show_conflictdetect(self):
        # 数据源确认
        try:
            print(filename)
        except:
            QtWidgets.QMessageBox.critical(self.centralwidget,"文件错误","请在数据源中选取正确的数据文件")
            return
        
        self.msg=QtWidgets.QMessageBox.information(self.centralwidget,"冲突侦测","点击OK开始计算船间冲突概率")
        # 数据准备
        AIS=Process1(filename)
        ships=getships(AIS)
        
        # 冲突计算
        global count,posb,posbmax,sortindex
        count,posb,posbmax,sortindex=conflict_process(ships)
        
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(len(sortindex))
        self.tableWidget.setHorizontalHeaderLabels(['冲突概率','MMSI','经度','纬度','对地航速','船长','船宽','航向'])
        # 首先清空地图标记
        self.mapshow.page().runJavaScript("clearmap();")
        for i in range(len(ships)):
            [lon,lat]=wgs84_to_gcj02(ships[i]["lng"],lat=ships[i]["lat"])
            theta=ships[i]["cog"]
            props=list(ships[i].values())
            props.append(posbmax[i])#冲突概率添加到属性列表
            conflict_cp=[]
            for j in range(len(ships)):
                if(posb[i][j]>0):
                    conflict_cp.append("{},".format(ships[j]["MMSI"]))
            props.append(conflict_cp)#冲突连接船舶对添加到属性列表
            if(posbmax[i]>0.5):
                cmd="drawship_conflict([{},{}],{},{},\"red\");".format(lon,lat,theta,props)
            elif(posbmax[i]<=0.5 and posbmax[i]>0):
                cmd="drawship_conflict([{},{}],{},{},\"rgba(255,128,0,0.3\");".format(lon,lat,theta,props)
            else:
                cmd="drawship_conflict([{},{}],{},{},\"blue\");".format(lon,lat,theta,props)
            self.mapshow.page().runJavaScript(cmd)
        for i in range(len(sortindex)):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem( '{:.2f}'.format(posbmax[sortindex[i]]) ) )
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["MMSI"]) ) )
            self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["lng"]) ) )
            self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["lat"]) ) )
            self.tableWidget.setItem(i,4,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["sog"]) ) )
            self.tableWidget.setItem(i,5,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["length"]) ) )
            self.tableWidget.setItem(i,6,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["width"]) ) )
            self.tableWidget.setItem(i,7,QtWidgets.QTableWidgetItem( str(ships[sortindex[i]]["cog"]) ) )
        self.tableWidget.verticalHeader().sectionClicked.connect(self.rowselect)
        # self.label_5.setPixmap(QtGui.QPixmap("冲突侦测.png"))
        # self.msg.close()
        QtWidgets.QMessageBox.information(self.centralwidget,"冲突侦测","冲突概率计算完成")
    
    # 实时展示槽函数
    def show_realtime(self):
        
        # 数据源确认
        try:
            print(filename)
        except:
            QtWidgets.QMessageBox.critical(self.centralwidget,"文件错误","请在数据源中选取正确的数据文件")
            return
        
        # 数据准备
        AIS=Process1(filename)
        # AIS=csvread(filename)
        timestamp=AIS["timestamp"][2]
        self.timeshow.display(time2epoch(timestamp))
        ships=getships(AIS)
        # 首先清空地图标记
        self.mapshow.page().runJavaScript("clearmap();")
        for i in range(len(ships)):
            [lon,lat]=wgs84_to_gcj02(ships[i]["lng"],lat=ships[i]["lat"])
            theta=ships[i]["cog"]
            props=list(ships[i].values())
            cmd="drawship([{},{}],{},{},\"blue\");".format(lon,lat,theta,props)
            self.mapshow.page().runJavaScript(cmd)
        
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(len(AIS))
        self.tableWidget.setHorizontalHeaderLabels(['MMSI','经度','纬度','对地航速','船长','船宽','航向'])
        for i in range(len(ships)):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem( str(ships[i]["MMSI"])) )
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem( str(ships[i]["lng"])) )
            self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem( str(ships[i]["lat"])) )
            self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem( str(ships[i]["sog"])) )
            self.tableWidget.setItem(i,4,QtWidgets.QTableWidgetItem( str(ships[i]["length"])) )
            self.tableWidget.setItem(i,5,QtWidgets.QTableWidgetItem( str(ships[i]["width"])) )
            self.tableWidget.setItem(i,6,QtWidgets.QTableWidgetItem( str(ships[i]["cog"])) )
        self.tableWidget.verticalHeader().sectionClicked.connect(self.rowselect)
    
    # 点击table表头槽函数
    def rowselect(self,row):
        colcount=self.tableWidget.columnCount()
        lonindex=0
        latindex=0
        mmsiindex=0
        for i in range(colcount):
            thname=self.tableWidget.horizontalHeaderItem(i).text()
            if(thname=="MMSI"):
                mmsiindex=i
            if(thname=="经度"):
                lonindex=i
            if(thname=="纬度"):
                latindex=i

        lon=float(self.tableWidget.item(row,lonindex).text())
        lat=float(self.tableWidget.item(row,latindex).text())
        MMSI=self.tableWidget.item(row,mmsiindex).text()
        glonlat=wgs84_to_gcj02(lon,lat)
        self.mapshow.page().runJavaScript("flytoship([{},{}],{})".format(glonlat[0],glonlat[1],MMSI))
    
    # 点击簇编号cell槽函数
    def groupselect(self,row,col):
        # 当且仅当动态簇模型功能时有效
        if(self.tableWidget.columnCount==9 or col==0):
            self.mapshow.page().runJavaScript("flytogroup({})".format(int(self.tableWidget.item(row,col).text())))
        
    # UI重设
    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "区域船舶航行风险评估系统"))
        self.pushButton.setText(_translate("mainWindow", "冲突风险计算"))
        self.checkBox.setText(_translate("mainWindow", "风险船舶对"))
        self.checkBox_2.setText(_translate("mainWindow", "动态簇"))
        self.pushButton_2.setText(_translate("mainWindow", "动态簇划分"))
        self.checkBox_3.setText(_translate("mainWindow", "水域实时"))
        self.pushButton_3.setText(_translate("mainWindow", "实时数据展示"))
        self.checkBox_4.setText(_translate("mainWindow", "15min"))
        self.checkBox_5.setText(_translate("mainWindow", "30min"))
        self.checkBox_6.setText(_translate("mainWindow", "45min"))
        self.label.setText(_translate("mainWindow", "预测时间步长"))
        self.label_2.setText(_translate("mainWindow", "自定义"))
        self.label_3.setText(_translate("mainWindow", "经纬度范围设置"))
        self.label_4.setText(_translate("mainWindow", "经度"))
        self.label_6.setText(_translate("mainWindow", "纬度"))
        self.label_7.setText(_translate("mainWindow", "计算结果"))
        self.label_8.setText(_translate("mainWindow", "区域船舶航行风险评估系统"))
        self.label_8.move(30,10)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.menu.setTitle(_translate("mainWindow", "主界面"))
        self.menu_2.setTitle(_translate("mainWindow", "数据源"))
        self.menu_3.setTitle(_translate("mainWindow", "历史结果查看"))
        self.menu_4.setTitle(_translate("mainWindow", "设置"))
        self.menu_5.setTitle(_translate("mainWindow", "不确定性模式选择"))
        self.action1.setText(_translate("mainWindow", "csv表格数据"))
        self.action2.setText(_translate("mainWindow", "经纬度设置"))
        self.action1_2.setText(_translate("mainWindow", "预置模式"))
        self.action1_3.setText(_translate("mainWindow", "从文件中创建"))
        self.action2_2.setText(_translate("mainWindow", "实时数据"))
        self.action_15min.setText(_translate("mainWindow", "-15min"))
        self.action_30min.setText(_translate("mainWindow", "-30min"))
        self.action_45min.setText(_translate("mainWindow", "-45min"))
        self.action3.setText(_translate("mainWindow", "自定义"))
    
# 主函数
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()