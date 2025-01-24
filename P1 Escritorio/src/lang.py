# Módulo para la instalación y configuración del local

from pathlib import Path
locale_dir = Path(__file__).parent/"locale"
import locale
locale.setlocale(locale.LC_ALL, '') #para que lea la config del usuario
locale.bindtextdomain("MedicalApp", str(locale_dir))
import gettext
gettext.bindtextdomain("MedicalApp", str(locale_dir))
gettext.textdomain("MedicalApp")
#gettext.install("MedicalApp", str(locale_dir))
lang = gettext.translation("MedicalApp", localedir=locale_dir, languages=[locale.getlocale()[0]])
lang.install()

print(f"Current locale: {locale.getlocale()}") #para ver q locale esta cogiendo (util para depurar)

def gettext(str:str):
    return _(str)