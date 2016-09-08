## Will need to install these libraries if not already on your computer
## Parses MSCluster .clust files
## Output:
##	1) header files that contains all of the cluster headers
##	2) cluster information with header tacked on at the end, which can be used as an index for looking up info later on

##	Example)
##	Have .clust file with the following:
##		data_0_0.0	1	52.1273	0
##		0	12	2254	52.1273	1.0	0	0

## In the header file would just be:
##		data_0_0.0	1	52.1273	0

## And in the indexed file
##		0	12	2254	52.1273	1.0	0	0 	data_0_0.0	1	52.1273	0
import glob
import natsort    

def main():
	path = "*.clust"
	files=glob.glob(path)
	files_sorted = natsort.natsorted(files)			#this is so the files are read in sorted by cluster index.
	with open("data_0_0_headers.txt",'w') as headers, open("data_0_0_indexed.txt",'w') as indexed:
		for file in files_sorted:
			with open (file,'r') as f:
				current_index = " "
				for line in f:
					if line[0]=="d":		#write to header file
						headers.write(line)
						current_index = line
					elif line[0] == "0":	#write to indexed file
						update_line = line.strip()+"\t" + current_index
						indexed.write(update_line)
	return 0

main()





