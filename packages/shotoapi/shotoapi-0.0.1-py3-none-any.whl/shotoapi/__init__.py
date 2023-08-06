import requests
import json
import base64

class ShotoApi:
    
    def __init__(self):
        self.apiversion=""

    def apikey(self,key):
        self.headers = {
            'Bearer': key,
            'accept' : 'application/json'
            }

    def endpoint(self,endpoint):
        self.endpoint=endpoint

    def study(self,studyname):
        self.study=studyname
        
    def search_face(self,image):
        url = self.endpoint+"deep/study/search_face/"
        with open(image, 'rb') as img:
            files = {'image': img.read()}
            payload = {'study':self.study}
            r = requests.post(url, headers=self.headers, files=files, data=payload)
            return json.loads(r.text)

    def enconding_faces(self,image,name):
        url = self.endpoint+"deep/study/enconding_faces/"
        with open(image, 'rb') as img:
            files = {'image': img.read()}
            payload = {'name':name,
                      'study':self.study}
            r = requests.post(url, headers=self.headers, files=files, data=payload)
            return json.loads(r.text)
        
    def analysis_faces(self,image):
        url = self.endpoint+"deep/analysis_img/"
        with open(image, 'rb') as img:
            files = {'image': img.read()}
            payload = {'name':"name"}
            r = requests.post(url, headers=self.headers, files=files, data=payload)
            return json.loads(r.text)   
        
    def compare_faces(self,image1,image2, stream=True):
        url = self.endpoint+"deep/compare_faces/"
        with open(image1, 'rb') as img:
            image1=img
            with open(image2, 'rb') as img:
                image2=img
                files = {'image1': image1.read(),
                         'image2': image2.read()
                        }
                payload = {'name':"name"}
        r = requests.post(url, headers=self.headers, files=files, data=payload)
        return json.loads(r.text)
        
    def extract_faces(self,image):
        url = self.endpoint+"deep/extract_faces/"
        with open(image, 'rb') as img:
            files = {'image': img.read()}
            payload = {'name':"name"}
            r = requests.post(url, headers=self.headers, files=files, data=payload, stream=True)
            return r.raw.read()
                  
    def count_faces(self,image):
        url = self.endpoint+"deep/detect_faces/"
        with open(image, 'rb') as img:
            files = {'image': img.read()}
            payload = {'name':"name"}
            r = requests.post(url, headers=self.headers, files=files, data=payload, stream=True)
            return r.raw.read()
        
    def search_face_study(self,study):
        url = self.endpoint+"deep/study/search_face_study/?study="+study
        r = requests.get(url, headers=self.headers, stream=True)
        return json.loads(r.text)

    def image_faceid(self,faceid):
        url = self.endpoint+"deep/study/image_faceid/?faceid="+faceid
        r = requests.get(url, headers=self.headers, stream=True)
        load=json.loads(r.text)
        image_code = load[0]['photo']
        byte_image= base64.b64decode(image_code)      
        return byte_image

    def image_serachid(self,searchid):
        url = self.endpoint+"deep/study/image_searchid/?serachid="+searchid
        r = requests.get(url, headers=self.headers, stream=True)
        load=json.loads(r.text)
        image_code = load[0]['photo']
        byte_image= base64.b64decode(image_code)      
        return byte_image
        
    
    
    def delete_face_study(self,faceid):
        url = self.endpoint+"deep/study/delete_face_study/"+faceid
        r = requests.delete(url, headers=self.headers, stream=True)
        return json.loads(r.text)

                  
    def image_barcode(self,image):
        url = self.endpoint+"image/barcode/"
        with open(image, 'rb') as img:
            files = {'image': img.read()}
            payload = {'name':"name"}
            r = requests.post(url, headers=self.headers, files=files, data=payload, stream=True)
            return r.raw.read()
        
    def image_ocr(self,image):
        url = self.endpoint+"image/ocr/"
        with open(image, 'rb') as img:
            files = {'image': img.read()}
            payload = {'name':"name"}
            r = requests.post(url, headers=self.headers, files=files, data=payload, stream=True)
            return r.raw.read()
