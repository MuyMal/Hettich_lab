## Alex Cope
## 4-22-2016
## Parse mzML files, pulls 
from pymzml import *
from os import path
import glob


## You will need to install pymzml and glob
## Make sure to pay attention to the file paths, including whether you are on a Linux or Windows based OS
## For simplicity, enter all file paths in Linux style. path.normpath() should handle these case if on
## Windows OS
def parseMZML(path_to_mzml=''):
	# File Path
	delim = ''
	if path_to_mzml != '' and path_to_mzml[-1:] != '/':
		delim = '/'
	file_path = path.normpath(delim.join([path_to_mzml,"*.mzML"])) 		# File path
	print file_path
	files=glob.glob(file_path)	# Finds all mzML files in the current directory
	for a_file in files:

		## If you want to pull any other accessions from the mzML files, add them to the extraAccessions array
		msrun = run.Reader(a_file,extraAccessions=[('MS:1000042',['value']),("MS:1000016",['value']),("MS:1000504",["value"]),("MS:1000505",["value"])]) 
		
		pre = a_file.split(".")			# gets the run
		
		 
		# File Path
		with open(pre[0]+"_depths_test_new.txt",'w') as out:
			print ("Creating "+"New_depth/"+pre[0]+"_depths_test_new.txt")
			out.write("MS2 Scan\tMS1 Scan\tScan Start Time\tBase Peak m/z\tBase Peak Intensity\tMS1 Precursor Intensity\n")
			

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
						ms1_scan = count - 1 		# since the ms1 scan precedes all ms2 scan associated with it
						ms2_found = True        	

					# PymzML tends to read in a scan that has no associated information with it.
					# This tends to occur at the end of the mzML file, so it might just be a bug in the library.
					# This try-except block is just meant to handle these situations. It will output
					# the corresponding scan number to the terminal so you can go look at it in the mzML file later.
					try:
						out.write("\t".join([str(count),str(ms1_scan),str(spectrum["MS:1000016"]),str(spectrum["MS:1000504"]),str(spectrum["MS:1000505"]),str(spectrum["MS:1000042"])]))
						out.write("\n")
					except KeyError:
						print count
						continue
					
				
	return None

def main():
	parseMZML()
	return 0

if __name__ == "__main__":
	main()
