import os
import datetime

file = 'posts/alexschweifer/alina_22o8-2022-05-24-13h-58m-38s.jpg'
filename = os.path.basename(file)
split = filename.split("-")
if (len(split) == 8):
    time = datetime.datetime(int(split[2]), int(split[3]), int(split[4]), int(split[5].replace('h', '')), int(split[6].replace('m', '')), int(split[7].split('.')[0].replace('s', '')))
    info = {
        "profile": split[0],
        "id": split[1],
        "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
        "fdatetime": str(time),
        "timestamp": time.timestamp()
    }
elif (len(split) == 7):
    time = datetime.datetime(int(split[1]), int(split[2]), int(split[3]), int(split[4].replace('h', '')), int(split[5].replace('m', '')), int(split[6].split('.')[0].replace('s', '')))
    info = {
        "profile": split[0],
        "datetime": time.strftime("%d. %b %Y %H:%M:%S"),
        "fdatetime": str(time),
        "timestamp": time.timestamp()
    }
else:
    print(filename)
    print(split)
print(info)