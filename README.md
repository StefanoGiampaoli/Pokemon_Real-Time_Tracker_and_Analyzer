# Pokémon Data Processing & App
Un'applicazione Python per l'elaborazione, pulizia e visualizzazione/gestione dei dati dei Pokémon. Include una pipeline di preparazione dei dati e la possibilità di avviare l'applicazione in locale oppure compilarla in un eseguibile standalone (.exe) tramite PyInstaller con icona personalizzata.

---

## Struttura del Progetto

```text
├── app.py               # Script principale
├── data_cleaner.py      # Pipeline di pulizia dati (genera final_pokemon.csv)
├── raw_pokemon.csv      # Dataset grezzo sorgente
├── ultraball.ico        # Icona per l'applicazione
├── requirements.txt     # Dipendenze del progetto
├── .gitignore           # File e cartelle privati
└── README.md            # Documentazione del progetto
```

---

## 1. Prerequisiti e Configurazione

1. **Clona o scarica il repository** ed entra nella cartella del progetto:
   ```bash
   git clone https://github.com/StefanoGiampaoli/pokemon_type_info_checker.git
   cd Db\ Pokemon\ Info/
   ```

2. **Crea e attiva l'ambiente virtuale:**
   - **Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate.bat
     ```

3. **Installa le dipendenze:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Preparazione dei Dati (Data Cleaning)

Prima di avviare o compilare l'applicazione, è necessario eseguire `data_cleaner.py`. Lo script elabora il dataset di partenza `raw_pokemon.csv` e genera il file pulito `final_pokemon.csv` richiesto dall'applicazione.

Esegui nel terminale:
```bash
python data_cleaner.py
```

Al termine troverai `final_pokemon.csv` all'interno della cartella principale.

---

## 3. Esecuzione del Progetto

Si può procedere in due modi:

### Opzione A: Esecuzione in Locale (Script Python)
Esegui nel ternimale:

```bash
python app.py
```

---

### Opzione B: Compilazione in Eseguibile con PyInstaller
Se desideri creare un'applicazione standalone (file `.exe` su Windows) da distribuire senza dover installare Python:

1. Assicurati che `pyinstaller` sia installato:
   ```bash
   pip install pyinstaller
   ```

2. Esegui il comando di build includendo l'icona (`ultraball.ico`) e i dati necessari (`final_pokemon.csv`):
   
   - **Windows (CMD / PowerShell):**
     ```bash
     pyinstaller --noconsole --onefile --icon=ultraball.ico --add-data "final_pokemon.csv;." --add-data "ultraball.ico;." app.py
     ```
   - **Linux / macOS:**
     ```bash
     pyinstaller --noconsole --onefile --icon=ultraball.ico --add-data "final_pokemon.csv:." --add-data "ultraball.ico:." app.py
     ```

   *Nota sui flag utilizzati:*
   * `--onefile`: impacchetta tutto in un unico file eseguibile.
   * `--noconsole` (o `--windowed`): impedisce l'apertura della finestra del terminale nero all'avvio.
   * `--icon=ultraball.ico`: assegna l'icona personalizzata al file eseguibile.
   * `--add-data`: include il dataset pulito e le risorse all'interno del bundle compilato.

3. **Trovare l'eseguibile:**  
   Il file generato si troverà nella cartella `dist/` (es. `dist/app.exe`). Le cartelle temporanee `build/` e il file `app.spec` possono essere rimossi in sicurezza dopo il build.

---

## 📄 Note e Manutenzione
* Se aggiorni o modifichi la logica di pulizia in `data_cleaner.py`, ricordati di rieseguirlo prima di avviare `app.py` o prima di rifare la build con PyInstaller.