import re

with open('monprojet/templates/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern pour trouver la section galerie culturelle
pattern = r'(<!-- Card 1: Tissus traditionnels -->.*?</div>\s*</div>\s*</div>\s*<!-- Card 2: Artisanat -->.*?</div>\s*</div>\s*</div>\s*<!-- Card 3: Femmes Baoulé -->.*?</div>\s*</div>\s*</div>)'

replacement = '''<!-- Card 1: Tissus traditionnels -->
    <div class="col-md-4 mb-4">
      <div class="card h-100">
        <div class="card-body">
          <h5 class="card-title">Tissus Traditionnels</h5>
          <p class="card-text">Des tissus aux motifs symboliques qui racontent l'histoire du peuple baoulé.</p>
        </div>
      </div>
    </div>
    <!-- Card 2: Artisanat -->
    <div class="col-md-4 mb-4">
      <div class="card h-100">
        <div class="card-body">
          <h5 class="card-title">Artisanat Baoulé</h5>
          <p class="card-text">L'art et l'artisanat traditionnel qui font la richesse du patrimoine baoulé.</p>
        </div>
      </div>
    </div>
    <!-- Card 3: Femmes Baoulé -->
    <div class="col-md-4 mb-4">
      <div class="card h-100">
        <div class="card-body">
          <h5 class="card-title">Femmes Baoulé</h5>
          <p class="card-text">Le rôle important des femmes dans la société baoulé et la transmission des traditions.</p>
        </div>
      </div>
    </div>'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('monprojet/templates/home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Galerie culturelle mise a jour avec texte simple')
