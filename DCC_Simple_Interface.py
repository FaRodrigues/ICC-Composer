import os
import sys
from datetime import datetime

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QThread, QFile, QRect
from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QApplication, QComboBox, QPushButton, QLineEdit, QDateEdit
from docxtpl import DocxTemplate
import ContextData


class UserInterfaceCertificado(QMainWindow):
    def __init__(self, parent=None):
        super(UserInterfaceCertificado, self).__init__()
        self.calibrationLaboratory_context = None
        self.proindex = 0
        self.customer_context = None
        self.lastVMvalue = None
        self.contextSlope = None
        self.daysinterval = None
        self.DRCGG = None
        self.lastFreqCorrCalculated = None
        self.lastFreCorrected = None
        self.dataprocesstoken = None
        self.newcorrectiontoken = False

        self.dataprocesstoken = False
        self.thread = QThread()

        self.HROGWidget = None

        loader = QUiLoader()
        guipath = os.path.abspath(os.path.join(".", "gui", "ui", "mainwindowCertEn.ui"))
        file = QFile(guipath)
        file.open(QFile.ReadOnly)
        self.mainwindow = loader.load(file, self.window())
        file.close()
        self.setWindowTitle("Dmtic - Processamento de Certificado de Calibração - Versão 0 (2024)")
        QtCore.QCoreApplication.processEvents()
        # self.mainwindow.show()

        self.dateEditLocal = self.findChildren(QDateEdit, 'dateEdit')[0]
        self.dateEditLocal.setDate(datetime.now().date())

        listatiposCert = ["TimeScale", "Internal", "Client"]
        self.comboBoxTipo = self.findChildren(QComboBox, 'comboBox_tipo')[0]
        self.comboBoxTipo.addItems(listatiposCert)
        listaProSEIEscala = ["0052600.002901/2024-56"]
        listaProSEIInterno = ["0052600-002840/2024-27"]
        listaProSEIExterno = ["0052600.002856/2024-30"]
        self.comboBoxTipo.activated.connect(self.defineProcessProfile)

        self.comboBoxSei = self.findChildren(QComboBox, 'comboBox_sei')[0]

        self.dictmapPro = {0: listaProSEIEscala, 1: listaProSEIInterno, 2: listaProSEIExterno}

        listaUF = ["RJ", "SP"]

        self.comboBoxUF = self.findChildren(QComboBox, 'comboBox_uf')[0]
        self.comboBoxUF.addItems(listaUF)
        # self.comboBoxTipo.activated.connect(loadClientProfile)
        self.dictpathtemplate = {0: "MOD-Dimci-1_14_template_lab.docx", 1: "MOD-Dimci-1_14_template_interno.docx",
                                 2: "MOD-Dimci-1_14_template_externo.docx"}

        self.doc = None
        self.doccontext = {}

        self.renderButton = self.findChildren(QPushButton, 'pushButton')[0]
        self.renderButton.clicked.connect(self.renderForm)
        self.customerName = self.findChildren(QLineEdit, 'lineEdit_cn')[0]
        self.customerShortName = self.findChildren(QLineEdit, 'lineEdit_csn')[0]
        self.customerStreet = self.findChildren(QLineEdit, 'lineEdit_street')[0]
        self.customerStreetNum = self.findChildren(QLineEdit, 'lineEdit_streetnum')[0]
        self.customerLocal = self.findChildren(QLineEdit, 'lineEdit_local')[0]
        self.customerCity = self.findChildren(QLineEdit, 'lineEdit_city')[0]
        self.customerCEP = self.findChildren(QLineEdit, 'lineEdit_cep')[0]
        self.comboCustomerUF = self.findChildren(QComboBox, 'comboBox_uf')[0]

        self.numcert = self.findChildren(QLineEdit, 'lineEdit_numcert')[0]

    def renderForm(self):
        labexe = ContextData.CalibrationLaboratoryData()
        labexe.setCalibrationLaboratoryName("Inmetro/Dimci/Dmtic")
        labexe.setCalibrationLaboratoryShortName("Dmtic")
        labexe.setCalibrationLaboratoryCompleteAddress("Av. Nossa Senhora das Graças, 50 - Xerém - Duque de Caxias - "
                                                       "RJ - CEP: 25250-020")

        self.calibrationLaboratory_context = labexe.getCalibrationLaboratoryContext()

        print(self.getProIndex())

        cd = ContextData.CustomerData()

        if self.getProIndex() == 0:
            cd.setCustomerName(f"{self.calibrationLaboratory_context['calibrationLaboratoryName']}")
            cd.setCustomerShortName(f"{self.calibrationLaboratory_context['calibrationLaboratoryShortName']}")
            cd.setCustomerCompleteAddress(f"{self.calibrationLaboratory_context['calibrationLaboratoryCompleteAddress']}")
        else:
            cd.setCustomerName(f"{self.customerName.text()}")
            cd.setCustomerShortName(f"{self.customerShortName.text()}")
            cd.setCustomerCompleteAddress(
                f"{self.customerStreet.text()}, {self.customerStreetNum.text()} - {self.customerLocal.text()} - {self.customerCity.text()} - {self.comboCustomerUF.currentText()} - CEP: {self.customerCEP.text()}")

        self.customer_context = cd.getCustomerContext()
        print(self.customer_context, "\n", self.calibrationLaboratory_context)

    def setProIndex(self, pi):
        self.proindex = pi

    def getProIndex(self):
        return self.proindex

    def defineProcessProfile(self):
        proindex = self.comboBoxTipo.currentIndex()
        self.setProIndex(proindex)
        listaProSEI = self.dictmapPro[proindex]
        # print(listaProSEI)
        self.comboBoxSei.clear()
        self.comboBoxSei.addItems(listaProSEI)
        docpath = os.path.join(".", "docs", self.dictpathtemplate[proindex])
        print(docpath)
        self.doc = DocxTemplate(docpath)
        QtCore.QCoreApplication.processEvents()


StyleSheet = '''
QMainWindow {
    border: 1px solid blue;
    font-weight:bold
}
QMenuBar {
    background-color: #F0F0F0;
    color: #000000;
    border: 1px solid #000;
    font-weight:bold
}
QMenuBar::item {
    background-color: rgb(49,49,49);
    color: rgb(255,255,255)
}
QMenuBar::item::selected {
    background-color: rgb(30,30,30)
}
QTabWidget {
    background-color: #F0F0F0;
    border: 1px solid blue;
    border-radius: 20px
}
QTabWidget::pane {
    border: 1px solid #31363B;
    padding: 2px;
    margin:  0px
}
QTableView {
    selection-background-color: #0088cc
}
QTabBar {
    border: 0px solid #31363B;
    color: #152464
}
QTabBar::tab:top:selected {
    background-color: #0066cc;
    color: white
}
QCalendarWidget{
    border: 2px solid black;
    background-color: rgb(255,255,255)
}
QComboBox {
    border: 1px solid black;
}
QGroupBox {
    border: 2px solid gray;
    border-radius: 4px;
    margin-top: 16px
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px
}
'''
if __name__ == '__main__':
    # os.environ['PYSIDE_DESIGNER_PLUGINS'] = "."
    # QPyDesignerCustomWidgetCollection.registerCustomWidget(QWidget, module="formHROGWidget")
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_Use96Dpi, True)
    # QtCore.QCoreApplication.setAttribute( QtCore.Qt.ApplicationAttribute.AA_PluginApplication)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_ForceRasterWidgets)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_NativeWindows)
    app = QApplication(sys.argv)
    QPyDesignerCustomWidgetCollection.instance()
    styles = ["Plastique", "Cleanlooks", "CDE", "Motif", "GTK+"]
    app.setStyle(QtWidgets.QStyleFactory.create(styles[1]))
    app.setStyleSheet(StyleSheet)
    # app.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
    app_icon = QtGui.QIcon()
    app_icon.addFile('gui/icons/inmetro.ico', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    rect = QRect(100, 100, 820, 720)
    window = UserInterfaceCertificado()
    window.setGeometry(rect)
    window.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
    # print("lastvalue = {}".format(dir(UserInterfaceDmtic)))
    window.show()
    app.exec()
