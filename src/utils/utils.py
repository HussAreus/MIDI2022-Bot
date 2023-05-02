import random

glitchCharacters = "あいうえおかきくけこがげぎぐごさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわをん―。～"

# Generates a glitched string from a given string


def glitch(string, probability=0.1):
    if random.random() < probability:
        new_string = ""
        for letter in string:
            if random.randint(0, 5):
                new_string += random.choice(glitchCharacters)
            else:
                new_string += letter
        return new_string
    else:
        return string


def random_string(n):
    string = ""
    for i in range(0, n):
        string += random.choice(glitchCharacters)
    return string
