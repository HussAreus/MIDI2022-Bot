import qrcode
from PIL import Image
import random
import json

import commands.mapCommands as mapCommands


def generateQuestsJSON():
    quests_data = {}
    for wmap in mapCommands.map_dict.values():
        for quest in wmap.quests:
            quests_data[quest.answer.lower()] = quest.__dict__

    with open("resources/quests.json", "w") as f:
        json.dump(quests_data, f)


def generateQuestSearchMapJSONs(keep_old_ids=True):
    if keep_old_ids:
        try:
            with open("resources/idtoansw.json", "r+") as f:
                old_id_to_answ = json.load(f)
        except FileNotFoundError:
            print(
                "Error: idtoansw.json not found. If you want to generate new IDs, set keep_old_ids to False")
    new_id_to_answ = {}
    name_to_answ = {}
    for map in mapCommands.map_dict.values():
        for quest in map.quests:
            # Generate new / gets old id
            quest_id = random_string(10)
            if keep_old_ids:
                quest_id = next(
                    (key for key in old_id_to_answ if old_id_to_answ[key]['answer'] == quest.answer.lower()), None)
                if not quest_id:
                    print(
                        "Error: Quest ID not found. Check idtoansw.json. If you want to generate new IDs, set keep_old_ids to False")
                    return False
            else:
                while quest_id in new_id_to_answ:
                    quest_id = random_string(10)

            new_id_to_answ[quest_id] = {"answer": quest.answer.lower(
            ), "spot_reward": quest.spot_reward}
            name_to_answ[quest.name.lower()] = {
                "answer": quest.answer.lower(), "spot_reward": quest.spot_reward}

    with open("resources/idtoansw.json", "w+") as f:
        json.dump(new_id_to_answ, f)
    with open("resources/nametoansw.json", "w+") as f:
        json.dump(name_to_answ, f)


def random_string(n):
    rand_string = ""
    for i in range(0, n):
        rand_string += random.choice(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789")
    return rand_string


def generateQRCodes():
    # taking image which user wants in the QR code center
    logo = Image.open('resources/midi.png')

    # taking base width
    basewidth = 100

    # adjust image size
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

    with open("resources/quests.json", "r") as f:
        questData = json.load(f)

    with open("resources/idtoansw.json", "r") as f:
        id_to_answ = json.load(f)
        for quest_id in id_to_answ:
            QRcode = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H
            )
            # taking url or text
            url = "quest " + quest_id

            # adding URL or text to QRcode
            QRcode.add_data(url)
            QRcode.make()

            # adding color to QR code
            QRimg = QRcode.make_image(
                fill_color="black", back_color="white").convert('RGB')
            # save the QR code generated
            QRimg.save(
                "QR/" + questData[id_to_answ[quest_id]["answer"]]["name"] + ".png")

            # set size of logo
            pos = ((QRimg.size[0] - logo.size[0]) // 2,
                   (QRimg.size[1] - logo.size[1]) // 2)
            QRimg.paste(logo, pos)
            # save the QR code generated with logo
            QRimg.save("QRlogo/" +
                       questData[id_to_answ[quest_id]["answer"]]["name"] + ".png")


"""
# Uncomment to generate required files
generateQuestsJSON()
generateQuestSearchMapJSONs(False)
generateQRCodes()
"""
