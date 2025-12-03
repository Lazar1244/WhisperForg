WhisperForg
Enregistrement Audio Micro + Audio interne de PC avec Python et Voicemeeter Banana
Cette partie permet d’enregistrer simultanément le micro et l’audio interne du PC avec Python et Voicemeeter Banana.

1️⃣ Prérequis
Python 3.10.8

Bibliothèques Python :

pip install sounddevice soundfile numpy
Voicemeeter Banana : VB-Audio Voicemeeter


Installation de Voicemeeter Banana


# Configuration de Voicemeeter

Dans Hardware Input 1 :

    Sélectionne : Mode WDM(WASAPI) -> Microphone (Realtek Audio)

    Active UNIQUEMENT B2 (PAS B1 sinon mélange )

    B2 = micro seul
    Vous pouvez activer A1 dans Micro si vous voulez vous entendre (facultatif et déconseillé)

Virtual Inputs
    Virtual Input (Voicemeeter Input) -> AUDIO INTERNE

    C’est le son du PC

    Active UNIQUEMENT B1

    B1 = audio interne seulement
    vous pouvez activer A1 dans VAIO (audio PC) pour entendre ton PC

Hardware Out
    Choisis ton casque :

    A1 → Haut-parleurs / écouteurs (Realtek Audio)
