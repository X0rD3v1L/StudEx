from ffprobe import FFProbe
import os,glob

def getsubjectnames():
	subjectNames = [os.path.abspath(name) for name in os.listdir(".") if os.path.isdir(name)]
	return subjectNames

def getunitNames(subjectName):
	Dirs = [];paths = []
	for (root,dirs,files) in os.walk(subjectName, topdown=True):
		for name in dirs:
			Dirs.append(name);paths.append(os.path.join(root, name))
	return Dirs,paths

def getvideoLength(videoPath):
	try:
		length = (int(float(FFProbe(videoPath).video[0].duration) * 1000))
		return length
	except:
		pass

def Onex(total):
	return '%02d hrs %02d mins %02d secs' % (int((total)/(1000*60*60))%24,int(total/(1000*60))%60, int(total/1000)%60)

def OneFivex(total):
	return "%02d hrs %02d mins %02d secs" % (int((total/1.5)/(1000*60*60))%24,int((total/1.5)/(1000*60))%60, int((total/1.5)/1000)%60)

def Twox(total):
	return "%02d hrs %02d mins %02d secs" % (int((total/2)/(1000*60*60))%24,int((total/2)/(1000*60))%60, int((total/2)/1000)%60)

def overallTime(totalTime):
	return ["%02d days %02d hrs %02d mins %02d secs" % (int(totalTime/(1000*60*60*24)),int((totalTime)/(1000*60*60))%24,int(totalTime/(1000*60))%60, int(totalTime/1000)%60),
	"%02d days %02d hrs %02d mins %02d secs" % (int((totalTime/1.5)/(1000*60*60*24)),int((totalTime/1.5)/(1000*60*60))%24,int((totalTime/1.5)/(1000*60))%60, int((totalTime/1.5)/1000)%60),
	"%02d days %02d hrs %02d mins %02d secs" % (int((totalTime/2)/(1000*60*60*24)),int((totalTime/2)/(1000*60*60))%24,int((totalTime/2)/(1000*60))%60, int((totalTime/2)/1000)%60)]

def allMP4Files(unitName):
	files = glob.iglob(unitName + '/*.mp4', recursive=True)
	total = 0
	for file in (files):
		try:
		 total += (getvideoLength(file))
		 print(total)
		except:
			pass
	return [Onex(total),OneFivex(total),Twox(total),total]


if __name__ == "__main__":
	subjectNames = getsubjectnames()
	megaDic = {os.path.relpath(subjectName) : 0 for subjectName in subjectNames}
	for name in subjectNames:
		Dirs,paths = getunitNames(name)
		folderNames = {}
		totalTime = 0
		for names,length in zip(Dirs,paths):
			returned = allMP4Files(length)
			totalTime += returned[-1]
			folderNames[names] = returned[:-1] + [returned[-1]//1000]
		folderNames['Total Time'] = overallTime(totalTime)
		folderNames['Total secs'] = totalTime//1000
		megaDic[os.path.relpath(name)] = folderNames
	print(megaDic)