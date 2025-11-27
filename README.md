# WhisperForg
# Enregistrement Audio Micro + Audio interne de PC avec Python et Voicemeeter Banana

Cette partie permet d’enregistrer simultanément le micro et l’audio interne du PC avec Python et Voicemeeter Banana.


## 1️⃣ Prérequis

- Python 3.10.8

- Bibliothèques Python :
```bash
pip install sounddevice soundfile numpy
Voicemeeter Banana : VB-Audio Voicemeeter


Installation de Voicemeeter Banana


# Configuration de Voicemeeter
Hardware Inputs
Input 1 : Micro principal → Mode WDM  (WASAPI) choisir microphone et activer B1 pour l’enregistrement.


Virtual Inputs
Voicemeeter VAIO : audio interne du PC → activer A1 pour écouter et B1 pour enregistrer.


Hardware Out
A1 : casque ou haut-parleurs → activer A1 et B1



