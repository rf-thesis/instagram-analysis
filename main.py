import sqlite3
import glob
import face_recognition

pics = "../datasets/instagram-pictures/"
db ="../datasets/instagram.sqlite3"

conn = sqlite3.connect('../datasets/instagram.sqlite3')
cur = conn.cursor()

missing = cur.execute("""SELECT media_id FROM instagram WHERE python_faces IS NULL""").fetchall()
cnt = 1
tot = len(missing)
print("Total images: %s" % tot)
for m in missing:
    media_id = m[0]
    try:
        image = face_recognition.load_image_file(pics + media_id + ".png")
        face_locations = face_recognition.face_locations(image)
        faces = len(face_locations)
        cur.execute("""UPDATE instagram SET python_faces = ? WHERE media_id = ?""", (faces, media_id))
    except OSError:
        print("OSError on %s " % media_id)
        pass
    print("%s processed images" % cnt)
    if cnt % 100 == 0:
        conn.commit()
    cnt +=1

cur.close()
conn.commit()
conn.close()