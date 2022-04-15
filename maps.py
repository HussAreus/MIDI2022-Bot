import discord
import json
import functions

"""**********************************************************
						QUESTS
**********************************************************"""



class Quest:
    def __init__(self, name, lead, task, answer, reward, wmap):
        self.name = name
        self.lead = lead
        self.task = task
        self.answer = answer
        self.reward = reward
        self.map = wmap


def check_answer(uid, answer):
    guildname = functions.find_user(uid)
    guild = functions.load_guild(guildname)
    with open("quests.json", "r") as f:
        data = json.load(f)
        if answer in data.keys():
            quest = Quest(*data[answer])
            if quest.map in guild.mapTokens:
                result = guild.add_qtoken(data[answer]["name"], data[answer]["reward"])
                functions.upload_guild(guild)
                if result:
                    return 'Quest "' + str(data[answer]["name"]) + '" completed\nReward: ' + str(
                        data[answer]["reward"]) + ' points'
            else:
                return "You haven't unlocked this map"


def get_task(uid, keyword):
    guildname = functions.find_user(uid)
    guild = functions.load_guild(guildname)
    with open("quests.json", "r") as f:
        data = json.load(f)
        if keyword in data.keys():
            guild.add_qtoken(keyword)
            return data[keyword]


"""**********************************************************
						MAPS
**********************************************************"""


class WorldMap:
    def __init__(self, link, lead, price, location, description, quests):
        self.link = link
        self.lead = lead
        self.price = price
        self.location = location
        self.description = description
        self.quests = []
        for quest in quests:
            self.quests.append(quest)


def load_map(uid, location):
    guildname = functions.find_user(uid)
    guild = functions.load_guild(guildname)
    if location in map_dict.keys():
        if guild:
            if not guild.mapTokens:
                guild.mapTokens = []
            if location not in guild.mapTokens:
                guild.mapTokens.append(location)
                guild.add_points(2, None)  # Should depend on map... But idk 2 seems reasonable
                functions.upload_guild(guild)
        return create_embed(map_dict[location], guild)
    else:
        return None


def create_embed(wmap, guild):
    embed = discord.Embed(title=str(wmap.location), description=str(wmap.description))
    embed.add_field(name="OBJECTIVES:", value="_ _", inline=False)
    for quest in wmap.quests:
        if not guild.questTokens:
            guild.questTokens = []
        if quest.name not in guild.questTokens:
            embed.add_field(name="_ _", value="* " + quest.lead, inline=False)
        else:
            embed.add_field(name="_ _", value="* ~~" + quest.lead + "~~", inline=False)
    if guild.style:
        embed.set_image(url=wmap.link[guild.style])
    return embed


def buy_map(uid, numb):
    temp = {"1": "backdoor", "2": "fetus fields", "3": "mega city", "4": "wells and lake", "5": "machine city", "6": "zion", "7": "capital city", "8": "mobil avenue"}
    if numb in temp:
        guildname = functions.find_user(uid)
        guild = functions.load_guild(guildname)
        if temp[numb] not in guild.mapTokens:
            guild.add_points(map_dict[temp[numb]].price, None)
            functions.upload_guild(guild)
        return load_map(uid, temp[numb])


def load_all(uid):
    guildname = functions.find_user(uid)
    guild = functions.load_guild(guildname)
    embed = discord.Embed(title="Map objectives", description="By solving these leads you can unlock a respective map")
    i = 0
    for wmap in map_dict.keys():
        i += 1
        if guild and wmap in guild.mapTokens:
            embed.add_field(name=map_dict[wmap].location, value="~~" + map_dict[wmap].lead + "~~", inline=False)
        else:
            embed.add_field(name="Map "+ str(i), value=map_dict[wmap].lead, inline=False)
    return embed


map_dict = {
    "backdoor": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152563427180664/MOMuziejus.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155959760678932/MOMuziejusBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161169451126814/MOMusziejusBM.png?width=670&height=670"},
        "RANDOM LEAD", -4, "Backdoor", "Neturiu description",
        [
            Quest("Petro Cvirkos aikštė", "rebusas i jo kurini arba istrauka", "Fizine matrica", "23", 2, "mo"),
            Quest("Frank Zappa", "Daina", "Kazka is graficiu, nueit paziuret", "23", 2, "mo"),
            Quest("Reformatų skveras", "Ieškok riedulio su šiuo tekstu: „Čia, buvusiose kapinėse, bus pastatytas paminklas XVI a. Lietuvos reformacijos pradininkams.“", "Fizine matrica", "23", 2, "mo"),
            Quest("Miesto vartų sargybinis", "Anksčiau saugojęs Vilniaus miesto vartus, dabar tebežiūri ir sergėja vieną labiausiai minusų neturinčių žmonių „pamėgtą“ kavinę-barą.", "Fizine matrica", "23", 2, "mo"),
            Quest("MO muziejus", "rankos, funkcija MO raides", "Fizine matrica", "23", 2, "mo")
        ]),
    "fetus fields": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152563804692500/Naujamiestis.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155960108802058/NaujamiestisBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161169836998656/NaujamiestisBM.png?width=670&height=670"},
        "RANDOM LEAD", -4, "Fetus fields", "Neturiu description",
        [
            Quest("Vokiečių g. 24", "35 34 2E 36 37 39 36 36 30 2C 20 32 35 2E 32 38 33 30 37 30", "Fizine matrica", "23", 2, "mo"),
            Quest("Margutis", "Nors Velykos ir pasibaigė, jis čia visus metus", "Kazka is graficiu, nueit paziuret", "23", 2, "mo"),
            Quest("Skulptūra „Katinas“", "https://www.youtube.com/watch?v=ndsaoMFz9J4&ab_channel=Markiplier", "Fizine matrica", "23", 2, "mo"),
            Quest("MIDI OFISAS", "https://drive.google.com/file/d/1-JfMyKulnqnpLsEQI9QBeoNpwGwuTYRB/view?usp=sharing", "Fizine matrica", "23", 2, "mo")
        ]),
    "mega city": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152564257673226/OnosBaznycia.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155960461107220/OnosBaznyciaBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161170109661264/OnosBaznyciaBM.png?width=670&height=670"},
        "RANDOM LEAD", -4, "Mega City", "Neturiu description",
        [
            Quest("Radvilų rūmai", "Orakulė išpranašavo jiems turtus, kurių Europoje beveik niekas nebuvo matęs. Išpranašavo ir plačius laukus, aukščiausias miesto pareigas ir Europos titulus. Juodas, rudas ir našlaitėlis žengė šiais koridoriais kadaise...bet orakulė numatė ir skausmus: antrosios motinos nuodus... Dabar čia stovi palikimas jų, paverstas muzieju.", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Skulptūra “Vilnietė”", "Panevėžietė, šiaulietė, klaipėdietė, kaunietė, o štai ir ji, X-ietė! Tik jai ši skulptūra skirta, tačiau ar sugebėsi rast tu ją?", "Fizine matrica", "23", 2, "mo"),
            Quest("Alumnato kiemelis", "Ženki universitetiniu žingsniu ir pažvelki pro vartus. O už jų uždraustas parkas, ten sėdės tiktai Gitanas xddd (universiteto g > bromas > kiemas>nuotrauka, kur u=duotis))??? kazka su kunigais", "Fizine matrica", "23", 2, "mo"),
            Quest("Grojantis Oginskio suoliukas", "Prieš septynis metus pastatytas, paminint jo ""savininko"" 250m. gimimo progą. Reto matytas, bet dažno girdėtas. Suradus, jis leis sekundei atsikvėpti.", "Fizine matrica", "23", 2, "mo"),
            Quest("Žibintininko skulptūra", "Matricos šviesos nešėjas buvo Neo, o XIX amžiuje Lietuvoje nakties metu šviesos nešėjais buvo jie. Šiandien vienas jis stovi visiškai prie pat mokslo šviesos šaltinio. (man oficialiai nesiseka pabaigų rašyt ;-;)", "Fizine matrica", "23", 2, "mo"),
            Quest("Literatų gatvė", "X-as tau parodys kelią.\nPrieš lietuvių kalbos abitūros\negzaminą, menu, su klasiokais\nX dūros\nprisirūkę ir po pedesioką\npadarę iš baimės, kol mąstėm\ntemas, kurios gal ir gali\nbūti nuleistos...", "Fizine matrica", "23", 2, "mo")
        ]),
    "wells and lake": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960154563749498890/GedoProspektas.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155959001501806/GedoProspektasBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161171372142592/GedoProspektasBM.png?width=670&height=670"},
        "RANDOM LEAD", -4, "Gedo Prospektas", "Neturiu description",
        [
            Quest("Suoliukas Vytautui Kernagiui atminti", "rebusas i jo kurini arba istrauka", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Žemaitės skveras", "1 banknotas. Reverso puse, galima uztusuot 1 verte?", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Operos ir baleto teatras", "MIDI seniau turėjo roko opėrą. (MIDI ISTORIJA, ŽODŽIAI SUNKUS). Kur dabar galėtum pasiklausyti operos", "Fizine matrica", "23", 2, "MO Muziejus")
        ]),
    "machine city": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152564610003024/Vyskupas.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155961132191805/VyskupasBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161170688462878/VyskupasBM.png?width=670&height=670"},
        "RANDOM LEAD", -4, "Machine City", "Neturiu description",
        [
            Quest("Tauro kalnas", "Kalnas kuris buvo minimas garsiausioje legendoje ,kuri yra susijusi su Vilniumi.", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Obuolis", "Netikėtai raudonos bangos matricijoje atsirado klaida - išliko tai kas neturėjo išlikt prie pastato kuris kartais sujungia dviejų žmonių gyvenimus amžinai. (zakso - bandyk i6 hnaujo)", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Berniukas su kaliošu", "\"Ką galima padaryti dėl meilės? Galbūt net suvalgyti kaliošą\"", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Provianto kvartalas", "Buvęs mažas ir gilus gyvybės šaltinis tarp naujoviškų dangoraižių. 54,6793855, 25,2582647", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Nepastatyta bažnyčia (atminimo ženklas architektui Antanui Vivulskiui)", "O ne ir vėl klaida matricoje! Kadaise turėjusi būti didžiausia Lietuvoje, o gal net Europoje bažnyčia teliko tokio dydžio, kad norint į ją patekti dabar - reikėtų tapti bent 10 kartų mažesne savo versija.", "Fizine matrica", "23", 2, "MO Muziejus")
        ]),
    "zion": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152565557903360/Uzupis.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155960800870421/UzupisBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161170390659152/UzupisBM.png?width=670&height=670"},
        "RANDOM LEAD", -4, "Zion", "Neturiu description",
        [
            Quest("Tibeto skveras", "Nors 1959 Dalai Lama buvo išvarytas iš savo namų, iš šių jo namų jis tikrai nebūtų išvaromas", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Edwardo van Longuso darbai ant fasadinės UMI sienos", "https://drive.google.com/file/d/18pBgS1oWHU4qnQfTrI5O959FQ1ffyRsc/view?usp=sharing", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Užupio katinas", "MINČIŲ GRANDINĖLĖ(dar nera, nors yra bet dont worry about)", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Subačiaus apžvalgos aikštelė", "https://drive.google.com/file/d/1CJ4EWmcC7vNhfBsc7Y2kCMvnVCyaKmSW/view?usp=sharing", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Užupio angelas", "Matrica turi Serafimą, o ką turi Užupis", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Užupio konstitucija", "https://drive.google.com/file/d/13styfOqDJWt3qj8lxck1DZG31qw8muPD/view?usp=sharing", "Fizine matrica", "23", 2, "MO Muziejus")
        ]),
    "capital city": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152575540363274/Katedra.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155959353819187/KatedraBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161169195278386/KatedraBM.png?width=670&height=670"},
        "RANDOM LEAD", -4, "Capital City", "Neturiu description",
        [
            Quest("Sėkmės pilvas", "Anot legendos, kadaise Vilniuje gyveno skurdi šeima, kuri vos sudurdavo galą su galu. Ir, nors vaikai lakstė apdriskę ir alkani, bet visų nuostabai, jie augo nepaprastai gabūs, o subrendę tapo turtingais pirkliais ir nagingais amatininkais, gaminančiais aukštuomenei madingiausius daiktus. Vaikų motina jų sėkmę paaiškino tuo, jog tam, kuris tapo juvelyru, kas rytą glostydavo rankeles, o pirkliui - glostydavo JĮ, nes, anot jos, „ką glostai, tas ir auga“", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Katedra", "Koridoriuj tarp religijos ir valdovu", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Seniausias skelbimų stulpas", "Šalia seniausio azuolo Vilniuj, geltonoji spauda", "Fizine matrica", "23", 2, "MO Muziejus")
        ]),
    "mobil avenue": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152638337482802/AusrosVartai.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155961471954974/AusrosVartaiBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161171065929788/AusrosVartaiBM.png?width=670&height=670"},
        "RANDOM LEAD", -4, "Mobil Avenue", "Neturiu description",
        [
            Quest("Vilniaus kompasas", "Vilniuj pasiklydes, čia surasi kelia.", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Vilniaus gynybinės sienos bastėja ", "Firewall apsaugo nuo kenkėjiškų programų, virusų, atakų.", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Dr. Jono Basanavičiaus aikštė", "Kas turi 41 gatve pavadinta jo vardu", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Aušros vartai", "https://drive.google.com/file/d/1K4NlJsMVV7CHWS9iPevW1-1UOjiVJuKN/view?usp=sharing", "Fizine matrica", "23", 2, "MO Muziejus"),
            Quest("Taraso Ševčenkos Paminklas", "Platus Dniepras riaumoja ir dejuoja, /n Piktas vėjas drasko lapus, /n Viskas, kas yra žemiau gluosnio, linksta į žemę /nIr bangos yra didžiulės. /nIr kartais blyškus mėnulis /nUž tamsaus debesies klaidžiojo. /nKaip bangos aplenktas valtis, /nJis plūduriavo, tada dingo. ", "Fizine matrica", "23", 2, "MO Muziejus"),
        ])
}