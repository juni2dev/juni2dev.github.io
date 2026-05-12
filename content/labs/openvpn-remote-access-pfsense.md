+++
date = '2026-04-22T01:11:17+02:00'
draft = false
title = '🔐 OpenVPN Remote Access Lab — pfSense'
tags = ["vpn", "pfsense", "cybersécurité", "digital signature"]
featureImage = "images/cover-openvpn.png"
featureImageAlt = "Architecture OpenVPN pfSense"
thumbnail = "images/logo-openvpn.svg"
toc = true
+++

## Description

Ce lab documente la mise en place complète d'un **VPN d'accès à distance** utilisant **OpenVPN** sur **pfSense**. Il couvre l'intégralité de la chaîne : création d'une autorité de certification interne (root-CA), émission d'un certificat serveur et d'un certificat client, configuration du serveur OpenVPN via le Wizard pfSense, export du profil client, et quelques tests de validation par capture réseau Wireshark.

<!--more-->

> ⚠️ Contrairement à un VPN site-à-site où il aurait fallu mettre en place au moins deux pfSense, le présent scénario met en lumière un utilisateur mobile se connectant à un serveur distant typiquement le réseau d'entreprise (télétravailleur / télétravailleuse). on peut modéliser la connexion comme suit **utilisateur ↔ serveur** . Par ailleurs, pfSense endossera la fonction de serveur d'authentififaction (local user authentication) bien qu'il soit tout à fait possible d'utiliser LDAP/Radius. Ce choix se justifie par une gestion plus simple au travers de la section User manager du GUI aussi, le test sera effectué avec un seul utilisateur (user).
---

## 🏗️ Architecture

![Remote access openvpn architecture](docs/images/architecture.jpg)

Il s'agit ici de l'environnement du lab dans son entièreté incluant un acteur malveillant.

---

## 🧰 Stack technique

| Composant | Détail |
|-----------|--------|
| Firewall/VPN Gateway | pfSense Community Edition |
| Protocole VPN | OpenVPN |
| Authentification | Local User Access (pfSense User Manager) |
| PKI | Root-CA interne pfSense |
| Algorithme de clé | RSA 2048 bits |
| Digest | SHA-256 |
| Chiffrement données | AES-256-GCM / AES-128-GCM / CHACHA20-POLY1305 |
| Chiffrement fallback | AES-256-CBC |
| Échange de clés | Diffie-Hellman 2048 bits |
| Authentification TLS | Clé TLS partagée (auto-générée) |
| Client OS | Kali Linux (OpenVPN CLI) |
| Analyse réseau | Wireshark |

---

## 📋 Étapes de configuration

### 1. Création de l'autorité de certification

> `System → Certificates → Authorities → Add`

| Champ | Valeur |
|-------|--------|
| Descriptive Name | `Root-CA` |
| Method | Create an internal Certificate Authority |
| Randomize Serial | ✅ Activé |
| Key Type | RSA |
| Key Length | **2048 bits** (minimum recommandé) |
| Digest Algorithm | SHA256 |
| Lifetime | **3650 jours** (10 ans) |
| Common Name | `Root-CA` |

> 💡 RSA 2048 est de facto la longueur de clé la plus utilisée par les CA. SHA-256 est considéré comme assez robuste face aux attaques du type arc-en-ciel (ou plus simplement collision).

![Configuration de l'autorité de certification](docs/images/create-editCA.png)
![Configuration de l'autorité de certification](docs/images/internal-certifcate-authority.png)

---

### 2. Création du certificat serveur

> `System → Certificates → Certificates → Add`

| Champ | Valeur |
|-------|--------|
| Method | Create an internal Certificate |
| Descriptive Name | `Authority-server` |
| Certificate Authority | `Root-CA` |
| Key Type | RSA 2048 |
| Digest Algorithm | SHA256 |
| Lifetime | **≤ 398 jours** ⚠️ |
| Certificate Type | **Server** (pas Client !) |
| Common Name | `Authority-server` |

> ⚠️ La durée de vie du certificat serveur ne doit **pas dépasser 398 jours** — au-delà, certains clients TLS le rejettent.

![configuration du certificat serveur](docs/images/add-sign-new-certificate.png)
![configuration du certificat serveur](docs/images/internal-certificate-server.png)

---

### 3. Configuration du serveur VPN via Wizard

> `VPN → OpenVPN → Wizards`
> Du fait que nous venons de créer la CA et le serveur, certaines étapes sont sautés par pfSense.

**Étape 1/11 — Authentication Backend**
- Type of Server : `Local User Access`

![configuration du certificat serveur](docs/images/firstStep-wizard.png)

**Étape 5/11 — Certificate Authority**
- Sélectionner `Root-CA`

![configuration du certificat serveur](docs/images/wizard-chooseCA.png)

**Étape 7/11 — Server Certificate**
- Sélectionner `Authority-server`

![configuration du certificat serveur](docs/images/wizard-chooseServerC.png)

**Étape 9/11 — Server Setup**

| Champ | Valeur |
|-------|--------|
| Description | `Remote workers from home` |
| Protocol | UDP on IPv4 only |
| Interface | WAN |
| Local Port | 1194 |
| TLS Authentication | ✅ Activé |
| Generate TLS Key | ✅ Auto-généré |
| DH Parameters Length | 2048 bits |
| Data Encryption | AES-256-GCM, AES-128-GCM, CHACHA20-POLY1305 |
| IPv4 Tunnel Network | `10.0.8.0/24` |
| IPv4 Local Network | `192.168.110.0/24` |
| Allow Compression | Refuse (Most Secure) |
| DNS Default Domain | `google.com` (exemple) |
| DNS Server 1 | `8.8.8.8` |

![configuration du certificat serveur](docs/images/wizard-generalsetting-endp.png)
![configuration du certificat serveur](docs/images/wizard-cryptographicsetting.png)
![configuration du certificat serveur](docs/images/wizard-tunnelSetting1.png)
![configuration du certificat serveur](docs/images/wizard-tunnelSetting2.png)
![configuration du certificat serveur](docs/images/wizard-advancedSetting.png)

**Étape 10/11 — Firewall Rules**
- ✅ Firewall Rule (Traffic from clients to server)
- ✅ OpenVPN rule (Traffic from clients through VPN)

> 💡 Par défaut pfSense applique un **default block**. Or les deux précédentes règles sont indispensables pour que le trafic VPN passe, il faut donc qu'ils soient explicitement mentionnées. On peut constater que les utilisateurs autorisés à se connecter n'ont pas été explicitement identifiés ce qui pourrait constituer une surface d'attaque potentielle. En production, affiner la règle WAN dans `Firewall → Rules → WAN` pour restreindre les IPs sources autorisées.

![configuration du certificat serveur](docs/images/wizard-lastStep.png)
![configuration du certificat serveur](docs/images/wizard-finish.png)

---

### 4. Création de l'utilisateur et du certificat client

> `System → User Manager → Users → Add`

| Champ | Valeur |
|-------|--------|
| Username | `edi` (exemple) |
| Password | (mot de passe fort) |
| Certificate | ✅ Cocher pour créer |
| Certificate Name | Identique au Username |
| Certificate Authority | `Root-CA` |
| Key Type | RSA 2048 |
| Digest Algorithm | SHA256 |

![configuration du certificat serveur](docs/images/createUser.png)
![configuration du certificat serveur](docs/images/userProperties.png)
![configuration du certificat serveur](docs/images/userCertificate.png)

---

### 5. Export du profil client

> `VPN → OpenVPN → Export Client`

1. Installer le package `OpenVPN Client Export` via `System → Package Manager`
2. Dans `Client Connection Behavior` → Bind Mode : **Use a random local source port** (permet des clients concurrents)
3. Cliquer **Save as default**
4. Dans `OpenVPN Clients` → colonne Export → télécharger **Most Clients** (`.ovpn`)

![configuration du certificat serveur](docs/images/clientExport-Behaviors.png)
![configuration du certificat serveur](docs/images/clentExport-export.png)
![configuration du certificat serveur](docs/images/clientExportOpenVPN.png)

---

### 6. Connexion depuis le client Linux

```bash
# Installation du client OpenVPN
sudo apt update && sudo apt install openvpn

# Connexion avec le profil exporté
sudo openvpn --config /chemin/vers/pfSense-UDP4-1194-edi-config.ovpn
# → Enter Auth Username: edi
# → Enter Auth Password: ****
```

**Indicateur de succès :**
```
Initialization Sequence Completed
```

![configuration du certificat serveur](docs/images/openvpnconnexion.png)

> ⚠️ Vérifier que la règle **Block Private Networks** (l'interface WAN de pfSense) n'empeche pas l'établissement de la connexion avec le serveur. 

---

## 🔬 Validation — Wireshark

### Test 1 : Sniff sur l'interface tunnel `tun0`

Capture effectuée à l'intérieur du tunnel depuis l'interface virtuelle `tun0` du client. À ce niveau, OpenVPN a déjà déchiffré les paquets — on observe donc le trafic applicatif en clair (HTTP, TCP...). C'est un comportement **attendu et normal** : les adresses source appartiennent au subnet `10.0.8.0/24`, ce qui confirme l'attribution d'adresse tunnel et le bon fonctionnement du routage vers le LAN.

![configuration du certificat serveur](docs/images/wireshark-tun0.png)

### Test 2 : Sniff sur l'interface WAN de pfSense

Capture effectuée côté WAN, avant déchiffrement. Tout le trafic apparaît en **OpenVPN P_DATA_V2** — le contenu est illisible, ce qui confirme que l'encapsulation OpenVPN fonctionne.

![configuration du certificat serveur](docs/images/wireshark-wan.png)
Voir l'analyse détaillée → [`docs/wireshark-analysis.md`](docs/wireshark-analysis.md)

---

## 📁 Structure du repo

```
openvpn-remote-access-lab/
├── README.md
├── configs/
│   └── client-config-example.ovpn
├── diagrams/
│   └── architecture.md
├── docs/
│   ├── wireshark-analysis.md
│   └── troubleshooting.md
└── screenshots/
    └── README.md
```

---

## ⚠️ Avertissement

Ce lab est réalisé dans un environnement virtualisé isolé à des fins **éducatives**. Les configurations présentées (règles de pare-feu larges, mots de passe de test) ne doivent **pas être reproduites en production** sans durcissement approprié.

---

## 📎 Ressources

- [pfSense OpenVPN Documentation](https://docs.netgate.com/pfsense/en/latest/vpn/openvpn/)
- [OpenVPN Community](https://openvpn.net/community-resources/)
- [RFC 5280 — Certificate Lifetime](https://datatracker.ietf.org/doc/html/rfc5280)
