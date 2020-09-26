SetupExists=False
try:
	Setup
	SetupExists=True
except NameError:
	pass
if SetupExists:
	Setup.ensurePackages("psutil,time,os,datetime,keyboard,pymsgbox,subprocess,traceback,win32gui,win32process".split(","))

import psutil,time,os,datetime,keyboard,pymsgbox,subprocess,traceback,win32gui,win32process
rawAppName = raw_input(" App name to track: ")or"roblox"

def GetPid(appName):
# Get a list of all running processes
	list = psutil.pids()

	# Go though list and check each processes executeable name for 'putty.exe'
	for i in range(0, len(list)):
		try:
			p = psutil.Process(list[i])
			if p.cmdline()[0].lower().find(appName) != -1 and p.pid!=os.getpid():
				return p.name(),p.cmdline()[0],p.pid
		except:
			pass
	return None,None,None

def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            # print hwnd
            if found_pid == pid:
                hwnds.append(hwnd)
                return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds 

appName,appPath,ATTACHEDPID = GetPid(rawAppName)
if not ATTACHEDPID:
	print("Can't find any process with %s in its name"%(rawAppName))
	raw_input()
	quit()
os.system('cls')
print " Traking: "+appName+", PID: "+str(ATTACHEDPID)

def getmillisec():
	c = datetime.datetime.now()
	return (c.day * 24 * 60 * 60 + c.second) * 1000 + c.microsecond / 1000.0



def fillEmptyWithZero(string,digit):
	if len(string)< digit:
		return "0"*(digit-len(string))+string
	return string

def main():
	def handler():
		global appName,ATTACHEDPID,appPath
		choices = ["Cancel","Restart"]
		if psutil.pid_exists(ATTACHEDPID):
			process = psutil.Process(ATTACHEDPID)
			choices = ["Cancel","Terminate",(process.status()=="running" and "Suspend" or "Resume"),"Focus","Maximize","Minimize"]
		choice = pymsgbox.confirm("Tracking: "+appName,buttons=choices)
		hwnds = get_hwnds_for_pid(ATTACHEDPID)
		try:
			hwnd = hwnds[0]
		except:
			print("Cannot find window (hwnd), ignoring")

		if choice == "Cancel": return
		if psutil.pid_exists(ATTACHEDPID):
			
			if choice == "Terminate":
				process.terminate()
			if choice == "Suspend":
				process.suspend()
			if choice == "Resume":
				process.resume()
			if choice == "Focus":
				win32gui.SetForegroundWindow(hwnd)
			if choice == "Minimize":
				win32gui.ShowWindow(hwnd, 6)
			if choice == "Maximize":
				win32gui.ShowWindow(hwnd, 9)

		else:
			if choice == "Restart":
				ATTACHEDPID = subprocess.Popen(appPath).pid

	keyboard.add_hotkey('ctrl+\\', handler)
	secondsAlive = 0
	calculateTime = 0
	extraUsedTime = 0
	while True:
		usedTime = (calculateTime/1000)
		if usedTime >1: extraUsedTime += usedTime - 1
		waittime=1-usedTime
		waittime = waittime>0 and waittime or 0 
		if extraUsedTime > 0: #If there is extra used time
			if extraUsedTime > waittime: #If it cant affort to pay all the time back
				#Pay as much as the sleeptime can
				extraUsedTime = extraUsedTime - waittime
				waittime = 0
			else: # Pay all
				waittime = waittime - extraUsedTime
				extraUsedTime = 0
		time.sleep(waittime)

		start=getmillisec()
		if psutil.pid_exists(ATTACHEDPID):
			secondsAlive+=1
		
		calculateTime = getmillisec()-start
		calculateTime=calculateTime>0 and calculateTime or 0
		try:
			process = psutil.Process(ATTACHEDPID)
		except psutil.NoSuchProcess:
			process = None
		print " Seconds alive: "+str(secondsAlive)+",status: "+(process and process.status() or "terminated")+",[ctrl + \\]:actions"+(" "*10)+"\r",

if __name__ == '__main__':
	main()

