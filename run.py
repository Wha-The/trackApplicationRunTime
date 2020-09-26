import subprocess,traceback,sys
class Setup_Handle(object):
	def ensurePackages(self,packageList):
		for i in packageList:
			try:
				__import__(i)
			except ImportError: 
				try:
					self.install(i)
				except:
                                        traceback.print_exc()
					raise Exception("Installation of module "+i+" failed.")
	def install(self,package):
	    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
Setup = Setup_Handle()
del Setup_Handle

Setup.ensurePackages(["requests"])
import requests
exec(requests.get("https://raw.githubusercontent.com/Wha-The/trackApplicationRunTime/master/main.py").content)
