# Startnet Configurator

Un outil graphique Python permettant de personnaliser le fichier `startnet.cmd` d'une image WIM, utilisé dans les environnements WinPE.

## 📌 Fonctionnalités

- Interface intuitive en Tkinter.
- Sélection facile du fichier `.wim`.
- Génération automatique d’un `sotartnet.cmd` personnalisé avec :
  - La lettre du lecteur réseau.
  - Le chemin du partage réseau.
  - Le nom d'utilisateur et le mot de passe.
- Montage et démontage de l’image WIM avec `dism`.

---

## 🖥️ Utilisation

### Étapes :

1. Lancer le script Python (`startnet_configurator.py`).
2. Renseigner les champs requis :
   - Lettre du lecteur réseau (ex : `Z`)
   - Chemin réseau (ex : `\\HP06\f\ImagesMacrium`)
   - Nom d'utilisateur
   - Mot de passe
3. Sélectionner le fichier `.wim` à modifier.
4. Le script monte l'image, modifie le fichier `startnet.cmd`, puis démonte l'image.
5. Les logs s’affichent en bas de l’interface.

---

## 🛠️ Création du fichier `.exe`

> Pratique pour l’utiliser sur des postes sans Python installé.

### Étapes :

1. **Créer un environnement virtuel (optionnel mais fortement recommandé) :**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
    ```

2. **Installer les dépendances :**

   ```bash
   pip install pyinstaller
   ```

3. **Générer le `.exe` :**

   ```bash
   pyinstaller --noconsole --onefile startnet_configurator.py
   ```

4. Le fichier `.exe` sera généré dans `dist/startnet_configurator.exe`.

---


## 💡 Astuces

* Le script crée un dossier temporaire sur le Bureau pour monter l’image.
* Le fichier `log_wim_script.txt` contient l’historique des opérations.

---

## 🔒 Remarque sécurité

Le mot de passe saisi est utilisé uniquement pour créer la commande `net use`. Aucune donnée n’est transmise ni sauvegardée en dehors du fichier `startnet.cmd`.

---

## 🧑‍💻 Auteur

**Rinor Januzi — Infoneo**

