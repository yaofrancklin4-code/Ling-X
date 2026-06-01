"""
create_pages_lingx.py
======================
Script tout-en-un pour le projet LingX (Django).

Ce script crée automatiquement trois nouvelles pages et les intègre
dans le menu déroulant du profil utilisateur (base.html).

  PAGE 1 — À propos  (/a-propos/)
    • Origine du projet LingX et de l'ESATIC
    • Portrait d'Othniel Yao, chef de projet, 2e année TWIN
    • Vision et mission de l'application

  PAGE 2 — Contact  (/contact/)
    • Coordonnées de toute l'équipe LingX
    • Lien vers l'ESATIC
    • Numéros WhatsApp, GitHub, Gmail de chaque membre

  PAGE 3 — Guide  (/guide/)
    • Explication claire pour les nouveaux utilisateurs
    • Présentation de toutes les fonctionnalités

UTILISATION :
    Placer ce fichier dans monprojet/ (dossier contenant manage.py et lingx/)
    puis exécuter :
        python create_pages_lingx.py

RÉSULTAT :
    • 3 fichiers HTML créés dans templates/
    • urls.py mis à jour avec les 3 nouvelles routes
    • views.py mis à jour avec les 3 nouvelles vues
    • base.html mis à jour : les 3 pages apparaissent dans le menu Profil

COMPATIBLE : Python 3.8+, Django 3.x / 4.x / 5.x
"""

import os
import re
import shutil
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
#  CHEMINS — adapter uniquement si ton projet a une structure différente
# ══════════════════════════════════════════════════════════════════════════════

BASE_DIR      = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
VIEWS_PATH    = BASE_DIR / "lingx" / "views.py"
URLS_PATH     = BASE_DIR / "lingx" / "urls.py"
BASE_HTML     = TEMPLATES_DIR / "base.html"


# ══════════════════════════════════════════════════════════════════════════════
#  TEMPLATE HTML — PAGE À PROPOS
# ══════════════════════════════════════════════════════════════════════════════

TEMPLATE_APROPOS = """\
{% extends 'base.html' %}
{% load static %}
{% block title %}À propos — LingX{% endblock %}
{% block content %}

<style>
  .apropos-hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: #fff;
    padding: 80px 0 60px;
    text-align: center;
  }
  .apropos-hero h1 { font-size: 3rem; font-weight: 900; letter-spacing: 2px; }
  .apropos-hero p  { font-size: 1.2rem; opacity: .85; max-width: 700px; margin: 20px auto 0; }
  .badge-esatic {
    display: inline-block;
    background: linear-gradient(90deg, #ffd700, #c0c0c0);
    color: #000;
    font-weight: 800;
    padding: 6px 18px;
    border-radius: 30px;
    font-size: .9rem;
    margin-bottom: 20px;
  }
  .section-card {
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 6px 30px rgba(0,0,0,.08);
    padding: 40px;
    margin-bottom: 30px;
  }
  .section-card h2 {
    font-weight: 800;
    color: #0f3460;
    border-left: 5px solid #ffd700;
    padding-left: 15px;
    margin-bottom: 20px;
  }
  .hero-othniel {
    background: linear-gradient(135deg, #0f3460, #1a1a2e);
    border-radius: 18px;
    color: #fff;
    padding: 40px;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
  }
  .hero-othniel::before {
    content: "⭐";
    font-size: 120px;
    opacity: .05;
    position: absolute;
    top: -20px;
    right: -10px;
  }
  .hero-othniel h2 { color: #ffd700; font-weight: 900; font-size: 1.8rem; }
  .hero-othniel .role-badge {
    background: #ffd700;
    color: #000;
    font-weight: 800;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: .85rem;
    display: inline-block;
    margin: 8px 0 15px;
  }
  .stat-row { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 20px; }
  .stat-box {
    background: rgba(255,255,255,.1);
    border-radius: 12px;
    padding: 15px 25px;
    text-align: center;
    flex: 1;
    min-width: 120px;
  }
  .stat-box .num { font-size: 2rem; font-weight: 900; color: #ffd700; }
  .stat-box .lbl { font-size: .8rem; opacity: .8; }
  .objectif-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }
  .objectif-item {
    background: #f8f9ff;
    border-radius: 14px;
    padding: 25px 20px;
    text-align: center;
    border-top: 4px solid #ffd700;
  }
  .objectif-item .icon { font-size: 2.5rem; margin-bottom: 10px; }
  .objectif-item h5 { font-weight: 800; color: #0f3460; margin-bottom: 8px; }
  .timeline { border-left: 3px solid #ffd700; padding-left: 25px; margin-top: 20px; }
  .timeline-item { margin-bottom: 25px; position: relative; }
  .timeline-item::before {
    content: "";
    width: 14px; height: 14px;
    background: #ffd700;
    border-radius: 50%;
    position: absolute;
    left: -32px; top: 4px;
  }
  .timeline-item .year {
    font-weight: 900; color: #0f3460; font-size: 1rem;
  }
</style>

<!-- HERO -->
<div class="apropos-hero">
  <div class="container">
    <span class="badge-esatic">ESATIC — Projet APP2 · 2025-2026</span>
    <h1>LingX</h1>
    <p>
      Une application née dans les salles de cours de l'ESATIC pour redonner vie
      à la langue baoulé — l'une des plus parlées de Côte d'Ivoire.
    </p>
  </div>
</div>

<div class="container py-5">

  <!-- ORIGINE DU PROJET -->
  <div class="section-card">
    <h2>D'où vient LingX ?</h2>
    <p>
      LingX est né d'un constat simple et alarmant : la langue baoulé, parlée par
      plus de <strong>30 % de la population ivoirienne</strong>, n'avait
      pratiquement <strong>aucune application numérique</strong> dédiée à son
      apprentissage. Les jeunes générations s'éloignaient de leur langue maternelle,
      faute d'outils modernes et accessibles.
    </p>
    <p>
      C'est dans ce contexte que des étudiants en <strong>2e année de licence TWIN
      (Technologies du Web et de l'Internet)</strong> à l'
      <a href="https://www.esatic.ci" target="_blank"><strong>ESATIC</strong></a>
      (École Supérieure Africaine des TIC) ont décidé de relever le défi, dans
      le cadre de leur projet d'Application (APP2) pour l'année académique
      <strong>2025-2026</strong>.
    </p>
    <p>
      Inspiré par la richesse du site <a href="https://baoule.ci" target="_blank">baoule.ci</a>
      — référence en ligne dédiée à la culture et à la mémoire du peuple baoulé —
      LingX s'est donné pour mission de rendre l'apprentissage de la langue
      <strong>ludique, accessible et gratuit</strong>, grâce à des jeux, des quiz
      et des sons enregistrés par des locuteurs natifs.
    </p>
  </div>

  <!-- OTHNIEL YAO — CHEF DE PROJET -->
  <div class="hero-othniel">
    <h2>Othniel Yao — Chef de Projet</h2>
    <div class="role-badge">Back-End Developer · Chef de Projet</div>
    <p style="font-size:1.05rem; line-height:1.8; opacity:.92;">
      Derrière LingX, il y a une vision, une détermination et un travail acharné
      portés par <strong style="color:#ffd700;">Othniel Yao Kouadio Franckline</strong>,
      étudiant en 2e année de TWIN à l'ESATIC et chef du projet de développement
      de l'application.
    </p>
    <p style="opacity:.9; line-height:1.8;">
      Othniel a conçu et mis en œuvre l'architecture complète de LingX :
      les <strong>modèles Django</strong>, l'<strong>ORM SQLite</strong>,
      les <strong>API REST</strong> et l'ensemble du back-end de l'application.
      C'est lui qui a transformé une idée de classe en un produit fonctionnel,
      en coordonnant l'équipe, en gérant les délais et en assurant la cohérence
      technique du projet de bout en bout.
    </p>
    <p style="opacity:.9; line-height:1.8;">
      Sa maîtrise de <strong>Python / Django</strong>, sa rigueur dans
      l'organisation du travail et son engagement personnel pour la valorisation
      de la culture baoulé ont été les pierres angulaires de la réussite
      de ce projet. Face aux obstacles techniques, aux nuits de débogage et
      aux délais serrés, Othniel a toujours maintenu le cap — avec la conviction
      que <em>préserver une langue, c'est préserver une identité</em>.
    </p>
    <div class="stat-row">
      <div class="stat-box">
        <div class="num">2e</div>
        <div class="lbl">Année TWIN</div>
      </div>
      <div class="stat-box">
        <div class="num">ESATIC</div>
        <div class="lbl">École</div>
      </div>
      <div class="stat-box">
        <div class="num">Chef</div>
        <div class="lbl">de Projet</div>
      </div>
      <div class="stat-box">
        <div class="num">Back-End</div>
        <div class="lbl">Développeur</div>
      </div>
    </div>
  </div>

  <!-- OBJECTIFS -->
  <div class="section-card">
    <h2>Nos Objectifs</h2>
    <div class="objectif-grid">
      <div class="objectif-item">
        <div class="icon">📚</div>
        <h5>Préserver</h5>
        <p>Numériser et sauvegarder le vocabulaire baoulé pour les générations futures.</p>
      </div>
      <div class="objectif-item">
        <div class="icon">🎮</div>
        <h5>Apprendre par le Jeu</h5>
        <p>Rendre l'apprentissage ludique grâce à des quiz, jeux et défis interactifs.</p>
      </div>
      <div class="objectif-item">
        <div class="icon">🔊</div>
        <h5>Audio Natif</h5>
        <p>Prononciations enregistrées par de vrais locuteurs baoulé.</p>
      </div>
      <div class="objectif-item">
        <div class="icon">🌐</div>
        <h5>Accessibilité</h5>
        <p>Gratuit, accessible hors-ligne, sans prérequis technique.</p>
      </div>
    </div>
  </div>

  <!-- TIMELINE -->
  <div class="section-card">
    <h2>Histoire du Projet</h2>
    <div class="timeline">
      <div class="timeline-item">
        <div class="year">Septembre 2025</div>
        <p>Identification du problème : absence d'outils numériques pour la langue baoulé.
           Formation de l'équipe et lancement du projet APP2 à l'ESATIC.</p>
      </div>
      <div class="timeline-item">
        <div class="year">Octobre – Novembre 2025</div>
        <p>Conception de l'architecture Django, création des modèles de données,
           premières maquettes UI/UX par Nando Nya.</p>
      </div>
      <div class="timeline-item">
        <div class="year">Décembre 2025 – Janvier 2026</div>
        <p>Développement du back-end (Othniel Yao), intégration du front-end (Auriol),
           collecte du contenu pédagogique (Elly) et enregistrements audio.</p>
      </div>
      <div class="timeline-item">
        <div class="year">Février – Avril 2026</div>
        <p>Tests, corrections, déploiement et finalisation de la plateforme LingX.</p>
      </div>
      <div class="timeline-item">
        <div class="year">2026 et au-delà</div>
        <p>Évolution continue : ajout de nouvelles leçons, intégration de l'IA,
           extension à d'autres langues ivoiriennes.</p>
      </div>
    </div>
  </div>

  <!-- ESATIC -->
  <div class="section-card" style="background:linear-gradient(135deg,#0f3460,#1a1a2e); color:#fff;">
    <h2 style="color:#ffd700; border-color:#ffd700;">L'ESATIC</h2>
    <p style="opacity:.9; line-height:1.8;">
      L'<strong style="color:#ffd700;">ESATIC</strong> (École Supérieure Africaine des TIC)
      est une grande école ivoirienne spécialisée dans les technologies de l'information
      et de la communication. Véritable vivier de talents numériques en Afrique de l'Ouest,
      elle forme des ingénieurs et techniciens capables de répondre aux défis
      de la transformation numérique du continent.
    </p>
    <p style="opacity:.9; line-height:1.8;">
      LingX est le fruit direct de cette formation d'excellence : c'est dans le cadre
      du module <strong style="color:#ffd700;">Projet d'Application (APP2)</strong> que
      l'équipe a conçu, développé et déployé cette plateforme — prouvant que
      la technologie africaine peut servir la culture africaine.
    </p>
    <a href="https://www.esatic.ci" target="_blank"
       style="display:inline-block; background:#ffd700; color:#000; font-weight:800;
              padding:10px 25px; border-radius:25px; text-decoration:none; margin-top:10px;">
      Visiter le site de l'ESATIC →
    </a>
  </div>

</div>
{% endblock %}
"""


# ══════════════════════════════════════════════════════════════════════════════
#  TEMPLATE HTML — PAGE CONTACT
# ══════════════════════════════════════════════════════════════════════════════

TEMPLATE_CONTACT = """\
{% extends 'base.html' %}
{% load static %}
{% block title %}Contact — LingX{% endblock %}
{% block content %}

<style>
  .contact-hero {
    background: linear-gradient(135deg, #0f3460, #1a1a2e);
    color: #fff;
    padding: 70px 0 50px;
    text-align: center;
  }
  .contact-hero h1 { font-size: 2.8rem; font-weight: 900; }
  .contact-hero p  { font-size: 1.1rem; opacity: .85; max-width: 600px; margin: 15px auto 0; }
  .member-card {
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 6px 30px rgba(0,0,0,.08);
    padding: 30px;
    margin-bottom: 25px;
    border-top: 5px solid #ffd700;
    transition: transform .2s;
  }
  .member-card:hover { transform: translateY(-4px); }
  .member-card.chef { border-top-color: #0f3460; background: linear-gradient(135deg, #f8f9ff, #fff); }
  .member-name {
    font-size: 1.4rem; font-weight: 900; color: #0f3460; margin-bottom: 4px;
  }
  .member-role {
    display: inline-block;
    background: #ffd700; color: #000; font-weight: 700;
    padding: 3px 12px; border-radius: 20px; font-size: .8rem; margin-bottom: 15px;
  }
  .member-card.chef .member-role { background: #0f3460; color: #fff; }
  .contact-link {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 15px;
    background: #f8f9ff;
    border-radius: 10px;
    margin-bottom: 8px;
    text-decoration: none;
    color: #333;
    font-weight: 600;
    transition: background .2s;
  }
  .contact-link:hover { background: #e8eeff; color: #0f3460; }
  .contact-link .icon { font-size: 1.3rem; width: 28px; text-align: center; }
  .section-title {
    font-size: 1.8rem; font-weight: 900; color: #0f3460;
    border-left: 5px solid #ffd700; padding-left: 15px; margin: 40px 0 25px;
  }
  .esatic-box {
    background: linear-gradient(135deg, #0f3460, #1a1a2e);
    border-radius: 18px; color: #fff; padding: 35px; margin-bottom: 30px;
  }
  .esatic-box h3 { color: #ffd700; font-weight: 900; margin-bottom: 15px; }
</style>

<!-- HERO -->
<div class="contact-hero">
  <div class="container">
    <h1>Contactez-nous</h1>
    <p>
      Une question, une suggestion ou envie de rejoindre l'aventure LingX ?
      Chaque membre de l'équipe est disponible pour vous répondre.
    </p>
  </div>
</div>

<div class="container py-5">

  <!-- CHEF DE PROJET -->
  <h2 class="section-title">Chef de Projet</h2>

  <div class="member-card chef">
    <div class="member-name">Othniel Yao Kouadio Franckline</div>
    <span class="member-role">Chef de Projet · Back-End Developer · 2e année TWIN</span>
    <p class="text-muted mb-3">
      Concepteur et développeur principal de LingX. Pour toute question technique,
      proposition de collaboration ou retour sur l'application, Othniel est votre
      premier point de contact.
    </p>
    <a class="contact-link"
       href="https://wa.me/2250501707887" target="_blank">
      <span class="icon">💬</span>
      WhatsApp : +225 05 01 70 78 87
    </a>
    <a class="contact-link"
       href="https://github.com/yaofrancklin4-code" target="_blank">
      <span class="icon">GitHub</span>
      yaofrancklin4-code
    </a>
    <a class="contact-link"
       href="mailto:franckliny77@gmail.com">
      <span class="icon">Gmail</span>
      franckliny77@gmail.com
    </a>
  </div>

  <!-- ÉQUIPE -->
  <h2 class="section-title">L'Équipe LingX</h2>

  <div class="row">

    <div class="col-md-6">
      <div class="member-card">
        <div class="member-name">Homplou Auriol</div>
        <span class="member-role">Lead Front-End</span>
        <p class="text-muted mb-3">Templates Django · Bootstrap · Animations · JS Quiz</p>
        <a class="contact-link"
           href="https://wa.me/22508840103" target="_blank">
          <span class="icon">💬</span>
          WhatsApp : +225 88 40 10 3
        </a>
      </div>
    </div>

    <div class="col-md-6">
      <div class="member-card">
        <div class="member-name">Nando Nya</div>
        <span class="member-role">UX / UI Designer</span>
        <p class="text-muted mb-3">Maquettes · Identité visuelle · Expérience utilisateur</p>
        <a class="contact-link"
           href="https://wa.me/225786767816" target="_blank">
          <span class="icon">💬</span>
          WhatsApp : +225 78 67 67 81
        </a>
      </div>
    </div>

    <div class="col-md-6">
      <div class="member-card">
        <div class="member-name">Tidiane</div>
        <span class="member-role">Back-End & Déploiement</span>
        <p class="text-muted mb-3">Django Admin · Authentification · Tests · Hébergement</p>
        <a class="contact-link"
           href="https://wa.me/225698937404" target="_blank">
          <span class="icon">💬</span>
          WhatsApp : +225 69 89 37 40
        </a>
      </div>
    </div>

    <div class="col-md-6">
      <div class="member-card">
        <div class="member-name">Elly</div>
        <span class="member-role">Contenu Pédagogique</span>
        <p class="text-muted mb-3">Leçons Baoulé · Audio · Validation par des experts</p>
        <a class="contact-link"
           href="https://wa.me/225438747950" target="_blank">
          <span class="icon">💬</span>
          WhatsApp : +225 43 87 47 95
        </a>
      </div>
    </div>

  </div>

  <!-- ESATIC -->
  <div class="esatic-box">
    <h3>ESATIC — École Supérieure Africaine des TIC</h3>
    <p style="opacity:.9; line-height:1.8;">
      LingX est un projet académique développé dans le cadre du module APP2
      de l'<strong>ESATIC</strong>, école de référence en technologies de l'information
      et de la communication en Côte d'Ivoire.
    </p>
    <a class="contact-link" href="https://www.esatic.ci" target="_blank"
       style="background:rgba(255,255,255,.15); color:#fff; margin-top:10px; display:flex; width:fit-content; padding:10px 20px;">
      <span class="icon">Web</span>
      www.esatic.ci
    </a>
    <a class="contact-link" href="mailto:contact@baoule.ci"
       style="background:rgba(255,255,255,.15); color:#fff; margin-top:8px; display:flex; width:fit-content; padding:10px 20px;">
      <span class="icon">Email</span>
      contact@baoule.ci
    </a>
  </div>

</div>
{% endblock %}
"""


# ══════════════════════════════════════════════════════════════════════════════
#  TEMPLATE HTML — PAGE GUIDE
# ══════════════════════════════════════════════════════════════════════════════

TEMPLATE_GUIDE = """\
{% extends 'base.html' %}
{% load static %}
{% block title %}Guide d'utilisation — LingX{% endblock %}
{% block content %}

<style>
  .guide-hero {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    color: #fff; padding: 70px 0 50px; text-align: center;
  }
  .guide-hero h1 { font-size: 2.8rem; font-weight: 900; }
  .guide-hero p  { font-size: 1.1rem; opacity: .85; max-width: 650px; margin: 15px auto 0; }
  .step-section {
    background: #fff; border-radius: 18px;
    box-shadow: 0 6px 30px rgba(0,0,0,.08);
    padding: 40px; margin-bottom: 30px;
  }
  .step-section h2 {
    font-weight: 900; color: #0f3460;
    border-left: 5px solid #ffd700; padding-left: 15px; margin-bottom: 25px;
  }
  .step {
    display: flex; gap: 20px; align-items: flex-start;
    margin-bottom: 25px; padding-bottom: 25px;
    border-bottom: 1px solid #f0f0f0;
  }
  .step:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
  .step-num {
    min-width: 48px; height: 48px;
    background: linear-gradient(135deg, #ffd700, #c0c0c0);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-weight: 900; font-size: 1.3rem; color: #000;
  }
  .step-content h5 { font-weight: 800; color: #0f3460; margin-bottom: 5px; }
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px; margin-top: 20px;
  }
  .feature-box {
    background: #f8f9ff; border-radius: 14px; padding: 25px;
    border-top: 4px solid #0f3460;
  }
  .feature-box .ficon { font-size: 2.2rem; margin-bottom: 10px; }
  .feature-box h5 { font-weight: 800; color: #0f3460; margin-bottom: 8px; }
  .tip-box {
    background: linear-gradient(135deg, #fffbea, #fff8d6);
    border-left: 5px solid #ffd700;
    border-radius: 0 14px 14px 0;
    padding: 20px 25px; margin: 20px 0;
  }
  .tip-box strong { color: #0f3460; }
  .faq-item {
    border: 1px solid #e8eeff; border-radius: 12px;
    padding: 20px; margin-bottom: 15px;
  }
  .faq-item h5 { color: #0f3460; font-weight: 800; margin-bottom: 8px; }
</style>

<!-- HERO -->
<div class="guide-hero">
  <div class="container">
    <h1>Guide d'utilisation</h1>
    <p>
      Bienvenue sur LingX ! Ce guide vous explique tout ce que vous pouvez faire
      sur la plateforme, étape par étape.
    </p>
  </div>
</div>

<div class="container py-5">

  <!-- DÉMARRAGE -->
  <div class="step-section">
    <h2>Démarrer sur LingX</h2>

    <div class="step">
      <div class="step-num">1</div>
      <div class="step-content">
        <h5>Créer votre compte</h5>
        <p>Cliquez sur <strong>Inscription</strong> en haut à droite.
           Entrez un nom d'utilisateur, une adresse e-mail et un mot de passe.
           Vous pouvez aussi vous connecter rapidement avec votre compte Google.</p>
      </div>
    </div>

    <div class="step">
      <div class="step-num">2</div>
      <div class="step-content">
        <h5>Se connecter</h5>
        <p>Utilisez le bouton <strong>Connexion</strong> avec votre e-mail et
           mot de passe, ou votre compte Google. Une fois connecté, toutes les
           fonctionnalités de la plateforme sont disponibles.</p>
      </div>
    </div>

    <div class="step">
      <div class="step-num">3</div>
      <div class="step-content">
        <h5>Découvrir le tableau de bord</h5>
        <p>Votre <strong>Tableau de bord</strong> résume votre progression,
           vos points, vos badges et vos activités récentes. C'est votre
           point de départ pour chaque session d'apprentissage.</p>
      </div>
    </div>

  </div>

  <!-- FONCTIONNALITÉS -->
  <div class="step-section">
    <h2>Les fonctionnalités de LingX</h2>

    <div class="feature-grid">

      <div class="feature-box">
        <div class="ficon">📚</div>
        <h5>Leçons</h5>
        <p>Des cours structurés par catégories (salutations, aliments, famille…).
           Chaque leçon présente le vocabulaire baoulé avec sa traduction française
           et sa prononciation.</p>
      </div>

      <div class="feature-box">
        <div class="ficon">?</div>
        <h5>Quiz</h5>
        <p>À la fin de chaque leçon, un quiz teste vos connaissances.
           Répondez correctement pour gagner des <strong>points XP</strong>
           et débloquer des badges.</p>
      </div>

      <div class="feature-box">
        <div class="ficon">JEUX</div>
        <h5>Jeux</h5>
        <p>Des mini-jeux interactifs pour apprendre en s'amusant :
           association de mots, devinettes, etc. Parfait pour réviser
           sans s'en rendre compte !</p>
      </div>

      <div class="feature-box">
        <div class="ficon">DICT</div>
        <h5>Dictionnaire</h5>
        <p>Un dictionnaire Baoulé ↔ Français consultable à tout moment.
           Recherchez un mot dans les deux langues grâce à la barre de recherche.</p>
      </div>

      <div class="feature-box">
        <div class="ficon">CULT</div>
        <h5>Culture</h5>
        <p>Découvrez l'histoire, les proverbes, les contes et la culture
           du peuple baoulé. Une façon d'apprendre la langue dans son contexte
           culturel.</p>
      </div>

      <div class="feature-box">
        <div class="ficon">RANK</div>
        <h5>Classement</h5>
        <p>Comparez votre score avec celui des autres apprenants.
           Montez dans le classement en accumulant des points et en
           maintenant votre <strong>streak</strong> quotidien.</p>
      </div>

      <div class="feature-box">
        <div class="ficon">BADGE</div>
        <h5>Badges & Récompenses</h5>
        <p>Débloquez des badges en atteignant des objectifs :
           première leçon terminée, 7 jours consécutifs, score parfait…
           Collectionnez-les tous !</p>
      </div>

      <div class="feature-box">
        <div class="ficon">COMM</div>
        <h5>Communauté</h5>
        <p>Rejoignez la communauté LingX, partagez votre progression
           et encouragez les autres apprenants dans leur voyage linguistique.</p>
      </div>

    </div>
  </div>

  <!-- CONSEILS -->
  <div class="step-section">
    <h2>Conseils pour progresser vite</h2>

    <div class="tip-box">
      <strong>Pratiquez tous les jours !</strong><br>
      Même 10 minutes par jour suffisent. LingX récompense la régularité
      avec un système de <em>streak</em> (série de jours consécutifs).
      Plus votre streak est long, plus vous gagnez de points bonus.
    </div>

    <div class="tip-box">
      <strong>Écoutez les prononciations</strong><br>
      Le baoulé est une langue tonale : la mélodie du mot est aussi
      importante que les lettres. Utilisez les boutons audio pour entendre
      chaque mot prononcé par un locuteur natif.
    </div>

    <div class="tip-box">
      <strong>Commencez par les jeux</strong><br>
      Si vous débutez complètement, les mini-jeux sont le moyen le plus
      naturel de mémoriser les premiers mots sans effort.
    </div>

    <div class="tip-box">
      <strong>Consultez le dictionnaire régulièrement</strong><br>
      Quand vous rencontrez un mot inconnu dans la vie courante,
      cherchez-le dans le dictionnaire LingX pour faire le lien.
    </div>

  </div>

  <!-- FAQ -->
  <div class="step-section">
    <h2>Questions fréquentes</h2>

    <div class="faq-item">
      <h5>LingX est-il gratuit ?</h5>
      <p>Oui, LingX est entièrement gratuit. Créez un compte et accédez
         à toutes les fonctionnalités sans aucun abonnement.</p>
    </div>

    <div class="faq-item">
      <h5>Faut-il parler français pour utiliser LingX ?</h5>
      <p>Oui, l'interface est en français. LingX vous apprend le baoulé
         à partir du français comme langue de référence.</p>
    </div>

    <div class="faq-item">
      <h5>Puis-je utiliser LingX sans connexion internet ?</h5>
      <p>Le mode hors-ligne est prévu dans les prochaines versions.
         Pour l'instant, une connexion internet est nécessaire.</p>
    </div>

    <div class="faq-item">
      <h5>Comment signaler un bug ou suggérer une amélioration ?</h5>
      <p>Rendez-vous sur la page <a href="{% url 'contact' %}"><strong>Contact</strong></a>
         et écrivez directement à l'équipe. Vos retours sont précieux !</p>
    </div>

    <div class="faq-item">
      <h5>Qui a créé LingX ?</h5>
      <p>LingX a été créé par une équipe d'étudiants de l'<strong>ESATIC</strong>
         en 2e année de licence TWIN, dans le cadre de leur projet APP2 2025-2026.
         Consultez la page <a href="{% url 'about' %}"><strong>À propos</strong></a>
         pour en savoir plus.</p>
    </div>

  </div>

  <!-- CTA -->
  <div style="text-align:center; padding: 30px 0;">
    <a href="{% url 'categories' %}"
       style="display:inline-block; background:linear-gradient(135deg,#0f3460,#1a1a2e);
              color:#fff; font-weight:800; padding:15px 40px; border-radius:30px;
              text-decoration:none; font-size:1.1rem; margin-right:15px;">
      Commencer à apprendre
    </a>
    <a href="{% url 'contact' %}"
       style="display:inline-block; background:#ffd700; color:#000;
              font-weight:800; padding:15px 40px; border-radius:30px;
              text-decoration:none; font-size:1.1rem;">
      Nous contacter
    </a>
  </div>

</div>
{% endblock %}
"""


# ══════════════════════════════════════════════════════════════════════════════
#  NOUVELLES VUES Django à ajouter dans views.py
# ══════════════════════════════════════════════════════════════════════════════

NEW_VIEWS = """

# ─── Pages statiques : À propos / Contact / Guide ──────────────────────────

def about_view(request):
    \"\"\"Page À propos — histoire de LingX et présentation de l'équipe.\"\"\"
    return render(request, 'about.html')


def contact_view(request):
    \"\"\"Page Contact — coordonnées de l'équipe LingX et de l'ESATIC.\"\"\"
    return render(request, 'contact.html')


def guide_view(request):
    \"\"\"Page Guide — aide et tutoriel pour les nouveaux utilisateurs.\"\"\"
    return render(request, 'guide.html')

"""

# ══════════════════════════════════════════════════════════════════════════════
#  NOUVELLES ROUTES à ajouter dans urls.py
# ══════════════════════════════════════════════════════════════════════════════

NEW_URLS = """\
    path('a-propos/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('guide/', views.guide_view, name='guide'),\
"""

# ══════════════════════════════════════════════════════════════════════════════
#  LIENS à insérer dans le dropdown Profil de base.html
# ══════════════════════════════════════════════════════════════════════════════

NEW_MENU_ITEMS = """\
                <li><hr class="dropdown-divider" /></li>
                <li>
                  <a class="dropdown-item" href="{% url 'about' %}">À propos</a>
                </li>
                <li>
                  <a class="dropdown-item" href="{% url 'contact' %}">Contact</a>
                </li>
                <li>
                  <a class="dropdown-item" href="{% url 'guide' %}">Guide</a>
                </li>\
"""

# ══════════════════════════════════════════════════════════════════════════════
#  FONCTIONS D'INSTALLATION
# ══════════════════════════════════════════════════════════════════════════════

def backup(path: Path) -> None:
    """Crée une sauvegarde .bak avant modification."""
    bak = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, bak)
    print(f"  [✓] Sauvegarde : {bak.name}")


def task1_creer_templates():
    """Crée les 3 fichiers HTML dans templates/."""
    print("\n── TÂCHE 1 : Création des templates HTML ───────────────────────")
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    pages = [
        ("about.html",   TEMPLATE_APROPOS, "À propos"),
        ("contact.html", TEMPLATE_CONTACT, "Contact"),
        ("guide.html",   TEMPLATE_GUIDE,   "Guide"),
    ]
    for filename, content, label in pages:
        path = TEMPLATES_DIR / filename
        path.write_text(content, encoding="utf-8")
        print(f"  [✓] templates/{filename} créé ({label})")


def task2_ajouter_vues():
    """Ajoute les 3 vues dans lingx/views.py."""
    print("\n── TÂCHE 2 : Ajout des vues dans views.py ──────────────────────")

    if not VIEWS_PATH.exists():
        print(f"  [ERREUR] Fichier introuvable : {VIEWS_PATH}")
        return

    source = VIEWS_PATH.read_text(encoding="utf-8")

    # Évite les doublons si le script est relancé
    if "def about_view" in source:
        print("  [i] Les vues existent déjà — aucune modification.")
        return

    backup(VIEWS_PATH)
    source += NEW_VIEWS
    VIEWS_PATH.write_text(source, encoding="utf-8")
    print("  [✓] about_view, contact_view, guide_view ajoutées à views.py")


def task3_ajouter_urls():
    """Ajoute les 3 routes dans lingx/urls.py."""
    print("\n── TÂCHE 3 : Ajout des routes dans urls.py ─────────────────────")

    if not URLS_PATH.exists():
        print(f"  [ERREUR] Fichier introuvable : {URLS_PATH}")
        return

    source = URLS_PATH.read_text(encoding="utf-8")

    # Évite les doublons si le script est relancé
    if "about_view" in source:
        print("  [i] Les routes existent déjà — aucune modification.")
        return

    backup(URLS_PATH)

    # Insère les routes juste avant le dernier "]" du urlpatterns
    # Cherche le marqueur "# API REST" ou la fin de urlpatterns
    marker = "    # API REST"
    if marker in source:
        source = source.replace(marker, NEW_URLS + "\n\n" + marker)
    else:
        # Fallback : insère avant le dernier "]"
        last_bracket = source.rfind("]")
        source = source[:last_bracket] + "\n" + NEW_URLS + "\n" + source[last_bracket:]

    URLS_PATH.write_text(source, encoding="utf-8")
    print("  [✓] Routes /a-propos/, /contact/, /guide/ ajoutées à urls.py")


def task4_mettre_a_jour_menu():
    """Ajoute les liens dans le menu déroulant Profil de base.html."""
    print("\n── TÂCHE 4 : Mise à jour du menu Profil dans base.html ─────────")

    if not BASE_HTML.exists():
        print(f"  [ERREUR] Fichier introuvable : {BASE_HTML}")
        return

    source = BASE_HTML.read_text(encoding="utf-8")

    # Évite les doublons si le script est relancé
    if "url 'about'" in source:
        print("  [i] Les liens de menu existent déjà — aucune modification.")
        return

    backup(BASE_HTML)

    # Cherche le bouton Déconnexion dans le dropdown profil et insère avant
    # Le marqueur est la ligne avec "text-danger" et "logout"
    marker = """                <li>
                  <a
                    class="dropdown-item text-danger"
                    href="{% url 'logout' %}\""""

    if marker in source:
        source = source.replace(marker, NEW_MENU_ITEMS + "\n" + marker)
        BASE_HTML.write_text(source, encoding="utf-8")
        print("  [✓] Liens À propos, Contact, Guide ajoutés dans le menu Profil")
    else:
        # Fallback : cherche juste "logout" dans le dropdown
        logout_marker = 'href="{% url \'logout\' %}"'
        if logout_marker in source:
            source = source.replace(logout_marker, logout_marker, 1)
            # Insère avant le premier <li> contenant logout
            idx = source.find(logout_marker)
            li_start = source.rfind("<li>", 0, idx)
            source = source[:li_start] + NEW_MENU_ITEMS + "\n                " + source[li_start:]
            BASE_HTML.write_text(source, encoding="utf-8")
            print("  [✓] Liens ajoutés dans le menu (méthode fallback)")
        else:
            print("  [!] Marqueur introuvable dans base.html — ajoute manuellement :")
            print("      (voir NEW_MENU_ITEMS dans ce script)")


# ══════════════════════════════════════════════════════════════════════════════
#  POINT D'ENTRÉE
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  create_pages_lingx.py")
    print("  Création des pages : À propos · Contact · Guide")
    print("=" * 60)

    task1_creer_templates()
    task2_ajouter_vues()
    task3_ajouter_urls()
    task4_mettre_a_jour_menu()

    print("\n" + "=" * 60)
    print("  [✓] Toutes les tâches terminées !")
    print()
    print("  PROCHAINE ÉTAPE :")
    print("  → Redémarre le serveur Django :")
    print("    python manage.py runserver")
    print()
    print("  PAGES DISPONIBLES :")
    print("    /a-propos/ · /contact/ · /guide/")
    print("  (accessibles aussi via le menu Profil)")
    print("=" * 60)


if __name__ == "__main__":
    main()
