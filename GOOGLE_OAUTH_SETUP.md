# Configuration Google OAuth pour LingX

## ✅ Status Actuel
- ✓ Custom OAuth views créées (google_login_direct, google_login_callback)
- ✓ Bouton "Se connecter avec Google" implémenté
- ✓ Auto-signup/login sans page intermédiaire configuré
- ⏳ Credentials Google OAuth manquantes (à configurer)

##  Configuration Requise

### Étape 1: Créer une application Google Cloud
1. Allez sur https://console.cloud.google.com/
2. Créez un nouveau projet (ex: "LingX Baoule")
3. Activez l'API Google+
4. Allez dans "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Type: Web Application
6. URLs autorisées:
   ```
   http://127.0.0.1:8000  (développement)
   https://votre-domaine.com  (production)
   ```
7. Redirect URIs:
   ```
   http://127.0.0.1:8000/auth/google/callback/  (développement)
   https://votre-domaine.com/auth/google/callback/  (production)
   ```

### Étape 2: Configurer les credentials
Option A - Via variables d'environnement:
```bash
set GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
set GOOGLE_SECRET=your_client_secret
python monprojet/setup_google_oauth.py
```

Option B - Via Django Admin:
1. Allez sur http://127.0.0.1:8000/admin/
2. Socialaccount → Social Applications
3. Ajoutez une nouvelle application:
   - Provider: Google
   - Name: Google
   - Client ID: votre_client_id
   - Secret: votre_secret
   - Sites: example.com (développement)

### Étape 3: Tester le flux
1. Allez sur http://127.0.0.1:8000/login/
2. Cliquez sur "Se connecter avec Google"
3. Vous serez redirigé directement vers Google (pas de page intermédiaire)
4. Après l'authentification, vous serez auto-connecté et redirigé au dashboard

##  Flux d'Authentification
```
Utilisateur → Bouton Google → /auth/google/login/ 
   ↓
Redirection directe vers Google OAuth
   ↓
Utilisateur s'authentifie sur Google
   ↓
Google redirige vers /auth/google/callback/
   ↓
Auto-création/connexion utilisateur
   ↓
Redirection vers dashboard
```

##  Notes Importantes
- ✓ Le custom adapter auto-populate le profil (first_name, last_name)
- ✓ Les signaux créent automatiquement un UserProfile
- ✓ Pas de pages intermédiaires allauth - flux direct
- ✓ Auto-signup activé pour nouveaux utilisateurs
- ⚠️ Les credentials Google sont MANQUANTES - à configurer
- ⚠️ Les credentials sont stockées en base de données Django

##  Sécurité
- Les credentials secrets ne sont jamais exposés au frontend
- Seul le client_id est utilisé pour le redirect vers Google
- Les tokens Google sont échangés côté serveur uniquement
