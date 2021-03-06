#!/usr/bin/python

from subprocess import Popen, PIPE

##class MediaInfoCommenterModel():

##def __init__(self, parent = None):
##        super(MediaInfoCommenterModel, self).__init__(parent)
##        fileToComment = raw_input("What files do you want?\n")
##        videoOrAudio = raw_input("0 for video, 1 for audio\n")
##        info = raw_input("What info do you want?\n")

##        def comment():
def main():
        inputFileList = []
        print "What files do you want to process? (enter -e when you are done)"
        inputFile = raw_input()
        while(inputFile != "-e"):
                inputFileList.append(inputFile)
                inputFile = raw_input()
        
        videoOrAudio = raw_input("0 for video track, 1 for audio track\n")
        info = raw_input("What info do you want?\n")
        print "Commenting on your files..."
        for inputFile in inputFileList:
                comment(inputFile, videoOrAudio, info)
        print "Done!"

##does videoOrAudio still need to be string?
def comment(inputFile, videoOrAudio, info):        
        if videoOrAudio == 0:
                selectStreams = 'v:0'
        else:
                selectStreams = 'a:0'

        stream = 'stream=%s'%info

        p = Popen(['/usr/local/Cellar/ffmpeg/3.0.2/bin/ffprobe', '-v', 'error', '-select_streams', selectStreams,
                   '-show_entries', stream, '-of', 'default=noprint_wrappers=1:nokey=1',
                   inputFile],stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()

        script = '''
                TELL APPLICATION \"FINDER\"
                SET filePath TO POSIX PATH OF \"{}\" as POSIX file
                SET COMMENT OF (filePath AS ALIAS) TO \"{}\"
                END TELL
                '''.format(inputFile.rstrip(),stdout.rstrip())

        p = Popen(['osascript', '-'],stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate(script)
        print(p.returncode, stdout.rstrip(), stderr.rstrip())

if __name__ == '__main__':
        main()
