import sqlite3, random, datetime
from models import Translation

DB_FILE_NAME = 'translations.db'

# seed data
translations = [
    {
        "category": "Chinese Dialog",
        "foreign_word": "niao4 shi1 de5 du3gui3",
        "characters": "Simplified characters: \u5c3f\u6e7f\u7684\u8d4c\u9b3c / Traditional characters: \u5c3f\u6fd5\u7684\u8ced\u9b3c",
        "back_translation": "urine-soaked habitual gamblers",
        "script_mandarin_translation": "niao SE duh DOO-gway",
        "script_english_translation": "p***-soaked pikers",
        "context": "\u201cHeart of Gold,\u201d Wash, referring to Rance\u2019s men now trapped on Serenity",
        "additional_info": "https://fireflychinese.kevinsullivansite.net/title/heartofgold.html"
    },
    {
        "category": "Cut Chinese Dialog",
        "foreign_word": "Lan2dan1 jiang4!",
        "characters": "Simplified characters: \u9611\u6b9a\u9171\uff01 / Traditional characters: \u95cc\u6bab\u91ac\uff01",
        "back_translation": "Worn-out sauce!",
        "script_mandarin_translation": "LAN-dan JIANG!",
        "script_english_translation": "Weak-ass sauce!",
        "context": "\u201cHeart of Gold\u201d [Cut], Mal, referring to his fancy drink",
        "additional_info": "https://fireflychinese.kevinsullivansite.net/title/heartofgold.html"
    },
    {
        "category": "Visible Chinese",
        "foreign_word": "Yu2",
        "characters": "Simplified/Traditional characters: \u81fe",
        "back_translation": "",
        "script_mandarin_translation": None,
        "script_english_translation": None,
        "context": "\u201cHeart of Gold,\u201d Visible Chinese, on Inara\u2019s hourglass stand, visible as Mal enters after eavesdropping",
        "additional_info": "https://fireflychinese.kevinsullivansite.net/title/heartofgold.html"
    },
]    

def connect():
    conn = sqlite3.connect(DB_FILE_NAME)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS translations (id INTEGER PRIMARY KEY, category TEXT, foreign_word TEXT, characters TEXT, back_translation TEXT, script_mandarin_translation TEXT, script_english_translation TEXT, context TEXT, additional_info TEXT);")
    conn.commit()
    conn.close()
    for i in translations:
        tr = Translation(None, i['category'], i['foreign_word'], i['characters'], i['back_translation'], i['script_mandarin_translation'], i['script_english_translation'], i['context'], i['additional_info'])
        insert(tr)

def insert(translation):
    conn = sqlite3.connect(DB_FILE_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO translations VALUES (?,?,?,?,?,?,?,?,?);", (
        translation.id,
        translation.category,
        translation.foreign_word,
        translation.characters,
        translation.back_translation,
        translation.script_mandarin_translation,
        translation.script_english_translation,
        translation.context,
        translation.additional_info
    ))
    conn.commit()
    conn.close()

def get_by_id(theId):
    conn = sqlite3.connect(DB_FILE_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM translations WHERE id=?;", (theId,))
    record = cur.fetchone()
    tr = None
    if record is not None:
        tr = Translation(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8])
    conn.close()
    return tr

def get_by_foreign_word(foreign_word):
    conn = sqlite3.connect(DB_FILE_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM translations WHERE foreign_word=?;", (foreign_word,))
    record = cur.fetchone()
    tr = None
    if record is not None:
        tr = Translation(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8])
    conn.close()
    return tr

def get_all():
    conn = sqlite3.connect(DB_FILE_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM translations;")
    rows = cur.fetchall()
    translations = []
    for i in rows:
        tr = Translation(i[0], i[1], i[2], i[3], i[4] ,i[5], i[6], i[7], i[8])
        translations.append(tr)
    conn.close()
    return translations

def update(translation):
    conn = sqlite3.connect(DB_FILE_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE translations SET category=?, foreign_word=?, characters=?, back_translation=?, script_mandarin_translation=?, script_english_translation=?, context=?, additional_info=? WHERE id=?;", (
        translation.category,
        translation.foreign_word,
        translation.characters,
        translation.back_translation,
        translation.script_mandarin_translation,
        translation.script_english_translation,
        translation.context,
        translation.additional_info,
        translation.id
    ))
    conn.commit()
    conn.close()

def delete(id):
    conn = sqlite3.connect(DB_FILE_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM translations WHERE id=?;", (id,))
    conn.commit()
    conn.close()

def truncate():
    conn = sqlite3.connect(DB_FILE_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM translations;")
    conn.commit()
    conn.close()