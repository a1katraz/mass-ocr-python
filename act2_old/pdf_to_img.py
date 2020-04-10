import PyPDF2
from PIL import Image
from google.cloud import storage
import os

if __name__ == '__main__':

    storage_client = storage.Client.from_service_account_json('/home/vishalvivek8/key.json')
    bucket = storage_client.bucket('raw_images_ocr')
    blob = bucket.blob('docs/VoterList_ASMB_2020_BR_AC238_PartNo_1.pdf')
    
    cwd = os.getcwd()

    blob.download_to_filename(cwd+'/docs/VoterList_ASMB_2020_BR_AC238_PartNo_1.pdf')

    filepath = cwd+'/docs/VoterList_ASMB_2020_BR_AC238_PartNo_1.pdf'
    
    input1 = PyPDF2.PdfFileReader(open(filepath, "rb"))

    for x in range(0, input1.getNumPages()):
        if(x==1):
            continue

        page0 = input1.getPage(x)
        xObject = page0['/Resources']['/XObject'].getObject()
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"
            
            if xObject[obj]['/Filter'] == '/FlateDecode':
                img = Image.frombytes(mode, size, data)
                img.save(cwd+'/images/'+obj[1:] + ".png")
