import discord
import json
from typing import Dict, List

from utils.utils import random_string

MAX_GUILD_MEMBERS = 5
last_leaederboard_update = "00:00"
mapStyles = ["red", "blue", "old", "cool"]
"""
GUILD: A party of MAX_GUILD_MEMBERS
basic layout:
* Guild name: string
* Guild members: list of user IDs
* Guild leader: user ID
* Guild points: int
* Guild channel: channel ID
* Guild quest tokens: dictionary of quest tokens and whether they have been used
* Guild map tokens: list of map tokens
"""


class Guild:
    def __init__(self, leaderUID: int, name: str, channelID: int, points=0, questTokens: Dict[str, bool] = {}, mapTokens: List[str] = [], style=mapStyles[0]):
        """ Initializes a new guild """
        self.members = [leaderUID]
        self.leader = leaderUID
        self.name = name
        self.channelid = channelID
        self.points = points
        self.questTokens = questTokens
        self.mapTokens = mapTokens
        self.style = style

    def __repr__(self):
        """ Returns a string representation of the guild """
        string = "**_" + self.name + "_**\n"
        for member in self.members:
            string += "<@" + str(member) + ">\n"
        string += "Total Guild Points: " + str(self.points)
        string += "\nMaps unlocked:\n"
        for token in self.mapTokens:
            string += str(token) + "\n"
        return string

    def new_member(self, uid):
        """ Adds a new member to the guild if there is space """
        if len(self.members) < MAX_GUILD_MEMBERS and uid not in self.members:
            self.members.append(uid)
            return True
        else:
            return False

    def add_points(self, value, questToken):
        """ Adds points to the guild """
        if questToken:
            if self.questTokens[questToken]:
                return False
            else:
                self.questTokens[questToken] = True
        # First time completing the quest
        self.points += value
        with open("resources/guildlist.json", "r+") as f:
            data = json.load(f)
            data[self.name] += value
            f.seek(0)
            f.truncate()
            json.dump(data, f)
            return True

    def add_quest_token(self, token):
        """ Registers a quest token as started quest """
        if token not in self.questTokens:
            self.questTokens[token] = False
            return True
        else:
            return False

    def set_style(self, choice):
        """ Sets the map style """
        if choice in mapStyles:
            self.style = choice
            return True
        else:
            return False

    # Quite stupid implementation. TODO: make it better
    def leaderboard(self):
        try:
            with open("resources/leaderboard.json", "r") as f:
                data = json.load(f)[self.name.lower()]
                embed = discord.Embed(title="Latest leaderboards:")
                for i in range(0, len(data)):
                    embed.add_field(
                        name=data[-i][0], value="Points collected: " + str(data[-i][1]), inline=False)
                embed.set_footer(text="Last update "+last_leaederboard_update)
                return embed
        except Exception as e:
            print("functions" + str(e))
            return discord.Embed(title="Leaderboard is not prepared yet. Try again later", description="We update leaderboards every 30 minutes")

    def all_quests(self):
        """ Returns a list of all quests """
        with open("resources/quests.json", "r") as f:
            data = json.load(f)
            embed = discord.Embed(title="Quests")
            questList = ""
            qindex = 1
            for qtoken in self.questTokens.keys():
                if self.questTokens[qtoken]:
                    questList += str(qindex) + " ~~" + \
                        data[qtoken]["name"] + "~~\n"
                    qindex += 1
                else:
                    questList += str(qindex) + " " + \
                        random_string(10) + "\n"
                    qindex += 1
            embed.add_field(name="_ _", value=questList, inline=False)
            embed.set_footer(
                text="You can access already unlocked quests by typing \"quest<number>\" command")
            return embed
