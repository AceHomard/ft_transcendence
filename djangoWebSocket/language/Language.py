import json
import os


class Language:
    def __init__(self):
        self.translations = {}
        self.loadTranslations()

    def loadTranslations(self):
        directory = "language/data"
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                lang_code = filename.split(".")[0]
                with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                    self.translations[lang_code] = json.load(f)

    def get(self, lang_code, key):
        return self.translations[lang_code][key]


language = Language()
