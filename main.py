import cv2
import face_recognition
import datetime
import os

# ========================
# CREATE FILE
# ========================
file_path = "Attendance.csv"

if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write("Name,Date,Time,Status\n")

# ========================
# LOAD ALL IMAGES (MULTI PERSON)
# ========================
path = "ImagesAttendance"
encodeListKnown = []
classNames = []

myList = os.listdir(path)

for file in myList:
    img = face_recognition.load_image_file(f"{path}/{file}")
    encodings = face_recognition.face_encodings(img)

    if len(encodings) > 0:
        encodeListKnown.append(encodings[0])
        classNames.append(os.path.splitext(file)[0])

print("✅ Faces Loaded:", classNames)

# ========================
# CAMERA START
# ========================
cap = cv2.VideoCapture(0)
print("📷 Camera started...")

marked = False
start_time = datetime.datetime.now()

# ========================
# LOOP
# ========================
while True:
    success, frame = cap.read()

    if not success:
        print("Camera error")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodes = face_recognition.face_encodings(rgb, faces)

    for encodeFace in encodes:
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        if len(faceDis) > 0:
            matchIndex = faceDis.argmin()

            # ✅ MATCH FOUND
            if faceDis[matchIndex] < 0.45:
                name = classNames[matchIndex]

                cv2.putText(frame, f"{name}", (50,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                if not marked:
                    now = datetime.datetime.now()
                    date = now.strftime("%Y-%m-%d")
                    time_now = now.strftime("%H:%M:%S")

                    try:
                        with open(file_path, "a") as f:
                            f.write(f"{name},{date},{time_now},Present\n")

                        print(f"✅ {name} Attendance Saved")
                    except Exception as e:
                        print("❌ File Error:", e)

                    marked = True

                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

            # ❌ NOT MATCH
            else:
                cv2.putText(frame, "CHECKING", (50,50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Face Attendance", frame)

    # ========================
    # WAIT 5 SEC → MISMATCH
    # ========================
    if (datetime.datetime.now() - start_time).seconds > 5:

        if not marked:
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
            time_now = now.strftime("%H:%M:%S")

            with open(file_path, "a") as f:
                f.write(f"Unknown,{date},{time_now},Mismatch\n")

            print("❌ Mismatch Stored")

        break

    # EXIT KEY (ESC)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# ========================
# CLEANUP
# ========================
cap.release()
cv2.destroyAllWindows()