import glob
from cx_Freeze import setup, Executable

def GetIncludeFiles():

	fl = []
	
	for resPath in glob.glob("Resources/*"):
		pathType = resPath[10:]
		
		if pathType == 'Fonts':
			fl.append("Resources/Fonts/PressStartK.ttf")
			
		elif pathType == 'Images':
			for imgTypePath in glob.glob(resPath+"/*"):
				imgType = imgTypePath[17:]
				
				if imgType == 'Characters':
					for charPath in glob.glob(imgTypePath+"/*"):
						for spriteLevelPath in glob.glob(charPath+"/*"):
							for imgPath in glob.glob(spriteLevelPath+"/*.png"):
								fl.append(imgPath)
					
				elif imgType == 'Objects':
					for imgPath in glob.glob(imgTypePath+"/*.png"):
						fl.append(imgPath)
			
	return fl
		
v = '0.0915'
includeFiles = GetIncludeFiles()
buildOptions = {"packages":["os"], "excludes":["tkinter"], "include_files":includeFiles}

setup(
	name = 'Platformer Engine Test Build (Ramp-Mods Disabled) '+v,
	version = v,
	description = 'Platformer Engine Test Build',
	author = 'Ix',
	options = {"build_exe":buildOptions},
		executables = [Executable(script="Main.py", base="Win32GUI", targetName="Game.exe")])
