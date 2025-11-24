# Ce fichier peut gérer la version du modèle et le chargement
from vosk import Model

def load_model(path="model-fr"):
    return Model(path)
