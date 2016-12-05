import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from MediaInfoCommenterModel import *

class MediaInfoCommenterGUI(QWidget):

   def __init__(self):
      super(MediaInfoCommenterGUI, self).__init__()

      win = QDialog()

      self.makeTable()

      self.makeAddBtn()

      self.makeRemoveBtn()

      self.makeStack()

      self.makeCommentMetadataBtn()

      self.makeClearMetadataBtn()

      self.mainLayout()


   def makeAddBtn(self):
      self.fileBtn = QPushButton("Add files")
      self.fileBtn.clicked.connect(self.getfiles)
      
   def makeRemoveBtn(self):
      self.removeBtn = QPushButton("Remove files")
      self.removeBtn.clicked.connect(self.removefiles)

   def makeStack(self):
      self.leftlist = QListWidget ()
      self.leftlist.insertItem (0, 'Video Metadata' )
      self.leftlist.insertItem (1, 'Audio Metadata' )
		
      self.videoMetadataStack = QWidget()
      self.audioMetadataStack = QWidget()
		
      self.videoMetadataStackUI()
      self.audioMetadataStackUI()
		
      self.Stack = QStackedWidget (self)
      self.Stack.addWidget (self.videoMetadataStack)
      self.Stack.addWidget (self.audioMetadataStack)

   def makeCommentMetadataBtn(self):
      self.commentMetadataBtn = QPushButton("Comment Metadata")
      self.connect(self.commentMetadataBtn, SIGNAL("clicked()"), self.commentInfo)

   def makeClearMetadataBtn(self):
      self.clearMetadataBtn = QPushButton("Clear Metadata")
      self.connect(self.clearMetadataBtn, SIGNAL("clicked()"), self.removeComment)

   def getfiles(self):
      dlg = QFileDialog()
      dlg.setFileMode(QFileDialog.ExistingFiles)

      if dlg.exec_():
         self.filenames = dlg.selectedFiles()
         while self.tableWidget.rowCount() != self.filenames.count():
            if self.tableWidget.rowCount() < self.filenames.count():
               self.tableWidget.insertRow(0)
            elif self.tableWidget.rowCount() > self.filenames.count():
               self.tableWidget.removeRow(0)
         for filename in self.filenames:
            startIndex = self.filenames[self.filenames.indexOf(filename)].lastIndexOf("/") + 1  ##MAGIC NUMBER to get to the next index
            endIndex = self.filenames[self.filenames.indexOf(filename)].count()
            self.tableWidget.setItem(self.filenames.indexOf(filename), 0, QTableWidgetItem(self.filenames[self.filenames.indexOf(filename)].mid(startIndex, endIndex)))

	 
   def removefiles(self):
      while self.tableWidget.rowCount() > 0:
         self.tableWidget.removeRow(0)

		
   def videoMetadataStackUI(self):
      layout = QFormLayout()
      videoInfo = QHBoxLayout()

      self.videoCodecRadioBtn = QRadioButton("Codec")
      self.connect(self.videoCodecRadioBtn, SIGNAL("clicked()"), lambda: self.changeInfoRequired(0, "codec_name"))
      videoInfo.addWidget(self.videoCodecRadioBtn)

      self.frameRateRadioBtn = QRadioButton("Frame Rate")
      self.connect(self.frameRateRadioBtn, SIGNAL("clicked()"), lambda: self.changeInfoRequired(0, "r_frame_rate"))
      videoInfo.addWidget(self.frameRateRadioBtn)

      self.durationRadioBtn = QRadioButton("Duration")
      self.connect(self.durationRadioBtn , SIGNAL("clicked()"), lambda: self.changeInfoRequired(0, "duration"))
      videoInfo.addWidget(self.durationRadioBtn)
      
      layout.addRow(QLabel("Video Metadata: "),videoInfo)
      self.videoMetadataStack.setLayout(layout)
      
   def audioMetadataStackUI(self):
      layout = QFormLayout()
      audioInfo = QHBoxLayout()

      self.audioCodecRadioBtn = QRadioButton("Codec")
      self.connect(self.audioCodecRadioBtn, SIGNAL("clicked()"), lambda: self.changeInfoRequired(1, "codec_name"))
      audioInfo.addWidget(self.audioCodecRadioBtn)

      self.audioBitPerSampleRadioBtn = QRadioButton("Bits per sample")
      self.connect(self.audioBitPerSampleRadioBtn , SIGNAL("clicked()"), lambda: self.changeInfoRequired(1, "bits_per_sample"))
      audioInfo.addWidget(self.audioBitPerSampleRadioBtn)
      
      layout.addRow(QLabel("Audio Metadata: "),audioInfo)		
      self.audioMetadataStack.setLayout(layout)

   def changeInfoRequired(self, videoOrAudio, info):
         self.videoOrAudio = videoOrAudio
         self.info = info

   def commentInfo(self):
      for filename in self.filenames:
         comment(str(filename), self.videoOrAudio, self.info)
      self.okDialog()

   def removeComment(self):
      self.info = ""
      self.commentInfo()

   def okDialog(self):
      runDialog = QDialog()
      runDialogLabel = QLabel(runDialog)
      runDialogLabel.setText("Done!")
      runDialogBtn = QPushButton("Ok", runDialog)
      runDialogBtn.clicked.connect(runDialog.close)
      runDialogLayout = QVBoxLayout()
      runDialogLayout.addWidget(runDialogLabel)
      runDialogLayout.addWidget(runDialogBtn)
      runDialog.setLayout(runDialogLayout)
      runDialog.exec_()

      

   def display(self,i):
      self.Stack.setCurrentIndex(i)

   def makeTable(self):
      self.tableWidget = QTableWidget()

      self.tableWidget.setRowCount(0)
      self.tableWidget.setColumnCount(1)
      
      self.tableHeader = ["Files"]
      self.tableWidget.setHorizontalHeaderLabels(self.tableHeader)
      self.tableWidget.verticalHeader().setVisible(False)

      self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
      self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
      self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
      self.tableWidget.setShowGrid(True)
      
      self.tableWidget.horizontalHeader().setStretchLastSection(True)
      self.tableWidget.verticalHeader().setResizeMode(QHeaderView.Fixed)
      self.tableWidget.verticalHeader().setDefaultSectionSize(16)
      self.tableWidget.setAlternatingRowColors(True)
      self.tableWidget.setStyleSheet("alternate-background-color: white;background-color: grey;")
      self.tableWidget.setStyleSheet("QTableView {selection-background-color: blue;}")


   def mainLayout(self):

      tablebox = QVBoxLayout()
      tablebox.addWidget(self.tableWidget)

      hbox = QHBoxLayout()
      # by changing the seq where widget is added, can change arrangement of left and right
      hbox.addWidget(self.leftlist)
      hbox.addWidget(self.Stack)
      hbox.addStretch()

      hboxBtn = QHBoxLayout()
      hboxBtn.addWidget(self.fileBtn)
      hboxBtn.addWidget(self.removeBtn)
      hboxBtn.addWidget(self.commentMetadataBtn)
      hboxBtn.addWidget(self.clearMetadataBtn)
      hboxBtn.setAlignment(Qt.AlignHCenter)
      
      vboxOverall = QVBoxLayout()
      vboxOverall.addLayout(tablebox)
      vboxOverall.addLayout(hbox)
      vboxOverall.addStretch()
      vboxOverall.addLayout(hboxBtn)
      
      self.setLayout(vboxOverall)
      self.leftlist.currentRowChanged.connect(self.display)
      self.setGeometry(10,10,550,50)
      self.setWindowTitle('Media Info Commenter')
      self.show()

def main():
   app = QApplication(sys.argv)
   ex = MediaInfoCommenterGUI()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
