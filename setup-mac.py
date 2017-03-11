from setuptools import setup


APP = ["MediaInfoCommenter.py"]
APP_NAME = "MediaInfoCommenter"
DATA_FILES = []

OPTIONS = {
    
}

setup(
    name=APP_NAME,
    app=APP,
    options={"py2app":
             {"argv_emulation": True,
                'iconfile': 'app.icns',
                'includes': ["sip", "PyQt4._qt"],
                'plist': {
                    'CFBundleName': APP_NAME,
                    'CFBundleDisplayName': APP_NAME,
                    'CFBundleGetInfoString': "Media Info Commenter",
                    'CFBundleIdentifier': "com.kuntat.osx.mediainfocommenter",
                    'CFBundleVersion': "0.1.0",
                    'CFBundleShortVersionString': "0.1.0",
                    'NSHumanReadableCopyright': u"GNU General Public License (GPL)"
                }
              }
    },
    setup_requires=["py2app"],
) 
