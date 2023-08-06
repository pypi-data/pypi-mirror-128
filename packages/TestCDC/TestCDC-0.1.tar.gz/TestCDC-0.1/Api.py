from flask import Flask, jsonify

app = Flask(__name__)

# Characters
# Wheel of Time
db = [{'id': "0", 'name': "Moiraine Sedai", 'gender': "Female",
       'description': "Moiraine says she has come to the Two Rivers in search of the one who will save or destroy the "
                      "world — but ask of her intentions and you’ll be met with cold stares and heavy silence. Aes "
                      "Sedai may never speak that which is not true, making her silence all the more concerning. Will "
                      "she protect the Dragon Reborn, whomever they may be, or are her intentions more nefarious?"},
      {'id': "1", 'name': "Egwene", 'gender': "Female",
       'description': "Innkeeper’s daughter, promised to Rand al’Thor, apprentice to Nynaeve... It all seems "
                      "inconsequential in light of the possibilities that lay before Egwene. Could she truly be a "
                      "powerful channeler, and perhaps even the Dragon Reborn? Whether or not what Moiraine suggests "
                      "is true, it’s beginning to seem that Egwene is far more powerful — and more important — than "
                      "she could have ever imagined."},
      {'id': "2", 'name': "Rand", 'gender': "Male",
       'description': "Rand doesn’t trust Moiraine. Her veiled intentions, and the forces of evil that seem to follow "
                      "her, make her a threat in his eyes. He is brash, impulsive, and impossibly stubborn, "
                      "but he’s driven to protect those he loves. If he’s not the one Moiraine seeks, he will still "
                      "do everything in his power to save them from whatever she has planned. But if he is, "
                      "perhaps he has the power to protect them all."},
      {'id': "3", 'name': "Mat", 'gender': "Male",
       'description': "Most see Mat as a witty, mischievous rogue — which he certainly is — but deep down, Mat fears "
                      "he’s a bastard like his father; a drunk like his mother. If this Dragon Reborn business comes "
                      "with responsibility, he’s not interested. But perhaps, whether or not he’s who Moiraine is "
                      "looking for, it can be his ticket to a better life."},
      {'id': "4", 'name': "Perrin", 'gender': "Male",
       'description': "Perrin is a kind, gentle soul woven into a powerful and physically imposing form. He takes as "
                      "much care in forming his words and actions as he would a fine blade on his forge. He strives "
                      "to avoid inadvertently harming others — physically or emotionally — yet his anger, "
                      "when provoked, is truly terrifying. Perrin has yet to unleash the full ferocity of his power, "
                      "and he hopes to keep it that way."},
      {'id': "5", 'name': "Nynaeve", 'gender': "Female",
       'description': "Nynaeve’s stubborn nature and brash self-righteousness were necessary tools of the trade when "
                      "she became the youngest Wisdom the Two Rivers had ever seen. And now it seems her inherent "
                      "ability to Listen to the Wind and profound aptitude for healing may be mere glimpses of her "
                      "true potential. She has no trust for Aes Sedai, but she will do what she must to find the "
                      "others from the Two Rivers and keep them safe."},
      {'id': "6", 'name': "Lan Mandragoran", 'gender': "Male",
       'description': "Lan is a man of honor, driven by duty. As Moiraine’s Warder, his commitment to her quest is "
                      "unwavering. Were you somehow able to gain his trust, you would find his stoic face and "
                      "propensity for silence mask an endearing depth and complexity of character. Still, "
                      "it’s best not to let your guard down around him. After all, there are few things more "
                      "formidable than an Aes Sedai and her Warder."}]


@app.route('/')
def getTitle():
    return "Flask is running\nWelcome to The Wheel of Time"


# Using the GET method
@app.route("/characters", methods=['GET'])
def getCharacters():
    return jsonify({'Characters': db})


# To get character based on user choice
@app.route("/characters/<int:characterId>", methods=['GET'])
def getCharacterById(characterId):
    return jsonify({'Character': db[characterId]})


# Using the POST method
# curl -i -H "Content-Type: Application/json" -X POST http://127.0.0.1:5000/characters
# Use the above link in windows cmd
@app.route("/characters", methods=['POST'])
def addCharacter():
    character = {'id': "7", 'name': "Trollocs", 'gender': "Male",
                 'description': "Wretched, horrifying amalgams of man and beast, these towering Shadowspawn are the "
                                "core of the Dark One's army. While their appearances are varied — some with horns, "
                                "others with beaks or snarled snouts — one thing is universal: their murderous rage. "
                                "They possess a ferocious bloodlust, and can only be controlled by the equally "
                                "terrifying Fades."}

    db.append(character)
    return jsonify({'Added Character': character})


# Using the PUT method to update database
# curl -i -H "Content-Type: Application/json" -X PUT http://127.0.0.1:5000/characters/4
@app.route("/characters/<int:characterId>", methods=['PUT'])
def updateCharacter(characterId):
    db[characterId]['description'] = "This is the updated description for the character selected"
    return jsonify({'Characters': db[characterId]})


# Using the DELETE method to delete a character
# curl -i -H "Content-Type: Application/json" -X DELETE http://127.0.0.1:5000/characters/3
@app.route("/characters/<int:characterId>", methods=['DELETE'])
def deleteCharacter(characterId):
    db.remove(db[characterId])
    return jsonify({'Result': True})


if __name__ == '__main__':
    app.run(debug=True)
