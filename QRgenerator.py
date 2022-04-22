"""
import qrcode
from PIL import Image
import random
import json
import maps

quests_data ={}
for wmap in maps.map_dict.values():
    for quest in wmap.quests:
        quests_data[quest.answer.lower()] = quest.__dict__

with open("quests.json", "w") as f:
    json.dump(quests_data, f)
    

with open("gateway.json", "r") as f:
    data = json.load(f)
with open("gateway2.json", "r") as f:
    data2 = json.load(f)
with open("quests.json", "r") as f:
    quests_data = json.load(f)

for key in data.keys():
    # Old quest per gateway ir quest faila
    old_quest = maps.Quest(*(quests_data[data[key]["answer"]].values()))
    # New quest pagal old quest pavadinima, mapa is map_dict
    new_quest = None
    for quest in maps.map_dict[old_quest.map].quests:
        if quest.name == old_quest.name:
            new_quest = quest
    # Atnaujina abu failus
    if new_quest:
        data[key] = {"answer": new_quest.answer.lower(), "spot_reward": new_quest.spot_reward}
        data2[new_quest.name.lower()] = {"answer": new_quest.answer.lower(), "spot_reward": new_quest.spot_reward}
        quests_data[new_quest.answer.lower()] = new_quest.__dict__


with open("gateway.json", "w") as f:
    json.dump(data, f)
with open("gateway2.json", "w") as f:
    json.dump(data2, f)
with open("quests.json", "w") as f:
    json.dump(quests_data, f)
"""
"""
def random_string(n):
    rand_string = ""
    for i in range(0, n):
        rand_string += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789")
    return rand_string


# Uploads current quests
with open("quests.json", "w") as f:
    quest_dict = {}
    for wmap in maps.map_dict.keys():
        for quest in maps.map_dict[wmap].quests:
            quest_dict[quest.answer] = quest.__dict__
    json.dump(quest_dict, f)


# taking image which user wants in the QR code center
logo = Image.open('../midi2.png')

# taking base width
basewidth = 100

# adjust image size
wpercent = (basewidth / float(logo.size[0]))
hsize = int((float(logo.size[1]) * float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

# generates gateway
new_dict = {}
new_dict2 = {}
with open("quests.json", "r") as f:
    data = json.load(f)
    for answer in data.keys():
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )
        # taking url or text
        quest_id = random_string(10)
        url = "quest " + quest_id

        # adding URL or text to QRcode
        QRcode.add_data(url)
        new_dict[quest_id] = {"answer": answer, "spot_reward": data[answer]["spot_reward"]}
        new_dict2[data[answer]["name"].lower()] = {"answer": answer, "spot_reward": data[answer]["spot_reward"]}
        # generating QR code
        QRcode.make()

        # adding color to QR code
        QRimg = QRcode.make_image(fill_color="black", back_color="white").convert('RGB')
        QRimg.save("../QR/" + data[answer]["name"] + ".png")
        # set size of QR code

        pos = ((QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)

        # save the QR code generated
        # QRimg.save("../QR2/" + data[answer]["name"] + ".png")
        QRimg.save("../QR2/" + data[answer]["name"] + ".png")

# For QRs

with open("gateway.json", "w") as f:
    json.dump(new_dict, f)

# for those who'll be using full names (default is by index, that eventually uses gateway.json)
with open("gateway2.json", "w") as f:
    json.dump(new_dict2, f)

QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
quest_id = random_string(10)
url = "quest " + quest_id
print(quest_id)
# adding URL or text to QRcode
QRcode.add_data(url)
# generating QR code
QRcode.make()

# adding color to QR code
QRimg = QRcode.make_image(fill_color="black", back_color="white").convert('RGB')
QRimg.save("../Vilniaus gynybinės sienos bastėja.png")
"""
