#sender
import json
import requests

f = open("C:\\apache\\2020_MARCH.json", "r")
json.loads(f.read)

username = input("USERID: ")
print("Write down with 19901127")
birthday = input("birthday: ")
infection = int(input("infection: "))
locate = "01"


j = {"username": username, "birthday": birthday, "JSON_DATA": json.loads(f.read), "locate": locate, infection: infection}
f.close()
requests.post("https://www.twitchdarkbot.com/api/comseba/corona/put", json=j)