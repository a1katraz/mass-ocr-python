from google.cloud import vision
import io
import os
#import cloudstorage
#from google.appengine.api import app_identity

#import webapp2


image_uri =  'gs://raw_images_ocr/hex_03.png'
output_uri = 'gs://raw_images_ocr/results.txt'

client = vision.ImageAnnotatorClient()
image = vision.types.Image()
image.source.image_uri = image_uri

response = client.text_detection(image=image)

#print(response.text_annotations)

print(response.text_annotations[0].description)


#bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
#self.response.headers['Content-Type'] = 'text/plain'
#self.response.write(
#        'Demo GCS Application running from Version: {}\n'.format(
#            os.environ['CURRENT_VERSION_ID']))
#self.response.write('Using bucket name: {}\n\n'.format(bucket_name))
#

#f = open(output_uri, 'wb')
#f.write(response.text_annotattions[0].description)

#f.close()

#for text in response.text_annotations:
#        print('=' * 79)
#        print(f'"{text.description}"')
        #vertices = [f'({v.x},{v.y})' for v in text.bounding_poly.vertices]
        ##print(f'bounds: {",".join(vertices)}')
