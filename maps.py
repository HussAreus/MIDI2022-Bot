import discord
import json
import functions

"""**********************************************************
						QUESTS
**********************************************************"""



class Quest:
    def __init__(self, name, lead, task, answer, spot_reward, reward, wmap):
        self.name = name
        self.lead = lead
        self.task = task
        self.answer = answer
        self.spot_reward = spot_reward #reikia prideti logikoj
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
        "RANDOM LEAD", -55, "Backdoor", "Nes zonos punktai išdėstyti panašiai kaip čia : https://preview.redd.it/hdqiy46zp4d81.jpg?width=640&crop=smart&auto=webp&s=e9de8cf506eed5720594cea33faeb67c4859efa5",
        [
            Quest("Petro Cvirkos aikštė", "https://drive.google.com/file/d/1CZbhaypo4420ee5RXrXxXeJcIjpRi1f9/view?usp=sharing", "Kur reikėtų padėti baltą figūrą, kad būtų skelbiamas Matas? https://drive.google.com/file/d/15-It7cJoKBXKXt6giqGeW8dzGHMYrBXr/view?usp=sharing", "H5/QH5", 20, 20, "backdoor"),
            Quest("Frank Zappa", "https://drive.google.com/file/d/1nCKpluYvUobjZtmZllJM6RGvUNeBaz2W/view?usp=sharing", "Kiek paukščių matote ant sienos?", "9", 20, 10, "backdoor"),
            Quest("Reformatų skveras", "Ieškokite riedulio su šiuo tekstu: „Čia, buvusiose kapinėse, bus pastatytas paminklas XVI a. Lietuvos reformacijos pradininkams.“", "Kad jau radai tokį masyvų riedulį, nusipelnei ir masyvių taškų", "23", 10, 10, "backdoor"),
            Quest("Miesto vartų sargybinio skulptūra", "Anksčiau saugojęs Vilniaus miesto vartus, dabar tebežiūri ir sergėja vieną labiausiai minusų neturinčių žmonių „pamėgtą“ kavinę-barą.", "https://drive.google.com/file/d/1nmCQI_LzOmXSVQTVxqvQmgSSHmC-wscw/view?usp=sharing", "Gediminaičių stulpai", 20, 15, "backdoor"),
            Quest("MO muziejus", "x = -4,5\ny = |8x + 32| - 1, x = [-4,5; -3,5]\ny = |8x + 24| - 1, x = [-3,5; -2,5]\ny = |8x + 16| - 1, x = [-2,5; -1,5]\nx = -1,5\ny^2 + x^2 = 1", "Kokia tai mįslė https://drive.google.com/file/d/1DC7HTVeeGeD7f3_h1TvJXM6R238D4kIC/view?usp=sharing", "23", 30, 20, "backdoor")
        ]),
    "fetus fields": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152563804692500/Naujamiestis.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155960108802058/NaujamiestisBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161169836998656/NaujamiestisBM.png?width=670&height=670"},
        "RANDOM LEAD", -35, "Fetus fields", "Ten \"augina\" žmones, tai naugė",
        [
            Quest("Vokiečių g. 24", "35 34 2E 36 37 39 36 36 30 2C 20 32 35 2E 32 38 33 30 37 30. hex", "Įeikite į kiemą ir prisiminkite 7 taisyklę", "Lietuva", 20, 15, "fetus fields"),
            Quest("Margutis", "Nors Velykos ir pasibaigė, jis čia visus metus", "Matricoje keista žinutė vertė neo sekti balta kiškį, o koki gyvūną turėjo sekti pagridninis veikėjas midi promo video?", "Melyną katiną", 20, 15, "fetus fields"),
            Quest("Skulptūra „Katinas“", "https://www.youtube.com/watch?v=ndsaoMFz9J4&ab_channel=Markiplier", "Pirmosios Matematikų dienos įvyko 11110111000 metais. Atkoduokite paslėptus metus", "1976", 20, 15, "fetus fields"),
            Quest("MIDI OFISAS", "Kur gi šitas katinas dirba? https://drive.google.com/file/d/1KAZ1DEDX86ZbgNTB7-CB7duOOSoB845c/view?usp=sharing", "Raskite atvirkštinę matrica ir parašykite skaičių eilutę, kurią sudaro skaičiai iš pagrindinės matricos įstrižainės https://drive.google.com/file/d/153CV0tmyCxEHjWogj6hdxYmzX-uv2SIn/view?usp=sharing", "1999", 20, 20, "fetus fields")
        ]),
    "mega city": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152564257673226/OnosBaznycia.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155960461107220/OnosBaznyciaBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161170109661264/OnosBaznyciaBM.png?width=670&height=670"},
        "RANDOM LEAD", -60, "Mega City", "Pats centras, pačio žemėlapio centras",
        [
            Quest("Radvilų rūmai", "Orakulė išpranašavo jiems turtus, kurių Europoje beveik niekas nebuvo matęs. Išpranašavo ir plačius laukus, aukščiausias miesto pareigas ir Europos titulus. Juodas, rudas ir našlaitėlis žengė šiais koridoriais kadaise...bet orakulė numatė ir skausmus: antrosios motinos nuodus... Dabar čia stovi palikimas jų,", "Prisimink 7 taisyklę", "Rožė", 20, 15, "mega city"),
            Quest("Skulptūra „Vilnietė“", "Panevėžietė, šiaulietė, klaipėdietė, kaunietė, o štai ir ji, X-ietė! Tik jai ši skulptūra skirta, tačiau ar sugebėsi rast tu ją?", "Cezaris 101001 pigphz BXSX xh cpjyd", "Atrask MIDI is naujo", 10, 30, "mega city"),
            Quest("Grojantis Oginskio suoliukas", "Prieš šešerius metus atidengtas, paminint jo „savininko“ 250m. gimimo progą. Reto matytas, bet dažno girdėtas. Suradus, jis leis sekundei atsikvėpti.", "https://drive.google.com/file/d/1ojfkS0s_1eb5rwSXpBnY13-Xr5bncNEQ/view?usp=sharing", "Headache", 20, 20, "mega city"),
            Quest("Žibintininko skulptūra", "Matricos šviesos nešėjas buvo Neo, o XIX amžiuje Lietuvoje nakties metu šviesos nešėjais buvo jie. Šiandien vienas jis stovi visiškai prie pat mokslo šviesos šaltinio.", "Paskambinkite žibintininkui ir pasakykite su kuo konkuravo jo dujiniai žibintai?", "Žvaigždėmis", 20, 20, "mega city"),
            Quest("Literatų gatvė", "X-as tau parodys kelią.\nPrieš lietuvių kalbos abitūros\negzaminą, menu, su klasiokais\nX dūros\nprisirūkę ir po pedesioką\npadarę iš baimės, kol mąstėm\ntemas, kurios gal ir gali\nbūti nuleistos...", "https://drive.google.com/file/d/1Bo0yQC6Zj6hR-b1luSp8iCQKK19iCHfQ/view?usp=sharing", "JERUNDA!", 20, 20, "mega city")
        ]),
    "wells and lake": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960154563749498890/GedoProspektas.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155959001501806/GedoProspektasBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161171372142592/GedoProspektasBM.png?width=670&height=670"},
        "RANDOM LEAD", -40, "Wells and Lake", "\"Wells and Lake\", nes  visi zonos punktai išdėstyti dviejose gatvėse (Gedimino prospektas ir A. Goštauto gatvė)",
        [
            Quest("Suoliukas Vytautui Kernagiui atminti", "https://drive.google.com/file/d/18jN5IT9XMbJYEeBpL5nVbhy8Q_XOnV5u/view?usp=sharing", "Suskaičiuoti plytelių aplink suoliuką neprašysime, bet paprašysime nelaukti lietaus ir pasakyti kas tai?", "aš", 20, 20, "wells and lakes"),
            Quest("Žemaitės skveras", "https://drive.google.com/file/d/1hA1IR27jGJrqTdjv1EU2iKWwLF8KMX8t/view?usp=sharing", "Kam žmogus pasakė Labą dieną?", "Vėjui", 30, 30, "wells and lakes"),
            Quest("Operos ir baleto teatras", "Šie metai, vieni iš nedaugelio, kai MIDI renginių savaitės nevainikuos legendininis/tradicinis renginys, kurio vienas iš tikslų, pasitelkiant kiek netikėtą formatą, kelti studentams aktualius klausimus bei problemas. Tačiau kas, jeigu mes esame įstrigę matricoje ir viskas aplink mus tik viena didelė apgaulė? Galbūt tik esame netinkamu laiku, netinkamoje vietoje? Pamėginkime išsiaiškinti!", "X jau dienos atėjo,\nNes studentams švenčių reikėjo,\nX jau dienos atėjo,\nNes studentams švenčių reikėjo.\nĮrašykite praleistą žodį.", "Katino", 20, 10, "wells and lakes")
        ]),
    "machine city": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152564610003024/Vyskupas.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155961132191805/VyskupasBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161170688462878/VyskupasBM.png?width=670&height=670"},
        "RANDOM LEAD", -60, "Machine City", "Nes Naujamiestis, tai tarkim moderniau",
        [
            Quest("Tauro kalnas", "Šios vietos pavadinimas siejamas su daugeliu legendų... Viena iš jų - kad šioje vietoje vaiduoklius galima išvysti ne tik Vėlinių naktį. Taip pat ši vieta ( kalnas) buvo minimas garsiausioje legendoje, kuri yra susijusi su Vilniumi.", "Šarados: 5 :kunigaikštis, Tauras, kalnas, Lietuva, kulka/os, vaiduoklis, orakulė/būrėja...", "Gediminas", 0, 10, "machine city"),
            Quest("Žaliasis Obuolys", "Pagal visų žinomą istoriją, kieno dėka buvo atrasta gravitacija. (Newtono) ir?", "Kiek matote katinukų? https://puzzel.org/jigsaw/play?p=-N0BteKriHm2Hp4wzeHi", "41", 10, 15, "machine city"),
            Quest("Berniukas su kaliošu", "„Ką galima padaryti dėl meilės? Galbūt net suvalgyti kaliošą“ - Romanas Garis", "Nekankinsime, valgyti nieko nereikalausime, pabūsime geraširdžiais ir dovanosime Jums  taškų. :)", "Gediminas", 15, 10, "machine city"),
            Quest("Provianto kvartalas", "Buvęs mažas ir gilus gyvybės šaltinis tarp naujoviškų dangoraižių. 54,6793855, 25,2582647", "Aukščiausias dangoraižis siekia net 828 metrų aukštį, o kokį gylį siekia mūsų pastatas.", "116,95/116.95", 15, 30, "machine city"),
            Quest("Nepastatyta bažnyčia (atminimo ženklas architektui Antanui Vivulskiui)", "O ne ir vėl klaida matricoje! Kadaise turėjusi būti didžiausia Lietuvoje, o gal net Europoje bažnyčia teliko tokio dydžio, kad norint į ją patekti dabar - reikėtų tapti bent 10 kartų mažesne savo versija.", "Kas už bažnyčios?", "Vilnius", 30, 20, "machine city")
        ]),
    "zion": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152565557903360/Uzupis.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155960800870421/UzupisBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161170390659152/UzupisBM.png?width=670&height=670"},
        "RANDOM LEAD", -65, "Zion", "Filme, tai yra sukilusių, atsiskyrusių žmonių miestas",
        [
            Quest("Tibeto skveras", "Nors 1959 Dalai Lama buvo išvarytas iš savo namų, iš šių jo namų jis tikrai nebūtų išvaromas", "Apsukus ratą kiek akių į tave žiūri?", "23", 20, 15, "zion"),
            Quest("Edwardo van Longuso darbai ant fasadinės UMI sienos", "https://drive.google.com/file/d/18pBgS1oWHU4qnQfTrI5O959FQ1ffyRsc/view?usp=sharing", "Kas tas hakeris?", "Ežys", 20, 10, "zion"),
            Quest("Užupio katinas", "1 Klausimas: Iš graikų kalbos kilęs žodis, buvęs oficialiu šios šalies pavadinimu iki 1935 m. Jums šį žodį rasti gali padėti 12-oji žymaus atlikėjo 2021 m. išleisto albumo „Justice“ dainos pavadinimo šaknis.\n\n2 klausimas Šis klausimas leis jums pailsėti nuo galvojimo! Tereikia parašyti vieną iš MIDI brandbook‘o spalvų.\n\n3 Klausimas: Sujunkite gautus visų klausimų atsakymus ir gausite žinomą gyvuno veislę kuri ir reiks jums surasti!", "Ką zimbolizuoja katinas?", "Drąsą/Drąsa", 30, 15, "zion"),
            Quest("Subačiaus apžvalgos aikštelė", "https://drive.google.com/file/d/1CJ4EWmcC7vNhfBsc7Y2kCMvnVCyaKmSW/view?usp=sharing Šioje vietoje rasite daugybę JŲ, tačiau jūsų užduotis - surasti tą vienitelę, kuria paliko MIDI", "Už tai kad suradai midi paliktą spyną, gausi atlygi, nemokamų taškų", "aaa", 15, 10, "zion"),
            Quest("Užupio angelas", "Matrica turi Serafimą, o ką turi Užupis", "Kol angelas stovi aukštai, kas stovi prie jo žemai?", "Kiaulė", 10, 15, "zion"),
            Quest("Užupio konstitucija", "https://drive.google.com/file/d/13styfOqDJWt3qj8lxck1DZG31qw8muPD/view?usp=sharing", "Kurias teises Užupyje Micius galėtų naudoti? (įrašykite numerį)", "13", 15, 15, "zion")
        ]),
    "capital city": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152575540363274/Katedra.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155959353819187/KatedraBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161169195278386/KatedraBM.png?width=670&height=670"},
        "RANDOM LEAD", -40, "Capital City", "Nes centras",
        [
            Quest("Sėkmės pilvas", "Atsiradus „Stebuklui“ miestelėnai iš karto suprato, kad plytelė žymi vietą norams galvoti, tačiau reikėjo suprasti, ką reikia daryti, kad noras galiausiai išsipildytų. Jeigu nepavyksta suprasti, kaip tai padaryti šioje vietoje, pakartotinai savo norą galite bandyti išpildyti apsilankę dar vienoje sėkmę nešančioje vietoje, kuri nuo plytelės yra nutolusi tik 600m.", "https://docs.google.com/document/d/1xexa6RaT8hRKS_f7TwCu8D-OKPS1miwogXkDgUsT9Uk/edit", "Čeburekai/Čeburekas", 30, 20, "capital city"),
            Quest("Katedra", "Jeigu netyčia pasiklystumėte matricoje ir nusikeltumėte atgal į praeitį einant šiuo koridoriumi galėtumėte prasilenkti su krikščionių dvasininkais ir Lietuvos kunigaikščiais. ", "Fizine užduotis", "striksintiskatinas", 10, 20, "capital city"),
            Quest("Seniausias skelbimų stulpas", "FOTO", "Kas yra X?", "seniausias skelbimų stulpas", 0, 40, "capital city")
        ]),
    "mobil avenue": WorldMap({
        "red": "https://media.discordapp.net/attachments/960152417687732245/960152638337482802/AusrosVartai.png?width=670&height=670",
        "blue": "https://media.discordapp.net/attachments/960152417687732245/960155961471954974/AusrosVartaiBP.png?width=670&height=670",
        "old": "https://media.discordapp.net/attachments/960152417687732245/960161171065929788/AusrosVartaiBM.png?width=670&height=670"},
        "RANDOM LEAD", -60, "Mobil Avenue", "Zonos vietos (vartai, kompasas, bastėja) primena ala stotį, vietą, kur vienus praleidžia, o kitų ne",
        [
            Quest("Vilniaus kompasas", "Kai Vilniuje pasimeti laike, Varpinės bokštas tau parodo laiką, o kai pasimeti erdvėje kas tau parodo kelią. ", "Kas yra tarp kapitono Artūro Dovydėno ir dizainerės Rasos Miliunaitės", "Rytai", 20, 30, "mobil avenue"),
            Quest("Vilniaus gynybinės sienos bastėja ", "Firewall apsaugo nuo kenkėjiškų programų, virusų, atakų.", "Parašyk IT supportui, kad jie gerai atlieka darbą :)", "ačiū", 15, 20, "mobil avenue"),
            Quest("Dr. Jono Basanavičiaus aikštė", " V. Kudirka turi 39 gatves pavadintas savo vardu, o Kęstučio vardu yra pavadintos net 44 gatvės. Y turi 41 gatvę pavadintą jo vardu. Suraskite Y žmogaus aikštę.", "Išspręsk lygti https://drive.google.com/file/d/1CBDYnNhwpDUqAb7dQvOZkwAbnltn8pbc/view?usp=sharing", "41", 15, 15, "mobil avenue"),
            Quest("Aušros vartai", "https://drive.google.com/file/d/1K4NlJsMVV7CHWS9iPevW1-1UOjiVJuKN/view?usp=sharing", "Ateina rytas ir aušra. Ir ateina nemokami taškai :)", "23", 15, 10, "mobil avenue"),
            Quest("Taraso Ševčenkos Paminklas", "Platus Dniepras riaumoja ir dejuoja,\nPiktas vėjas drasko lapus,\nViskas, kas yra žemiau gluosnio, linksta į žemę\nIr bangos yra didžiulės.\nIr kartais blyškus mėnulis\nUž tamsaus debesies klaidžiojo.\nKaip bangos aplenktas valtis,\nJis plūduriavo, tada dingo.", "Įveskite praleistas raides + kūrinio pavadinimą, be pirmo žodžio:\nTeka vandenys pro girią\nIr pakalnė_ bėga.\nPlūko nardo ančiukėl_ai\nPakraštį nen_rėtą.\nIš paskos vis ga_galėlis,\nO su juo antelė,\nSkabo plūdenas ir klega\nSu savais vaikeliais.", "MIDI iš po jovarėlio", 20, 20, "mobil avenue"),
        ])
}
