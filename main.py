from json import JSONDecodeError
from urllib.error import HTTPError
from urllib.request import urlopen
import json

while True:
    try:
        a = input("Please Enter Your Minecraft Name: ")
    except KeyboardInterrupt:
        print("\nexit...")
        break

    if len(a) > 16:
        print("Username exceeds character limit.")
        continue
    elif len(a) <= 2:
        print("Username too short.")
        continue

    username_url = "https://api.mojang.com/users/profiles/minecraft/" + a

    try:
        username_response = urlopen(username_url)
    except HTTPError as e:
        code = str(e.code)
        if code == "400":
            print("user not found (error: " + code + ")")
        elif code == "329":
            print("you're being rate limited (error: " + code + ")")
        else:
            print("a http error occurred (error: " + code + ")")
        continue

    try:
        username_data = json.loads(username_response.read())
    except JSONDecodeError:
        print("This username is NOT taken (unless blocked by mojang)")
        continue

    data = username_data
    print("name: " + data["name"])
    print("UUID: " + data["id"])
    UUID = data["id"]
    uuid_url = "https://api.mojang.com/user/profiles/" + UUID + "/names"
    uuid_response = urlopen(uuid_url)
    json_data = json.loads(uuid_response.read())
    print()
    print("previous names (oldest to newest):")

    count = 0
    for name in json_data:
        print(json_data[count]["name"])
        count += 1
