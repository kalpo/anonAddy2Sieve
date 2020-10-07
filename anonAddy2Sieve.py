#!/usr/bin/python

import json, csv, sys, getopt, requests
from tkinter import filedialog
from tkinter import *
from tkinter.scrolledtext import ScrolledText

tokenFile = ""
inputJSONfile = ""
outputFile = ""
useCLI = False

def getFile(location, mode="r"):
	try:
		f = open(location, mode)
		return f
	except FileNotFoundError as error:
		print(error)
		sys,exit(2)
	
def getArguments():
	"""
	Processes the arguments from the command line and writes them into the global variables
	"""
	try:
		opts, args = getopt.getopt(sys.argv[1:],"chj:t:o:",["useCLI", "help","json=", "token=","output="])
	except getopt.GetoptError:
		printCLIHelp()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-c' or opt == '--useCLI': 
			global useCLI
			useCLI = True
		elif opt == '-h' or opt == '--help':
			printCLIHelp()
			sys.exit(1)
		elif opt == '-j' or opt == '--json':
			global inputJSONfile
			inputJSONfile = arg
		elif opt == '-t' or opt == '--token':
			global tokenFile
			tokenFile = arg
		elif opt == '-o' or opt == '--output':
			global outputFile
			outputFile = arg
				
def buildSieve(json):
	""" Builds a Sieve email filter given a JSON dict object from AnonAddy's API """
	sieveCode = ""
	isFirstIf = True
	for alias in json["data"]: 
		if not isFirstIf: # Add the "el" for the elif statement after the first iteration of the loop is over
			sieveCode += "els"
		else:
			isFirstIf = False
		sieveCode += ("if allof (address :all :comparator \"i;unicode-casemap\" :is \"From\" \"%(email)s\") {\n"
					  "	fileinto \"%(description)s\";\n"
					  "\n}"%alias)
	return sieveCode
	
def getAliasesFromAPI(token):
	""" Makes a request to AnonAddy's service for a list of aliases as described on their API
		The argument token is a string provided to AnonAddy's users as authentification for the API
		Returns a JSON dict object
	"""

	headers = {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
    'Authorization': 'Bearer %s'%token}
	r = requests.get('https://app.anonaddy.com/api/v1/aliases', headers=headers)
	return r.json() 
	
def outputSieveCode(code):
	if outputFile != "":
		f = open(outputFile, 'w')
		f.write(code)
	else:
		print(code)
		
def startCLI():
	""" If an inputJSONfile has been specified, use it, otherwise use anonaddy API"""
	def printCLIHelp():
		"""
		Prints a simple useage guide
		
		"""
		
		helpStr = """usage: ./anonAddy2Sieve.py [option]
	Options and arguments (and corresponding environment variables):
	-c       : disables the GUI and outputs either to terminal or to a file if -o option specified. (also --useCLI)
	-h       : print this help message and exit. (also --help)
	-j file  : uses json text from a given file instead of contacting anonaddy. 
			   this option will overide -t. (also --json=<file>)
	-o file  : specifies the file where the Sieve code will be writen.
			   If empty, the code will print on the default channel (e.g. terminal) (also --output=<file>)
	-t file  : specifies the file containing anonaddy's API token. (also --token=<file>)

	EXAMPLE:
	./anonAddy2Sieve.py -c -t token.txt -o protonMailFilter.sieve"""
		print(helpStr)	
		
	if inputJSONfile != "":  
		f = getFile(inputJSONfile,'r')
		outputSieveCode(buildSieve(json.loads(f.read())))
	else:
		f = getFile(tokenFile, 'r')
		token = f.read()
		outputSieveCode(buildSieve(getAliasesFromAPI(token.replace("\n",""))))
		
def startGUI():	
	
	def getTokenGUI():
		def askGUIforTokenFile():
			tokenFile = filedialog.askopenfilename(initialdir = "", title = "Select Personal Token File", filetypes = [("all files","*")])
			st.insert(INSERT, getFile(tokenFile,"r").read())
	
		def buttonOKaction():
			token = st.get(1.0,END)
			root.destroy()
		root = Tk()
		root.title("AnonAddy2Sieve")
		root.resizable(False, False)
		Label(root,text="Paste here your Personal Token File").grid(row=0, column=0, columnspan=2)		
		st = ScrolledText(root, height=15); st.grid(row=1, column=0, columnspan=2)
		Button(root, text="OK", width=30, command=buttonOKaction).grid(row=2, column=0)
		Button(root, text="Load token from a file",command=askGUIforTokenFile).grid(row=2, column=1)
		root.mainloop()
	
	def displayCodeGUI(token):
		def saveCodeOnFile():
			tokenFile = filedialog.askopenfilename(initialdir = "", title = "Select Personal Token File", filetypes = [("all files","*")])
			st.insert(INSERT, getFile(tokenFile,"r").read())
	
		def copyText():
			root.clipboard_clear()
			root.clipboard_append(st.get(1.0,END))
			root.update() # now it stays on the clipboard after the window is closed
			
		root = Tk()
		root.title("AnonAddy2Sieve")
		root.resizable(False, False)	
		st = ScrolledText(root, height=15); st.grid(row=0, column=0, columnspan=2)
		st.insert(INSERT, buildSieve(json.loads(getFile('json').read())))       # getAliasesFromAPI(token.replace("\n",""))))
		Button(root, text="Copy to clipboard", width=30, command=copyText).grid(row=2, column=0)
		Button(root, text="Save in a file", command=saveCodeOnFile).grid(row=2, column=1)
		root.mainloop()
		
	global tokenFile
	token =""
	if tokenFile == "":
		token = getTokenGUI()
	else:
		token = getFile(tokenFile)
	displayCodeGUI(token)

def main():
	getArguments()
	if useCLI:
		startCLI()
	else:
		startGUI()
		
main()
