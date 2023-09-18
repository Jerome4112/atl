# ATL

Produktbeschreibung:
--------------------
Die Software, Easy Client dient zur Erfassung der Kundenbedürfnisse, wenn diese ein neues Gerät benötigen bzw. wenn Sie ein neues Gerät bestellt haben . Die vorab Informationsbeschaffung war in den meissten fällen sehr dürftig und ich als Techniker musste beim Kunden genaue details einholen welche Programme vorab für ihn installiert sein müssen. Mein Produkt dient der erfassung dieser Daten, in dem zuerst der Kunde als Firma, der einlene Mitarbeiter als Auftraggeber und der effektive Auftrag erstellt wird und die zu installierenden Programme dem Auftrag hinzugefügt werden. Dadurch kann die Kunenzufriedenheit und der Prozess der informationsbeschaffung verbessert werden, da alle Daten vorab gesammelt werden.

Start Anleitung:
-------------------------------------------------------------------------------------------------------------------------------------------------
1. Um die Apllikation zu starten zu können stellen Sie sicher, dass Sie poetry installiert haben.
2. Mit dem befehl "poetry install" werden die Projektabhängigen Dienste installiert.
3. Mit dem Befehl "poetry run uvicorn ATL.main:app --reload" können Sie das program starten, wenn alles geklappt hat sollte es so aussehen wie unten beschrieben:
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [20568] using WatchFiles
INFO:     Started server process [18112]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
4. Öffnen Sie diesen Pfad im Browser Ihres vertrauens : http://127.0.0.1:8000
5. Geben Sie am Ende des Pfades /docs ein um die einzelnen Endpunkte sehen zu können, der Pfad sollte so aussehen: http://127.0.0.1:8000/docs

Benutzung Anleitung:
--------------------------------------------------------------------------------------------------------------------------------------------------
1. Bevor Sie die Software benutzen können müssen Sie sich registrieren, nutzen Sie dazu den Endpunkt user/register.
   Geben Sie einen belibigen Benutzernamen und ein Passwort an.
2. Um die anderen Endpunkte benutzen zu können drücken sie den Authorize Button(ganz oben rechts).
3. Melden Sie sich mit dem von Ihnen erstellten Benutzernamen und Passwort an.
   Die anderen Endpunkte sind nun entsperrt.
4. Erstellen Sie zuerst einen Kunden mit dem Endpunkt "Create Customer", achten Sie darauf, dass die ID (Kundennummer)noch nicht verwendet wird.
5. Erstellen Sie anschliessend einen Mitrabeiter mit dem Endpunkt "Create Employee", geben sie die ID des zuvor erstellten Kunden an.
6. Erstellen Sie nun einen Auftrag mit dem Endpunkt "Create Order". Geben Sie die zuvor erstellten ID's vom Kunden (Customer)und dem Mitarbeiter(Employee) an.
7. Erstellen Sie nun die Programme die bei diesem Auftrag installiert sein müssen mit dem Endpunkt "Create Program".
8. Fügen sie die erstellten Programme dem Auftrag hinzu mit dem Endpunkt Add_program_to_order.
9. Sie können nun mit dem Endpunkt "Read Customer Orders" unter angabe der Kunden ID den gesammten Auftrag mit allen informationen ausgeben. Sie können auch die anderen Read Endpunkte benutzen, wenn sie beispielsweise nur den Auftrag mit den Programmen sehen wollen nuntzen Sie den Endpunkt "Read Order"

Überlegungen:
--------------------------------------------------------------------------------------------------------------------------------------------------

Struktur:
Eine grosse Schwierigkeit lag in der Struktur und die Vielseitigkeit unserer Kunden. Wir haben grösstenteils KMU's als Kunden aber auch Einzelpersonen bzw. Privatpersonen die wir betreuen und für Sie Geräte aufsetzen. Den Kompromiss den ich machen musste war, dass alle Einzelkunden in meinem Program wie als Firma behandelt werden müssen, in dem zuerst der Kunde wie als Firma und dann der einzelne Mitarbeiter in diesem Fall die Einzelperson erfasst werden muss, dies erscheint mir als die beste Lösung. 

Da viele Kunden auch oft Freeware installiert haben möchten wollte ich nicht z.B 10 Mal Firefox erfassen. Daher hab ich die Beziehung von Programmen zu Aufträgen in einer Many to Many beziehung gelöst. Damit einige Programme mehreren Aufträgen zugewiesen sein können. 

Sicherheit:
Da ich in meinem Programm Passwörter und Zugangsdaten von Kunden nicht gehashed Speichere, was normalersweise keine gute Idee ist, aber leider nötig, Bedarf es Sicherheitsvorkehrungen damit diese Daten nicht in falsche Hände geraten. Die Passwörter oder Lizenzen der Kunden zu hashen hätte nichts gebracht, da ich sie ohnehin wieder im Klartext ausgeben muss, daher habe ich mich für eine Authentifizierung mit OAuth entschieden und so umgesetzt. Aufgrund der eher experimentellen umgebung habe ich den Registrierungsendpunkt offen gelassen um die benutzung nicht zu erschweren. In einer Produktivumgebung wird dieser Enpunkt dann nur für Administatoren zugänglich sein.


Verbesserungen bei mehr Zeit:
--------------------------------------------------------------------------------------------------------------------------------------------------

GUI Implementierung: Sehr gerne hätte ich noch eine Graphische Benutzeroberfläche für das Programm entwickelt, leider habe ich ein wenig unterschätzt, wie viel Aufwand mein Projekt generiert und ich schon deutlich über den Büdgetierten 16 Stunden liege für diese ATL. Daher hatte ich leider keine Zeit mehr ein GUI zu Implementieren.

Überprüfen der Tokengültigkeit: Damit mein Programm benutzt werden kann muss man sich registrieren und anmelden. Die einzelnen Endpunkte überprüfen aber nicht ober der Token noch gültig ist sondern nur ob es mitgegeben wird. Wenn ich mehr Zeit gehabt hätte, hätte ich dies gerne sauberer gelöst. 








