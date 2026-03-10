# 📝 You-Blog — Hugo + PaperMod + GitHub Pages

Blog personnel déployé automatiquement via GitHub Actions sur GitHub Pages.

**URL** : [https://your github url/you-blog/](https://your github url/you-blog/)

---

## 🛠️ Stack

- **[Hugo](https://gohugo.io/)** v0.146.0+ (générateur de site statique)
- **[PaperMod](https://github.com/adityatelange/hugo-PaperMod)** (thème)
- **GitHub Actions** (CI/CD)
- **GitHub Pages** (hébergement gratuit)

---

## 📦 Installation

### 1. Installer Hugo (Linux)

```bash
wget https://github.com/gohugoio/hugo/releases/download/v0.146.0/hugo_extended_0.146.0_linux-amd64.deb
sudo dpkg -i hugo_extended_0.146.0_linux-amd64.deb
hugo version
```

### 2. Créer le projet

```bash
hugo new site you-blog
cd you-blog
git init
```

### 3. Ajouter le thème PaperMod

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
```

### 4. Configurer `hugo.toml`

```toml
baseURL = "https://your github url/you-blog/"
languageCode = "fr"
title = "Your name if you want | Blog" # You can shape this part at your taste
theme = "PaperMod"

[params]
  author = "Your name"
  description = "Cybersécurité, Réseaux, ML & DevOps" # You can shape this part at your taste 
  ShowReadingTime = true
  ShowShareButtons = false
  ShowPostNavLinks = true
  ShowToc = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true

  [params.homeInfoParams]
    Title = "Your name"
    Content = "Étudiant ingénieur en réseaux & cybersécurité · ML & DevOps" # You can shape this part at your taste 

  [[params.socialIcons]]
    name = "github"
    url = "https://your github url"

  [[params.socialIcons]]
    name = "linkedin"
    url = "https://your linkedin if you're interested" # You can shape this part at your taste 

[taxonomies]
  tag = "tags"
  category = "categories"

[menu]
  [[menu.main]]
    name = "Blog"
    url = "/posts/"
    weight = 1
  [[menu.main]]
    name = "Tags"
    url = "/tags/"
    weight = 2
  [[menu.main]]
    name = "À propos"
    url = "/about/"
    weight = 3
  [[menu.main]]
    name = "Portfolio"
    url = "https://your portfolio url" # You can shape this part at your taste
    weight = 4
```

### 5. Créer le `.gitignore`

```bash
echo "public/" > .gitignore
```

### 6. Tester en local

```bash
hugo server -D
# Ouvre http://localhost:1313/you-blog/
```

---

## 🚀 Déploiement

### 1. Créer le repo GitHub

Créer un repo `you-blog` sur GitHub (sans README ni .gitignore).

```bash
git remote add origin https://your github url/you-blog.git
git add .
git commit -m "init: hugo blog with PaperMod"
git push -u origin main
```

### 2. Créer le workflow GitHub Actions

Fichier `.github/workflows/deploy.yml` :

```yaml
name: Deploy Hugo Blog

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: "latest"
          extended: true

      - name: Build
        run: hugo --minify

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

```bash
git add .github/
git commit -m "ci: add hugo deploy workflow"
git push
```

### 3. Activer GitHub Pages

Dans **Settings → Pages** du repo GitHub :
- Source : **GitHub Actions**
- Sauvegarder

Le blog sera disponible sur `https://your github url.github.io/you-blog/` après le premier déploiement réussi (~1 min).

---

## ✍️ Publier un nouvel article

### Workflow complet

```bash
# 1. Créer le fichier de l'article
hugo new posts/titre-de-larticle.md

# 2. Éditer l'article
nano content/posts/titre-de-larticle.md
```

### Structure d'un article

```markdown
---
title: "Titre de l'article"
date: day of the publication
draft: false
tags: ["cybersécurité", "réseaux"]
categories: ["Veille technique"]
description: "Courte description affichée dans les previews."
---

## Introduction

Ton contenu ici en Markdown...

## Section 2

- Point 1
- Point 2

## Conclusion

...
```

> ⚠️ **Important** : `draft: false` est obligatoire pour que l'article soit publié. Tant que c'est `draft: true`, l'article n'apparaît qu'en local avec `hugo server -D`.

### 3. Vérifier en local

```bash
hugo server -D
# Vérifie sur http://localhost:1313/you-blog/
```

### 4. Publier

```bash
git add .
git commit -m "post: titre de l'article"
git push
```

GitHub Actions déploie automatiquement en ~1 minute.

---

## 📁 Structure du projet

```
ed-blog/
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD GitHub Actions
├── content/
│   ├── posts/               # Articles du blog
│   │   └── mon-article.md
│   └── about.md             # Page À propos
├── themes/
│   └── PaperMod/            # Thème (submodule git)
├── .gitignore               # Exclut public/
└── hugo.toml                # Configuration Hugo
```

---

## 🔧 Commandes utiles

| Commande | Description |
|---|---|
| `hugo server -D` | Serveur local avec drafts |
| `hugo new posts/titre.md` | Créer un nouvel article |
| `hugo --minify` | Build de production |
| `git submodule update --remote` | Mettre à jour PaperMod |
