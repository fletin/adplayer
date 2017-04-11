import os, time, sys
import threading
import codecs
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY

global ModifyFlag
ModifyFlag = False
scriptdir=os.path.dirname(os.path.realpath(__file__))
DNAME='GD-01'

class MyEventHandler(ProcessEvent):
	def process_IN_CREATE(self, event):
		global ModifyFlag
		ModifyFlag = True
		print("catch it! ModifyFlag=",ModifyFlag)

	def process_IN_DELETE(self, event):
		global ModifyFlag
		ModifyFlag = True
		print("catch it! ModifyFlag=",ModifyFlag)

	def process_IN_MODIFY(self, event):
		global ModifyFlag
		ModifyFlag = True
		print("catch it! ModifyFlag=",ModifyFlag)

class eventListen(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		mask = IN_DELETE | IN_CREATE | IN_MODIFY
		wm = WatchManager()
		notifier = Notifier(wm, MyEventHandler())
		wm.add_watch(scriptdir+"/Common", mask, auto_add= True, rec=True)
		wm.add_watch(scriptdir+"/Special", mask, auto_add= True, rec=True)
		wm.add_watch(scriptdir+"/Override", mask, auto_add= True, rec=True)

		while True:
			try:
				notifier.process_events()
				if notifier.check_events():
					notifier.read_events()
			except KeyboardInterrupt:
				notifier.stop()


class syncftp(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while True:
			#os.system("sudo ./syncftp.sh")
			os.system("lftp -u adplayer,adplayer -e \"mirror --delete --only-newer --verbose Common %s/Common; quit\" ftp.dhjy.com.cn"%scriptdir)
			os.system("lftp -u adplayer,adplayer -e \"mirror --delete --only-newer --verbose Special/%s %s/Special; quit\" ftp.dhjy.com.cn"%(DNAME,scriptdir))
			os.system("lftp -u adplayer,adplayer -e \"mirror --delete --only-newer --verbose Override/%s %s/Override; quit\" ftp.dhjy.com.cn"%(DNAME,scriptdir))

			print("synced! ModifyFlag=",ModifyFlag)
			if ModifyFlag:
				print("about to reboot.")
				os.system("sudo reboot")
			time.sleep(600)

def replaceGarbage(a):
	return a.replace("\r\n","").replace("\ufeff","")



if __name__ == "__main__":
	if (os.path.isfile(scriptdir+"/adplayer.debug")):
		sys.exit()

	os.system("sudo DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority /usr/bin/feh --quiet --preload --recursive --randomize --full-screen "+scriptdir+"/black1920x1080.jpg &")

	
	filelist=[]
	supportExt=["mp4","avi"]

	# Common
	if (not os.path.isfile(scriptdir + "/Common/playlist.txt")):
		a = os.listdir(scriptdir + "/Common")
		for i in a:
			i=replaceGarbage(i)
			ext=i.split(".")[-1]
			print(ext)
			if (ext in supportExt):
				filelist.append(scriptdir+"/Common/"+i)
	else:
		with codecs.open(scriptdir + "/Common/playlist.txt","r","utf-8") as playlist:
			for line in playlist:
				line=replaceGarbage(line)
				filelist.append(scriptdir+"/Common/"+line)

	# Special
	a = os.listdir(scriptdir + "/Special")
	for i in a:
		i=replaceGarbage(i)
		ext=i.split(".")[-1]
		print(ext)
		if (ext in supportExt):
			filelist.append(scriptdir+"/Special/"+i)

	#Override
	a = os.listdir(scriptdir + "/Override")
	if a!=[]:
		filelist=[]
		for i in a:
			i=replaceGarbage(i)
			ext=i.split(".")[-1]
			print(ext)
			if (ext in supportExt):
				filelist.append(scriptdir+"/Override/"+i)

	threadListen=eventListen()
	threadListen.start()
	threadSync=syncftp()
	threadSync.start()

	print(filelist)
	while True:
		for i in filelist:
			os.system("DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority /usr/bin/omxplayer -o hdmi "+i)
			pass
		# break