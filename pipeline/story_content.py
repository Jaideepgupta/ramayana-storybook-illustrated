"""
Editorial story content for the storybook app (v4). Kept separate from the curation logic so a
reviewer can read and correct the prose in one place.

All text is a PARAPHRASE of well-known episodes of the Valmiki Ramayana, written for this app.
Details follow the Valmiki tradition (popular later additions are avoided). Review before
public use.
"""

# Clearer titles for key moments (the episodes readers know by these names).
TITLE_OVERRIDES = {
    "E004": "Tataka and the sage's sacrifice",
    "E020": "War with Khara and Dushana",
    "E022": "The golden deer and Sita's abduction",
    "E033": "Hanuman sets Lanka ablaze",
    "E036": "Building the bridge to Lanka",
    "E038": "Kumbhakarna awakens",
    "E039": "Lakshmana and Meghnad",
    "E040": "Rama and Ravana",
}

# Key moments: event id -> detailed narration (shown on its own page).
NARRATIVE = {
    "E002": "Dasharatha, king of Ayodhya, has no heir. The sage Rishyasringa conducts the Putrakameshti sacrifice, and from the fire rises a radiant being bearing a vessel of payasa, a sacred sweet. The king shares it among his queens. Kaushalya gives birth to Rama, Kaikeyi to Bharata, and Sumitra to the twins Lakshmana and Shatrughna.",
    "E004": "The sage Vishvamitra asks for young Rama to guard his sacrifice from demons. On the way, Rama slays the fearsome Tataka, and the sage rewards him with celestial weapons. At Siddhashrama, as Maricha and Subahu swoop down on the ritual, Rama hurls Maricha far out into the ocean and slays Subahu. The sacrifice is completed in peace.",
    "E006": "In Mithila, King Janaka keeps the great bow of Shiva, which no suitor has even been able to lift. Sita will marry the one who strings it. Rama lifts the bow with ease and draws the string, and the bow breaks with a sound like thunder. Sita garlands Rama, and his three brothers marry Urmila, Mandavi and Shrutakirti.",
    "E009": "Ayodhya prepares to crown Rama as heir. The maid Manthara poisons Queen Kaikeyi's mind, and Kaikeyi reminds Dasharatha of two boons he once promised her for saving his life in battle. She claims them now: Bharata must be crowned, and Rama must live in the forest for fourteen years. Bound by his word, the king is broken.",
    "E010": "Rama receives the news without anger. To keep his father's promise, he puts aside his royal robes for the bark garments of an ascetic. Sita refuses to stay behind: her place, she says, is beside her husband. Lakshmana vows to serve them both. The three leave Ayodhya as the whole city weeps.",
    "E015": "Dasharatha cannot bear the loss. He remembers a wrong from his youth: hunting by a river at night, he killed a young ascetic by mistake, and the boy's blind father cursed him to die grieving for a son. The curse comes true. Calling Rama's name, the king dies on the sixth night after the exile.",
    "E017": "Bharata returns from his uncle's kingdom, rejects his mother's scheme and goes to Chitrakuta to beg Rama to come home. Rama will not break their father's word. Bharata takes Rama's sandals, places them on the throne, and rules from Nandigrama as regent, living as an ascetic until his brother returns.",
    "E019": "In Panchavati, Ravana's sister Shurpanakha sees Rama and desires him. Rejected by Rama and mocked by Lakshmana, she rushes at Sita in rage. Lakshmana cuts off her nose and ears. Wounded and humiliated, she flees to her brother Khara, and the peace of the forest is broken.",
    "E020": "To avenge Shurpanakha, Khara first sends fourteen rakshasas, and Rama kills them all. Then Khara, Dushana and Trishiras march out with an army of fourteen thousand. Rama sends Lakshmana to guard Sita in a cave and faces the host alone. His arrows destroy the army; Dushana, Trishiras and finally Khara fall. Only the news escapes, carried to Ravana in Lanka.",
    "E022": "Ravana sends Maricha into the hermitage disguised as a golden deer. Sita longs for it, and Rama gives chase. Struck by Rama's arrow, Maricha cries out in Rama's voice, and Sita sends Lakshmana after him. Ravana appears as a wandering ascetic, reveals himself, and carries Sita away through the sky in his chariot.",
    "E023": "The old vulture king Jatayu, a friend of Dasharatha, hears Sita's cries and attacks Ravana. He shatters the chariot and wounds the demon king, but Ravana cuts off his wings. Rama and Lakshmana find him dying. Jatayu tells them who has taken Sita, and Rama performs his funeral rites as he would for his own father.",
    "E025": "At Rishyamuka hill, the exiled Vanara prince Sugriva sees two armed strangers and sends his minister Hanuman to learn who they are. Hanuman, disguised as a mendicant, speaks with such grace that Rama is moved. He brings the brothers to Sugriva, and Rama and Sugriva swear friendship before a sacred fire.",
    "E027": "Sugriva challenges his brother Vali, who had driven him out and taken his wife. In the first duel the brothers look so alike that Rama cannot shoot. Sugriva returns wearing a garland of flowers, and as they fight, Rama shoots Vali from behind a tree. Dying, Vali questions the justice of it, a debate readers have continued ever since. Sugriva becomes king of Kishkindha.",
    "E029": "The search party led by Angada reaches the southern sea without news and despairs. Then they meet Sampati, the aged brother of Jatayu. Grieving for his brother, he tells them what his far-seeing eyes can make out: Sita is held in Lanka, an island a hundred yojanas across the ocean.",
    "E030": "No one believes the sea can be crossed until Jambavan reminds Hanuman of the strength he has forgotten. Hanuman grows to an enormous size, springs from Mahendra mountain and flies across the ocean, passing the tests of the mountain Mainaka, the serpent-mother Surasa and the demoness Simhika on the way.",
    "E031": "Hanuman searches Lanka by night and finds Sita in the Ashoka grove, guarded by rakshasis, thin with grief but steadfast. He watches Ravana threaten her. When Ravana leaves, Hanuman softly recites Rama's story, shows her Rama's signet ring, and receives her hair jewel, the chudamani, as a token for Rama.",
    "E033": "Before leaving, Hanuman wrecks the grove and kills Ravana's son Aksha. Meghnad binds him with a divine weapon, and he is brought before Ravana, whom he warns to return Sita. Ravana orders his tail set on fire. Hanuman breaks free and leaps from roof to roof, setting Lanka ablaze, then cools his tail in the sea and flies home.",
    "E035": "Vibhishana urges his brother Ravana to return Sita and avoid ruin. Ravana insults him in open court. Vibhishana leaves Lanka with four companions and asks Rama for refuge. Though some of the Vanaras distrust him, Rama accepts him, saying he will never turn away anyone who comes seeking shelter.",
    "E036": "The ocean blocks the army. Rama prays to the sea for three days and, when no answer comes, raises his bow in anger. The god of the ocean appears and advises that Nala, son of the divine architect Vishvakarma, can build a bridge. The Vanaras haul rocks and trees, and in five days the bridge to Lanka is complete.",
    "E038": "Ravana wakes his giant brother Kumbhakarna, who sleeps for months at a time. Kumbhakarna tells Ravana that taking Sita was wrong, yet goes to fight out of loyalty. He crushes and swallows Vanaras by the hundreds and carries off Sugriva. Rama cuts off his arms and legs with his arrows, and finally his head, and the giant falls.",
    "E039": "Ravana's son Meghnad, called Indrajit for once defeating Indra, fights unseen from the clouds. He binds Rama and Lakshmana with serpent arrows, from which Garuda frees them, and later strikes down much of the army, which Hanuman revives by bringing a mountain of healing herbs from the Himalaya. Finally Vibhishana leads Lakshmana to Nikumbhila, where Meghnad is performing a sacrifice to become invincible. Lakshmana breaks it off and, after a fierce duel, slays him.",
    "E040": "Grief-stricken by the loss of Meghnad and Kumbhakarna, Ravana rides out himself. Indra sends his own chariot and charioteer Matali to Rama, and the sage Agastya teaches him the Aditya Hridayam hymn. Each time Rama cuts off one of Ravana's heads, another grows back. At last Rama looses the Brahmastra, which pierces Ravana's heart, and the ten-headed king falls.",
    "E043": "With the war over, Vibhishana is crowned king of Lanka. Rama, Sita and Lakshmana return to Ayodhya in the flying chariot Pushpaka, with their allies. Bharata hands back the sandals he has kept on the throne for fourteen years, and Rama is crowned king. His reign, Rama Rajya, is remembered as an age of justice and peace.",
    "E044": "The final book tells of Rama's reign, Sita's second exile after public gossip, her years in the hermitage of the sage Valmiki, and the birth of their twin sons Lava and Kusha, who sing the Ramayana before their father. Many scholars see this book as a later addition, so its episodes are told only briefly here.",
}

# Approximate map positions of TRADITIONAL associations (lat, lon). Not historical claims;
# the Locations "Confidence Label" still applies and is shown with the map.
MAP_COORDS = {
    "L001": (26.79, 82.20),   # Ayodhya
    "L002": (26.73, 85.92),   # Mithila - Janakpur
    "L003": (25.56, 83.98),   # Siddhashrama - Buxar (one tradition)
    "L005": (25.60, 81.63),   # Shringaverapura
    "L006": (25.17, 80.86),   # Chitrakuta
    "L007": (19.80, 81.50),   # Dandaka forest - broad central region, centroid only
    "L008": (20.01, 73.79),   # Panchavati - Nashik
    "L010": (15.33, 76.46),   # Kishkindha - Hampi region
    "L013": (9.45, 78.90),    # Southern coast (search party reaches the ocean)
    "L014": (8.39, 77.55),    # Mahendra mountain - one southern tradition
    "L015": (7.30, 80.70),    # Lanka - traditional association with Sri Lanka
    "L017": (9.17, 79.42),    # Setubandha - Rameswaram / Dhanushkodi
    "L018": (26.62, 82.12),   # Nandigrama
    "L019": (25.43, 81.88),   # Prayaga - Prayagraj
}
