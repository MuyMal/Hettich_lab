import glob

## Author: Alex Cope
## Use this to collect information from MSCuster, ScanRanker, and mzMl files, as well as generate matrices
## Wasn't for sure how to generalize this one so it works for everyone with relatively few issues. Ask me 
## if you need help.

## If have different cluster groups, such as assigned and unassigned, you should call createMatrix() and combineData() with an argument
## that will differentiate between the output for the functions. Otherwise, if you leave these as the default values, the output of the second
## function calls will overwrite the output of the first function calls. For example, if you have assigned and unassigned clusters, you
## will want to call combineData("assigned") and combineData("unassigned"). Similarly, call createMatrix(1290442, "assigned") and createMatrix(5425990,"unassigned")


## Create a list of files that serve as keys for mzml_dict and scan_dict
## Setup so file index from MSCluster file I generated will correspond to the index of the file in the array
## Might be a better way to do this
def createFileList(): 
	file_list = []
	with open("assigned_list.txt") as fin: ## I just use this to create the file names that will be used as keys in mzml_dict and scan_dict
		index = 0
		for line in fin:
			line = line.strip().split("\\")
			entry = line[5].split("_assigned")[0]
			value = ("MSCluster/New_depth/" + entry + "_depths.txt", "MSCluster/ScanRanker_Test/"+ entry +"-ScanRankerMetrics-adjusted.txt")
			file_list.append(value)


## creates the mzml_dict, which is indexed by file names. Each file points to a sub-dictionary which is indexed by the MS2 scan number. The values of these dictionaries are
## lists that store the values we are going to use.
def createMzMLDict():
	mzml_dict = {}
	path = "*_depths.txt"
	files = glob.glob(path)
	for name in files:
		indices = {}
		with open(name,"r") as fin:
			fin.readline()			#reads past header
			for line in fin:
				values = []
				line_spt = line.split()
				values = [line_spt[0],line_spt[2],line_spt[5]] #currently stores MS2 scan number, Scan start time, and MS1 precursor intensity
				indices[line_spt[0]] = values          ## each sub-dictionary is indexed by MS2 scan number
			mzml_dict[name] = indices
	return None
				

## Functions in a similar fashion to createMzMLDict()
def createScanDict():
	scan_dict = {}
	path = "MSCluster/ScanRanker/*-adjusted.txt"
	files=glob.glob(path)
	for name in files:
		indices = {}
		with open(name,'r') as fin:
			for line in fin:
				if line[0] == "H": # skip header
					continue
				values = []
				line_spt = line.strip().split()
				
				values = [line_spt[3][5:],line_spt[4], line_spt[5], line_spt[6], line_spt[10],line_spt[11]] # MS2 scan numebr, precursor m/z, charge, 
																											# precursor mass, scan ranker score, adjusted scan ranker score
				indices[line_spt[3][5:]] = values
			scan_dict[name] = indexes
	return scan_dict


## Creates 2 matrices for both assigned and unassigned folders. One matrix represents the number of members for that cluster in a given file, the other
## represents the summed MS1 precursor intensities. Note that files in this case are condensed down to the 42 runs. This will likely need to be changed on case-by-case basis
## You will need to know how many clusters you have and pass this value into the function.
def createMatrix(j_range = 0 ,entry = "data"):
	# j_range = 0
	# if entry == "assigned":
	# 	j_range = 1290442
	# else:
	# 	j_range = 5425990
	if j_range == 0:
		print "You need to pass in the number of clusters as an argument to this function."
		sys.exit(1)
	with open(entry+"_collective.txt","r") as fin, open(entry+"_clust_mem_matrix.txt","w") as out_1, open(entry+"_pre_intensity_matrix.txt","w") as out_2:
		clust_matrix = [[0 for i in range(0,42)] for j in range(0,j_range)]
		int_matrix = [[0.0 for i in range(0,42)] for j in range(0,j_range)]
		fin.readline()
		for line in fin:
			line = line.split()
			clust = int(line[12].split(".")[1])
			f_index = int(line[0])/11	
			clust_matrix[clust][f_index] = clust_matrix[clust][f_index] + 1
			int_matrix[clust][f_index] = int_matrix[clust][f_index] + float(line[10])
		for i in xrange(0,42):			
			out_1.write("".join(["\t",str(i)]))
			out_2.write("".join(["\t",str(i)]))
		out_1.write("\n")
		out_2.write("\n")
		for i in xrange(0,j_range):
			for j in xrange(0,42):
				if j == 0:
					out_1.write("".join([entry,"_0_0.",str(i)]))
					out_2.write("".join([entry,"_0_0.",str(i)]))
				out_1.write("".join(["\t",str(clust_matrix[i][j])]))
				out_2.write("".join(["\t",str(int_matrix[i][j])]))
			out_1.write("\n")
			out_2.write("\n")
	return None



def combineData(entry = "data"):
	print "Creating Dictionaries"
	file_list = createFileList(file_list)
	mzml_dict = createMzMLDict_2(mzml_dict)
	scan_dict = createScanDict(scan_dict)
	print "Done...Collecting information for collective files"
	with open(entry+"_indexed.txt","r") as fin, open(entry+"_collective_test.txt","w") as out:
		out.write("File_Index_Number\tTarget_MS2_Scan\tScan_Index_Num\tNative_ID\tm/z\tPrecursorMZ\tCharger\tPrecursor_Mass\tScanRankerScore\tAdjusted_ScanRanker_Score\tMS1_Precursor_Intensity\tMS2_Start_Time\tCluster_Index\tSimilarity_Score\tp-value\tNum_Cluster_Members\tCluster_m/z\n")
		for line in fin:
			line_spt = line.split()
			file_index = int(line_spt[1])
			scan_index = line_spt[2]
			mzml_sub_dict = mzml_dict.get(file_list[file_index][0])
			scan_sub_dict = scan_dict.get(file_list[file_index][1])
			mzml_values = mzml_sub_dict.get(scan_index)
			sr_values = scan_sub_dict.get(scan_index)
			out.write("\t".join([str(file_index),mzml_values[0],scan_index,sr_values[0],line_spt[3],sr_values[1],sr_values[2],sr_values[3],sr_values[4],sr_values[5],mzml_values[2],mzml_values[1],line_spt[7],line_spt[4],line_spt[5],line_spt[8],line_spt[9]]))
			out.write("\n")
	return None
	
def main():
	combineData()
	print "Done...creating data matrices"
	createMatrix()
	return 0

if __name == "__main__":	
	main()
