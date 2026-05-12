+++
title = "🔐 TLS/SSL : le protocole que tout le monde utilise sans vraiment comprendre"
date = 2026-04-23
tags = ["tls", "ssl", "cryptographie", "cybersécurité", "réseau"]
draft = false
toc = true
thumbnail = "images/logo-tls.svg"
description = "Retour sur TLS/SSL : comment fonctionne vraiment le handshake, ce que chiffre (et ne chiffre pas) ce protocole, et pourquoi certaines versions sont encore dangereuses aujourd'hui."
+++

Quand j'ai commencé à monter mon lab OpenVPN sur pfSense, j'ai dû générer des certificats, configurer une CA, choisir des algorithmes de chiffrement... et là j'ai réalisé que je ne comprenais pas vraiment ce que je faisais. Je savais que TLS = cadenas vert dans le navigateur. Mais derrière ce cadenas, que se passe-t-il exactement ?

Voici ce que j'aurais aimé lire à l'époque.

<!--more-->

## 🤔 SSL ou TLS — on parle de quoi ?

SSL (Secure Sockets Layer) est le prédécesseur de TLS (Transport Layer Security). Aujourd'hui **SSL est mort** — SSL 2.0, SSL 3.0, TLS 1.0 et TLS 1.1 sont tous dépréciés et vulnérables. Quand on dit "SSL" dans la vie courante, on parle en réalité de **TLS 1.2 ou TLS 1.3**.

La version actuelle recommandée est **TLS 1.3** (RFC 8446, 2018). TLS 1.2 est encore acceptable si bien configuré. Tout le reste est à proscrire.
