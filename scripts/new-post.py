#!/usr/bin/env python3
"""
Création interactive d'un article Hugo pour ed-blog.
Usage : python3 scripts/new-post.py
"""

import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

BLOG_ROOT = Path(__file__).parent.parent
CONTENT_DIR = BLOG_ROOT / "content"
STATIC_IMAGES_DIR = BLOG_ROOT / "static" / "images"

SECTIONS = ["cybersecurite", "labs", "reseau", "articles"]

# ── helpers ───────────────────────────────────────────────────────────────────

def clr(code, text):
    return f"\033[{code}m{text}\033[0m"

def titre(text):
    print(f"\n{clr('1;36', '▶ ' + text)}")

def ok(text):
    print(clr('1;32', '  ✓ ' + text))

def err(text):
    print(clr('1;31', '  ✗ ' + text))

def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    val = input(f"  {prompt}{suffix} : ").strip()
    return val if val else default

def ask_yn(prompt, default="o"):
    suffix = "[O/n]" if default == "o" else "[o/N]"
    val = input(f"  {prompt} {suffix} : ").strip().lower()
    if not val:
        return default == "o"
    return val in ("o", "oui", "y", "yes")

def slugify(text):
    text = text.lower()
    text = re.sub(r"[àáâãäå]", "a", text)
    text = re.sub(r"[èéêë]", "e", text)
    text = re.sub(r"[ìíîï]", "i", text)
    text = re.sub(r"[òóôõö]", "o", text)
    text = re.sub(r"[ùúûü]", "u", text)
    text = re.sub(r"[ç]", "c", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def separator():
    print(clr("90", "  " + "─" * 56))

# ── étapes ────────────────────────────────────────────────────────────────────

def choisir_section():
    titre("Section de l'article")
    for i, s in enumerate(SECTIONS, 1):
        print(f"  {i}. {s}")
    while True:
        choix = ask("Numéro de section")
        if choix and choix.isdigit() and 1 <= int(choix) <= len(SECTIONS):
            return SECTIONS[int(choix) - 1]
        err("Choix invalide, entrez un numéro entre 1 et " + str(len(SECTIONS)))


def choisir_slug():
    titre("Nom du fichier (slug)")
    print("  Ce nom deviendra l'URL de l'article (ex: vpn-wireguard-linux)")
    while True:
        slug = ask("Slug")
        if not slug:
            err("Le slug ne peut pas être vide.")
            continue
        slug = slugify(slug)
        print(f"  Slug généré : {clr('1;33', slug)}")
        if ask_yn("Confirmer ce slug ?"):
            return slug


def saisir_contenu():
    titre("Contenu de l'article")
    print("  1. Coller le texte directement")
    print("  2. Fournir le chemin d'un fichier texte (.txt)")
    choix = ask("Choix (1 ou 2)", default="1")

    if choix == "2":
        while True:
            chemin = ask("Chemin du fichier")
            p = Path(chemin).expanduser()
            if p.is_file():
                contenu = p.read_text(encoding="utf-8")
                ok(f"Fichier chargé ({len(contenu)} caractères)")
                return contenu
            else:
                err(f"Fichier introuvable : {p}")
    else:
        print("  Collez votre texte puis appuyez sur " + clr("1;33", "Ctrl+D") + " pour valider.")
        lignes = []
        while True:
            try:
                ligne = input()
            except EOFError:
                break
            lignes.append(ligne)
        # Réouvrir le terminal pour les questions suivantes
        try:
            sys.stdin = open("/dev/tty")
        except OSError:
            pass
        contenu = "\n".join(lignes)
        ok(f"Contenu reçu ({len(contenu)} caractères)")
        return contenu


def traiter_images(contenu):
    titre("Images")
    refs = re.findall(r"\[image:([^\]]+)\]", contenu)

    if not refs:
        print("  Aucune référence image détectée dans le contenu.")
        return contenu, []

    print(f"  Références détectées : {clr('1;33', str(refs))}")
    print("  Fournissez le dossier contenant ces images (laisser vide pour ignorer).")
    dossier = ask("Dossier images")

    images_copiees = []
    if dossier:
        src_dir = Path(dossier).expanduser()
        if not src_dir.is_dir():
            err(f"Dossier introuvable : {src_dir}")
        else:
            STATIC_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
            for ref in refs:
                src = src_dir / ref
                if src.is_file():
                    dst = STATIC_IMAGES_DIR / ref
                    shutil.copy2(src, dst)
                    images_copiees.append(ref)
                    ok(f"Image copiée : {ref}")
                else:
                    err(f"Image non trouvée : {src}")

    # Remplacer les [image:xxx] par du Markdown
    def remplacer(m):
        nom = m.group(1)
        return f"![{nom}](/images/{nom})"

    contenu_md = re.sub(r"\[image:([^\]]+)\]", remplacer, contenu)
    return contenu_md, images_copiees


def saisir_metadonnees():
    titre("Métadonnées de l'article")

    title = ask("Titre de l'article")
    description = ask("Description courte (résumé pour SEO/aperçu)")

    print("  Tags (séparés par des virgules, ex: vpn, réseau, linux)")
    tags_raw = ask("Tags", default="")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]

    toc = ask_yn("Afficher une table des matières (toc) ?", default="o")
    draft = ask_yn("Publier en brouillon (draft) ?", default="n")

    return {
        "title": title,
        "description": description,
        "tags": tags,
        "toc": toc,
        "draft": draft,
        "date": date.today().isoformat(),
    }


def generer_frontmatter(meta):
    tags_str = ", ".join(f'"{t}"' for t in meta["tags"])
    toc_str = "true" if meta["toc"] else "false"
    draft_str = "true" if meta["draft"] else "false"
    return (
        "+++\n"
        f'title = "{meta["title"]}"\n'
        f'date = {meta["date"]}\n'
        f'tags = [{tags_str}]\n'
        f'draft = {draft_str}\n'
        f'toc = {toc_str}\n'
        f'description = "{meta["description"]}"\n'
        "+++"
    )


def apercu(section, slug, meta, images):
    separator()
    titre("Résumé avant génération")
    print(f"  Fichier  : content/{section}/{slug}.md")
    print(f"  Titre    : {meta['title']}")
    print(f"  Date     : {meta['date']}")
    print(f"  Tags     : {meta['tags']}")
    print(f"  TOC      : {meta['toc']} | Draft : {meta['draft']}")
    print(f"  Images   : {images if images else 'aucune'}")
    separator()


def ecrire_fichier(section, slug, frontmatter, contenu):
    dest_dir = CONTENT_DIR / section
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{slug}.md"
    dest.write_text(frontmatter + "\n\n" + contenu, encoding="utf-8")
    ok(f"Fichier créé : {dest.relative_to(BLOG_ROOT)}")
    return dest


def git_push(slug):
    titre("Déploiement Git")
    msg_default = f"feat: nouvel article — {slug}"
    print(f"  Message par défaut : {clr('90', msg_default)}")
    msg_saisi = ask("Message de commit (laisser vide = message par défaut)")
    msg = msg_saisi if msg_saisi else msg_default

    try:
        subprocess.run(["git", "-C", str(BLOG_ROOT), "add", "."], check=True)
        subprocess.run(["git", "-C", str(BLOG_ROOT), "commit", "-m", msg], check=True)
        subprocess.run(["git", "-C", str(BLOG_ROOT), "push"], check=True)
        ok("Article publié avec succès !")
    except subprocess.CalledProcessError as e:
        err(f"Erreur Git : {e}")
        sys.exit(1)

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print(clr("1;35", "\n╔══════════════════════════════════════╗"))
    print(clr("1;35",   "║   Nouvel article — ed-blog (Hugo)    ║"))
    print(clr("1;35",   "╚══════════════════════════════════════╝"))

    section = choisir_section()
    slug = choisir_slug()
    contenu_brut = saisir_contenu()
    contenu_md, images = traiter_images(contenu_brut)
    meta = saisir_metadonnees()
    frontmatter = generer_frontmatter(meta)

    apercu(section, slug, meta, images)

    if not ask_yn("Générer et publier l'article ?"):
        print("  Annulé.")
        sys.exit(0)

    ecrire_fichier(section, slug, frontmatter, contenu_md)

    if ask_yn("Faire le git push maintenant ?"):
        git_push(slug)
    else:
        print("  Git push ignoré. Lance `git push` quand tu es prêt.")

    print(clr("1;32", "\n  Terminé ! 🎉\n"))


if __name__ == "__main__":
    main()
