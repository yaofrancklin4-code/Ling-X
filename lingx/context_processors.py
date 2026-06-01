from pathlib import Path

from django.conf import settings


def sous_groupes_images(request):
    """Expose la liste des images présentes dans `static/images/SOUS GROUPES/`.

    IMPORTANT:
    - On cible directement le chemin du repo (`monprojet/static/...`) afin d’éviter
      les divergences entre STATIC_ROOT / STATICFILES_DIRS selon l’environnement.
    """

    # Chemin sûr vers le dossier dans le repo
    # monprojet/lingx/context_processors.py -> parents[1]=lingx, parents[2]=monprojet, puis /static
    repo_static = Path(__file__).resolve().parents[2] / 'static'
    images_dir = repo_static / 'images' / 'SOUS GROUPES'

    if not images_dir.exists() or not images_dir.is_dir():
        return {'sous_groupes_images': []}

    items = []
    for p in sorted(images_dir.iterdir()):
        if not p.is_file():
            continue
        items.append(
            {
                'filename': p.name,
                'label': p.stem,
                'url': f"{settings.STATIC_URL}images/SOUS GROUPES/{p.name}",
            }
        )

    return {'sous_groupes_images': items}


