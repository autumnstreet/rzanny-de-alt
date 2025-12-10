
			        Sysinfo 2.25
				============
1. Installation
2. Sicherheitshinweise
3. Hinweise
4. Updates
5. History
6. Lizenz


	1. Installation:
	-------------------------------------------------------------------------------------------------------
	a) Entpacken Sie das Zip File mit einem Dekomprimierungsprogramm wie WinZip oder WinRar.

	b) Speichern Sie die beinhalteten Dateien auf Ihren Computer.

	c) Starten Sie Ihr FTP Programm und Verbinden sich mit Ihren Internet Service Provider (ISP) zu Ihrer Domain.

	d) Stellen Sie sicher ob Sie ein bestimmtes CGI-BIN Verzeichnis benötigen oder ob Sie das Script in jedem 
	   beliebigen Verzeichnis ausführen können. Ihr ISP gibt Ihnen darüber Auskunft. Ihr gemieteter Webspace 
	   muss eigene CGI-BIN Scripte ausführen können. In den meisten Fällen ist das mit im angemieteten Paket 
	   enthalten. Nur in kleineren Paketen muss so eine Funktion zusätzlich beauftragt werden !!

	e) Öffnen Sie das Vorhandene CGI-BIN Verzeichnis oder erstellen Sie ein Verzeichnis mit dem Namen CGI-BIN und öffnen es dann.

	f) Erstellen Sie im Verzeichnis "CGI-BIN" einen Ordner "sys". Der Ordner kann auch einen von
	   Ihnen selbst bestimmten Namen erhalten. Wechseln Sie in den neu angelegten Ordner "sys".

	g) Stellen Sie Ihr FTP Programm auf den Modus ASCII. Ein FTP Programm verüfugt meist über drei verschiedene Modis: ASCII BINARY und AUTO.

	h) Kopieren Sie jetzt alle Dateien im lokalen cgi-bin Verzeichnis in den Ordner "sys" auf Ihren Webspace:

	Berechtigung der Files:
	        Berechtigen Sie die Files mit einer Berechtigung von 755:
	        - sysinfo.cgi

	        Weitere Informationen über Berechtigungen finden Sie unter:
	        http://www.coder-world.de/cw/seite__pagezugriffsrechte.html

	i) Nun noch im Browser die "sysinfo.cgi" aufrufen 
	   und die Installation ist abgeschlossen.

	Weitere Informationen über Installationen finden Sie unter:
	http://www.coder-world.de/cw/seite__pageinstall.html

	Mehr Informationen über Templates und HTML-Dateien finden Sie unter:
	http://www.coder-world.de/cw/seite__pagetemplates.html
	-------------------------------------------------------------------------------------------------------


	2. Sicherheitshinweise
	-------------------------------------------------------------------------------------------------------
	Falls die Datei "sysinfo.cache" für den Cache erstellt wurde, so wird das Zugriffsrecht 666 statt 777 empfohlen.
	-------------------------------------------------------------------------------------------------------


	3. Hinweise
	-------------------------------------------------------------------------------------------------------
	Sysinfo.cgi öffnen mit Text-Editor

	 $free = "50"; # Anzahl an Verfügbaren MB's auf dem Webspace
	 Die Zahl "50" durch die jeweilige Anzahl an MB die sie auf ihrem Webspace zur verfügung haben ersetzen.

	 $passwort = "test"; # Passwort
	 Das Wort "test" durch ihr Passwort ersetzen.

	Viele weitere Einstellungen befinden sich dort auch.
	-------------------------------------------------------------------------------------------------------


	4. Updates
	-------------------------------------------------------------------------------------------------------
	Bei einem Update muss lediglich die Datei "sysinfo.cgi" überschrieben werden.
	-------------------------------------------------------------------------------------------------------


	5. History
	-------------------------------------------------------------------------------------------------------
	18.09.2005 version 2.25
	- Mime-Typen werden nun auch angezeigt, wenn nichts gefunden wurde, in dem Fall wird die neue interne Liste benutzt
	- Das iFrame für die Perl-Module wurde um 20 Pixel in der Breite erhöht.
	- Reloadzeit der CPU Auslastung kann nun in Sekunden eingestellt werden.
	- Unter "Lastlog" werden nun auch "Protokolle" angezeigt.
	- Bugfix: Bei "Hostname" werden doppelte gefiltert.
	- Bugfix: Die Erkennung der Perl-Module zeigt keine Unterfunktionen in Modulen als Untermodul mehr an.
	- Bugfix: Warnungen wurden durch "no warnings;" weitgehend ausgeschaltet, die durch z.B. nicht existierende Verzeichnisse hervorgerufen werden.
	- Bugfix: Beim Server "Microsoft-IIS/4.0" wird die Erkennung über WMI/Win32-OLE ausgeschaltet um den Abbruch des Scriptes im gesamten zu Verhindern.

	30.08.2005 version 2.24
	- Downloadfunktion für Logfiles integriert.
	- Einzelne Bereiche wie Serverinfos, Systeminfos, Perl-Debugger, Logfiles, Webspace berechnen können nun deaktiviert werden.

	16.06.2005 version 2.23
	- Suchfuntkion für Logfiles integriert.

	31.01.2005 version 2.22
	- Anzeige der Umgebungsvariable "PATH" unter Windows verbessert.
	- "Allgemeine Pfade", "Hardware Informationen", "Netzwerk Informationen" und "Prozessbaum" werden nun auch unter Windows erkannt.
	- Mime-Types werden nun auch unter Windows erkannt. (Xampp/Apache)
	- Es wird angezeigt ob Threads erlaubt sind.
	- Lastlog wurde in ein iFrame integriert.

	08.09.2004 version 2.21
	- Erkennung für Sendmail bzw. Postfix verbessert.

	08.05.2004 version 2.2
	- Erkennung für Apache2 integriert.
	- diverse Fehler bei "Jetzt laufende Server Prozesse" behoben.

	04.04.2004 version 2.1
	- Erkennung der Perl-Module verbessert.

	05.03.2004 version 2.0
	- Erkennung für "IDN" integriert.
	- Neuprogrammierung des gesamten Scriptes.

	18.09.2003 version 1.39
	- Erkennung der "Allgemeinen Pfade" verbessert und "traceroute" hinzugefügt.

	5.08.2003 version 1.38
	- Erkennung der Module verfeinert.
	- Unter Windows wird nun auch der Arbeitsspeicher(Memory Usage) und Dateisysteme(Mounted Filesystems) angezeigt.
	- Zudem wird nun unter Windows auch die MHZ-Zahl vom Prozessor angezeigt.

	15.05.2003 version 1.37
	- Erkennung für "Apache Lib" integriert.
	- Erkennung für "Apache modules installed" integriert.
	- Erkennung für "Fly" integriert und dafür "sh"/"ls" entfernt.

	20.04.2003 version 1.36
	- Erkennung für Logfiles verbessert.
	- gepackte Logfiles können nun gelesen werden. (z.B.: access.tgz oder error.tar.gz)

	1.04.2003 version 1.35
	- Erkennung für "Hostname" wurde verbessert.
	- Erkennung für "Kernel" bzw. "Betriebssystem" wurde verbessert.
	- Erkennung für Compress-Pfad eingebaut.
	- Erkennung für Mime-Types verbessert.
	- Erkennung für Logfiles verbessert.
	- Anzeige von "HTTP_ACCEPT" in den Umgebungsvariablen angepasst.
	- diverse Fehler wurden behoben.

	8.12.2002 version 1.34
	- Erkennung für Perlmodule wurde verbessert.
	- Erkennung für die Version von Perlmodulen wurde verbessert.
	- CPU Auslastung in Prozentzahl hinzugefügt.

	11.9.2002 version 1.33
	- Bei ENV-Variablen wurde "PATH" optisch angepasst.
	- Bei ENV-Variablen wurde "REMOTE_HOST" hinzugefügt.

	20.6.2002 version 1.32
	- Sicherheitsloch wurde geschlossen.

	4.6.2002 version 1.31
	- Erkennung für GPG-Pfad eingebaut.
	- Erkennung für Compiled-In Module eingebaut.

	24.4.2002 version 1.30
	- Erkennung von "Alle laufende Server Prozesse" verbessert.
	- "Perl zuletzt geändert" unter "Server-Infos" hinzugefügt.
	- "eingebundene Libs" hinzugefügt.
	- Mehr Dokumentationen bei "Allgemeine Pfade" sofern man auf den Pfad klickt.
	- Mehr Dokumentationen bei "Installierte Module (@INC)" sofern man auf den Pfad klickt sowie bessere Versionserkennung.

	3.1.2001 version 1.21
	- Erkennung für PGP,SH und Gunzip hinzugefügt.
	- Die meissten Namen von "Allgemeine Pfade" sind ankickbar und wenn möglich erscheint dann eine Hilfeseite von diesem Befehl.

	31.12.2001 version 1.20
	- Dead.Letter Erkennung verbessert.
	- Die Modul Namen sind nun anklickbar und wenn vorhanden wird die Dokumentation von dem Perl Modul angezeigt!
	- GZIP Komprimierung hinzugefügt.(optional)
	- Script optimiert und verkleinert um viele Kilobytes!

	30.12.001 version 1.19
	- Logfile Erkennung verbessert.

	29.11.2001 version 1.18
	- Modul-Versions Erkennung wurde verbessert.
	- Logfile Anzeige-Bug behoben.
	- einwenig optimiert.

	29.11.2001 version 1.17
	- Windows Version hinzugefügt. Nun wird die Windows Version Angezeigt genauso wie die Kernel Version auf einem Linux Server.
	- Windows-Uptime hinzugefügt. Nun wird auch unter Windows Angezeigt seit wann der Server aktiv ist.
	- "Allgemeine Pfade" wurden um folgende Erkennungen erweitert: Pfad zu Tar & Gzip
	- Dank an HeXaChLoR(chaospunk@gmx.net) von www.perlhelp.de das ich "Windows-Uptime" Codestück entwenden durfte aus Tellme.

	25.10.2001 version 1.16
	- "Mime-Types" überarbeitet deutlich schneller und bessere Erkennung.
	- "Allgemeine Pfade" wurden um folgende Erkennungen erweitert: Pfad zu Whois, Ping, Nslookup, Finger, Dnsquery
	- kleine detail Verbesserungen am Quellcode

	12.9.2001 version 1.15
	- "Systeminfos" stark überarbeitet. Besseres Design, bessere Erkennung, mehr Speed.
	- Neue Lizenz (weniger Einschränkungen)
	- kleine detail Verbesserungen am Quellcode
	- Signal Alarm geändert auf 300 Sekunden. Danach schaltet das Script sich selbst ständig ab. (Internal Error 500)

	23.8.2001 version 1.14
	- Fehlermeldungen ausradiert im Kopf.
	- Signal Alarm eingebaut. Das Script läuft maximal 30 Sekunden danach schaltet es sich selbst ab.
	- Einige kleinere Bugs gefixt.

	1.7.2001 version 1.13
	- Komplett neue Logfile erkennung.
	- Perl-Debugger kann nun Warnungen ausgeben.
	- Allgemeine Pfade werden nun auf mehr Servern erkannt.
	- Ports sind weggefallen wegen ungenauigkeit.

	21.5.2001 version 1.12
	- Webspace berechnen funktioniert nun auf den Systemen: Unix, Linux, Windows NT und Windows 9x
	- Systeminfos funktioniert nun auch ohne oder mit DBI.(Autoerkennung durch einen Begin block)

	7.5.2001 version 1.1
	- Das Skript wurde von Kopf bis Fuss komplett neugeschrieben. Deswegen keine Einzelaufzählung.
	- Dank an HeXaChLoR(chaospunk@gmx.net) von www.perlhelp.de das ich einige Codestücke entwenden durfte aus Tellme.

	11.4.2001 version 1.04
	- Perl-Debugger bugfixed.
	- Packen bugfixed.

	22.2.2001 version 1.03
	- Datenbank erkennung hinzugefügt.
	- Grep / Date / Userid erkennung hinzugefügt.
	- Perlpfad erkennung verbessert.
	- Sendmailpfad erkennung verbessert.
	- Dank an HeXaChLoR(chaospunk@gmx.net) von www.perlhelp.de das ich einige Codestücke entwenden durfte aus Tellme.

	20.1.2001 version 1.02
	- Internet-Zeit hinzugefügt.(beats)
	- Logfiles erkennung und anzeige verbessert.
	- Packen mit Passwortschutz, das passwort muss man im kopf der system.cgi festlegen.
	- Relativer-Pfad anzeige verbessert.
	- Uptime erkennung verbessert.(1 Routine erkennt alles, 2 Routine erkennt nur Tage)

	10.1.2001 version 1.01
	- Logfiles erkennung verbessert.
	- In Mime-Types werden nun auch Akzeptierte Dateisysteme des Server's angezeigt.
	- Dead.letter (Tote Mails) falls vorhanden werden angezeigt.
	- Ports des Servers werden nun angezeigt.
	- Man kann verzeichnis Packen, sofern das Betriebsystem Unix oder Linux ist.
	- Mounted Filesystem erkennung verbessert.
	- Laufende Server Prozesse (im detail) in Systemninfos per link nun erreichbar.
	- Systeminfos wurde optisch an Mozilla, Netscape und Opera angepasst.
	- Geschwindigkeit optimiert.
	- Kernel Version erkennung verbessert.
	- Hardware Informationen (2) erkennung und anzeige in SCSI Devices verbessert.

	19.12.2000 version 1.0
	- Webspace berechnen wurde verbessert.

	18.12.2000 version 0.9
	- Webspace berechnen erweitert.
	- Errorpages (404,401,403,500,usw.) hinzugefügt.
	- Fehler im Perl-Debugger behoben.
	- Mime-Types falls nicht gefunden wird dies nun auch angezeigt.

	8.12.2000 version 0.8
	- Erste Veröffentlichung.
	-------------------------------------------------------------------------------------------------------

	6. Lizenz
	-------------------------------------------------------------------------------------------------------
	Die Lizenzbestimmungen finden Sie im Entpackten Verzeichnis unter lizenz.html.
	-------------------------------------------------------------------------------------------------------


---------------------------------------------------------------------------
Euer Stefanos - support@coder-world.de - http://www.coder-world.de