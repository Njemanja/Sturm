import subprocess
from googletrans import Translator
from transliterate import translit
import polib

def translate_po_file(input_file, src_lang, dest_lang):
    translator = Translator()
    po = polib.pofile(input_file)
    for entry in po:
        if not entry.msgstr:
            try:
                if dest_lang == "sr_Cyrl":
                    translation = translit(entry.msgid, language_code='sr')
                    entry.msgstr = translation
                else:
                    translation = translator.translate(entry.msgid, src=src_lang, dest=dest_lang).text
                    entry.msgstr = translation
            except Exception as e:
                print(f"Greška pri prevođenju '{entry.msgid}': {e}")
                entry.msgstr = entry.msgid
    po.save(input_file)


if __name__ == "__main__":
    subprocess.run("python ./manage.py makemessages -l sr", shell=True, check=True, text=True, capture_output=True)
    subprocess.run("python ./manage.py makemessages -l sr_Cyrl", shell=True, check=True, text=True, capture_output=True)
    subprocess.run("python ./manage.py makemessages -l en", shell=True, check=True, text=True, capture_output=True)
    subprocess.run("python ./manage.py makemessages -l de", shell=True, check=True, text=True, capture_output=True)

    translate_po_file('locale/sr/LC_MESSAGES/django.po', 'sr', 'sr')
    translate_po_file('locale/sr_Cyrl/LC_MESSAGES/django.po', 'sr', 'sr_Cyrl')
    translate_po_file('locale/en/LC_MESSAGES/django.po', 'sr', 'en')
    translate_po_file('locale/de/LC_MESSAGES/django.po', 'sr', 'de')

    subprocess.run("python manage.py compilemessages", shell=True, check=True, text=True, capture_output=True)
