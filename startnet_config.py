import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Combobox, Progressbar
import threading

# --- Chemins et configuration ---
user_desktop = Path.home() / "Desktop"
mount_folder = user_desktop / "Mount"
temp_folder = user_desktop / "Temp"
log_file = user_desktop / "log_wim_script.txt"

# --- Logger ---
def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}"
    log_area.insert(tk.END, entry + "\n")
    log_area.see(tk.END)
    with open(log_file, "a", encoding="utf-8") as logf:
        logf.write(entry + "\n")

# --- Préparation des dossiers ---
def create_folder(path):
    if path.exists():
        log(f"Dossier existant détecté : {path}, suppression en cours.")
        try:
            shutil.rmtree(path)
        except Exception as e:
            log(f"Erreur suppression : {e}")
            raise
    path.mkdir(parents=True)
    log(f"Dossier créé : {path}")

# --- Montage DISM ---
def mount_wim(wim_path):
    cmd = [
        "dism", "/Mount-Wim",
        f"/WimFile:{wim_path}",
        "/Index:1",
        f"/MountDir:{temp_folder}"
    ]
    log(f"Montage du WIM : {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

# --- Démontage DISM ---
def unmount_wim(commit=True):
    cmd = [
        "dism", "/Unmount-Wim",
        f"/MountDir:{temp_folder}",
        "/Commit" if commit else "/Discard"
    ]
    log(f"Démontage WIM ({'Commit' if commit else 'Discard'}) : {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

# --- Création de startnet.cmd personnalisé ---
def create_custom_startnet(letter, path, user, password):
    startnet_path = temp_folder / "Windows" / "System32" / "startnet.cmd"

    if startnet_path.exists():
        try:
            os.remove(startnet_path)
            log("Ancien startnet.cmd supprimé.")
        except Exception as e:
            log(f"Erreur suppression startnet.cmd : {e}")
            raise

    try:
        with open(startnet_path, "w", encoding="utf-8") as f:
            f.write("wpeinit\n")
            f.write(f"net use {letter.upper()}: {path} /USER:{user} {password}\n")
            f.write("exit\n")
        log("✅ Nouveau startnet.cmd créé avec succès.")
    except Exception as e:
        log(f"Erreur lors de la création de startnet.cmd : {e}")
        raise

# --- Processus principal dans un thread ---
def start_process_thread():
    def thread_func():
        try:
            log_area.delete(1.0, tk.END)
            create_folder(temp_folder)

            wim_path = filedialog.askopenfilename(title="Sélectionner un fichier .wim", filetypes=[("WIM files", "*.wim")])
            if not wim_path:
                log("Opération annulée par l'utilisateur.")
                return

            if not os.path.isfile(wim_path):
                log("Fichier .wim introuvable.")
                return

            letter = drive_letter_var.get().strip()
            path = share_path_var.get().strip()
            user = username_var.get().strip()
            password = password_var.get().strip()

            if not all([letter, path, user, password]):
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
                return

            # Mise à jour de la barre de progression
            progress_bar.start()

            # Simulation de tâches longues en mettant à jour la barre
            mount_wim(wim_path)
            create_custom_startnet(letter, path, user, password)
            unmount_wim(commit=True)

            log("✅ Script terminé avec succès.")
            messagebox.showinfo("Succès", "Script terminé avec succès.")
            
        except Exception as e:
            log(f"❌ Erreur détectée : {e}")
            try:
                unmount_wim(commit=False)
            except Exception as e2:
                log(f"⚠️ Échec du démontage forcé : {e2}")
        finally:
            progress_bar.stop()

    # Démarrage du thread
    thread = threading.Thread(target=thread_func)
    thread.start()

# --- Interface utilisateur ---
root = tk.Tk()
root.title("Configuration startnet.cmd pour image WIM")
root.geometry("750x700")
root.resizable(False, False)
root.configure(bg="#F0F0F0")  # Fond de la fenêtre

frame = tk.Frame(root, padx=20, pady=20, bg="#F0F0F0")
frame.pack(fill="both", expand=True)

# --- Titre et sous-titres ---
title_label = tk.Label(frame, text="Configurer startnet.cmd pour WIM", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
title_label.pack(pady=10)

# --- Widgets de l'interface ---
tk.Label(frame, text="Lettre du lecteur réseau (ex: Z)", bg="#F0F0F0").pack()
drive_letter_var = tk.StringVar()
drive_letter_combobox = Combobox(frame, textvariable=drive_letter_var, values=[chr(i) for i in range(65, 91)], width=5)
drive_letter_combobox.set("Z")  # Valeur par défaut
drive_letter_combobox.pack(pady=5)

tk.Label(frame, text="Chemin du partage réseau (ex: \\\\HP06\\f\\ImagesMacrium)", bg="#F0F0F0").pack()
share_path_var = tk.StringVar()
tk.Entry(frame, textvariable=share_path_var, width=60).pack(pady=5)

tk.Label(frame, text="Nom d'utilisateur", bg="#F0F0F0").pack()
username_var = tk.StringVar()
tk.Entry(frame, textvariable=username_var).pack(pady=5)

tk.Label(frame, text="Mot de passe", bg="#F0F0F0").pack()
password_var = tk.StringVar()
tk.Entry(frame, textvariable=password_var, show="*").pack(pady=5)

# --- Bouton démarrer (tk.Button au lieu de ttk.Button) ---
start_button = tk.Button(frame, text="Démarrer", command=start_process_thread, font=("Arial", 12), width=20, bg="#4CAF50", fg="white")
start_button.pack(pady=15)

# --- Barre de progression ---
progress_bar = Progressbar(frame, length=400, mode='indeterminate')
progress_bar.pack(pady=20)

# --- Zone de log ---
log_area = scrolledtext.ScrolledText(frame, height=10, width=80, font=("Consolas", 10), bg="#F0F0F0", wrap=tk.WORD)
log_area.pack(pady=10)

root.mainloop()
