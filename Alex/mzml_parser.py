## Alex Cope
## 3-17-2017
from pymzml import *
import os
import glob
import sys

def parseMZML(path_to_mzml='',path_to_output='',accessionNames={"MS:1000042":"MS1 Precursor Intensity","MS:1000016":"Scan Start Time","MS:1000504":"Base Peak m/z","MS:1000505":"Base Peak Intensity"},
	accessions = [('MS:1000042',['value']),("MS:1000016",['value']),("MS:1000504",["value"]),("MS:1000505",["value"])]):
	# File Path
	if path_to_output[-1] != "/":
		path_to_output = path_to_output +"/"
	delim = ''
	if path_to_mzml != '' and path_to_mzml[-1:] != '/':
		delim = '/'
	file_path = os.path.normpath(delim.join([path_to_mzml,"*.mzML"])) 		# File path
	print file_path
	files=glob.glob(file_path)	# Finds all mzML files in the current directory
	outputFiles = []
	for a_file in files:
		msrun = run.Reader(a_file,extraAccessions=accessions) 
		truncate = a_file.split("/")
		run_name = truncate[-1].split(".mzML")[0]		
		names = ["MS2 scan","MS1 scan"]
		accessions.sort()
		for name in accessions:
			names.append(accessionNames.get(name[0]))
		header = "\t".join(names)

		with open(path_to_output+run_name+"_depths.txt",'w') as out:
			outputFiles.append(run_name+"_depths.txt")
			print ("Creating "+run_name+"_depths.txt")
			out.write(header+"\n")
			

			count = 0 			# This is just used to keep track of the scan number since they are ordered in the mzML files
			ms2_found = False	# When ms2 scan is found, this is switched to true
			ms1_scan = -1 		# Stores the ms1 scan value associated with a set of ms2 scans
			

			# Iterates through all of the scans within a run
			for spectrum in msrun:
				count+=1
				if spectrum["ms level"] == 1:
					if ms2_found == True:
						ms2_found = False	
						ms1_scan = -1       
				else:
					if ms1_scan == -1:
						ms1_scan = count - 1 		#ms1 scan precedes all ms2 scan associated with it
						ms2_found = True        	

					# PymzML tends to read in a scan that has no associated information with it.
					# This tends to occur at the end of the mzML file, so it might just be a bug in the library.
					# This try-except block is just meant to handle these situations. It will output
					# the corresponding scan number to the terminal so you can go look at it in the mzML file later.
					try:
						values = [str(count),str(ms1_scan)]
						for name in accessions:
							values.append(str(spectrum[name[0]]))
						out.write("\t".join(values))
						out.write("\n")
					except KeyError:
						print "KeyError for scan",count,"in run",run_name
						continue			
	return outputFiles

def parseAccessionFile(path_to_file=""):
	accessions = []
	metric_names = {}
	with open(path_to_file,'r') as fin:
		for line in fin:
			line_spt = line.split("\t")
			metric_names[line_spt[0]] = line_spt[1].strip()
			accessions.append((line_spt[0],['value']))
	return accessions, metric_names
	
if __name__ == "__main__":
	kwargs = {}
	if "-input" in sys.argv:
		inputDir = sys.argv[sys.argv.index("-input") + 1]
		print "Input directory specified as ", inputDir
		kwargs["path_to_mzml"] = inputDir
	if "-output" in sys.argv:
		outputDir = sys.argv[sys.argv.index("-output") + 1]
		print "Files to be output to ",outputDir
		kwargs["path_to_output"] = outputDir
	if "-accessions" in sys.argv:
		accessions,metric_names = parseAccessionFile(sys.argv[sys.argv.index("-accessions") + 1])
		kwargs["accessionNames"] = metric_names
		kwargs["accessions"] = accessions
	parseMZML(**kwargs)
