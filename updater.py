import face_recognition
import glob
from models import *
import os
import time
from elasticsearch import Elasticsearch
import requests
import config

db_eng = db_connect()
db_session = create_db_session(db_eng)
es = Elasticsearch(host=config.es_host, port=config.es_port, request_timeout=45)
start = time.time()


filename = "current.png"
images = db_session.query(Insta).filter_by(n_faces=None).all()
n_images = len(images)
print("Analyzing %s images" % n_images)

cnt = 1.0
for file in images:
    img = file.media_id
    url = file.photo_url
    r = requests.get(url, stream=True)
    
    if r.status_code == 200:
        with open("current.png", 'wb') as f:
            for chunk in r:
                f.write(chunk)

        image = face_recognition.load_image_file(filename)
        face_locations = face_recognition.face_locations(image)
        faces = len(face_locations)
        current = db_session.query(Insta).filter_by(media_id=img).first()
        current.n_faces = faces
        db_session.commit()
        es_insta = {"doc": {"n_faces": faces}}
        try:
            result = es.update(index="instagram", doc_type="insta",
                               id=img, body=es_insta,
                               request_timeout=30)
        except:
            pass
            # print("\t - found %s faces in image %s" % (faces, img))

        if cnt % 10 == 0:
            print("%.2f%%, %.f images done, %.2f seconds"
                  % (cnt / n_images * 100, cnt, time.time() - start))

    cnt += 1
print("Total time: %.2f seconds" % (time.time() - start))
