import io
from PIL import Image
import os
from bord import find_boxes
import pytesseract
import argparse
import os
import re
import cv2


def get_names_cv(filepath, serial):
    cwd = os.path.abspath(os.getcwd())
    print ('Reading file:'+filepath.split('/')[-1])
    im = Image.open(filepath)
    ##### Get Election Type and  Constituency Name
    #try:
    #    im = Image.open(filepath)
    #    crop_rectangle = (40, 10, 600, 40)
    #    im_crop = im.crop(crop_rectangle)	
    #    texts = pytesseract.image_to_string(im_crop, lang='hin')
    #    election_name = ''
    #    constituency_name = ''
    #    if (len(texts) > 0 and ':' in texts):
    #        election_name = texts.split(",")[0].strip()
    #        constituency_name = texts.split(":")[1].strip()
    #except:
    #    election_name = 'ERROR'
    #    constituency_name = 'ERROR'
    #    pass
    #
    ####Get Header Address
    #try:
    #    crop_rectangle = (40, 50, 300, 90)
    #    im_crop = im.crop(crop_rectangle)
    #    texts = pytesseract.image_to_string(im_crop, lang='hin')
    #    major_address = ''
    #    if (len(texts) > 0 and ':' in texts):
    #        major_address = texts.split('\n')[0].split(":")[2].strip()				# dont' read anything apart from the first line
    #        #	print(major_address)
    #except:
    #    major_address = 'ERROR'
    #    pass
    #
    ##### Get Part Number
    #try:
    #    crop_rectangle = (990, 10, 1130, 35)
    #    im_crop = im.crop(crop_rectangle)
    #    w, h = im_crop.size
    #    im_crop_mag = im_crop.resize((w*3, h*5), Image.ANTIALIAS)
    #    texts = pytesseract.image_to_string(im_crop_mag, lang='eng', config='--psm 7 -c tessearct_char_whitelist=0123456789')
    #    part_number = ''
    #    part_number = texts.strip()
    #except:
    #    part_number = 'ERROR'
    #    pass
    #
    ####Get Voter Details
    counter = 1
    boxes = find_boxes(filepath)
    outcomes = list()
    prev_serial = serial - 1     
    
    for box in boxes:
        print ('Reading voter counter: '+str(counter))
        try:
	    ### Get Boundign Box
            crop_rectangle = (box[0], box[1], box[2], box[3])
            im_crop = im.crop(crop_rectangle)
	   
	    ####Get Serial Num
            crop_rectangle = (7, 2, 80, 20)
            im_serial = im_crop.crop(crop_rectangle)
            w, h = im_serial.size
            im_serial_mag = im_serial.resize((w*3, h*5), Image.ANTIALIAS)
            texts = pytesseract.image_to_string(im_serial_mag, lang='eng', config='--psm 7 -c tessedit_char_whitelist=0123456789')
            serial_num = texts.strip()
            if(not(serial_num.isdigit()) or int(serial_num) != prev_serial + 1):
              serial_num = str(prev_serial + 1)
	    
            ### Get Name and Father's Name
            crop_rectangle = (4, 21, 269, 136)
            im_main = im_crop.crop(crop_rectangle)
            
            texts = pytesseract.image_to_string(im_main, lang='hin')
            lines = texts.split('\n')
            
            for linex in lines:
                if (linex.strip() == ''):
                    lines.remove(linex)

            voter_det = ['', '', '', '', '']
            voter_det[0] = lines[0].split(":")[1].strip()					#name
            voter_det[1] = lines[1].split(":")[1].strip()					#father's name
                
            #####Get House No
            crop_rectangle = (59, 48, 100, 65)
            im_house = im_main.crop(crop_rectangle)
            w, h = im_house.size
            # Blow up image to get the characters clearly
            im_house_mag = im_house.resize((w*5, h*5), Image.BICUBIC)
            texts = pytesseract.image_to_string(im_house_mag, lang='eng', config='--psm 7 -c tessedit_char_whitelist=0123456789')
            voter_det[2] = texts.strip()									#house no
            #print ('House No:' + texts)
                
	    #####Get Age
            crop_rectangle = (32, 66, 55, 85)
            im_age = im_main.crop(crop_rectangle)
            w, h = im_house.size
            # Blow up image to get the characters clearly
            im_age_mag = im_age.resize((w*3, h*5), Image.BICUBIC)
            texts = pytesseract.image_to_string(im_age_mag, lang='eng', config='--psm 7 -c tessedit_char_whitelist=0123456789')
            voter_det[3] = texts.strip()									#age
            #print('Age: '+texts)
                
            #####Get Gender
            crop_rectangle = (95, 65, 160, 84)
            im_gender = im_main.crop(crop_rectangle)
            #im_gender.show()
            #im_gender_mag = im_gender.resize((w*3, h*3), Image.BILINEAR) 
            texts = pytesseract.image_to_string(im_gender, lang='hin', config='--psm 7')
            voter_det[4] = texts.strip()									#gender
            if(voter_det[4].startswith('प')):
                voter_det[4] = 'Male'
            else:
                voter_det[4] = 'Female'
            #print('Gender: ' + texts)		
                    
            ######Address Correction for special characters:
            voter_det[2] = voter_det[2].replace('।', '1')
            voter_det[2] = voter_det[2].replace('॥', '11')
            
	    #####Voter Card 
            crop_rectangle = (150, 1, 372, 25)
            im_code = im_crop.crop(crop_rectangle)
            w, h = im_code.size
            im_code_mag = im_code.resize((w*2, h*2), Image.BICUBIC) 
            texts = pytesseract.image_to_string(im_code_mag, lang='eng')
	    #print (texts)
            voter_card = ''
            error_switch = 'FALSE'

            if(len(texts) > 0):
                voter_card = re.sub(r"[^a-zA-Z0-9]+", '/', texts.strip()).lstrip('1234567890,.').rstrip('/')
                if(voter_card.startswith('BR/') and len(voter_card)>=16):
                    voter_card = voter_card
                elif (len(voter_card)>=10):
                    voter_card = voter_card
                else:
                    voter_card = voter_card+'_ERROR'

            if(voter_card.endswith('_ERROR')):
                error_switch = 'TRUE'
					
	    ####Voter's surname is person's last name if male or father's last name if not male
            voter_surname = ''
            if(voter_det[4] == 'Male'):
                if(len(voter_det[0].split(" "))>1):
                    voter_surname = voter_det[0].split(" ")[-1]
            else:
                if(len(voter_det[1].split(" "))>1):
                    voter_surname = voter_det[1].split(" ")[-1]
	    
            if(error_switch=='FALSE'): 
                single_tuple = list()
                single_tuple.extend((serial_num, \
                               voter_card, voter_det[0], voter_det[1], voter_det[3], voter_det[4], voter_det[2], \
                               voter_surname, '', '', error_switch))
                outcomes.append(single_tuple)
        
        except Exception as e:
            #pass
            print('Error in reading voter details for:' + str(counter) + ' Error:'+str(e))
        
        finally:
            prev_serial = serial
            counter = counter + 1
            serial = serial + 1    
            
    return outcomes, counter - 1;
