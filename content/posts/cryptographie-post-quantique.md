---
title: "Cryptographie Post-Quantique"
date: 2026-03-10
draft: false
tags: ["cybersécurité", "cryptographie", "réseaux"]
categories: ["Veille technique"]
description: "🔐 Pourquoi s’intéresse-t-on particulièrement à TLS, SSH et IPsec dans la transition post-quantique ?"
---

📅 Le 2 février 2026, l’ANSSI a publié plusieurs fiches techniques concernant la transition post-quantique de trois protocoles majeurs :\
🔹 TLS 1.3\
🔹 SSHv2\
🔹 IPsec\
Ces documents proposent à la fois un état des lieux et des pistes techniques pour préparer la migration vers la cryptographie post-quantique.


En parcourant ces publications, une question m’est immédiatement venue à l’esprit :


❓ Pourquoi seulement ces trois protocoles ?


La menace quantique ne concerne-t-elle pas un ensemble bien plus large de systèmes cryptographiques ?


Cette interrogation m’a conduit à mener quelques investigations sur les menaces projetées du calcul quantique sur les systèmes cryptographiques actuels.


🧠 Qu’est-ce que la cryptographie post-quantique ?

Commençons par rappeler ce qu’est la cryptographie post-quantique (PQC).

Selon l’ANSSI :
La cryptographie post-quantique (PQC) est un ensemble d’algorithmes de cryptographie classique comprenant les établissements de clés et les signatures numériques et assurant une sécurité conjecturée contre la menace quantique en plus de leur sécurité classique.

Cette définition révèle déjà un indice important.

Les expressions « établissement de clés » et « signatures numériques » renvoient principalement à la cryptographie à clé publique (cryptographie asymétrique).

Je me suis alors naturellement posé une autre question :


❓ La cryptographie à clé secrète (symétrique) sera-t-elle elle aussi fortement affectée ?

Pour répondre à ces questions, je propose le cheminement suivant :

1️⃣ rappeler le rôle de TLS, SSH et IPsec\
2️⃣ comprendre pourquoi la cryptographie asymétrique est menacée\
3️⃣ expliquer pourquoi la cryptographie symétrique est beaucoup moins impactée


🌐 TLS, SSH et IPsec : des piliers de la sécurité sur Internet

Ces trois protocoles utilisent des algorithmes de cryptographie à clé publique, tels que :\
🔹 RSA\
🔹 Diffie-Hellman\
🔹 les courbes elliptiques (ECC)\
Bien qu’ils remplissent des fonctions différentes, ils peuvent être considérés comme des pierres angulaires des communications sécurisées sur Internet.


🔒 TLS (Transport Layer Security)

TLS est principalement utilisé avec HTTP, donnant naissance à HTTPS.

Ce protocole permet aux applications client-serveur de communiquer de manière sécurisée en évitant :\
🕵️ l’écoute du trafic\
🛑 la falsification des données\
⚠️ les attaques de type Man-in-the-Middle

Concrètement, lorsque nous accédons à un site web, notre navigateur (Firefox, Brave, etc.) établit une connexion avec un serveur web.

Sans TLS, toutes ces communications seraient visibles par toute personne capable d’écouter le réseau.


🖥️ SSH (Secure Shell)
SSH permet :\
🔹 des sessions de connexion interactives\
🔹 l’exécution de commandes à distance\
🔹 le transfert sécurisé de fichiers\
🔹 le tunneling de connexions TCP/IP\
Plus simplement, SSH permet d’administrer un système distant de manière sécurisée, sans être physiquement (ou nécessairement) présent sur le réseau de la machine.


🛡️ IPsec (Internet Protocol Security)

IPsec est une suite de protocoles de sécurité opérant au niveau de la couche IP.

Son usage le plus courant est la mise en place de VPN (Virtual Private Networks) :

🌍 site-à-site\
👨‍💻 accès distant

C’est notamment une technologie largement utilisée dans le cadre du télétravail, afin de permettre aux employés d’accéder de manière sécurisée aux ressources de l’entreprise.


⚛️ Pourquoi ces protocoles sont concernés par la menace quantique ?

Ces protocoles reposent en partie sur des algorithmes de cryptographie à clé publique.

Ces derniers tirent leur sécurité de problèmes mathématiques réputés difficiles, tels que :

🔢 la factorisation de grands nombres premiers (RSA)\
📊 le logarithme discret (Diffie-Hellman)


Or, l’algorithme de Shor, exécuté sur un ordinateur quantique suffisamment puissant, pourrait résoudre ces problèmes de manière efficace, rendant ces systèmes vulnérables.\
Pour anticiper cette évolution, l’ANSSI recommande une approche dite d’hybridation cryptographique.\
🔗 Concrètement, il s’agit d’utiliser simultanément des algorithmes classiques et des algorithmes post-quantiques.

Cette approche permet :\
✔️ de maintenir la sécurité aujourd’hui\
✔️ tout en se préparant à l’ère du calcul quantique\
Elle permet également de se protéger contre les attaques de type :

📦 Store Now, Decrypt Later

Dans ce scénario, un attaquant collecte aujourd’hui du trafic chiffré dans l’espoir de pouvoir le déchiffrer plus tard grâce à un ordinateur quantique.


🔑 Pourquoi la cryptographie symétrique est moins menacée ?

Contrairement à la cryptographie à clé publique, la cryptographie à clé secrète est beaucoup moins affectée par la menace quantique.\
Le guide de l’ANSSI intitulé\
📄 ANSSI views on the Post-Quantum Cryptography transition (30 mars 2022) apporte un éclairage intéressant sur ce point.\
Les systèmes symétriques ne sont pas vulnérables à l’algorithme de Shor, mais seulement à l’algorithme quantique de Grover.\
Cet algorithme permet d’accélérer les attaques par force brute, mais uniquement avec un gain quadratique.\
En pratique, cela revient à diviser par deux la sécurité effective des clés.

Par exemple :\
🔐 AES-256 face à Grover offrirait une sécurité équivalente à AES-128 aujourd’hui.\
La solution consiste donc simplement à augmenter la taille des clés, ce qui rend ces systèmes toujours robustes dans un contexte post-quantique.


🌍 Une transition qui rappelle celle d’IPv6

La transition vers la cryptographie post-quantique me rappelle, à certains égards, la migration vers IPv6.\
À l’époque, certains envisageaient un abandon complet d’IPv4.\
Mais il est rapidement apparu que cette approche n’était pas réaliste. La solution adoptée a finalement été la cohabitation des deux protocoles.\
De manière similaire, l’approche hybride en cryptographie semble aujourd’hui pertinente.\
D’autant plus que nous ne connaissons pas encore l’étendue réelle des capacités futures des ordinateurs quantiques.\
Il est possible que nous les surestimions…\
Mais il serait tout aussi dangereux de les sous-estimer.

📄 Lien vers tous les documents de l’ANSSI :\
🔗 https://messervices.cyber.gouv.fr

💬 Curieux d’avoir vos retours :\
Commencez-vous déjà à anticiper la transition post-quantique ?

#CyberSecurity
#PostQuantumCryptography
#TLS
#Cryptography
