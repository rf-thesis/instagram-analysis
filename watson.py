import sqlite3
import glob
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3



pictures = "../datasets/instagram-pictures/1482144903252238041_221639390.png"
db ="../datasets/instagram.sqlite3"

conn = sqlite3.connect(db)
cur = conn.cursor()
pics = glob.glob(pictures)

watson_key = environ.get("WATSON_KEY")
visual_recognition = VisualRecognitionV3('2016-05-20', api_key=watson_key)

missing = cur.execute("""SELECT media_id, photo_url FROM instagram WHERE watson_classify IS NULL""").fetchall()
cnt = 1
tot = len(missing)
print("Total images: %s" % tot)


for m in missing[0:1]:
    url = m[1]
    media_id = m[0]
    cl = json.dumps(visual_recognition.classify(images_url=url))
    faces = json.dumps(visual_recognition.detect_faces(images_url=url))
    cur.execute("""UPDATE instagram SET watson_classify = ?, watson_faces = ? WHERE media_id = ?""", (cl, faces, media_id))

    if cnt % 100 == 0:
        print("%s processed images" % cnt)
        conn.commit()
    cnt +=1

cur.close()
conn.commit()
conn.close()

