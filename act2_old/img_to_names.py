import os
import PIL
from os import listdir
from os.path import isfile, join
#from names import get_names
from names_cv import get_names_cv
from headers_cv import get_headers

def filenum(fname):
    return int(fname[3:len(fname)-4])

def get_files(cwd):
    dirpath = cwd+'/images'
    files = [f for f in listdir(dirpath) if isfile(join(dirpath, f))]
    files.sort()
    #files.pop(0)								#remove that first file name
    files.sort(key=filenum)
    for x in range(0, len(files)):
        files[x] = dirpath + "/" + files[x]		
    
    return files
		
	
if __name__ == '__main__':
    cwd = os.path.abspath(os.getcwd())
    f_names = get_files(cwd)
    f = open(cwd+'/results.csv', 'w+')
    f.write('Election Year, Assembly constituency, AC No, AC Reservation, \
		Parliamentary Constituency, PC No, PC Reservation, Part No., \
		EPRD, Booth Name, Booth No, PIN Code, Serial No, \
            	Voter ID, Voter Name, Fathers name, Age, Gender, Address details, Voter Surname,\
		Grouped Surname, Linked Caste, ERRORS\n')
    
    serial = 1
    #len(f_names)-1-2
    ####### Get Header Details
    header_details = get_headers(f_names[0])

    for x in range(1, len(f_names)-2):
        name_list, counter = get_names_cv(f_names[x], serial)
        for name_tuple in name_list:
            #	print >> f, name_tuple
            name_tuple = header_details + name_tuple
            f.write(','.join(str(item) for item in name_tuple))
            f.write('\n')

        f.flush()
        serial = serial + counter
            
    f.close()
		
	
