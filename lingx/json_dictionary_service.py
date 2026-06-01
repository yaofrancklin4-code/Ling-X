"""
Service de recherche JSON pour le dictionnaire Baoulé
Recherche directe dans dictionnaire_baoule_cleaned.json
"""
import json
import os
from django.conf import settings

class JSONDictionaryService:
    """Service de recherche dans le fichier JSON"""
    
    _data = None
    _json_path = None
    
    @classmethod
    def _load_data(cls):
        """Charger le JSON une seule fois"""
        if cls._data is None:
            # Chercher le fichier JSON
            json_path = os.path.join(settings.BASE_DIR, 'dictionnaire_baoule_cleaned.json')
            
            if not os.path.exists(json_path):
                # Essayer dans le dossier parent
                json_path = os.path.join(settings.BASE_DIR, '..', 'dictionnaire_baoule_cleaned.json')
            
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    cls._data = json.load(f)
                    cls._json_path = json_path
                    print(f"✅ JSON chargé: {len(cls._data)} entrées depuis {json_path}")
            else:
                cls._data = []
                print(f"❌ Fichier JSON non trouvé: {json_path}")
        
        return cls._data
    
    @staticmethod
    def search(word, limit=10):
        """
        Recherche un mot dans le dictionnaire JSON
        Retourne maximum 10 résultats
        """
        if not word or len(word) < 2:
            return []
        
        word = word.lower().strip()
        data = JSONDictionaryService._load_data()
        
        results = []
        
        for entry in data:
            fr = entry.get("french", "").lower()
            ba = entry.get("baoule_suggested", "").lower()
            
            # Recherche exacte ou partielle
            if word in fr or word in ba:
                # Normaliser les clés pour le template
                normalized_entry = {
                    'baoule': entry.get('baoule_suggested', ''),
                    'french': entry.get('french', ''),
                    'pronunciation': entry.get('pronunciation', ''),
                    'definition': entry.get('definition', ''),
                    'example_baoule': entry.get('example_baoule', ''),
                    'example_french': entry.get('example_french', ''),
                    'is_common': entry.get('is_common', False),
                }
                results.append(normalized_entry)
                
                # Limiter à 10 résultats
                if len(results) >= limit:
                    break
        
        print(f"🔍 Recherche '{word}': {len(results)} résultat(s)")
        return results[:limit]
    
    @staticmethod
    def translate_french_to_baule(text):
        """Traduire du français vers le baoulé"""
        if not text:
            return []
        
        words = text.lower().split()
        data = JSONDictionaryService._load_data()
        translations = []
        
        for word in words:
            word_clean = word.strip()
            found = False
            
            for entry in data:
                fr = entry.get("french", "").lower()
                if word_clean == fr:
                    translations.append({
                        'french': word,
                        'baule': entry.get("baoule_suggested", ""),
                        'pronunciation': entry.get("pronunciation", ""),
                        'found': True
                    })
                    found = True
                    break
            
            if not found:
                translations.append({
                    'french': word,
                    'baule': word,
                    'pronunciation': '',
                    'found': False
                })
        
        return translations
    
    @staticmethod
    def translate_baule_to_french(text):
        """Traduire du baoulé vers le français"""
        if not text:
            return []
        
        words = text.lower().split()
        data = JSONDictionaryService._load_data()
        translations = []
        
        for word in words:
            word_clean = word.strip()
            found = False
            
            for entry in data:
                ba = entry.get("baoule_suggested", "").lower()
                if word_clean == ba:
                    translations.append({
                        'baule': word,
                        'french': entry.get("french", ""),
                        'pronunciation': entry.get("pronunciation", ""),
                        'found': True
                    })
                    found = True
                    break
            
            if not found:
                translations.append({
                    'baule': word,
                    'french': word,
                    'pronunciation': '',
                    'found': False
                })
        
        return translations
