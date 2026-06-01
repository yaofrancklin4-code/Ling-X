# Référence des Images Baoulé

## Images Disponibles

### Images Hero
- **hero_peuple_baoule.jpg** (458.4 Ko)
  - Usage: Banners, headers, backgrounds
  - Path: `{% static 'images/baoule/hero_peuple_baoule.jpg' %}`

### Logos
- **logo_baoule_officiel.jpg** (4.8 Ko)
  - Usage: Branding, headers
  - Path: `{% static 'images/baoule/logo_baoule_officiel.jpg' %}`

- **logo_baoule_carre.jpg** (5.7 Ko)
  - Usage: Favicons, compact branding
  - Path: `{% static 'images/baoule/logo_baoule_carre.jpg' %}`

### Images de Contenu
- **unsplash_afrique_tissage.jpg** (38.2 Ko)
  - Usage: Artisanat, sections
  - Path: `{% static 'images/baoule/unsplash_afrique_tissage.jpg' %}`

- **unsplash_afrique_village.jpg** (283.6 Ko)
  - Usage: Territoire, culture
  - Path: `{% static 'images/baoule/unsplash_afrique_village.jpg' %}`

- **unsplash_masque_africain.jpg** (61.9 Ko)
  - Usage: Art, rituels
  - Path: `{% static 'images/baoule/unsplash_masque_africain.jpg' %}`

- **unsplash_pagne_africain.jpg** (83.4 Ko)
  - Usage: Mode, vêtements traditionnels
  - Path: `{% static 'images/baoule/unsplash_pagne_africain.jpg' %}`

## Usage dans les Templates

### Format basique
```html
{% load static %}
<img src="{% static 'images/baoule/hero_peuple_baoule.jpg' %}" alt="Peuple Baoulé">
```

### Format responsive
```html
{% load static %}
<img 
  src="{% static 'images/baoule/hero_peuple_baoule.jpg' %}" 
  alt="Peuple Baoulé"
  class="img-fluid"
  style="max-width: 100%; height: auto;">
```

### Fond d'écran
```html
<div style="background-image: url('{% static 'images/baoule/hero_peuple_baoule.jpg' %}'); background-size: cover;">
  <!-- Contenu -->
</div>
```

## Accessibilité Media

Les images sont aussi accessibles via MEDIA_URL pour les uploads:
```
/media/images/baoule/hero_peuple_baoule.jpg
/media/images/baoule/unsplash_afrique_village.jpg
```

## Total
- **7 images** importées avec succès
- **936.0 Ko** de poids total
- **Prêt pour utilisation** en production
