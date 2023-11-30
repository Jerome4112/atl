# ATL

## Produktbeschreibung:
-------------------------------------------------------------------------------------------------------------------------------------------------
Die Software, Easy Client dient zur Erfassung der Kundenbedürfnisse, wenn diese ein neues Gerät benötigen bzw. wenn sie ein neues Gerät bestellt haben. Die Informationen, welche vorab beschaft wurden, waren in den meisten Fällen sehr dürftig. Ich, als Techniker, musste beim Kunden genaue Details einholen, welche Programme vorab für ihn installiert werden sollen. Mein Produkt dient der Erfassung dieser Daten, in dem zuerst der Kunde als Firma, der einzelne Mitarbeiter als Auftraggeber und der effektive Auftrag erstellt wird und die zu installierenden Programme dem Auftrag hinzugefügt werden. Dadurch kann die Kundenzufriedenheit und der Prozess der Informationsbeschaffung verbessert werden, da alle Daten vorab gesammelt werden.

## Start Anleitung:
-------------------------------------------------------------------------------------------------------------------------------------------------
1. Um die Applikation starten zu können, stellen Sie sicher, dass Sie poetry installiert haben.
2. Mit dem Befehl "poetry install" werden die projektabhängigen Dienste installiert.
3. Mit dem Befehl "poetry run uvicorn ATL.main:app --reload" können Sie das Programm starten, wenn alles geklappt hat, sollte es so aussehen, wie unten beschrieben:
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [20568] using WatchFiles
INFO:     Started server process [18112]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
4. Öffnen Sie diesen Pfad im Browser Ihres Vertrauens : http://127.0.0.1:8000
5. Geben Sie am Ende des Pfades /docs ein um die einzelnen Endpunkte sehen zu können, der Pfad sollte so aussehen: http://127.0.0.1:8000/docs

# Benutzung Anleitung:
--------------------------------------------------------------------------------------------------------------------------------------------------
1. Bevor Sie die Software benutzen können, müssen Sie sich registrieren, nutzen Sie dazu den Endpunkt user/register.
   Geben Sie einen beliebigen Benutzernamen und ein Passwort ein.
2. Um die anderen Endpunkte benutzen zu können, drücken Sie den Authorize Button (ganz oben rechts).
3. Melden Sie sich mit dem von Ihnen erstellten Benutzernamen und Passwort an.
   Die anderen Endpunkte sind nun entsperrt.
4. Erstellen Sie zuerst einen Kunden mit dem Endpunkt "Create Customer", achten Sie darauf, dass die ID (Kundennummer) noch nicht verwendet wird.
5. Erstellen Sie anschliessend einen Mitarbeiter mit dem Endpunkt "Create Employee", geben Sie die ID des zuvor erstellten Kunden an.
6. Erstellen Sie nun einen Auftrag mit dem Endpunkt "Create Order". Geben Sie die zuvor erstellten ID's vom Kunden (Customer) und dem Mitarbeiter (Employee) an.
7. Erstellen Sie nun die Programme, mit dem Endpunkt "Create Program", die bei diesem Auftrag installiert sein müssen.
8. Fügen Sie die erstellten Programme mit dem Endpunkt Add_program_to_order dem Auftrag hinzu.
9. Sie können nun mit dem Endpunkt "Read Customer Orders" unter Angabe der Kunden ID den gesamten Auftrag mit allen Informationen ausgeben. Sie können auch die anderen Read Endpunkte benutzen, wenn sie beispielsweise nur den Auftrag mit den Programmen sehen wollen, nutzen Sie den Endpunkt "Read Order".

## Überlegungen:
--------------------------------------------------------------------------------------------------------------------------------------------------

Struktur:
Eine grosse Schwierigkeit lag in der Struktur und der Vielseitigkeit unserer Kunden. Wir haben grösstenteils KMU's als Kunden aber auch Einzelpersonen bzw. Privatpersonen, die wir betreuen und für sie Geräte aufsetzen. Der Kompromiss, den ich machen musste, war dass alle Einzelkunden in meinem Programm wie Firmen behandelt werden müssen, in dem zuerst der Kunde wie als Firma und dann der einzelne Mitarbeiter, in diesem Fall die Einzelperson erfasst werden muss, dies erscheint mir als die beste Lösung. 

Da viele Kunden auch oft Freeware installiert haben möchten, wollte ich nicht z.B 10 Mal Firefox erfassen. Daher hab ich die Beziehung von Programmen zu Aufträgen in einer Many to Many Beziehung gelöst, damit einige Programme mehreren Aufträgen zugewiesen sein können. 

Sicherheit:
Da ich in meinem Programm Passwörter und Zugangsdaten von Kunden nicht gehashed speichere, was normalerweise keine gute Idee ist, aber leider nötig, bedarf es Sicherheitsvorkehrungen, damit diese Daten nicht in falsche Hände geraten. Die Passwörter oder Lizenzen der Kunden zu hashen hätte nichts gebracht, da ich sie ohnehin wieder im Klartext ausgeben muss. Daher habe ich mich für eine Authentifizierung mit OAuth entschieden und so umgesetzt. Aufgrund der eher experimentellen Umgebung habe ich den Registrierungsendpunkt offen gelassen, um die Benutzung nicht zu erschweren. In einer Produktivumgebung wird dieser Enpunkt dann nur für Administratoren zugänglich sein.


## Verbesserungen bei mehr Zeit:
--------------------------------------------------------------------------------------------------------------------------------------------------

GUI Implementierung: Sehr gerne hätte ich noch eine Graphische Benutzeroberfläche für das Programm entwickelt, leider habe ich ein wenig unterschätzt, wie viel Aufwand mein Projekt generiert und ich schon deutlich über den budgetierten 16 Stunden liege für diese ATL. Daher hatte ich leider keine Zeit mehr, ein GUI zu Implementieren.

Überprüfen der Tokengültigkeit: Damit mein Programm benutzt werden kann, muss man sich registrieren und anmelden. Die einzelnen Endpunkte überprüfen aber nicht ob der Token noch gültig ist, sondern nur ob er mitgegeben wird. Wenn ich mehr Zeit gehabt hätte, hätte ich dies gerne sauberer gelöst. 


# ATL 2

## Durchgeführte Schritte
Folgende Schritte waren nötig um die Software in der Cloud zu deployen:

### Erstellen des Kontos in der Google Cloud.
   Die Googlecloud stellt einen Kostenlosen Testzeitraum von 90Tagen bzw. bis 271CHF(Stand: 29.11.2023) aufgebraucht sind zur verfügung. Um diesen Dienst zu nutzen musste die Kreditkarte hinterlegt werden.

### Einrichten der Budget begrenzung.
   Da Kosten von Clouddiensten im vorfeld schwierig zu berechnen sind, da sie nach effektiven benutzung von Ressourcen abgerechnet werden, war es nötig eine entsprechnde Budget begrenzung bzw einen Alarm einzurichten sofern mehr wie 10 CHF.- innerhalb eines Monats abgebucht werden, damit keine unbeabsichtigten horende Kosten entstehen.
   ![Budgetbegrenzung](https://github.com/Jerome4112/atl/blob/main/Images/Budgetbegrenzung.png)

### Aktivieren von Cloudbuild.
   Um aus dem Dockerfile direkt ein Container zu erstellen war es nötig den Dienst "Cloudbuild" zu aktivieren.

### Erstellen des Triggers auf GitHub Repository
   Der Auftrag sieht vor, dass wenn ein neuer Push auf das Github Repository erkannt wird automatisch ein neuer Build ausgeführt wird. Dazu musste ein entsprechender Trigger konfiguriert werden.
   Unter Cloud Build -> Trigger -> Trigger erstellen. Der Radio Button "Push zu Zweig" muss aktiviert sein. Anschliessend muss das entsprechende Github Repository verbunden werden. Anmelden mit dem entsprechendem Profil und angabe des Repositorys.
   ![Trigger](https://github.com/Jerome4112/atl/blob/main/Images/Trigger.png) 
   ![Trigger aktiv](https://github.com/Jerome4112/atl/blob/main/Images/trigger%20aktiv.png)

### Anpassungen am pyproject.toml File
   Da ich wärend der Entwicklung diverse Libarys installiert habe die für den Betrieb nicht nötig sind habe ich das File mit folgendem dev. bereich ergänzt:
   
```yaml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4.2"
httpx = "^0.25.0"
```
   
    So wird der Dockercontainer nur mit den wirklich nötigen Libarys erstellt die zum betrieb erforderlich sind.
- Erstellen des Dockerfile.
   Damit der Dockercontainer korrekt erstellt wird habe ich diese konfiguration verwendet:

   <clipboard-copy for="blob-path" class="btn btn-sm BtnGroup-item">
  https://github.com/Jerome4112/atl/blob/main/Dockerfile
</clipboard-copy>
<div id="blob-path">src/index.js</div>
   Im ersten Schritt wird poetry installiert und die Dateien pyproject.toml und poetry.lock exportiert in eine requirements.txt datei. Dadurch muss nicht zusätzlich poetry in den Runcontainer installiert sein und ist dadurch schlanker und sparen somit Speicher.
   Im zweiten schritt wird mit pip aus der requirements.txt Datei alle Projektabhängigkeiten installiert und mit uvicorn ausgeführt.

### Erstellen des cloudbuild.yaml File.
    Damit die Google Cloud den Container richtig erstellt habe ich diese Konfiguration verwendet:
   <clipboard-copy for="blob-path" class="btn btn-sm BtnGroup-item">
   https://github.com/Jerome4112/atl/blob/main/cloudbuild.yaml
   </clipboard-copy>
   <div id="blob-path">src/index.js</div>
   Da gemäss Aufgabe der Container erst erstellt werden darf, wenn alle tests erfolgreich waren,  wird zuerst pytest ausgeführt. Wenn dies der fall war, wird gemäss Docker der Container erstellt. Der Container wird zu google Cloud run gepusht und somit ausgeführt.

### Ausführen eines Push in das Github Repository
   Damit der Trigger auslöst wird, ist ein Push in das Github repository nötig. Die vier Steps aus dem Cloudbuild.yaml file werden im anschluss abgearbeitet.
   ![Cloudbuild schritte](https://github.com/Jerome4112/atl/blob/main/Images/Cloudbuild-Steps.png)

### Öffnen der Service Url.
   Meine Applikation ist nun über folgenden link erreichbar:
   (https://atl-diti5vaa7a-ew.a.run.app/docs)


## Cloudbuild abbruch Tests fehlerhaft
Um zu testen, ob der Cloudbuild abgebrochen wird, wenn ein test fehlerhaft ist habe ich den Test test_create_customer() angepasst und das erwatete ergebnis auf Test Customer1 gesetzt.
![angepasster test](https://github.com/Jerome4112/atl/blob/main/Images/angepasster%20test.png)

Der Build wurde abgebrochen aufgrund des erwarteten Test ergebnisses Customer1, der aber tatsächlich Test Customer heisst.
![Build abgebrochen](https://github.com/Jerome4112/atl/blob/main/Images/Build%20abgebrochen.png)



## Probleme 
Ich bin auf folgende probleme gestossen:
### Git Hub Repository in Grossbuchstaben
Der build wurde bei mir abgebrochen, weil die Variable $PROJECT_ID im cloudbuild.yaml File keine grossmuchstaben akzeptiert. 
![grossbuchstaben](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
Ich habe mich entschieden, das Github Repository umzubenennen von "ATL" zu "atl".Dadurch wurde der Fehler behoben.

### Cloud Run nicht aktiviert
Ein build wurde bei mir abgebrochen, da ich den Dienst Cloudrun nicht aktiviert hatte. Sobald ich diesen in der Googlecloud aktiviert habe het es fehlerfrei funktioniert.
![Cloudrun nicht aktiviert](https://github.com/Jerome4112/atl/blob/main/Images/Cloudrun%20nicht%20aktiviert.png)







