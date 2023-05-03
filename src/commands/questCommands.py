import json
import discord

from utils.utils import glitch
import commands.guildCommands as guildCommands


class Quest:
    def __init__(self, name: str, lead: str, task: str, answer: str, spot_reward: int, reward: int, map: str):
        self.name = name
        self.lead = lead
        self.task = task
        self.answer = answer
        self.spot_reward = spot_reward
        self.reward = reward
        self.map = map


def check_answer(uid: int, answer: str):
    """ Checks if answer maps to any quest and adds points to the guild """
    with open("resources/quests.json", "r") as f:
        data = json.load(f)
        if answer in data:
            quest = Quest(*data[answer].values())
            guild = guildCommands.get_user_guild(uid)
            if guild and quest.map in guild.mapTokens:
                # result is 0 if quest is already completed
                result = guild.add_points(quest.reward, quest.answer.lower())
                guildCommands.upload_guild(guild)
                if result:
                    return 'Quest "' + str(quest.name) + '" completed\nReward: ' + str(
                        quest.reward) + ' points'
            else:
                return "You haven't unlocked this map"

# TODO: Rename get_quest and load_quest
def get_quest(uid: int, quest_id: str):
    """ Finds quest answer based on quest id. Adds points for finding the quest"""
    with open("resources/idtoansw.json", "r") as f:
        data = json.load(f)
        if quest_id in data.keys():
            guild = guildCommands.get_user_guild(uid)
            answer = data[quest_id]["answer"]
            if guild.add_quest_token(answer):
                guild.add_points(data[quest_id]["spot_reward"], None)
                guildCommands.upload_guild(guild)
                return load_quest(answer, True)
            return load_quest(answer, False)
    """ Finds quest answer based on quest name. Adds points for finding the quest"""
    with open("resources/nametoansw.json", "r") as f:
        data = json.load(f)
        if quest_id.lower() in data.keys():
            guild = guildCommands.get_user_guild(uid)
            answer = data[quest_id.lower()]["answer"]
            if guild.add_quest_token(answer):
                guild.add_points(data[quest_id.lower()]["spot_reward"], None)
                guildCommands.upload_guild(guild)
                return load_quest(answer, True)
            return load_quest(answer, False)


def load_quest(answer: str, new: bool):
    """ Loads quest from quests.json and returns description"""
    with open("resources/quests.json", "r") as f:
        quest = json.load(f)[answer]
        embed = discord.Embed(title=quest["name"], description=quest["task"])
        if new:
            embed.set_footer(text=glitch(
                "Reward for unlocking this quest: ") + str(quest["spot_reward"]))
    return embed
