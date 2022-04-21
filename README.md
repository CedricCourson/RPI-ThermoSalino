# RPI-ThermoSalino
**Thermosalinometre sur Raspberry pi**

Instrument de mesure de température et conductivité électrique (salinité) de l'eau. Version dérivé de SensOcean, simplifier pour une utilisation rapide en laboratoire. 
le projet SensOcean : https://www.astrolabe-expeditions.org/programme-de-sciences/sensocean/

### Page notion de cet instrument
https://cedriccoursonopensourceoceanography.notion.site/Version-RPI-Labo-c03d6406405d425c827c820fadc21462
Cette page détaille toutes les procédures d'installation, de configuration et donne les plans de construction de l'instrument. 


### Contenu de ce repo
Fichiers de code python pour l'enregistrement des données en CSV.
- Programme/cdt-ok.py : programme de lecture des données des cartes Atlas Scientific
- Programme/bouton-led.py : programme pou activier l'enregistrment sur déclenchement d'un interrupteur. 
Ces 2 fichiers sont à installer sur /home/public/

- lancerment.py : pour lancer les fichiers python au démarrage
Celui là est à installer sur /home/pi/

##### Bonus : 
- Programme/cdt-plot.py : permet de tracer les courbes en direct, a condition de le lancer depuis un console sur un écran connecté au raspberry pi. 