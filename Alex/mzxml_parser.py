## You will need to install glob and xmltodict
## Make sure to pay attention to the file paths, including whether you are on a Linux or Windows OS
## If running on Windows, file paths will need to replace / with \\

from os import path
import glob
import xmltodict

## Enter all file paths in Linux style
def parseMZXML(path_to_mzml=''):
	delim = ''
	if path_to_mzml != '' and path_to_mzml[-1:] != '/':
		delim = '/'
	file_path = path.normpath(delim.join([path_to_mzml,"*.mzML"])) 		# File path
	
	

	files=glob.glob(path)	# Finds all mzXML files in the current directory
	for a_file in files:
		pre = a_file.split(".")			# gets the run
		with open(a_file,'r') as fin, open(pre[0]+"_depths_new.txt",'w') as out:
			print ("Creating "+pre[0]+"_depths_new.txt")
			out.write("MS2 Scan\tMS1 Scan\tScan Start Time\tBase Peak m/z\tBase Peak Intensity\tMS1 Precursor Intensity\n")
			msrun = xmltodict.parse(fin.read())
			count = 0 			# This is just used to keep track of the scan number since they are ordered in the mzML files
			ms2_found = False	# When ms2 scan is found, this is switched to true
			

			# Iterates through all of the scans within a run
			scans = msrun['mzXML']['msRun']['scan']
			for spectrum in scans:
				if int(spectrum["@msLevel"]) != 1:
					try:
						out.write("\t".join([spectrum["@num"],spectrum["precursorMz"]["@precursorScanNum"],"Not Listed",spectrum["@basePeakMz"],spectrum["@basePeakIntensity"],spectrum["precursorMz"]["@precursorIntensity"]]))
						out.write("\n")
					except:
						print count
						continue
					

	return None


def main():
	parseMZXML()
	return 0

if __name__ == "__main__":
	main()