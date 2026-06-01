"""
Service de recherche intelligent pour le dictionnaire Baoulé
"""
from django.db.models import Q, F
from lingx.models import DictionaryEntry, Vocabulary
import re

class DictionarySearchService:
    """Service de recherche avancée dans le dictionnaire"""
    
    @staticmethod
    def normalize_text(text):
        """Normaliser le texte pour la recherche"""
        if not text:
            return ""
        # Supprimer les accents et caractères spéciaux
        text = text.lower().strip()
        # Remplacer les apostrophes
        text = text.replace("'", " ").replace("'", " ")
        return text
    
    @staticmethod
    def search(query, limit=10):
        """
        Recherche intelligente dans le dictionnaire
        Retourne les résultats triés par pertinence (MAX 10)
        """
        if not query or len(query) < 2:
            return []
        
        normalized_query = DictionarySearchService.normalize_text(query)
        words = normalized_query.split()[:3]  # Limiter à 3 mots max
        
        # Construction de la requête (seulement champs principaux)
        q_objects = Q()
        
        for word in words:
            q_objects |= Q(word_baule__icontains=word)
            q_objects |= Q(word_french__icontains=word)
        
        # Recherche limitée
        results = DictionaryEntry.objects.filter(q_objects).distinct()[:30]
        
        # Tri par pertinence
        results_with_score = []
        for entry in results:
            score = DictionarySearchService._calculate_relevance_score(entry, normalized_query, words)
            results_with_score.append((entry, score))
        
        # Trier par score décroissant et limiter à 10
        results_with_score.sort(key=lambda x: x[1], reverse=True)
        final_results = results_with_score[:limit]
        
        # Mettre à jour le compteur (batch update, pas de boucle save)
        entry_ids = [entry.id for entry, _ in final_results]
        DictionaryEntry.objects.filter(id__in=entry_ids).update(search_count=F('search_count') + 1)
        
        return [entry for entry, _ in final_results]
    
    @staticmethod
    def _calculate_relevance_score(entry, query, words):
        """Calculer le score de pertinence d'une entrée"""
        score = 0
        
        # Correspondance exacte = score élevé
        if entry.word_baule.lower() == query:
            score += 100
        if entry.word_french.lower() == query:
            score += 100
        
        # Correspondance au début du mot
        if entry.word_baule.lower().startswith(query):
            score += 50
        if entry.word_french.lower().startswith(query):
            score += 50
        
        # Correspondance partielle
        for word in words:
            if word in entry.word_baule.lower():
                score += 20
            if word in entry.word_french.lower():
                score += 20
            if word in entry.pronunciation.lower():
                score += 10
            if word in entry.definition.lower():
                score += 5
        
        # Bonus pour les mots communs
        if entry.is_common:
            score += 15
        
        # Bonus basé sur la popularité (nombre de recherches)
        score += min(entry.search_count, 20)
        
        return score
    
    @staticmethod
    def get_suggestions(query, limit=5):
        """Obtenir des suggestions de recherche (MAX 5)"""
        if not query or len(query) < 2:
            # Retourner les mots les plus recherchés
            return list(DictionaryEntry.objects.filter(
                is_common=True
            ).order_by('-search_count')[:limit])
        
        normalized_query = DictionarySearchService.normalize_text(query)
        
        # Recherche de mots similaires
        suggestions = list(DictionaryEntry.objects.filter(
            Q(word_baule__istartswith=normalized_query) |
            Q(word_french__istartswith=normalized_query)
        ).order_by('-is_common', '-search_count')[:limit])
        
        return suggestions
    
    @staticmethod
    def get_related_words(entry_id, limit=5):
        """Obtenir des mots liés à une entrée"""
        try:
            entry = DictionaryEntry.objects.get(id=entry_id)
        except DictionaryEntry.DoesNotExist:
            return []
        
        # Rechercher des mots avec des racines similaires
        related = DictionaryEntry.objects.filter(
            Q(word_baule__icontains=entry.word_baule[:3]) |
            Q(word_french__icontains=entry.word_french.split()[0])
        ).exclude(id=entry_id)[:limit]
        
        return related
    
    @staticmethod
    def translate_french_to_baule(french_text):
        """Traduire un texte français en baoulé (mot par mot)"""
        words = french_text.lower().split()
        translations = []
        
        for word in words:
            # Nettoyer le mot
            clean_word = re.sub(r'[^\w\s]', '', word)
            
            # Chercher dans le dictionnaire
            entry = DictionaryEntry.objects.filter(
                word_french__iexact=clean_word
            ).first()
            
            if entry:
                translations.append({
                    'french': word,
                    'baule': entry.word_baule,
                    'pronunciation': entry.pronunciation,
                    'found': True
                })
            else:
                translations.append({
                    'french': word,
                    'baule': word,
                    'pronunciation': '',
                    'found': False
                })
        
        return translations
    
    @staticmethod
    def translate_baule_to_french(baule_text):
        """Traduire un texte baoulé en français (mot par mot)"""
        words = baule_text.lower().split()
        translations = []
        
        for word in words:
            # Nettoyer le mot
            clean_word = re.sub(r'[^\w\s]', '', word)
            
            # Chercher dans le dictionnaire
            entry = DictionaryEntry.objects.filter(
                word_baule__iexact=clean_word
            ).first()
            
            if entry:
                translations.append({
                    'baule': word,
                    'french': entry.word_french,
                    'pronunciation': entry.pronunciation,
                    'found': True
                })
            else:
                translations.append({
                    'baule': word,
                    'french': word,
                    'pronunciation': '',
                    'found': False
                })
        
        return translations
    
    @staticmethod
    def get_word_of_the_day():
        """Obtenir le mot du jour"""
        from datetime import date
        import random
        
        # Utiliser la date comme seed pour avoir le même mot toute la journée
        today = date.today()
        seed = today.year * 10000 + today.month * 100 + today.day
        random.seed(seed)
        
        # Sélectionner un mot commun aléatoire
        common_words = list(DictionaryEntry.objects.filter(is_common=True))
        if common_words:
            return random.choice(common_words)
        
        # Sinon, n'importe quel mot
        all_words = list(DictionaryEntry.objects.all())
        if all_words:
            return random.choice(all_words)
        
        return None
    
    @staticmethod
    def get_popular_words(limit=10):
        """Obtenir les mots les plus recherchés (MAX 10)"""
        return list(DictionaryEntry.objects.filter(
            search_count__gt=0
        ).order_by('-search_count')[:limit])
    
    @staticmethod
    def get_recent_additions(limit=10):
        """Obtenir les mots récemment ajoutés"""
        return DictionaryEntry.objects.order_by('-created_at')[:limit]
