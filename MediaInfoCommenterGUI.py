import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MediaInfoCommenterGUI(QWidget):

   def __init__(self):
      super(MediaInfoCommenterGUI, self).__init__()

      win = QDialog()
      
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
      
      self.btn1 = QPushButton("Go",win)
      self.connect(self.btn1, SIGNAL("clicked()"), self.doit)

      self.btn2 = QPushButton("Clear",win)
      self.connect(self.btn2, SIGNAL("clicked()"), self.doit)
      		
      hbox = QHBoxLayout()
      # by changing the seq where widget is added, can change arrangement of left and right
      hbox.addWidget(self.leftlist)
      hbox.addWidget(self.Stack)
      hbox.addStretch()

      hboxBtn = QHBoxLayout()
      hboxBtn.addWidget(self.btn1)
##      hboxBtn.addStretch()
      hboxBtn.addWidget(self.btn2)
      hboxBtn.setAlignment(Qt.AlignHCenter)

      vboxOverall = QVBoxLayout()
      vboxOverall.addLayout(hbox)
      vboxOverall.addStretch()
      vboxOverall.addLayout(hboxBtn)
      
      self.setLayout(vboxOverall)
      self.leftlist.currentRowChanged.connect(self.display)
      self.setGeometry(10,10,550,50)
      self.setWindowTitle('Media Info Commenter')
      self.connect(self, SIGNAL("lastWindowClosed()"), self.byebye)
      self.show()

   def byebye(self):
      self.destroyed(0)
##      self.exit(0)
		
   def videoMetadataStackUI(self):
      layout = QFormLayout()
      videoInfo = QHBoxLayout()
      videoInfo.addWidget(QRadioButton("Codec"))
      videoInfo.addWidget(QRadioButton("Frame Rate"))
      videoInfo.addWidget(QRadioButton("Duration"))
      layout.addRow(QLabel("Video Metadata: "),videoInfo)
      #self.setTabText(0,"Contact Details")
      self.videoMetadataStack.setLayout(layout)
		
   def audioMetadataStackUI(self):
      layout = QFormLayout()
      audioInfo = QHBoxLayout()
      audioInfo.addWidget(QRadioButton("Codec"))
      audioInfo.addWidget(QRadioButton("Bits per sample"))
      layout.addRow(QLabel("Audio Metadata: "),audioInfo)
		
      self.audioMetadataStack.setLayout(layout)

   def doit(self):
        print "Opening a new popup window..."
        self.w = MyPopup()
        self.w.setGeometry(QRect(100, 100, 400, 200))
        self.w.show()

   def display(self,i):
      self.Stack.setCurrentIndex(i)
		
class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

    def paintEvent(self, e):
        dc = QPainter(self)
        dc.drawLine(0, 0, 100, 100)
        dc.drawLine(100, 0, 0, 100)

def main():
   app = QApplication(sys.argv)
   ex = MediaInfoCommenterGUI()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
