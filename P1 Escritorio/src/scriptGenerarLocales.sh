<<<<<<< HEAD
xgettext -d MedicalApp -o ./locale/MedicalApp.pot ./view.py --from-code UTF-8  #extraer las cadenas de texto del view.py al .pot
xgettext -d Presenter -o ./locale/Presenter.pot ./presenter.py --from-code UTF-8 #extraer las cadenas de texto del presenter.py al .pot
#generar el archivo de traduciones para el español para el MedicalApp
msginit --locale=es --input=./locale/MedicalApp.pot --output=./locale/es/LC_MESSAGES/MedicalApp.po --no-translator 
msginit --locale=es --input=./locale/Presenter.pot --output=./locale/es/LC_MESSAGES/Presenter.po --no-translator # para el presenter
#Para el ingles
msginit --locale=en --input=./locale/MedicalApp.pot --output=./locale/en/LC_MESSAGES/MedicalApp.po --no-translator 
msginit --locale=en --input=./locale/Presenter.pot --output=./locale/en/LC_MESSAGES/Presenter.po --no-translator # para el presenter
#Para el Arabe
msginit --locale=ar --input=./locale/MedicalApp.pot --output=./locale/ar/LC_MESSAGES/MedicalApp.po --no-translator 
msginit --locale=ar --input=./locale/Presenter.pot --output=./locale/ar/LC_MESSAGES/Presenter.po --no-translator # para el presenter

#una vez traduzcas los archivos hay que compilarlos, pasarlos al .mo
msgfmt ./locale/es/LC_MESSAGES/MedicalApp.po -o ./locale/es/LC_MESSAGES/MedicalApp.mo #compilar
msgfmt ./locale/es/LC_MESSAGES/Presenter.po -o ./locale/es/LC_MESSAGES/Presenter.mo #compilar
msgfmt ./locale/en/LC_MESSAGES/MedicalApp.po -o ./locale/en/LC_MESSAGES/MedicalApp.mo #compilar
msgfmt ./locale/en/LC_MESSAGES/Presenter.po -o ./locale/en/LC_MESSAGES/Presenter.mo #compilar
msgfmt ./locale/ar/LC_MESSAGES/MedicalApp.po -o ./locale/ar/LC_MESSAGES/MedicalApp.mo #compilar
msgfmt ./locale/ar/LC_MESSAGES/Presenter.po -o ./locale/ar/LC_MESSAGES/Presenter.mo #compilar


=======
xgettext -d MedicalApp -o ./locale/MedicalApp.pot ./view.py ./presenter.py --from-code UTF-8  #extraer las cadenas de texto del view.py al .pot
>>>>>>> 5495fa2 (Cambiada la forma en la que se formatean las fechas. Cambiados los scripts de generacion de traducciones)

#generar el archivo de traduciones para el MedicalApp
#es
msginit -l es_ES.UTF8 --input=./locale/MedicalApp.pot --output=./locale/es/LC_MESSAGES/MedicalApp.po --no-translator 
#en
msginit -l en_US.UTF8 --input=./locale/MedicalApp.pot --output=./locale/en/LC_MESSAGES/MedicalApp.po --no-translator 
#ar
#msginit --locale=ar --input=./locale/MedicalApp.pot --output=./locale/ar/LC_MESSAGES/MedicalApp.po --no-translator