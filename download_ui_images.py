"""Télécharge des photos Unsplash (licence Unsplash) pour l'UI LingX."""
import ssl
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent / "static" / "img" / "ui"
BASE.mkdir(parents=True, exist_ok=True)

# Photos simples et lisibles (Unsplash — usage libre)
IMAGES = {
    "star.jpg": "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=400&h=400&fit=crop&q=85&auto=format",
    "trophy.jpg": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400&h=400&fit=crop&q=85&auto=format",
    "fire.jpg": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=400&h=400&fit=crop&q=85&auto=format",
    "check.jpg": "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=400&h=400&fit=crop&q=85&auto=format",
    "dashboard.jpg": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=400&fit=crop&q=85&auto=format",
    "clock.jpg": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=400&fit=crop&q=85&auto=format",
    "inbox.jpg": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=400&h=400&fit=crop&q=85&auto=format",
    "chart.jpg": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=400&fit=crop&q=85&auto=format",
    # Même énergie / vitesse que le feu (photo foudre souvent indispo sur le CDN)
    "lightning.jpg": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=400&h=400&fit=crop&q=85&auto=format",
    "book.jpg": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop&q=85&auto=format",
    "controller.jpg": "https://images.unsplash.com/photo-1552820728-8b83bb6b773f?w=400&h=400&fit=crop&q=85&auto=format",
    "person.jpg": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=400&h=400&fit=crop&q=85&auto=format",
    "calendar.jpg": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=400&h=400&fit=crop&q=85&auto=format",
    "infinity.jpg": "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=400&h=400&fit=crop&q=85&auto=format",
    "question.jpg": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=400&fit=crop&q=85&auto=format",
    "info.jpg": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400&h=400&fit=crop&q=85&auto=format",
    "volume.jpg": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&q=85&auto=format",
    "play.jpg": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=400&fit=crop&q=85&auto=format",
    "arrow-left.jpg": "https://images.unsplash.com/photo-1506617420156-8e4536971650?w=400&h=400&fit=crop&q=85&auto=format",
    "arrow-repeat.jpg": "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=400&h=400&fit=crop&q=85&auto=format",
    "gem.jpg": "https://images.unsplash.com/photo-1617038260897-41a1f14a8ca0?w=400&h=400&fit=crop&q=85&auto=format",
    "folder.jpg": "https://images.unsplash.com/photo-1586281380117-5a60ae2050cc?w=400&h=400&fit=crop&q=85&auto=format",
    "hourglass.jpg": "https://images.unsplash.com/photo-1501139083538-0139583c060f?w=400&h=400&fit=crop&q=85&auto=format",
    "grid.jpg": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&h=400&fit=crop&q=85&auto=format",
    "link.jpg": "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=400&h=400&fit=crop&q=85&auto=format",
    "mic.jpg": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=400&h=400&fit=crop&q=85&auto=format",
    "login.jpg": "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400&h=400&fit=crop&q=85&auto=format",
    "register.jpg": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=400&h=400&fit=crop&q=85&auto=format",
    "menu.jpg": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=400&fit=crop&q=85&auto=format",
    "rank-1.jpg": "https://images.unsplash.com/photo-1614732414444-096e5f1122d5?w=400&h=400&fit=crop&q=85&auto=format",
    "rank-2.jpg": "https://images.unsplash.com/photo-1578269174936-2709b6aeb913?w=400&h=400&fit=crop&q=85&auto=format",
    "rank-3.jpg": "https://images.unsplash.com/photo-1578269174936-2709b6aeb913?w=400&h=400&fit=crop&q=85&auto=format",
    "celebration.jpg": "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=400&h=400&fit=crop&q=85&auto=format",
    "wave.jpg": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400&h=400&fit=crop&q=85&auto=format",
    "signal.jpg": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=400&h=400&fit=crop&q=85&auto=format",
    "graph-up.jpg": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=400&fit=crop&q=85&auto=format",
    "whatsapp.jpg": "https://images.unsplash.com/photo-1611746872915-64382b5c76da?w=400&h=400&fit=crop&q=85&auto=format",
    "home-users.jpg": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=400&h=400&fit=crop&q=85&auto=format",
    "home-lessons.jpg": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400&h=400&fit=crop&q=85&auto=format",
    "home-badges.jpg": "https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?w=400&h=400&fit=crop&q=85&auto=format",
    "feat-audio.jpg": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&q=85&auto=format",
    "feat-games.jpg": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=400&fit=crop&q=85&auto=format",
    "feat-badges.jpg": "https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?w=400&h=400&fit=crop&q=85&auto=format",
    "feat-progress.jpg": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=400&fit=crop&q=85&auto=format",
}


def main():
    ctx = ssl.create_default_context()
    for name, url in IMAGES.items():
        dest = BASE / name
        print(f"Téléchargement {name}...")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "LingX-assets/1.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
                dest.write_bytes(r.read())
            print(f"  OK ({dest.stat().st_size} octets)")
        except Exception as e:
            print(f"  ERREUR: {e}")


if __name__ == "__main__":
    main()
