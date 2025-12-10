#!/usr/bin/perl -w
#!C:\Perl\bin\perl.exe
#!c:\apachefriends\xampp\perl\bin\perl.exe
#use CGI::Carp qw(fatalsToBrowser);
#no warnings;
use Socket;
use Config;
#alarm(300);

# Setup - Begin
$cgiORpl = "cgi"; # Falls die Datei "sysinfo.pl" heisst, bitte auf pl umÑndern.
$passwort = ""; # Hiermit wird das gesamte Script durch ein Passwort geschÅtzt. Aufruf sysinfo.cgi?pass=IhrPasswort
$free = "100"; # In MB Angeben wieviel Webspace sie haben!
$gzip = "0"; # GZIP Komprimierung - Um den Inhalt schneller und platzsparender zu öbertragen! - 0 = Aus - 1 = An
$cache = "1"; # 1=AN, 0=AUS - Die Datei "sysinfo.cache" sollte vorhanden sein im selben Verzeichnis wie sysinfo.cgi mit dem Zugriffsrecht 666 !
$maxdisplay = "250"; # Zeichenanzahl bei Logfiles die pro Seite dargestellt werden sollen.
$flock = "1"; # Sollte bei Windows auf "0" gesetzt werden sonst auf "1"
$reload = "60"; # Bestimmt in welchem Sekundenabstand die Anzeige "CPU Auslastung" aktualisiert werden soll.

# Bereiche AN/AUS:
$serverON = "1"; # 1=AN - 0=AUS, Bereich "Serverinfos"
$systemON = "1"; # 1=AN - 0=AUS, Bereich "Systeminfos"
$debuggerON = "1"; # 1=AN - 0=AUS, Bereich "Perl-Debugger
$logfilesON = "1"; # 1=AN - 0=AUS, Bereich "Logfiles"
$webspaceON = "1"; # 1=AN - 0=AUS, Bereich "Webspace berechnen"

# 
# Das MenÅ oben in jeder Seite bleibt unverÑndert, lediglich die Funktionen zeigen nichts an.
#
# Setup - End

($letztesFeld) = ($ENV{'DOCUMENT_ROOT'} =~ /\/([^\/\\]+?)$/);
if($ENV{'DOCUMENT_ROOT'} =~ /\/$letztesFeld$/i){
	$ENV{'DOCUMENT_ROOT'} =~ s/\/$letztesFeld$//ig;
	$ENV{'DOCUMENT_ROOT'} =~ s/\/$//g;
	$htmldocument_root = 1;
}
# Apache - Begin
@apache = (	"/usr/local/apache/libexec",
		"/opt/lib/apache",
		"/usr/lib/apache",
		"/usr/lib/apache/modules",
		"/usr/local/apache/modules",
		"/System/Library/Apache/Modules",
		"/usr/local/apache2/libexec",
		"/opt/lib/apache2",
		"/usr/lib/apache2",
		"/usr/lib/apache2/modules",
		"/usr/local/apache2/modules",
		"/System/Library/Apache2/Modules",
#		"C:/apachefriends/xampp/apache/modules",
		);

@mimetypes = (
	"/etc/mime.types",
	"/usr/etc/mime.types",
	"/etc/apache2/mime.types",
	"/etc/httpd/conf/apache-mime.types",
#	"C:/apachefriends/xampp/apache/conf/mime.types",
	"mime.types",
);

@protokoll = (
	"/etc/protocols",
	"/usr/etc/protocols",
	"/etc/apache2/protocols",
	"/etc/httpd/conf/apache-protocols",
#	"C:/apachefriends/xampp/apache/conf/protocols",
	"protocols",
);

@standard = (	"mod_rewrite.so","mod_cgi.so","mod_env.so","mod_imap.so","mod_include.so","libperl.so","mod_alias.so","mod_access.so","mod_browser.so","mod_python.so","mod_unique_id.so",
		"mod_auth.so","mod_digest.so","mod_auth_anon.so","mod_auth_db.so","mod_auth_dbm.so","mod_auth_cookie.so","mod_auth_digest.so","mod_auth_mysql.so",
		"mod_expires.so","mod_fastcgi.so","mod_gzip.so","mod_deflate.so","mod_headers.so","libphp3.so","libphp4.so","mod_proxy.so","mod_speling.so","mod_status.so',  'mod_usertrack.so","mod_vhost_alias.so"
		);
# Apache - End

# Logs - Begin
@logs = ("/etc/logfiles",
	"/etc/log",
	"/etc/log.old",
	"/log/httpd",
	"/var/lib/mysql",
	"/etc/httpd/logs",
	"/usr/local/apache/logs",
	"/usr/local/apache2/logs",
	"/opt/apache/logs",
	"/opt/apache2/logs",
	"/var/lib/xdm/xdm-errors",
	"/var/spool/smail/log",
	"/var/squid/logs",
	"/var/account/pacct",
	"/var/lib/perforce/log",
	"/var/log",
	"$ENV{'DOCUMENT_ROOT'}/log",
	"$ENV{'DOCUMENT_ROOT'}/logs",
#	"C:/apachefriends/xampp/apache/logs",
);
# Logs - End
if($htmldocument_root == 1){
	$ENV{'DOCUMENT_ROOT'} .= "/$letztesFeld";
}

##############################################################################################################
# Nutzungsbedingungen (Sysinfo): Lizenz: Stand: 3.09.2001
#
# Durch Download der Software erklÑren Sie sich mit diesen Lizenzabkommen einverstanden. 
# Der Sysinfo ist Freeware, jedoch nicht zum GNU/GPL - Abkommen zuzuordnen. 
# Diese Lizenz erlaubt es Ihnen, Sysinfo zu benutzen. 
# Als Nutzer des Sysinfo k˜nnen Sie auf eigenes Risiko die Software verÑndern und/oder auf Ihre BedÅrfnisse anpassen. 
# Sie k˜nnen auch Dritte mit der Anpassung/VerÑnderung beauftragen. 
# Die Original-Software unverÑndert darf weitergegeben werden jedoch nicht verkauft oder wiederverkauft werden.
#
# Die angepasste/verÑnderte Software und Teile dieser dÅrfen nicht weitergegeben, verkauft oder wiederverkauft werden.
#
# Alle Copyright- und Versions-Hinweise, die im Sysinfo oder deren HTML-Seiten verwendet, erstellt und/oder gezeigt 
# werden, dÅrfen nicht entfernt werden. Die Copyright- und Versions-Hinweise mÅssen fÅr Benutzer sichtbar und in 
# ungeÑnderter Form dargestellt werden.
#
# Dieses Lizenzabkommen beruht sich auf der aktuellen internationalen Gesetzeslage.
#
# Bei einem Verstoò gegen diesen Lizenzvertrag kann durch die Firma Coder-World oder deren Beauftragten die erworbene Lizenz 
# jederzeit zurÅckgezogen und fÅr nichtig erklÑrt werden sowie die Benutzung untersagt werden. 
# Sysinfo und die dazugeh˜renden Dateien werden ohne Funktionsgarantie fÅr die im Umfeld verwendete Hardware 
# oder Software verkauft.
#
# Coder-World oder deren Beauftragten sind in keiner Form fÅr Inhalte oder Verfasser verantwortlich, die durch diese 
# Software erstellt wurden.
#
# Das Risiko der Benutzung vom Sysinfo obliegt dem Lizenznehmer, jegliche Erstattungen im Rechtsfall sind ausgeschlossen. 
# Eine Lizenz ist zeitlich unbegrenzt nutzbar, in der Lizenz ist grundsÑtzlich der Zugriff auf alle neuen Versionen fÅr 
# einen unbegrenzten Zeitraum enthalten.
#
# Hinweis: Es existieren keine Reseller-, Wiederverkaufs- oder SchÅler-/Studenten - Versionen. Nach den Lizenzbedingungen muò der Website-Besitzer die Lizenz selbst erhalten.  
#
# Verfasser: Stefan Gipper (Stefanos)
# E-Mail: support@coder-world.de
# Webseite: http://www.coder-world.de
#
# Bei Ver˜ffentlichung dieses Dokuments ist es eine feine Geste, mir eine Nachricht zukommen zu lassen.
##############################################################################################################
$version = "2.25";

BEGIN {
	eval { $eval_in_died = 1; require DBI; };
	if(!$@){
		$mod_dbi = 1;
		import DBI;
	}
	if ($^O =~ /win/i){
		eval { $eval_in_died = 1; require Win32::Registry; };
		if(!$@){
			$mod_w32r = 1;
			import Win32::Registry;
		}
		eval { $eval_in_died = 1; require Win32::OLE; };
		if(!$@){
			$mod_w32ole = 1;
			import Win32::OLE qw( in );
		}
		eval { $eval_in_died = 1; require Win32::API; };
		if(!$@){
			$mod_w32s = 1;
			import Win32::API;
		}
		eval { $eval_in_died = 1; require Win32::Process::Info; };
		if(!$@){
			$mod_w32i = 1;
			import Win32::Process::Info;
		}
		eval { $eval_in_died = 1; require Win32::Process; };
		if(!$@){
			$mod_w32p = 1;
			import Win32::Process;
		}
		eval { $eval_in_died = 1; require Win32; };
		if(!$@){
			$mod_w32 = 1;
			import Win32;
		}
	}
	eval { $eval_in_died = 1; require Compress::Zlib; };
	if(!$@) {
		$zlib = 1;
		import Compress::Zlib;
	}
#	eval { $eval_in_died = 1; require File::Find; };
#	if(!$@){
#		$mod_file = 1;
#		import File::Find;
#	}
}
if($ENV{'SERVER_SOFTWARE'} eq "Microsoft-IIS/4.0"){
	$mod_w32ole = 0;
}

if($mod_w32ole){
	$WMI = Win32::OLE->GetObject("winmgmts:{impersonationLevel=impersonate}\\\\.\\Root\\cimv2");
	foreach $Proc ( sort {lc $a->{ProcessId} cmp lc $b->{ProcessId}} in( $WMI->InstancesOf( "Win32_Process" ) ) ){
		if($Proc->{ExecutablePath} =~ /apache.exe$/i){
			$newpfad = $Proc->{ExecutablePath};
			$newpfad =~ s/\\/\//g;
			$newpfad =~ s/\/bin\/apache.exe$//;
			push(@logs,"$newpfad/logs");
			push(@mimetypes,"$newpfad/conf/mime.types");
			push(@apache,"$newpfad/modules");
			last;
		}
	}
}

use Cwd;
$ENV{'PWD'} = getcwd;

read(STDIN,$input,$ENV{'CONTENT_LENGTH'});
foreach (split(/&/,$input)) {
	($name,$value) = split(/=/);
	$name =~ tr/+/ /;
	$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$FORM{$name} = $value;
}
foreach (split(/&/,$ENV{'QUERY_STRING'})){
	($name,$value) = split(/=/);
	$name =~ tr/+/ /;
	$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ s/<!--(.|\n)*-->//g;
	$INFO{$name} = $value;
}
$action = $INFO{'action'} || $FORM{'action'};
$pass = $INFO{'pass'} || $FORM{'pass'};
if($passwort){
	&error("Falsches Passwort.") if($passwort ne $pass);
}

@timestamp = localtime(time);
$timestamp[5] += 1900;
$timestamp[4]++;
$timestamp[1] = "0$timestamp[1]" if($timestamp[1] < 10);
$timestamp[2] = "0$timestamp[2]" if($timestamp[2] < 10);
$timestamp[3] = "0$timestamp[3]" if($timestamp[3] < 10);
$timestamp[4] = "0$timestamp[4]" if($timestamp[4] < 10);
$date = "$timestamp[3].$timestamp[4].$timestamp[5] - $timestamp[2]:$timestamp[1]";

if($action =~ /^\w+$/){
	&$action;
}else{
	&index;
}

sub lastlog {
	if($serverON){
		@lastlog = split(/\n/,&command("lastlog"));
		shift(@lastlog);
	}

	$lastlogtemp .= qq~<table cellpadding="3" cellspacing="1" border="0">
		<tr>
			<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2" size="3"><b>Lastlog:</b></font></td>
		</tr>
		<tr>
			<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Username</font></td>
			<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Port</font></td>
			<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">From</font></td>
			<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Latest</font></td>
		</tr>~;

	foreach (@lastlog){
		if($_ =~ /^(.+?)\s+(.+?)\s+(.+?)\s+(.+?)$/ && $_ !~ /\*\*/){
			$LLname = $1;
			$LLport = $2;
			$LLfrom = $3;
			$LLdatum = "$4 $5 $6 $7 $9";
		}elsif($_ =~ /^(.+?)\s+(.+?)$/){
			$LLname = $1;
			$LLport = "";
			$LLfrom = "";
			$LLdatum = $2;
		}
		$lastlogtemp .= qq~
	<tr>
		<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$LLname</font></td>
		<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$LLport</font></td>
		<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$LLfrom</font></td>
		<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$LLdatum</font></td>
	</tr>
		~;
	}
		$lastlogtemp .= "</table>";

	if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /(x-gzip|gzip)/ && $ENV{'SERVER_PROTOCOL'} eq "HTTP/1.1" && $gzip == 1){
		print "Content-Encoding: $1\n";
		print "Content-Type: text/html\n\n";
		binmode STDOUT;
		if($zlib){
			print Compress::Zlib::memGzip($lastlogtemp);
		}else{
			open(GZIP, "| gzip -f");
			binmode(GZIP);
			print GZIP $lastlogtemp;
			close(GZIP);
		}
	}else{
		print "Content-Type: text/html\n\n";
		print $lastlogtemp;
	}
	exit;
}

sub cpulast {
	if(-e("/proc/stat") && $serverON){
		open(F,"</proc/stat");
		$temp = <F>;
		close(F);

		($name,$user,$wert,$system,$idle) = split(/\s+/,$temp);
		$usage = $user + $wert + $system;
		$total = $user + $wert + $system + $idle;

		sleep(1);

		open(F,"</proc/stat");
		$temp = <F>;
		close(F);

		($newName, $newUser, $newWert, $newSystem, $newIdle) = split(/\s+/,$temp);
		$newUsage = $newUser + $newWert + $newSystem;
		$newTotal = $newUser + $newWert + $newSystem + $newIdle;

		$xUsage = $newUsage - $usage;
		$xTotal = $newTotal - $total;

		if($xTotal > 1 or $xUsage > 1){
			$cpulast = sprintf("%.1f", (($xUsage / $xTotal) * 100));
		}
	}else{
		$cpulast = "??.?";
	}
	$cpulast = qq~
	<html>
	<head>
	<meta http-equiv="Refresh" CONTENT="$reload;URL=sysinfo.$cgiORpl?pass=$pass&action=cpulast">
	</head>
	<body>
	<font face="Verdana,Arial" size="2">$cpulast\%</font>
	</body>
	</html>
	~;

	if($mod_w32ole){
		$WMI = Win32::OLE->GetObject("winmgmts:{impersonationLevel=impersonate}\\\\.\\Root\\cimv2");
		($Proc) = ( sort {lc $a->{Name} cmp lc $b->{Name}} in( $WMI->InstancesOf( "Win32_Processor" ) ) );
		$cpulast = $Proc->{LoadPercentage} . "%";
	}

	if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /(x-gzip|gzip)/ && $ENV{'SERVER_PROTOCOL'} eq "HTTP/1.1" && $gzip == 1){
		print "Content-Encoding: $1\n";
		print "Content-Type: text/html\n\n";
		binmode STDOUT;
		if($zlib){
			print Compress::Zlib::memGzip($cpulast);
		}else{
			open(GZIP, "| gzip -f");
			binmode(GZIP);
			print GZIP $cpulast;
			close(GZIP);
		}
	}else{
		print "Content-Type: text/html\n\n";
		print $cpulast;
	}
	exit;
}

sub filefind {
	local(@e) = @_;
	local(@myfind);
	foreach (@e){
		&searchit($_);
	}
	return(@myfind);
}

sub searchit {
	local($dir) = @_;
	local($path);

	opendir(DIR,"$dir");
	foreach (readdir(DIR)){
		next if $_ eq '.' || $_ eq '..';
		$path = "$dir/$_";
		push(@myfind, $path);
		if(-d $path){
			&searchit($path);
		}
	}
	closedir(DIR);
}

sub perlmodule {
	if($serverON){
		if($cache or $INFO{'cache'}){
			if(-e("/tmp/sysinfo.cache")){
				open(F,"</tmp/sysinfo.cache");
				@keys = <F>;
				close(F);
				$no = 1;
			}elsif(-e("sysinfo.cache")){
				open(F,"<sysinfo.cache");
				@keys = <F>;
				close(F);
				$no = 1;
			}
		}

		if($no && !$INFO{'cache'}){
			foreach (@keys) {
				$_ =~ s/[\n\r]//g;
				$modulzahl++;
				($modulname,$modTab,$modFile) = split(/\|/);
				$modTab = "?" unless defined $modTab;
				if($_ =~ /\Q$INFO{'suchwort'}\E/i or !$INFO{'suchwort'}){
					$m___a .= qq~<tr><td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systemdoc&name=$modulname" target="_blank">$modulname</a></font></td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">~;
					if($modFile =~ /\.[Pp][Mm]$/){
						$m___a .= qq~<a href="#$modFile">$modTab</a>~;
					}else{
						$m___a .= qq~$modTab~;
					}
					$m___a .= qq~</font></td></tr>~;
				}
			}
		}else{
			foreach $filename (&filefind(@INC)){
			        if($filename =~ /\.[Pp][Mm]$/){
			                open(M,"<$filename");
			                while($xline=<M>) {
			                        if($xline =~ /^ *package +(\S+);/){
			                                $modName = $1;
			                                $modTab{$modName}="?";
			                                $modFile{$modName} = $filename;
							$packageversion = $modName . "::VERSION" if($modName);
			                        }

						if($xline =~ /\$Id: ([\w\-\.]+),v ([\d\.]+)/ && $modTab{$modName} !~ /^[\d\.]+$/){
							$modTab{$modName} = $2;
						}elsif($xline =~ /.*?VERSION\s*=\s*(["\'\sv]*)([\d\.]*)(["\'\sv;]*)/ && $modTab{$modName} !~ /^[\d\.]+$/){
							$modTab{$modName} = $2;
						}elsif($xline =~ /Revision: ([\d\.]+) \$/ && $modTab{$modName} !~ /^[\d\.]+$/){
							$modTab{$modName} = $1;
						}elsif($xline =~ /$packageversion\s*=\s*(?:["\'\s]?)([0-9\.]+)(?:["\'\s]?)/ && $modTab{$modName} !~ /^[\d\.]+$/){
							$modTab{$modName} = $2;
						}

					}
			               close(M);
			        }
			}
			foreach (grep(!/^XMLRPC|^UDDI|^[^\w]|^Win32::OLE::Tie$|^DBD::File::|^Here$|^Hang$|^Tk::Date::|^Person$|^SOAP::MIMEParser$|^SOAP::Parser$|^SOAP::Schema$|^SOAP::Schema::Deserializer$|^SOAP::Schema::WSDL$|^SOAP::Serializer$|^SOAP::Server$|^SOAP::Server::Object$|^SOAP::Server::Parameters$|^SOAP::SOM$|^SOAP::Client$|^SOAP::Cloneable$|^SOAP::Constants$|^SOAP::Custom::XML::Data$|^SOAP::Custom::XML::Deserializer$|^SOAP::Data$|^SOAP::Deserializer$|^SOAP::Fault$|^SOAP::Header$|^SOAP::Lite$|^SOAP::Lite::COM$|^SOAP::Lite::QNameValue$|^SOAP::Trace$|^SOAP::Transport$|^SOAP::Utils$|^SOAP::Test::Server$|^SOAP::Transport::FTP::Client$|^SOAP::Transport::HTTP::|^SOAP::XMLSchema|^SWF::BinStream::Write::|^SOAP::Transport::TCP::|^SOAP::Transport::POP3::|^SOAP::Transport::MQ::|^SOAP::Transport::MAILTO::|^SOAP::Transport::LOCAL::|^SOAP::Transport::IO::|^SWF::Builder::MaskInstance$|^SWF::Builder::Movie$|^SWF::Builder::Movie::Root$|^SWF::BinStream::File::|^SOAP::Transport::JABBER::|^SWF::Builder::ActionScript::SyntaxNode::|^PPM::Repository::Result$|^Spreadsheet::ParseExcel::SaveParser::|^SWF::BinStream::Codec::Zlib::|^SWF::Builder::DisplayInstance|^SWF::Builder::ExElement::|^SWF::Builder::Shape::|^SWF::Builder::Text::TEXTRECORD$|^SWF::Builder::ActionScript::|^SWF::Builder::ActionScript::Compiler::|^SWF::Builder::Character::|^SWF::Builder::Character::Bitmap::|^SWF::Builder::Character::Bitmap::Lossless::Custom::|^SWF::Builder::Character::Bitmap::Lossless::GD::|^SWF::Builder::Character::Bitmap::Lossless::ImageMagick::|^SWF::Builder::Character::EditText::|^SWF::Builder::Character::Font::|^SWF::Builder::Character::MovieClip::|^SWF::Builder::Character::Shape::|^SWF::Builder::Character::Text::|^SWF::Builder::ExElement::|^SWF::Builder::Gradient::|^PPM::Repository::PPM3Server::|^SWF::Element::|^Plot$|^Raygun$|^ReportHash$|^OLE::Tie$|^OLE::Variant$|^MyClass$|^MySubs$|^IO::WrapTie::Master$|^IO::WrapTie::Slave$|^Image::TIFF::Rational$|^Foo::ZZZ$|^FOOBAR$|^FooHandle$|^Fuz$|^Archive::Zip::Archive$|^NewExtraHash$|^Baz$|^CGITempFile$|^DB$|^DBD::Proxy::db$|^DBD::Proxy::dr$|^DBD::Proxy::st$|^DBD::SQLite::db$|^DBD::SQLite::dr$|^DBDI$|^DBI::ProxyServer::db$|^DBI::ProxyServer::dr$|^DBI::ProxyServer::st$|^Digest::Foo$|^Demo$|^DemoRevCat$|^Derived1$|^Derived2$|^Descriptions$|^DBD::Proxy::db$|^DBD::Proxy::dr$|^Error::Simple$|^Error::subs$|^EVERY$|^EVERY::LAST$|^Dog$|^DBD::Proxy::st$|^DBD::DBM::db$|^DBD::DBM::dr$|^DBD::DBM::st$|^DBD::DBM::Statement$|^DBD::DBM::Table$|^DBD::Driver::db$|^DBD::Driver::dr$|^DBD::Driver::st$|^CPAN::Queue$|^CPAN::Shell$|^CPAN::Tarzip$|^CPAN::Version$|^NullHang$|^Other$|^OtherClass$|^Painful$|^SomeOtherClass$|^Stuff$|^variance$|^YourModule$|^Car$|^Any::Package$|^CPAN::Author$|^CPAN::Bundle$|^CPAN::CacheMgr$|^CPAN::Complete$|^CPAN::Config$|^CPAN::Debug$|^CPAN::Distribution$|^CPAN::Exception::RecursiveDependency$|^CPAN::FTP$|^CPAN::FTP::netrc$|^CPAN::Index$|^CPAN::InfoObj$|^CPAN::LWP::UserAgent$|^CPAN::Mirrored::By$|^CPAN::Module$|^Ball$|^BANG$|^Tk::DummyEncode::X11ControlChars$|^Archive::Zip::BufferedFileHandle$|^Archive::Zip::DirectoryMember$|^Archive::Zip::FileMember$|^Archive::Zip::Member$|^Archive::Zip::MockFileHandle$|^Archive::Zip::NewFileMember$|^Archive::Zip::StringMember$|^Archive::Zip::ZipFileMember$|^Bar$|^baz$|^NewArray$|^NewHandle$|^NewHash$|^NewScalar$|^NewStdArray$|^NewStdHash$|^NewStdScalar$|^Number$|^pdflibc$|^SomeThing$|^symbolic$|^TableStripper$|^TempFile$|^two_face$|^two_refs$|^two_refs1$|^MySubDBI$|^MySubDBI::db$|^myUA$|^NAME$|^NAME::option1$|^NAME::option2$|^MM$|^ModuleName$|^MultipartBuffer$|^MY$|^My::Test::Module$|^MyDataHandler$|^MyObj$|^Myobj$|^MyParser$|^MyPodParserTree$|^MyPodParserTree2$|^MyQPDecoder$|^Mysql::db$|^Mysql::dr$|^Mysql::st$|^DBD::Proxy::dbb$|^DBD::Proxy::drb$|^DBD::Proxy::stb$|^DBD::mysql::dbb$|^DBD::mysql::drb$|^DBD::mysql::stb$|^DBD::Driver::dbb$|^DBD::Driver::drb$|^DBD::Driver::stb$|^DBI::ProxyServer::dbb$|^DBI::ProxyServer::drb$|^DBI::ProxyServer::stb$|^FilterIntoStringb$|^Foo::ZZZb$|^FOOBARb$|^FooHandleb$|^Fuzb$|^DBD::\$\{driver\}::db$|^DBD::\$\{driver\}::GetInfo$|^DBD::\$\{driver\}::TypeInfo$|^Felis$|^Fh$|^CGI::mod_perl$|^Class::Struct::Tie_ISA$|^Calculator$|^Canine$|^Archive::Tar::_io$|^CLASS_NAME$|^CLIENT$|^CommentStripper$|^Yet::Another::AutoSplit$|^Yet::More::Attributes$|^YourPackage$|^MyHandlers$|^MyPackage$|^IDEA$|^Image::TIFF$|^TiffFile$|^main$|^MySubDBI::st$|^BufferWithInt$|^Cinna$|^Critter::Sounds$|^Mail::Mailer::smtp::pipe$|^My::PingPong$|^Foo$|^Web::Server$|^pdflib_pl$|\$|_|^\w$/,sort { lc($a) cmp lc($b)} keys %modTab)){
				if($modulit{$modFile{$_}}){
					next;
				}else{
					$modulit{$modFile{$_}} = 1;
				}
				$modulzahl++;
				$modTab{$_} = "?" unless($modTab{$_});
				if($_ =~ /\Q$INFO{'suchwort'}\E/i or !$INFO{'suchwort'}){
					$m___a .= qq~<tr><td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systemdoc&name=$_" target="_blank">$_</a></font></td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">~;
					if($modFile{$_} =~ /\.[Pp][Mm]$/){
						$m___a .= qq~<a href="#$modFile{$_}">$modTab{$_}</a>~;
					}else{
						$m___a .= qq~$modTab{$_}~;
					}
					$m___a .= qq~</font></td></tr>~;
				}
				push(@write,"$_\|$modTab{$_}\|$modFile{$_}\n") if($cache or $INFO{'cache'});
			}

			if($cache or $INFO{'cache'}){
				if(-e("sysinfo.cache")){
					open(F,">sysinfo.cache");
					print F @write;
					close(F);
				}else{
					open(F,">/tmp/sysinfo.cache");
					print F @write;
					close(F);
					unless(-e("/tmp/sysinfo.cache")){
						open(F,">sysinfo.cache");
						print F @write;
						close(F);
					}
				}
			}
		}
	}
	$cpulast = qq~
	<html>
	<head>
	<style type="text/css">
	<!--
	INPUT.button {font:Lucida,Verdana,Helvetica,Sans-Serif;}
	INPUT.box {font:Lucida,Verdana,Helvetica,Sans-Serif;}
	SELECT {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	OPTION {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	TEXTAREA {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	INPUT {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	A:link {text-decoration: none;color: black;}
	A:visited {text-decoration: none;color: black;}
	A:active {background: #FFFFFF;color: black;text-decoration: underline;}
	A:hover {background: #FFFFFF;color: black;text-decoration: underline;}
	-->
	</style>
	<body bgcolor="#FFFFFF" topmargin="0" leftmargin="0" marginheight="0" marginwidth="0">

	<table border="0" cellspacing="1" cellpadding="1">
		<tr>
			<td bgcolor="#bcbcEE" colspan="2"><font face="Verdana,Arial" size="2" size="3"><b>$modulzahl Installierte Module (\@INC)</b></font></td>
		</tr>
		$m___a
	</table>
	</body>
	</html>
	~;

	if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /(x-gzip|gzip)/ && $ENV{'SERVER_PROTOCOL'} eq "HTTP/1.1" && $gzip == 1){
		print "Content-Encoding: $1\n";
		print "Content-Type: text/html\n\n";
		binmode STDOUT;
		if($zlib){
			print Compress::Zlib::memGzip($cpulast);
		}else{
			open(GZIP, "| gzip -f");
			binmode(GZIP);
			print GZIP $cpulast;
			close(GZIP);
		}
	}else{
		print "Content-Type: text/html\n\n";
		print $cpulast;
	}
	exit;
}

sub mimetype {
	if($serverON){
		foreach (@mimetypes){
			if(-r("$_")){
				$mimes = $_;
				last;
			}
		}

		if(-r("$mimes")){
			open(F,"<$mimes");
			@mime = <F>;
			close(F);
		}else{
			@mime = <DATA>;
		}
		$zahl = (scalar(@mime)) / 3;

		foreach (@mime){
			s/[\n\r]//g;
			if($_ =~ /Port/){
				last;
			}elsif($_ !~ /\#/){
				@mimeX = split(" ",$_);

				$wert1 = shift @mimeX;
				$wert2 = shift @mimeX;
				$rownspan = 1;
				$mime_ausgabe2 = "";
				foreach $lines (@mimeX){
					$mime_ausgabe2 .= qq~<tr><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$lines</font></td></tr>~;
					$rownspan++;
				}

				if($mime_ausgabe2 ne ""){
					$spawn = "rowspan=" . $rownspan;
					$more = $mime_ausgabe2;
				}

				if($wert1 =~ /\Q$INFO{'suchwort'}\E/i or !$INFO{'suchwort'}){
					$wert1 =~ s/(.{45})/$1<br>\n/g;
					$m_au .= qq~<tr><td bgcolor="#ddddFF" $spawn valign="top"><font face="Verdana,Arial" size="2">$wert1</font></td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$wert2</font></td></tr>$more\n~ if($wert1);
				}
			}
		}
	}

	$ausgabe = qq~
	<html>
	<head>
	<style type="text/css">
	<!--
	INPUT.button {font:Lucida,Verdana,Helvetica,Sans-Serif;}
	INPUT.box {font:Lucida,Verdana,Helvetica,Sans-Serif;}
	SELECT {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	OPTION {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	TEXTAREA {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	INPUT {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	A:link {text-decoration: none;color: black;}
	A:visited {text-decoration: none;color: black;}
	A:active {background: #FFFFFF;color: black;text-decoration: underline;}
	A:hover {background: #FFFFFF;color: black;text-decoration: underline;}
	-->
	</style>
	</head>
	<body bgcolor="#FFFFFF" topmargin="0" leftmargin="0" marginheight="0" marginwidth="0">

	<table cellpadding="1" cellspacing="1" border="0">
		<tr>
			<td bgcolor="#bcbcEE" colspan="3"><font face="Verdana,Arial" size="2" size="3"><b>MIME-Typen</b></font></td>
		</tr>
		$m_au
	</table>

	</body>
	</html>
	~;

	if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /(x-gzip|gzip)/ && $ENV{'SERVER_PROTOCOL'} eq "HTTP/1.1" && $gzip == 1){
		print "Content-Encoding: $1\n";
		print "Content-Type: text/html\n\n";
		binmode STDOUT;
		if($zlib){
			print Compress::Zlib::memGzip($ausgabe);
		}else{
			open(GZIP, "| gzip -f");
			binmode(GZIP);
			print GZIP $ausgabe;
			close(GZIP);
		}
	}else{
		print "Content-Type: text/html\n\n";
		print $ausgabe;
	}
	exit;
}

sub ports {
	if($serverON){
		foreach (@protokoll){
			if(-r("$_")){
				$mimes = $_;
				last;
			}
		}

		if(-r("$mimes")){
			open(F,"<$mimes");
			@mime = <F>;
			close(F);
		}else{
			@mime = <DATA>;
		}

		foreach (@mime){
			s/[\n\r]//g;
			if($_ =~ /\#/ && $_ !~ /^\#/){
				($name,$port,$gname,$raute,$des) = split(/\s+/,$_,5);
				next if($port !~ /^\d+$/);
				$m_au .= qq~<tr>
			<td bgcolor="#eeeeee" valign="top"><font face="Verdana,Arial" size="2">$name</font></td>
			<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$port</font></td>
			<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$des</font></td>
		</tr>\n~;
			}
		}
	}

	$ausgabe = qq~
	<html>
	<head>
	<style type="text/css">
	<!--
	INPUT.button {font:Lucida,Verdana,Helvetica,Sans-Serif;}
	INPUT.box {font:Lucida,Verdana,Helvetica,Sans-Serif;}
	SELECT {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	OPTION {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	TEXTAREA {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	INPUT {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	A:link {text-decoration: none;color: black;}
	A:visited {text-decoration: none;color: black;}
	A:active {background: #FFFFFF;color: black;text-decoration: underline;}
	A:hover {background: #FFFFFF;color: black;text-decoration: underline;}
	-->
	</style>
	</head>
	<body bgcolor="#FFFFFF" topmargin="0" leftmargin="0" marginheight="0" marginwidth="0">

	<table cellpadding="1" cellspacing="1" border="0">
		<tr>
			<td bgcolor="#bcbcEE" colspan="3"><font face="Verdana,Arial" size="2" size="3"><b>Protokolle</b></font></td>
		</tr>
		<tr>
			<td bgcolor="#ddddFF" valign="top"><font face="Verdana,Arial" size="2">Name</font></td>
			<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Nr</font></td>
			<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Beschreibung</font></td>
		</tr>
		$m_au
	</table>

	</body>
	</html>
	~;

	if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /(x-gzip|gzip)/ && $ENV{'SERVER_PROTOCOL'} eq "HTTP/1.1" && $gzip == 1){
		print "Content-Encoding: $1\n";
		print "Content-Type: text/html\n\n";
		binmode STDOUT;
		if($zlib){
			print Compress::Zlib::memGzip($ausgabe);
		}else{
			open(GZIP, "| gzip -f");
			binmode(GZIP);
			print GZIP $ausgabe;
			close(GZIP);
		}
	}else{
		print "Content-Type: text/html\n\n";
		print $ausgabe;
	}
	exit;
}

sub signal {
	if($serverON){
		foreach $l (sort keys %SIG) {
			$sig_a .= qq~<tr><td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">$l</font></td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$SIG{$l}</font></td></tr>~ if(!$INFO{'suchwort'} or $l =~ /\Q$INFO{'suchwort'}\E/i);
		}
	}

	$ausgabe = qq~
	<html>
	<head>
	<style type="text/css">
	<!--
	INPUT.button {font:Lucida,Verdana,Helvetica,Sans-Serif;}
	INPUT.box {font:Lucida,Verdana,Helvetica,Sans-Serif;}
	SELECT {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	OPTION {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	TEXTAREA {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	INPUT {FONT-FAMILY:Lucida,Verdana,Helvetica,Sans-Serif;}
	A:link {text-decoration: none;color: black;}
	A:visited {text-decoration: none;color: black;}
	A:active {background: #FFFFFF;color: black;text-decoration: underline;}
	A:hover {background: #FFFFFF;color: black;text-decoration: underline;}
	-->
	</style>
	</head>
	<body bgcolor="#FFFFFF" topmargin="0" leftmargin="0" marginheight="0" marginwidth="0">

	<table cellpadding="1" cellspacing="1" border="0" width="65%">
	<tr>
		<td bgcolor="#bcbcEE" colspan="3"><font face="Verdana,Arial" size="2" size="3"><b>Signal Handler (\%SIG)</b></font></td>
	</tr>
	$sig_a
	</table>

	</body>
	</html>
	~;

	if($ENV{'HTTP_ACCEPT_ENCODING'} =~ /(x-gzip|gzip)/ && $ENV{'SERVER_PROTOCOL'} eq "HTTP/1.1" && $gzip == 1){
		print "Content-Encoding: $1\n";
		print "Content-Type: text/html\n\n";
		binmode STDOUT;
		if($zlib){
			print Compress::Zlib::memGzip($ausgabe);
		}else{
			open(GZIP, "| gzip -f");
			binmode(GZIP);
			print GZIP $ausgabe;
			close(GZIP);
		}
	}else{
		print "Content-Type: text/html\n\n";
		print $ausgabe;
	}
	exit;
}

sub command {
	local($e) = @_;
	eval {
		local $SIG{ALRM} = sub { die "alarm\n" };
		alarm(5);
		$return = join("",`$e`);
		alarm(0);
	};
	return($return);
}

sub index {
	if($serverON){
		($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime;
		$stunde = $hour+1;
		$stunde = 0 if($stunde == 24);
		$beats = (($stunde * 60 * 60) + ($min * 60) + $sec) / 86.4;
		$beats = int($beats);
		$ltime = localtime;
		$gtime = gmtime;

		if ($^O !~ /win/i) {
			foreach ("/bin/sendmail","/sbin/sendmail","/usr/lib/sendmail","/usr/bin/sendmail","/usr/share/sendmail","/usr/sbin/sendmail","/usr/bin/sendmail.restart","/etc/sendmail.cf","/etc/sendmail.cw","/usr/man/man8/sendmail.8","/var/qmail/bin/qmail-inject","/bin/postfix","/sbin/postfix","/usr/lib/postfix","/usr/bin/postfix","/usr/share/postfix","/usr/sbin/postfix","/usr/bin/postfix.restart","/etc/postfix.cf","/etc/postfix.cw","/usr/man/man8/postfix.8","/var/qmail/bin/qmail-inject","/bin/sendmail.postfix","/sbin/sendmail.postfix","/usr/lib/sendmail.postfix","/usr/bin/sendmail.postfix","/usr/share/sendmail.postfix","/usr/sbin/sendmail.postfix","/usr/bin/sendmail.postfix.restart","/etc/sendmail.postfix.cf","/etc/sendmail.postfix.cw","/usr/man/man8/sendmail.postfix.8","/var/qmail/bin/qmail-inject"){
				if(-e $_ && -X _){
					$sm .= "$_<br>";
				}
			}

			$ENVold{'PATH'} = $ENV{'PATH'};
			$ENV{'PATH'} .= ":/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/X11R6/bin:/root/bin"; # unless($ENV{'PATH'});
			@pathsearch = split(/\:/,$ENV{'PATH'});
			foreach $befehl ("httpd","httpd2","perl","grep","date","whois","tar","gzip","gunzip","ping","nslookup","finger","dnsquery","pgp","gpg","fly","idn","convert","compress","traceroute","sendmail","postfix"){
				foreach (@pathsearch){
					if(-e("$_/$befehl")){
						$info{$befehl} = "$_/$befehl";
					}
				}

				unless($info{$befehl}){
					$info{$befehl} = &command("which $befehl");
					$info{$befehl} = "" if($info{$befehl} !~ /^\//);
				}

				unless($info{$befehl}){
					$info{$befehl} = &command("whereis $befehl");
					$info{$befehl} = "" if($info{$befehl} !~ /^\//);
				}

				$info{$befehl} =~ s/^$befehl:\s*//g;
				$info{$befehl} =~ s/^(.+?) .*/$1/sg;
				$info{$befehl} = "<small>nicht installiert</small>" unless($info{$befehl});
			}
			$ENV{'PATH'} = $ENVold{'PATH'};
			unless($sm){
				$info{'sendmail'} =~ s/\n/<br>/g;
				$sm .= $info{'sendmail'} . "<br>";
				$info{'postfix'} =~ s/\n/<br>/g;
				$sm .= $info{'postfix'};
			}
			$traceit = 'traceroute';

			$kernel = &command("cat /proc/sys/kernel/osrelease");
			$kernel = &command("uname -r") unless($kernel);

			$hostuname = &command("uname -n");
			$gethost  = gethostent();

			if($^O =~ /OpenBSD/i){
				$sysname = &command("hostname -s");
			}elsif($^O =~ /linux/i){
				$sysname = &command("hostname -f");
			}else{
				$sysname = &command("hostname");
			}

			$httpd = &command("$info{'httpd'} -l");
			$httpd = &command("$info{'httpd2'} -l") if($httpd !~ /Compiled[\s-]in modules/i);
			if($httpd){
				$httpd =~ s/\r//g;
				$httpd =~ s/^Compiled[\s-]in modules:\n//sg;
				$httpd =~ s/\n(.+?)\n/,$1<br>/sg;
			}else{
				$httpd = "<small>nicht gefunden</small>";
			}

			$userid = &command("id"); # "whoami" oder "id -un" fÅr Username
			$userid =~ s/ /<br>/g;
			$load = &command("uptime");
			if($load =~ /^.*?(\d+?) users?.*?$/){
				$useron = $1;
			}else{
				$useron = "?";
			}

			if($load =~ /^.+?average: +?(\S*? \S*? \S*?)$/){
	  			($load1, $load5, $load15) = split(',',$1,4);
			}else{
				open(F,"/proc/loadavg");
				($load1,$load5,$load15,$load30) = split(/\s+/,join("",<F>),4);
				close(F);

				$load1 = "<small>nicht gefunden</small>" unless($load1);
				$load5 = "<small>nicht gefunden</small>" unless($load5);
				$load15 = "<small>nicht gefunden</small>" unless($load15);
			}
			if($load =~ m/^.*?up +(\d+?) day[s\)\(\s,]+(\d+):(\d+).+?/i){
	  			$updays = $1;
				$upstd = $2;
				$upmin = $3;
			}elsif($load =~ m/^.*?up +(\d+?) day[s\)\(\s,]+(\d+):(\d+).+?/i){
	  			$updays = $1;
				$upstd = $2;
				$upmin = $3;
			}elsif($load =~ m/^.*?up +(\d+):(\d+).+?/i){
				$updays = "0";
				$upstd = $1;
				$upmin = $2;
			}elsif($load =~ m/^.*?up +(\d+) day[s\)\(\s,]+(\d+).+?/i){
				$updays = $1;
				$upstd = "0";
				$upmin = $2;
			}elsif($load =~ m/^.*?up +(\d+).+?/){
				$updays = "0";
				$upstd = "0";
				$upmin = $1;
			}else{
				open(uptime,"/proc/uptime");
				$buffer = <uptime>;
				close(uptime);
				@list = split(/\s+/, $buffer);
				$ticks = sprintf("%.0u",(split(/\./,$list[0]))[0]);
				$mins  = $ticks / 60;
				$mins  = sprintf("%.0u", $mins); 
				$hours = $mins / 60;
				$hours = sprintf("%.0u", $hours); 
				$days  = ($hours / 24);
				$updays  = sprintf("%.0u", $days);
				$hours = $hours - ($days * 24);
				$upstd = sprintf("%.0u", $hours);
				$upmin  = $mins - ($days * 60 * 24) - ($hours * 60);
				if(!$upstd && $upmin && $updays){
					$upstd = "0";
				}elsif(!$upstd){
					$upstd = "?"
				}

				if(!$upmin && $upstd && $updays){
					$upmin = "0";
				}elsif(!$upmin){
					$upmin = "?"
				}

				if($upmin && $upstd && !$updays){
					$updays = "0";
				}elsif(!$updays){
					$updays = "?"
				}
			}

			foreach $apachepfad (@apache){
				foreach (@standard){
					if(-e("$apachepfad/$_")){
						$output .= "Module '$_' installed<br>\n";
						$apachelib = $apachepfad unless($apachelib);
					}
				}
			}
			$output .= "<br>\n";
			$apachelib = "<small>nicht gefunden</small>" unless($apachelib);
		}else{
			foreach $apachepfad (@apache){
				foreach (@standard){
					if(-e("$apachepfad/$_")){
						$output .= "Module '$_' installed<br>\n";
						$apachelib = $apachepfad unless($apachelib);
					}
				}
			}
			$output .= "<br>\n";
			$apachelib = "<small>nicht gefunden</small>" unless($apachelib);

			$ENV{'PATH'} = "C:/Perl/bin/;C:/WINNT/system32;C:/WINNT" unless($ENV{'PATH'});
			@pathsearch = split(/\;/,$ENV{'PATH'});
			foreach $befehl ("httpd","httpd2","perl","grep","date","whois","tar","gzip","gunzip","ping","nslookup","finger","dnsquery","pgp","gpg","fly","idn","convert","compress","tracert","sendmail","postfix"){
				foreach (@pathsearch){
					if(-e("$_/$befehl" . ".exe")){
						$_ =~ s/\\/\//g;
						$info{$befehl} = "$_/$befehl" . ".exe";
					}elsif(-e("$_/$befehl" . ".com")){
						$_ =~ s/\\/\//g;
						$info{$befehl} = "$_/$befehl" . ".com";
					}
				}

				$info{$befehl} =~ s/^$befehl:\s*//g;
				$info{$befehl} =~ s/^(.+?) .*/$1/sg;
				$info{$befehl} = "<small>nicht installiert</small>" unless($info{$befehl});
			}
			unless($sm){
				$info{'sendmail'} =~ s/\n/<br>/g;
				$sm .= $info{'sendmail'} . "<br>";
				$info{'postfix'} =~ s/\n/<br>/g;
				$sm .= $info{'postfix'};
			}
			$traceit = 'tracert';

			if($mod_w32){
				$ticks = Win32::GetTickCount();
				$updays = int($ticks/86400000);
				$upstd  = int(($ticks = ($ticks - $updays*86400000)) /3600000);
				$upmin  = int(($ticks = ($ticks - $upstd*3600000)) /60000);
			}

			if($mod_w32ole){
				$WMI = Win32::OLE->GetObject("winmgmts:{impersonationLevel=impersonate}\\\\.\\Root\\cimv2");
				($Proc) = ( sort {lc $a->{Name} cmp lc $b->{Name}} in( $WMI->InstancesOf( "Win32_OperatingSystem" ) ) );
				$ver = $Proc->{Version};
				if($Proc->{ServicePackMajorVersion} > 0){
					$ver .= " SP" . $Proc->{ServicePackMajorVersion};
				}
				$ver = "($ver)<br>$Proc->{Caption}";
				$useron = $Proc->{NumberOfUsers};
			}
		}
		$ENV{'REMOTE_HOST'} = gethostbyaddr(inet_aton($ENV{'REMOTE_ADDR'}), AF_INET);

		foreach (sort keys %ENV) {
			$ENV{$_} =~ s/\\/\//g;
			if($_ eq "DOCUMENT_ROOT" || $_ eq "PWD" || $_ eq "SCRIPT_FILENAME"){
				$w = "<b>$_</b>";
			}elsif($_ eq "PATH"){
				$w = $_;
				if ($^O =~ /win/i){
					$ENV{$_} =~ s/\;/<br>/g;
				}else{
					$ENV{$_} =~ s/\:/<br>/g;
				}
			}elsif($_ eq "HTTP_ACCEPT"){
				$w = $_;
				$ENV{$_} =~ s/\,/<br>/g;
			}elsif($_ eq "HTTP_COOKIE"){
				$w = $_;
				foreach $s (split(/; /,$ENV{$_})){
					$s =~ s/(.{50})/$1<br>\n/g;
					$http_cookie .= $s . "; ";
				}
				$ENV{'HTTP_COOKIE'} = $http_cookie;
			}else{
				$w = $_;
			}

			$env_a .= qq~<tr><td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">$w</font></td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$ENV{$_}</font></td></tr>~;
		}

		foreach (sort { lc($a) cmp lc($b)} @INC){
			chomp;
			$mv .= $_ . "<br>" if($_ ne ".");
		}

		if($mod_w32 == 1 && $^O =~ /win/i){
			@os = Win32::GetOSVersion;
			$ver = "(Version: $os[1]\.$os[2] Build $os[3])" unless($ver);
		}else{
			if(-e("/proc/version")){
				open (F,"</proc/version");
				$data = (<F>)[0];
				close (F);

				$kernel = (split(/\ /,$data))[2];
				$kernel .= " (SMP)" if($data =~ /smp/);
			}
			$kernel = "Unbekannt" unless($kernel);

			foreach ("/etc/debian_version","/etc/SuSE-release","/etc/mandrake-release","/etc/fedora-release","/etc/redhat-release","/etc/gentoo-release","/etc/slackware-version","/etc/eos-version","/etc/trustix-release","/etc/arch-release"){
				if(-e("$_")){
					open(F,"$_");
					$kernel2 = (<F>)[0];
					close(F);
					if($_ =~ /Debian/){
						$kernel2 = "Debian " . $kernel2;
					}
				}
			}

			if($kernel2){
				$ver = "(Kernel: $kernel)<br>$kernel2";
			}else{
				$ver = "(Kernel: $kernel)";
			}
		}

		if(-e("/proc/sys/kernel/hostname")){
			open(F,"/proc/sys/kernel/hostname");
			$h_a = (<F>)[0];
			close(F);
		}
		$sysname .= ", $hostuname" if($sysname ne $hostuname);
		$sysname .= ", $h_a" if($sysname ne $h_a);

		$ipadresse = $ENV{'SERVER_ADDR'};
		unless($ipadresse){
			$ipadresse = $ENV{'SERVER_NAME'};
		}

		$hostip = gethostbyaddr(inet_aton($ipadresse), AF_INET) . ", $gethost, $sysname";
		$hostip =~ s/[\n\r]//g;

		foreach (split(/\,\s+/,$hostip)){
			$hostipnew{$_} = 1;
		}
		$hostip = join(", ",sort keys %hostipnew);

		unless($httpd){
			$httpd = "-" . $Config{"cc"} . " " . $Config{"ccflags"} . " " . $Config{"optimize"} . " " . $Config{"cppflags"};
		}

		if($Config{"useithreads"} eq "define"){
			$threads = "erlaubt";
		}else{
			$threads = "verboten";
		}

		$liblist = $Config{"libs"}." ".$Config{"perllibs"};
		foreach (split / /,$liblist){$lib .= $_.' '};
		$info{'perl'} =~ s/\/\//\//g;
	}

$ausgabe =qq~
<table cellpadding="4" cellspacing="1" border="0">
	<td valign="top" align="left">
		<table cellpadding="3" cellspacing="1" border="0">
			<tr>
				<td bgcolor="#bcbcEE" colspan="2"><font face="Verdana,Arial" size="2" size="3"><b>Server - Infos:</b></font> <font face="Verdana,Arial" size="1">(Threads: $threads)</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Betriebssystem:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$^O $ver</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Perl Version:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$]</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Hostname:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$hostip</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">IP Adresse:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$ipadresse</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">IDs:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$userid</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Internet-Zeit:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">\@$beats</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Lokale Uhrzeit:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$ltime</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">GMT Uhrzeit:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$gtime</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Perl zuletzt ge&auml;ndert:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Config{"cf_time"}</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Server aktiv seit:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$updays Tage, $upstd Stunden, $upmin Minuten</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Eingeloggte User:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$useron</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">CPU Auslastung:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><iframe width="55" height="15" frameborder="0" scrolling="no" marginheight="0px" marginwidth="0px" src="sysinfo.$cgiORpl?pass=$pass&action=cpulast"></iframe><br></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" colspan="2"><font face="Verdana,Arial" size="2"><b>Durchschnittliche Serverlast vor:</b></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">01 Minuten:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$load1</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">05 Minuten:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$load5</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">15 Minuten:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$load15</font></td>
			</tr>
		</table>
	</td>
	<td valign="top" align="left">
	<form action="sysinfo.$cgiORpl" target="module" method="get"><input type="hidden" name="action" value="perlmodule"><input type="hidden" name="pass" value="$pass">
	<font face="Verdana,Arial" size="2">Suchen nach: <input type="text" name="suchwort" size="15"> <input type="submit" value="OK"> &nbsp; <a href="sysinfo.$cgiORpl?pass=$pass&action=perlmodule" target="module"><font color="blue">[alle&nbsp;anzeigen]</font></a> <a href="sysinfo.$cgiORpl?pass=$pass&cache=1&action=perlmodule" target="module"><font color="blue">[cache erneuern]</font></a></font><br>
	<iframe name="module" width="500" height="440" frameborder="0" scrolling="yes" marginheight="0px" marginwidth="0px" src="sysinfo.$cgiORpl?pass=$pass&action=perlmodule"></iframe>
	</form>
	</td>
</table>

<br><br>
<table cellpadding="4" cellspacing="1" border="0" width="750">
	<td valign="top" align="left">
		<table cellpadding="3" cellspacing="1" border="0">
			<tr>
				<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2" size="3"><b>Allgemeine Pfade:</b></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Pfad zu Perl:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=perl" target="_blank"><font color="black">$info{'perl'}</font></a></font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">ImageMagick convert:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=convert" target="_blank"><font color="black">$info{'convert'}</font></a></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Grep:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=grep" target="_blank"><font color="black">$info{'grep'}</font></a></font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Date:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=date" target="_blank"><font color="black">$info{'date'}</font></a></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Whois:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=whois" target="_blank"><font color="black">$info{'whois'}</font></a></font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Ping:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=ping" target="_blank"><font color="black">$info{'ping'}</font></a></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Nslookup:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=nslookup" target="_blank"><font color="black">$info{'nslookup'}</font></a></font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Finger:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=finger" target="_blank"><font color="black">$info{'finger'}</font></a></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Traceroute:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=$traceit" target="_blank"><font color="black">$info{$traceit}</font></a></font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Dnsquery:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=dnsquery" target="_blank"><font color="black">$info{'dnsquery'}</font></a></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Tar:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=tar" target="_blank"><font color="black">$info{'tar'}</font></a></font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Compress:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=compress" target="_blank"><font color="black">$info{'compress'}</font></a></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Gzip:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=gzip" target="_blank"><font color="black">$info{'gzip'}</font></a></font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Gunzip:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=gunzip" target="_blank"><font color="black">$info{'gunzip'}</font></a></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">PGP:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=pgp" target="_blank"><font color="black">$info{'pgp'}</font></a></font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">GPG:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=gpg" target="_blank"><font color="black">$info{'gpg'}</font></a></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Fly:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=fly" target="_blank"><font color="black">$info{'fly'}</font></a></font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">IDN:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=systeminf&name=idn" target="_blank"><font color="black">$info{'idn'}</font></a></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Apache Lib:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$apachelib</font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">eingebundene Libs:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$lib</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Apache modules installed:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$output</font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Compiled-In Module:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$httpd</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Modul-Verz. (\@INC):</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$mv</font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Sendmail:</font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$sm</font></td>
			</tr>
		</table>
	</td>
	<td valign="top" align="left">
		<form action="sysinfo.$cgiORpl" target="mimetype" method="get"><input type="hidden" name="action" value="mimetype"><input type="hidden" name="pass" value="$pass">
		<font face="Verdana,Arial" size="2">Suchen nach: <input type="text" name="suchwort" size="15"> <input type="submit" value="OK"> &nbsp; <a href="sysinfo.$cgiORpl?pass=$pass&action=mimetype" target="mimetype"><font color="blue">[alle&nbsp;anzeigen]</font></a></font><br>
		<iframe name="mimetype" width="400" height="400" frameborder="0" scrolling="yes" marginheight="0px" marginwidth="0px" src="sysinfo.$cgiORpl?pass=$pass&action=mimetype"></iframe>
		</form><br>

		<form action="sysinfo.$cgiORpl" target="signal" method="get"><input type="hidden" name="action" value="signal"><input type="hidden" name="pass" value="$pass">
		<font face="Verdana,Arial" size="2">Suchen nach: <input type="text" name="suchwort" size="15"> <input type="submit" value="OK"> &nbsp; <a href="sysinfo.$cgiORpl?pass=$pass&action=signal" target="signal"><font color="blue">[alle&nbsp;anzeigen]</font></a></font><br>
		<iframe name="signal" width="400" height="220" frameborder="0" scrolling="yes" marginheight="0px" marginwidth="0px" src="sysinfo.$cgiORpl?pass=$pass&action=signal"></iframe>
		</form>
	</td>
</table>

<br><br>

<table cellpadding="4" cellspacing="1" border="0">
	<td valign="top" align="left">
		<table cellpadding="3" cellspacing="1" border="0">
		<tr><td bgcolor="#bcbcEE" colspan="2"><font face="Verdana,Arial" size="2" size="3"><b>Umgebungsvariablen (\%ENV)</b></font></td></tr>
		$env_a
		</table>
	</td>

	<td valign="top" align="right">
		<iframe name="lastlog" width="400" height="365" frameborder="0" scrolling="yes" marginheight="0px" marginwidth="0px" src="sysinfo.$cgiORpl?pass=$pass&action=lastlog"></iframe><br><br>
		<iframe name="ports" width="400" height="420" frameborder="0" scrolling="yes" marginheight="0px" marginwidth="0px" src="sysinfo.$cgiORpl?pass=$pass&action=ports"></iframe>
	</td>
</table>
~;
	&ausgabe($ausgabe);
}

sub system {
	if($systemON){
		if($^O !~ /win/i){
			foreach(split(/\n/,&command("ps -Aelfwww"))){
				chomp;
				@ps_fields = split(/\s+/,$_,15);
				if($ps_fields[5] != 0){
					$jlsp_a .= qq~<tr><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$ps_fields[5]</font></td>
							<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$ps_fields[2]</font></td>
							<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$ps_fields[9]</font></td>
							<td bgcolor="#eeeeee"><font face=Verdana,Arial size=2><a href="sysinfo.$cgiORpl?pass=$pass&action=pid&name=$ps_fields[3]" target="_blank"><u>$ps_fields[3]</u></a></font></td>
							<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$ps_fields[13]</font></td>
							<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">~;

					$jlsp_a .= "<input type=\"text\" value=\"$ps_fields[14]\" size=\"55\">";
					$jlsp_a .= qq~</font></td></tr>~;
				}
			}

			foreach (split(/\n/,&command("w -h"))){
				($Wuser,$Wtty,$Wfrom,$Wlogin,$Widle,$Wjcpu,$Wpcpu,$Wwhat) = split(/\s+/);
				$top_a .= qq~<tr>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Wuser</font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Wtty</font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Wfrom</font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Wlogin</font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Widle</font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Wjcpu</font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Wpcpu</font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Wwhat</font></td></tr>~;
			}

			foreach (split(/\n/,&command("pstree -lpuc"))){
				s/\s\s/&nbsp; /g;
				s/\((\d+)/\(<a href="sysinfo.$cgiORpl?pass=$pass&action=pid&name=$1" target="_blank"><u>$1<\/u><\/a>/g;
				$pstree_a .= qq~<tr><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$_</font></td></tr>~;
			}

	#
	# Speicher anfang
	#
			open(F,"</proc/meminfo"); # Alternativ Befehl: "free"
			@meminfo = <F>;
			close(F);

			$phy = (grep(/Mem:/,@meminfo))[0];
			$swap = (grep(/Swap:/,@meminfo))[0];

			if(!$phy && !$swap){
				@meminfo = split(/\n/,&command("free"));
				$phy = (grep(/Mem:/,@meminfo))[0];
				$swap = (grep(/Swap:/,@meminfo))[0];
				$freecommand = 1;
			}
			$phy =~ s/\s+/ /g;
			$swap =~ s/\s+/ /g;
			($phyName, $phyTotal, $phyUsed, $phyFree, $phyShared, $phyBuffers, $phyCached) = split(/ /,$phy);

			$REALphyUsed = $phyUsed - $phyCached - $phyBuffers;
			$REALphyFree = $phyFree + $phyCached + $phyBuffers;
			if($REALphyUsed && $phyTotal){
				$REALphyPercent = sprintf("%.0f",($REALphyUsed / $phyTotal) * 100);
			}else{
				$REALphyPercent = "0";
			}

			if($phyUsed && $phyTotal){
				$phyPercent = sprintf("%.0f",($phyUsed / $phyTotal) * 100);
			}else{
				$phyPercent = "0";
			}

			($swapName, $swapTotal, $swapUsed, $swapFree) = split / /, $swap, 4;
			if($swapUsed && $swapTotal){
				$swapPercent = sprintf("%.0f",($swapUsed / $swapTotal) * 100);
			}else{
				$swapPercent = "0";
			}

			$totalTotal = $phyTotal + $swapTotal;
			$totalUsed = $phyUsed + $swapUsed;
			$totalFree = $phyFree + $swapFree;
			if($totalUsed && $totalTotal){
				$totalPercent = sprintf("%.0f", ( $totalUsed / $totalTotal ) * 100);
			}else{
				$totalPercent = "0";
			}

			if($freecommand){
				$phyUsed = berechnen($phyUsed * 1024);
				$phyFree = berechnen($phyFree * 1024);
				$phyTotal = berechnen($phyTotal * 1024);

				$swapUsed = berechnen($swapUsed * 1024);
				$swapFree = berechnen($swapFree * 1024);
				$swapTotal = berechnen($swapTotal * 1024);

				$totalUsed = berechnen($totalUsed * 1024);
				$totalFree = berechnen($totalFree * 1024);
				$totalTotal = berechnen($totalTotal * 1024);
			}else{
				$phyUsed = berechnen($phyUsed);
				$phyFree = berechnen($phyFree);
				$phyTotal = berechnen($phyTotal);

				$swapUsed = berechnen($swapUsed);
				$swapFree = berechnen($swapFree);
				$swapTotal = berechnen($swapTotal);

				$totalUsed = berechnen($totalUsed);
				$totalFree = berechnen($totalFree);
				$totalTotal = berechnen($totalTotal);
			}

			if($phyPercent > 90){
				$breit = ($phyPercent - $REALphyPercent) * 2;
				$REALbreit = $REALphyPercent * 2;
	#			$phycap = qq~<table border="0" cellspacing="0" cellpadding="1"><td width="$REALbreit" height="8" bgcolor="red" align="right"><font color="white" face="Arial,Verdana">$REALphyPercent\%</font></td><td width="$breit" height="8" bgcolor="#FF6666">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $phyPercent\%</font></td></table>~;
				$phycap = qq~<table border="0" cellspacing="0" cellpadding="1"><td width="$REALbreit" height="8" bgcolor="red" align="right">&nbsp;</td><td width="$breit" height="8" bgcolor="#FF6666">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $phyPercent\%</font></td></table>~;
			}else{
				$breit = ($phyPercent - $REALphyPercent) * 2;
				$REALbreit = $REALphyPercent * 2;
	#			$phycap = qq~<table border="0" cellspacing="0" cellpadding="1"><td width="$REALbreit" height="8" bgcolor="green" align="right"><font color="white" face="Arial,Verdana">$REALphyPercent\%</font></td><td width="$breit" height="8" bgcolor="#66FF66">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $phyPercent\%</font></td></table>~;
				$phycap = qq~<table border="0" cellspacing="0" cellpadding="1"><td width="$REALbreit" height="8" bgcolor="green" align="right">&nbsp;</td><td width="$breit" height="8" bgcolor="#66FF66">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="green">&nbsp;&nbsp; $phyPercent\%</font></td></table>~;
			}

			$n_a .= qq~<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Physical Memory: </font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$phycap</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$phyFree</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$phyUsed</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$phyTotal</font></td>
			</tr>~;

			$breit = $swapPercent * 2;
			if($swapPercent > 90){
				$swapcap = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$breit" height="8" bgcolor="red">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $swapPercent\%</font></td></table>~;
			}else{
				$swapcap = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$breit" height="8" bgcolor="green">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="green">&nbsp;&nbsp; $swapPercent\%</font></td></table>~;
			}


			$breit = $totalPercent * 2;
			if($totalPercent > 90){
				$totalcap = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$breit" height="8" bgcolor="red">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $totalPercent\%</font></td></table>~;
			}else{
				$totalcap = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$breit" height="8" bgcolor="green">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="green">&nbsp;&nbsp; $totalPercent\%</font></td></table>~;
			}

			$n_a .= qq~<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">DiskSwap: </font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$swapcap</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$swapFree</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$swapUsed</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$swapTotal</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Gesamt: </font></td>
				<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$totalcap</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$totalFree</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$totalUsed</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$totalTotal</font></td>
			</tr>~;
	#
	# Speicher end
	#
			if(-e("/proc/cpuinfo")){
				open(F,"/proc/cpuinfo");
				while(<F>){
					chomp;
					($name,$inhalt) = split(/\s+:\s+/);
					if($name =~ /processor|ncpus probed/){
	#					$processor = $inhalt;
						$processor++;
					}elsif($name =~ /cpus detected/){
						$processor++;
					}elsif($name =~ /platform string|system type|model name|cpu model|revision/i){
						if($model){
							$model .= ", " . $inhalt;
						}else{
							$model = $inhalt;
						}
					}elsif($name =~ /Cpu0ClkTck|cpu MHz|clock|cycle frequency/){
						if($cpu){
							$inhalt =~ s/\s//g;
							$cpu .= ", " . sprintf("%.2f",$inhalt);
						}else{
							$inhalt =~ s/\s//g;
							$cpu = sprintf("%.2f",$inhalt);
						}
					}elsif($name =~ /cache size|L2 cache/){
						if($cachegroesse){
							$cachegroesse .= ", " . $inhalt;
						}else{
							$cachegroesse = $inhalt;
						}
					}elsif($name =~ /bogomips|Cpu0Bogo/i){
						if($bogomips){
							$bogomips .= ", " . $inhalt;
						}else{
							$bogomips = $inhalt;
						}
					}
				}
				close(F);
			}
			$machine = &command("uname -m");

			$floppy = 0;
			open(F,"</etc/fstab");
			while(<F>){
				if(/\/dev\/fd0/i && /\/dev\/fd1/i){
					$floppy = 2;
				}elsif(/\/dev\/fd0/i or /\/dev\/fd1/i){
					$floppy = 1;
				}
			}
			close(F);

	#
	# PCI/SCSI anfang
	#
			open(F,"</proc/pci");
			while(<F>){
				if(/ISA|IDE|Ethernet|SBUS|AGP|VGA|Controller|Interface|Bridge/i){
					$pci_a .= (split(/\s*:\s*/))[1] . "<br>";
				}elsif(/USB/i){
					$usb_a .= (split(/\s*:\s*/))[1] . "<br>";
				}
			}
			close(F);

			opendir(V,"/proc/ide");
			foreach (grep(/hd/,readdir(V))){
					open(F,"</proc/ide/$_/model");
					$modelide = (<F>)[0];
					close(F);

					open(F,"</proc/ide/$_/capacity");
					$capacity = (<F>)[0];
					close(F);
					chomp $capacity;

					if($capacity){
						$capacity = berechnen($capacity / 2 * 1024);
				        	$ide_a .= qq~$modelide ($capacity)<br>~;
					}else{
				        	$ide_a .= qq~$modelide<br>~;
					}
			}
			closedir(V);

			open(F,"</proc/scsi/scsi");
			foreach (<F>){
			        if(/Vendor|Model|Rev/){
					$scsi_a .= (split(/: /))[1] . ": " . (split(/: /,((split(/: /))[2])))[0] . " ( Rev: " . (split(/: /))[3] . " )<br>";
			        }
			}
			close(F);
			$scsi_a = "none" unless($scsi_a);
			$ide_a = "none" unless($ide_a);
			$pci_a = "none" unless($pci_a);
			$usb_a = "none" unless($usb_a);
	#
	# PCI/SCSI end
	#

	#
	# Network start
	#

			open(F,"</proc/net/dev");
			@network = grep(/:/,split(/\n/,join("",<F>)));
			close(F);

			foreach (@network){
				($NETWORKname,$NETWORKlist) = split(/:/,$_,2);
				$NETWORKlist =~ s/^\s+//;
				($rBytes, $rPackets, $rErrs, $rDrop, $rFifo, $rFrame, $rCompressed, $rMulticast, $tBytes, $tPackets, $tErrs, $tDrop, $tFifo, $tColls, $tCarrier, $tCompressed) = split(/\s+/,$NETWORKlist); 

				$rDrop += $tDrop;
				$rError += $tError;
				$allError += $rError;
				$allDrop += $rDrop;
				$allrBytes += $rBytes;
				$alltBytes += $tBytes;
				$rBytes = berechnen($rBytes);
				$tBytes = berechnen($tBytes);
				$net_a .= qq~<tr>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$NETWORKname</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$rBytes</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$tBytes</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$rDrop/$rError</font></td></tr>~;
			}
			$allrBytes = berechnen($allrBytes);
			$alltBytes = berechnen($alltBytes);
			$net_a .= qq~<tr>
			<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">Gesamt</font></td>
			<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$allrBytes</font></td>
			<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$alltBytes</font></td>
			<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$allDrop/$allError</font></td></tr>~;
	#
	# Network end
	#
			@df = split(/\n/,&command("df -TPa"));
			if($df[0]){
				shift @df;
				foreach (@df) {
					($dev, $systemtyp, $size, $used, $avail, $capacity, $mount) = split(/\s+/);
					$capacity =~ s/%//;
					if($capacity > 0 or $capacity ne "-"){
						$capacity2 = $capacity;
					}else{
						$capacity = "0";
						$capacity2 = "0";
					}
					$capacity2 = $capacity;
					if($capacity){
						$capacity3 = $capacity * 3;
					}else{
						$capacity3 = "0";
					}

					if($capacity > 90) {
						$picture = qq~<table border="0" cellspacing="0" cellpadding="0">
								<td width="$capacity3" height="7" bgcolor="red">&nbsp;</td>
								<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $capacity\%</font></td>
								</table>~;
					}else{
						$picture = qq~<table border="0" cellspacing="0" cellpadding="0">
								<td width="$capacity3" height="7" bgcolor="green">&nbsp;</td>
								<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="green">&nbsp;&nbsp; $capacity\%</font></td>
								</table>~;
					}

					$allavail += $avail;
					$allused += $used;
					$allsize += $size;
					$avail = berechnen($avail * 1024);
					$used = berechnen($used * 1024);
					$size = berechnen($size * 1024);
					$allzahl++;

					$mount_a .= "<tr><td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$mount</font></td>
							<td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$systemtyp</font></td>
							<td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$dev</font></td>
							<td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$picture</font></td>
							<td bgcolor=#eeeeee align=right><font face=Verdana,Arial size=2>$avail</font></td>
							<td bgcolor=#eeeeee align=right><font face=Verdana,Arial size=2>$used</font></td>
							<td bgcolor=#eeeeee align=right><font face=Verdana,Arial size=2>$size</font></td></tr>";
				}
					if($allused && $allavail){
						$allcapacity = sprintf("%.0f",($allused / $allsize) * 100);
					}else{
						$allcapacity = "0";
					}
					if($allcapacity){
						$allcapacity3 = $allcapacity * 3;
					}else{
						$allcapacity3 = "0";
					}
					if($allcapacity > 90) {
						$picture = qq~<table border="0" cellspacing="0" cellpadding="0">
								<td width="$allcapacity3" height="7" bgcolor="red">&nbsp;</td>
								<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $allcapacity\%</font></td>
								</table>~;
					}else{
						$picture = qq~<table border="0" cellspacing="0" cellpadding="0">
								<td width="$allcapacity3" height="7" bgcolor="green">&nbsp;</td>
								<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="green">&nbsp;&nbsp; $allcapacity\%</font></td>
								</table>~;
					}
					$allavail = berechnen($allavail * 1024);
					$allused = berechnen($allused * 1024);
					$allsize = berechnen($allsize * 1024);

					$mount_a .= "<tr><td bgcolor=#ddddFF colspan=3 align=right><font face=arial,verdana size=2><b>Gesamt:</b></font></td>
							<td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$picture</font></td>
							<td bgcolor=#eeeeee align=right><font face=Verdana,Arial size=2>$allavail</font></td>
							<td bgcolor=#eeeeee align=right><font face=Verdana,Arial size=2>$allused</font></td>
							<td bgcolor=#eeeeee align=right><font face=Verdana,Arial size=2>$allsize</font></td></tr>";
				$mount_a .= "</table><br>\n";
			}else{
				open(F, "</etc/mtab");
				@fstab = <F>;
				close(F);

				unless($fstab[0]){
					open(F,"</proc/mounts");
					@fstab = <F>;
					close(F);
				}
				unless($fstab[0]){
					open(F,"</etc/fstab");
					@fstab = <F>;
					close(F);
				}

				foreach $line (@fstab){
					$two2 =~ s/\ \ /\ /g;
					@line = split(/\s+/, $line);
					$mount_a .= qq~<tr><td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$line[1]</font></td><td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$line[2]</font></td><td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$line[0]</font></td><td bgcolor=#eeeeee align=right>&nbsp;</td><td bgcolor=#eeeeee align=right>&nbsp;</td><td bgcolor=#eeeeee align=right>&nbsp;</td><td bgcolor=#eeeeee align=right>&nbsp;</td></tr>~;
				}
			}

	#
	# Prozesse anfang
	#
			@ps_info = split(/\n/,&command("ps eaxSuhwww | sort -n +0"));
			foreach (@ps_info){
				@psfeld = split(/\s+/);
				if($second eq "eeeeee"){
					$second = "e6e6e6";
				}else{
					$second = "eeeeee";
				}
				$pro2_a .= qq~<tr><td bgcolor=$second><font face=Verdana,Arial size=2>$psfeld[0]</font></td>
					<td bgcolor=$second><font face=Verdana,Arial size=2><a href="sysinfo.$cgiORpl?pass=$pass&action=pid&name=$psfeld[1]" target="_blank"><u>$psfeld[1]</u></a></font></td>
					<td bgcolor=$second><font face=Verdana,Arial size=2>$psfeld[2]\%</font></td>
					<td bgcolor=$second><font face=Verdana,Arial size=2>$psfeld[3]\%</font></td>
					<td bgcolor=$second align=\"right\"><font face=Verdana,Arial size=2>~;
				$pro2_a .= &berechnen($psfeld[4] * 1024);
				$pro2_a .= qq~</font></td>
					<td bgcolor=$second><font face=Verdana,Arial size=2>$psfeld[6]</font></td>
					<td bgcolor=$second><font face=Verdana,Arial size=2>$psfeld[7]</font></td>
					<td bgcolor=$second><font face=Verdana,Arial size=2>$psfeld[8]</font></td>
					<td bgcolor=$second><font face=Verdana,Arial size=2>$psfeld[9]</font></td>
					<td bgcolor=$second><input type=\"text\" size=\"35\" value=\"~;

				for($i=10;$i<@psfeld;$i++){
					$psfeld[$i] =~ s/"/&quot;/g;
					$pro2_a .= " " . $psfeld[$i];
				}
				$pro2_a .= "\"></td></tr>";
			}
	#
	# Prozesse end
	#
			$hardware2[1] =~ s/ /\&nbsp\;/g;
			$pci_a =~ s/ /\&nbsp\;/g;
		}else{
			if($mod_w32s){
				Win32::API::Struct->typedef( MEMORYSTATUS => qw{
				   DWORD dwLength;
				   DWORD MemLoad;
				   DWORD TotalPhys;
				   DWORD AvailPhys;
				   DWORD TotalPage;
				   DWORD AvailPage;
				   DWORD TotalVirtual;
				   DWORD AvailVirtual;
				});
				Win32::API->Import('kernel32', 'VOID GlobalMemoryStatus(LPMEMORYSTATUS lpMemoryStatus)');

				$memorystatus = Win32::API::Struct->new('MEMORYSTATUS');
				GlobalMemoryStatus($memorystatus);
				#MemLoad TotalPhys AvailPhys TotalPage AvailPage TotalVirtual AvailVirtual

				$swapfree = sprintf("%.0f", $memorystatus->{'AvailPage'}/(1024*1024));
				$swaptotal = sprintf("%.0f", $memorystatus->{'TotalPage'}/(1024*1024));
				$memoryfree = sprintf("%.0f", $memorystatus->{'AvailPhys'}/(1024*1024));
				$memorytotal = sprintf("%.0f", $memorystatus->{'TotalPhys'}/(1024*1024));

				$memoryblock = $memorytotal - $memoryfree;
				if($memoryblock && $memorytotal){
					$cap = sprintf("%.2f", $memoryblock / $memorytotal * 100);
				}else{
					$cap = sprintf("%.2f", $memoryblock / $memorytotal * 100);
				}

				$breit = $cap * 2;
				$cap2 = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$breit" height="8" bgcolor="green">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="green">&nbsp;&nbsp; $cap\%</font></td></table>~;
				if ($cap > 90){
					$cap2 = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$breit" height="8" bgcolor="red">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $cap\%</font></td></table>~;
				}

				$memoryfree = &berechnen($memoryfree * (1024*1024));
				$memoryblock = &berechnen($memoryblock * (1024*1024));
				$memorytotal = &berechnen($memorytotal * (1024*1024));
				$n_a .= qq~<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Physical Memory:</font></td>
					<td bgcolor="#eeeeee">$cap2</td>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$memoryfree</font></td>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$memoryblock</font></td>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$memorytotal</font></td>
				</tr>~;

				$swapblock = $swaptotal - $swapfree;
				$cap = sprintf("%.2f", $swapblock / $swaptotal * 100);

				$breit = $cap * 2;
				$cap2 = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$breit" height="8" bgcolor="green">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="green">&nbsp;&nbsp; $cap\%</font></td></table>~;
				if ($cap > 90){
					$cap2 = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$breit" height="8" bgcolor="red">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $cap\%</font></td></table>~;
				}

				$swapfree = &berechnen($swapfree * (1024*1024));
				$swapblock = &berechnen($swapblock * (1024*1024));
				$swaptotal = &berechnen($swaptotal * (1024*1024));
				$n_a .= qq~<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">DiskSwap:</font></td>
					<td bgcolor="#eeeeee">$cap2</td>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$swapfree</font></td>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$swapblock</font></td>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$swaptotal</font></td>
				</tr>~;

				$wert = chr(0);
				$getBuffer = $wert x 64;
				$GetLogicalDrives = new Win32::API("kernel32","GetLogicalDriveStrings", NP, N);
				$GetLogicalDrives = $GetLogicalDrives->Call(64, $getBuffer);
				@laufwerke = split(/$wert/,$getBuffer);

				@typ = ("Unbekannt","Unbekannt","Diskette","Festplatte","Netzlaufwerk","CD-ROM","RAM-Disk");

				foreach $x (@laufwerke){ # WMI: Win32_LogicalDisk (Win32_LogicalDisk)
					$GetDriveType = new Win32::API("kernel32","GetDriveType", P, N);
					$GetDriveType = $GetDriveType->Call($x);

					$GetDiskFreeSpace = new Win32::API("kernel32", "GetDiskFreeSpace" , [P, P, P, P, P], N);
					$getBuffer = $x;

					$lpSectsPerCluster = pack("L", 0);
					$lpBytesPerSect = pack("L", 0);
					$lpNumOfFreeClusters = pack("L", 0);
					$lpTotNumOfClusters = pack("L", 0);

					$GetDiskFreeSpace->Call("$getBuffer", $lpSectsPerCluster, $lpBytesPerSect, $lpNumOfFreeClusters, $lpTotNumOfClusters);

					($SectsPerCluster) = unpack("L",$lpSectsPerCluster);
					($BytesPerSect) = unpack("L",$lpBytesPerSect);
					($NumOfFreeClusters) = unpack("L",$lpNumOfFreeClusters);
					($TotNumOfClusters) = unpack("L",$lpTotNumOfClusters);

					$TotalDiskSpace = sprintf("%.0f", ($SectsPerCluster * $BytesPerSect * $TotNumOfClusters)/(1024*1024));
					$FreeDiskSpace = sprintf("%.0f", ($SectsPerCluster * $BytesPerSect * $NumOfFreeClusters)/(1024*1024));
					$UsedDiskSpace = sprintf("%.0f", ($SectsPerCluster * $BytesPerSect * ($TotNumOfClusters - $NumOfFreeClusters))/(1024*1024));

					$floppy++ if($typ[$GetDriveType] eq "Diskette");
					push(@df,"$typ[$GetDriveType] $TotalDiskSpace $UsedDiskSpace $FreeDiskSpace $x");
				}

				foreach $line (@df) {
					($dev, $size, $used, $avail, $mount) = split(/\s+/,$line);
					$line =~ s/\s/&nbsp;/g;

					if($avail){
						$block = $size - $avail;
						$capacity = sprintf("%.2f", $block / $size * 100);
						$capacity2 = $capacity;
						$capacity3 = $capacity * 3;
					}else{
						$block = "100";
						$capacity = "100";
						$capacity2 = "100";
						$capacity3 = "100" * 3;
					}

					$picture = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$capacity3" height="8" bgcolor="green">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="green">&nbsp;&nbsp; $capacity\%</font></td></table>~;
					if ($capacity > 90) {
						$picture = qq~<table border="0" cellspacing="0" cellpadding="0"><td width="$capacity3" height="8" bgcolor="red">&nbsp;</td><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2" color="red">&nbsp;&nbsp; $capacity\%</font></td></table>~;
					}

					if($cap > 90){
						$capacity =~ s/$capacity/\<FONT COLOR=red>$capacity2\<\/FONT\>/;
					}else{
						$capacity =~ s/$capacity/\<FONT COLOR=green>$capacity2\<\/FONT\>/;
					}
					$size = &berechnen($size * (1024*1024));
					$used = &berechnen($used * (1024*1024));
					$avail = &berechnen($avail * (1024*1024));
					$mount_a .= qq~<tr><td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$mount</font></td><td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$dev</font></td><td bgcolor=#eeeeee><font face=Verdana,Arial size=2></font></td><td bgcolor=#eeeeee><font face=Verdana,Arial size=2>$picture</font></td><td bgcolor=#eeeeee align=right><font face=Verdana,Arial size=2>$avail</font></td><td bgcolor=#eeeeee align=right><font face=Verdana,Arial size=2>$used</font></td><td bgcolor=#eeeeee align=right><font face=Verdana,Arial size=2>$size</font></td></tr>~;
				}
				$mount_a .= "</table><br>\n";
			}

			if($mod_w32r){
				$::HKEY_LOCAL_MACHINE->Open("Hardware\\Description\\System\\CentralProcessor\\0", $mhz);
	#			$mhz->QueryValueEx("~MHz", $type, $cpu);
	#			$mhz->QueryValueEx("ProcessorNameString", $type, $model);

	#			$::HKEY_LOCAL_MACHINE->Open("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkCards\\1", $networkcard1);
	#			$networkcard1->QueryValueEx("Description", $type, $networkcardfirst);
	#			$pci_a .= $networkcardfirst . "<br>\n";
	#			$::HKEY_LOCAL_MACHINE->Open("SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkCards\\2", $networkcard2);
	#			$networkcard2->QueryValueEx("Description", $type, $networkcardsecond);
	#			$pci_a .= $networkcardsecond . "<br>\n";

	#			$::HKEY_LOCAL_MACHINE->Open("HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 0\\Scsi Bus 0\\Target Id 0\\Logical Unit Id 0", $pci1);
	#			$pci1->QueryValueEx("Identifier", $type, $PCI);
	#			$ide_a .= $PCI . "<br>\n";

	#			$::HKEY_LOCAL_MACHINE->Open("HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 0\\Scsi Bus 0\\Target Id 1\\Logical Unit Id 0", $pci2);
	#			$pci2->QueryValueEx("Identifier", $type, $PCI2);
	#			$ide_a .= $PCI2 . "<br>\n";

	#			$::HKEY_LOCAL_MACHINE->Open("HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 1\\Scsi Bus 0\\Target Id 0\\Logical Unit Id 0", $pci3);
	#			$pci3->QueryValueEx("Identifier", $type, $PCI3);
	#			$ide_a .= $PCI3 . "<br>\n";

	#			$::HKEY_LOCAL_MACHINE->Open("HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 1\\Scsi Bus 0\\Target Id 1\\Logical Unit Id 0", $pci4);
	#			$pci4->QueryValueEx("Identifier", $type, $PCI4);
	#			$ide_a .= $PCI4 . "<br>\n";
			}

			if($mod_w32ole){
	#			use Win32::OLE qw( in );
				$WMI = Win32::OLE->GetObject("winmgmts:{impersonationLevel=impersonate}\\\\.\\Root\\cimv2");
				foreach my $Proc ( sort {lc $a->{Name} cmp lc $b->{Name}} in( $WMI->InstancesOf( "Win32_Process" ) ) ){
					push(@topo,$Proc->{ProcessID} . " $Proc->{Name} <font size=\"1\">($Proc->{ExecutablePath})</font><br>");
				}

	#			foreach (sort {$a <=> $b} @topo){
	#				s/\s\s/&nbsp; /g;
	#				$pstree_a .= qq~<tr><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$_</font></td></tr>~;
	#			}

				foreach my $Proc ( sort {lc $a->{Name} cmp lc $b->{Name}} in( $WMI->InstancesOf( "Win32_PnPEntity" ) ) ){
					next if($PnPEntity{$Proc->{Name}});
					if($Proc->{PNPDeviceID} =~ /^PCI\\/i){
						$pci_a .= "$Proc->{Name}<br>";
						$PnPEntity{$Proc->{Name}} = 1;
					}elsif($Proc->{PNPDeviceID} =~ /^USB\\/i){
						$usb_a .= "$Proc->{Name}<br>";
						$PnPEntity{$Proc->{Name}} = 1;
					}elsif($Proc->{PNPDeviceID} =~ /^SCSI\\/i){
						$scsi_a .= "$Proc->{Name}<br>";
					}elsif($Proc->{PNPDeviceID} =~ /^IDE\\/i){
						$ide_a .= "$Proc->{Name}<br>";
					}
				}

				foreach my $Proc ( sort {lc $a->{Name} cmp lc $b->{Name}} in( $WMI->InstancesOf( "Win32_PerfRawData_Tcpip_NetworkInterface" ) ) ){
	#				$rBytes = $Proc->{BytesReceivedPersec} * 1024;
	#				$rBytes = $Proc->{PacketsReceivedPersec} . "000";
					$rBytes =~ s/[^\d]//g;
	#				$tBytes = $Proc->{BytesSentPersec} * 1024;
	#				$tBytes = $Proc->{PacketsSentPersec} . "000";
					$tBytes =~ s/[^\d]//g;
					$rDrop += $Proc->{PacketsReceivedDiscarded};
					$rError += $Proc->{PacketsReceivedErrors};
					$allError += $rError;
					$allDrop += $rDrop;
					$allrBytes += $rBytes;
					$alltBytes += $tBytes;
					$rBytes = berechnen($rBytes);
					$tBytes = berechnen($tBytes);
					$net_a .= qq~<tr>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$Proc->{Name}</font></td>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$rBytes</font></td>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$tBytes</font></td>
					<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$rDrop/$rError</font></td></tr>~;
				}
				$allrBytes = berechnen($allrBytes);
				$alltBytes = berechnen($alltBytes);
				$net_a .= qq~<tr>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">Gesamt</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$allrBytes</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$alltBytes</font></td>
				<td bgcolor="#eeeeee" align="right"><font face="Verdana,Arial" size="2">$allDrop/$allError</font></td></tr>~;

				foreach $Proc ( sort {lc $a->{ProcessId} cmp lc $b->{ProcessId}} in( $WMI->InstancesOf( "Win32_Process" ) ) ){
					if($parentID{$Proc->{ParentProcessId}}){
						$parentID{$Proc->{ParentProcessId}} .= "," . $Proc->{ProcessId};
					}else{
						$parentID{$Proc->{ParentProcessId}} .= $Proc->{ProcessId};
					}
					$HauptID{$Proc->{ProcessId}} = $Proc->{ParentProcessId};
					$ID{$Proc->{ProcessId}} = $Proc->{ExecutablePath};
					$ID{$Proc->{ProcessId}} = "System" unless($ID{$Proc->{ProcessId}});
					$NameID{$Proc->{ProcessId}} = $Proc->{Name};
					$NameID{$Proc->{ProcessId}} = "System" unless($NameID{$Proc->{ProcessId}});
				}

				$first = "|----";
				foreach (sort keys %ID){
					if(!$ID{$HauptID{$_}} && !$NameID{$HauptID{$_}} or $_ == 0){
						$pstree_a .= qq~<tr><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">|-$NameID{$_} (<a href="sysinfo.$cgiORpl?pass=$pass&action=pid&name=$_" target="_blank"><u>$_<\/u><\/a>)</font></td></tr>~;
						&subprozesse($parentID{$_},$first) if($parentID{$_});
					}
				}

				$WMI = Win32::OLE->GetObject("winmgmts:{impersonationLevel=impersonate}\\\\.\\Root\\cimv2");
				foreach $Proc ( sort {lc $a->{Name} cmp lc $b->{Name}} in( $WMI->InstancesOf( "Win32_Processor" ) ) ){
					$processor++;
					if($cachegroesse){
						$cachegroesse .= ", " . $Proc->{L2CacheSize} . " KB";
					}else{
						$cachegroesse = $Proc->{L2CacheSize} . " KB";
					}

					if($model){
						$model .= ", " . $Proc->{Name};
					}else{
						$model = $Proc->{Name};
					}

					if($cpu){
						$cpu .= ", " . $Proc->{CurrentClockSpeed};
					}else{
						$cpu = $Proc->{CurrentClockSpeed};
					}
				}
			}else{
				if($mod_w32s){
					Win32::API::Struct->typedef( SYSTEM_INFO => qw{
					   DWORD dwOemID;
					   DWORD dwPageSize;
					   DWORD lpMinimumApplicationAddress;
					   DWORD lpMaximumApplicationAddress;
					   DWORD dwActiveProcessorMask;
					   DWORD dwNumberOfProcessors;
					   DWORD dwProcessorType;
					   DWORD dwAllocationGranularity;
					   DWORD dwReserved;
					});
					Win32::API->Import('kernel32', 'VOID GetSystemInfo(SYSTEM_INFO lpSystemInfo)');
					$system = Win32::API::Struct->new('SYSTEM_INFO');
					GetSystemInfo($system);

					$processor = $system->{'dwNumberOfProcessors'};
					$cpu .= " (" . $system->{'dwProcessorType'} . ")";
				}

				if($mod_w32p == 1 && $mod_w32i == 1){
					$pi = Win32::Process::Info->new ();
					@info = $pi->GetProcInfo();
					foreach $pid (@info){
						push(@topo,sprintf("%04.f",$pid->{ProcessId}) . " $pid->{Name} <font size=\"1\">($pid->{ExecutablePath})</font><br>"); # - $pid->{UserModeTime} - $pid->{KernelModeTime} - $pid->{CreationDate}- 
					}
					foreach (sort {$a <=> $b} @topo){
						s/\s\s/&nbsp; /g;
						$pstree_a .= qq~<tr><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$_</font></td></tr>~;
					}
				}
			}
		}
		$processor = $ENV{'NUMBER_OF_PROCESSORS'} unless($processor);

		$bogomips = "?" unless($bogomips);
		$cachegroesse = "?" unless($cachegroesse);
		$model = "?" unless($model);
		$processor = "?" unless($processor);
		$cpu = "?" unless($cpu);
		chomp($machine);
		$cpu .= " ($machine)" if($machine);
	}

$ausgabe =qq~<table cellpadding="1" cellspacing="1" border="0">
	<td align="right" valign="top">
		<table cellpadding="1" cellspacing="1" border="0">
			<tr>
				<td bgcolor="#bcbcEE" colspan="2"><font face="Verdana,Arial" size="2" size="3"><b>Hardware Informationen:</b></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right"><font face="Verdana,Arial" size="2">Prozessor(en):</font></td>
				<td bgcolor="#eeeeee" align="left"><font face="Verdana,Arial" size="2">$processor</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right"><font face="Verdana,Arial" size="2">Model:</font></td>
				<td bgcolor="#eeeeee" align="left"><font face="Verdana,Arial" size="2">$model</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right"><font face="Verdana,Arial" size="2">Chip&nbsp;Mhz:</font></td>
				<td bgcolor="#eeeeee" align="left"><font face="Verdana,Arial" size="2">$cpu</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right"><font face="Verdana,Arial" size="2">Cache&nbsp;Gr&ouml;sse:</font></td>
				<td bgcolor="#eeeeee" align="left"><font face="Verdana,Arial" size="2">$cachegroesse</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right"><font face="Verdana,Arial" size="2">System&nbsp;Bogomips:</font></td>
				<td bgcolor="#eeeeee" align="left"><font face="Verdana,Arial" size="2">$bogomips</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right"><font face="Verdana,Arial" size="2">Floppy:</font></td>
				<td bgcolor="#eeeeee" align="left"><font face="Verdana,Arial" size="2">$floppy</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right" valign="top"><font face="Verdana,Arial" size="2">PCI&nbsp;Devices:</font></td>
				<td bgcolor="#eeeeee" align="left" valign="top"><font face="Verdana,Arial" size="2">$pci_a</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right" valign="top"><font face="Verdana,Arial" size="2">IDE&nbsp;Devices:</font></td>
				<td bgcolor="#eeeeee" align="left" valign="top"><font face="Verdana,Arial" size="2">$ide_a</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right" valign="top"><font face="Verdana,Arial" size="2">SCSI&nbsp;Devices:</font></td>
				<td bgcolor="#eeeeee" align="left" valign="top"><font face="Verdana,Arial" size="2">$scsi_a</font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF" align="right" valign="top"><font face="Verdana,Arial" size="2">USB&nbsp;Devices:</font></td>
				<td bgcolor="#eeeeee" align="left" valign="top"><font face="Verdana,Arial" size="2">$usb_a</font></td>
			</tr>
		</table>
	</td>
	<td align="left" valign="top">
		<table cellpadding="3" cellspacing="1" border="0">
			<tr>
				<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2" size="3"><b>Netzwerk Informationen:</b></font></td>
			</tr>
			<tr>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Device</font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Recieved</font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Sent</font></td>
				<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Err/Drop</font></td>
			</tr>
			$net_a
		</table>
	</td>
</table>

<br><br>

<table cellpadding="1" cellspacing="1" border="0" width="65%">
<tr>
	<td bgcolor="#bcbcEE" colspan="7"><font face="Verdana,Arial" size="2" size="3"><b>Dateisysteme:</b></font></td>
</tr>
<tr>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Mount</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Typ</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Partion</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Belegte Kapazit&auml;t (\%)</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Frei</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Belegt</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Gesamt</b></font></td>
</tr>
$mount_a
</table>

<br><br>

<table cellpadding="1" cellspacing="1" border="0" width="65%">
<tr>
	<td bgcolor="#bcbcEE" colspan="6"><font face="Verdana,Arial" size="2" size="3"><b>Speichernutzung:</b></font></td>
</tr>
<tr>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Typ</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Belegte Kapazit&auml;t (\%)</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Frei</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Belegt</b></font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Gesamt</b></font></td>
</tr>
$n_a
</table>

<br><br>

<table cellpadding="1" cellspacing="1" border="0" width="65%">
<tr>
	<td bgcolor="#bcbcEE"><font face="Verdana,Arial" size="2" size="3"><b>Der komplette Prozessbaum:</b></font></td>
</tr>
$pstree_a
</table>

<br><br>

<table cellpadding="1" cellspacing="1" border="0" width="65%">
<tr>
	<td bgcolor="#bcbcEE" colspan="9"><font face="Verdana,Arial" size="2" size="3"><b>Alle Benutzer die derzeit im System sind:</b></font></td>
</tr>
<tr>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">User</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">TTY</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">FROM</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Login\@</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Idle</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">JCPU</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">PCPU</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">What</font></td>
</tr>
$top_a
</table>

<br><br>

<table cellpadding="1" cellspacing="1" border="0" width="65%">
<tr>
	<td bgcolor="#bcbcEE" colspan="6"><font face="Verdana,Arial" size="2" size="3"><b>Jetzt laufende Prozesse:</b></font></td>
</tr>
<tr>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">load</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">user</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">size</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">process</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">time</font></td>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">command</font></td>
</tr>
$jlsp_a
</table>

<br><br>

<table cellpadding="1" cellspacing="1" border="0" width="70%">
<tr>
	<td bgcolor="#bcbcEE" colspan="11"><font face="Verdana,Arial" size="2" size="3"><b>Alle laufende Prozesse:</b></font></td>
</tr>
<tr>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>USER</font></td>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>PID</font></td>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>%CPU</font></td>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>%MEM</font></td>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>VSZ</font></td>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>TTY</font></td>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>STAT</font></td>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>START</font></td>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>TIME</font></td>
	<td bgcolor=#ddddFF><font face=Verdana,Arial size=2>COMMAND</font></td>
</tr>
$pro2_a
</table>

</center>~;
	&ausgabe($ausgabe);
	exit;
}

sub logfiles {
	if($logfilesON){
		@files = ();
		foreach (@logs){
			 push(@files,&filefind($_));
		}

		foreach (sort @files){
			if(!-d("$_") && $_ ne "\.\." && $_ ne "\." && $_ !~ /\||\;|\.\.|\.\// && $_ !~ /\.[Tt][aA][Rr]$/){
				if((-s("$_")) && (-B("$_")) or (-s("$_")) && (-T("$_"))){
					unless($logwert){
						$INFO{'log'} = "$_" unless($INFO{'log'});
						$logwert = "$_";
					}
					$ausgabe .= qq~<tr><td bgcolor="#eeeeee" align="left"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=logfiles&log=$_"><font color="blue"><u>$_</u></font></td></tr>~;
				}
			}
		}

		unless($ausgabe){
			$ausgabe .= "<tr><td><br><center><font face=verdana,arial>Nichts gefunden!</font></center><br></td></tr>";
		}else{
			$ausgabe = qq~<hr>
			<table cellpadding="1" cellspacing="1" border="0" width="95%">
			<td align="left" valign="top" width="25%">
				<table cellpadding="1" cellspacing="1" border="0">
					<tr>
						<td bgcolor="#bcbcEE" colspan="2"><font face="Verdana,Arial" size="2" size="3"><b>Logfiles:</b></font></td>
					</tr>$ausgabe~;

			$ausgabe .= qq~</table>
					</td>
					<td align="left" valign="top" width="75%"><pre>~;

			foreach (@logs){
				if($INFO{'log'} =~ /\Q$_\E/i){
					$accept = 1;
					last;
				}
			}
			if($INFO{'log'} !~ /\||\;|\.\.|\.\// && $accept == 1){
				$file = $INFO{'log'};

				if($file =~ /\.gz$|\.tgz$/){
					open(F,"gzip -cd $file |");
					@database = reverse(<F>);
					close(F);
				}else{
					open(F,"<$file");
					@database = reverse(<F>);
					close(F);
				}
				$anzahlLOG = @database - 1;
				$x_a = "1";
			}else{
				&error("Datei nicht gefunden oder nicht erlaubt.");
				$x_a = "0";
			}

			if($x_a == 1){
				$start = $INFO{'start'} || 0;
			        $ncount = 0;

			        while(($ncount*$maxdisplay)<@database) {
			                $nviewc = $ncount+1;
			                $nstrt = ($ncount*$maxdisplay);
			                if($start == $nstrt) {
			                        $sspan .= "$nviewc ";
			                } else {
			                        $sspan .= qq~<a href="sysinfo.$cgiORpl?pass=$pass&action=logfiles&start=$nstrt&log=$INFO{'log'}">$nviewc</a> ~;
			                }
			                ++$ncount;
				}

			        if ($ncount==1 or $ncount==0){
			                $sspan="[&lt;&lt;] 1 [&gt;&gt;]";
			        } else {
			                $x=($start/$maxdisplay)+1;
			                $xs=$start+$maxdisplay;
			                $xs2=$start-$maxdisplay;

			                if ($x<$ncount){
			                        if($x>1){
			                                $sspan= qq~<a href="sysinfo.$cgiORpl?pass=$pass&action=logfiles&start=$xs2&log=$INFO{'log'}">[&lt;&lt;]</a> $sspan~;
			                        }else{
			                                $sspan="[&lt;&lt;] $sspan";
			                        }
						$sspan .= qq~ <a href="sysinfo.$cgiORpl?pass=$pass&action=logfiles&start=$xs&log=$INFO{'log'}">[&gt;&gt;]</a>~;
			                } else {
			                        if($x>1){
			                                $sspan= qq~<a href="sysinfo.$cgiORpl?pass=$pass&action=logfiles&start=$xs2&log=$INFO{'log'}">[&lt;&lt;]</a> $sspan~;
			                        }else{
			                                $sspan="[&lt;&lt;] $sspan";
			                        }
			                        $sspan .=" [&gt;&gt;]";
			                }
			        }
			        
			        $sspan =~ s/  / /g;

				if($INFO{'dl'}){
					$file = (split(/\//,$INFO{'log'}))[-1];
					print "Content-Type: application/octet-stream;\n";
					print "Content-Disposition: attachment; filename=$file;\n\n";
				}

			        $num = 0;
			        for ($i = $start; $i < @database; $i++) {
					$num++;
				        $database[$i] =~ s!&!&amp;!g;
				        $database[$i] =~ s!&lt;!&#60;!g;
				        $database[$i] =~ s!&gt;!&#62;!g;
				        $database[$i] =~ s/>/&gt;/g;
				        $database[$i] =~ s/</&lt;/g;
				        $database[$i] =~ s/\|/\&\#124;/g;
					if($INFO{'dl'}){
						print $database[$i] if(!$INFO{'search'} or $database[$i] =~ /\Q$INFO{'search'}\E/i);
					}else{
						$ausgabe .= $database[$i] if(!$INFO{'search'} or $database[$i] =~ /\Q$INFO{'search'}\E/i);
					}

					last if($num >= $maxdisplay && !$INFO{'search'} && !$INFO{'dl'});
				}

				if($INFO{'dl'}){
					exit;
				}
			}
			$ausgabe .= qq~
					</pre><hr>$sspan<br><br><b>$anzahlLOG Zeilen</b> - <a href="sysinfo.$cgiORpl?pass=$INFO{'pass'}&action=logfiles&search=$INFO{'search'}&log=$INFO{'log'}&dl=1"><u><b>Download</b></u></a></td>
				</table>
			~;
		}
		$ausgabe .= qq~<form action="sysinfo.$cgiORpl" method="get"><input type="hidden" name="log" value="$INFO{'log'}"><input type="hidden" name="action" value="logfiles"><input type="hidden" name="pass" value="$INFO{'pass'}"><input type="text" name="search" value="" size="35" maxlength="255"> &nbsp; <input type="submit" value="Suchen"></form>~;
	}

	&ausgabe($ausgabe);
	exit;
}

sub webspace {
	if($webspaceON){
		if($DOCUMENT_ROOT eq "" && $FORM{'webspace'} eq ""){
			$DOCUMENT_ROOT = $ENV{'DOCUMENT_ROOT'};
		}else{
			$DOCUMENT_ROOT = $FORM{'webspace'};
		}
		
		if($^O !~ /win/i){
			$space = &command("du -m -s $DOCUMENT_ROOT");
	#		$space = &command("du -s $DOCUMENT_ROOT");
	#		$space=sprintf("%.2f",($space / 1024));
			$space =~ s/^([0-9]+)[\n\r\s](.*)/$1/isg;
		}else{
			$space=sprintf("%.2f",(((&checkspace($DOCUMENT_ROOT))[0]) / 1024 / 1024));
		}
		$space=sprintf("%.2f",(((&checkspace($DOCUMENT_ROOT))[0]) / 1024 / 1024)) if(!$space);


		$frei = $free;
		$free -= $space;
		if($frei < $space){$frei = $space;$free = 0;}

		$free .= " MB";
		$space .= " MB";
		$free2 = sprintf("%.2f",($space / $frei * 100));
		$webspace_a = qq~<font face="Verdana,Arial" size="2"><b>belegt:</b> Es sind $space belegt und frei $free von $frei MB ($free2\% von 100\%)<br><br>
		<form action="$cgi" method="POST">
		<input type=hidden name="action" value="webspace">
		<input type=text name="webspace" size="40" value="$DOCUMENT_ROOT">
		<input type=submit value="Berechnen">
		</form>
		</font>~;
	}

	&ausgabe($webspace_a);
	exit;
}

sub checkspace {local($e) = @_;
	($e) = shift;
	($size,$used_space,$free_space) = 0;
	foreach (&filefind($e)){
		$size += -s $_;
	}
	$used_space = int($size /1024);
	$free_space = ($size - $used_space);
	return($free_space,$size,$used_space);
}

sub debugger {
	&ausgabe("<hr><font face=Verdana,Arial>Bitte den Pfad inkl. Datei des Scriptes eingeben:<br><br><form action=\"sysinfo.$cgiORpl\" method=\"POST\"><input type=hidden name=\"action\" value=\"debugger2\"><font face=\"Arial,Verdana\"><input type=text name=\"pfad\" value=\"$ENV{'DOCUMENT_ROOT'}\" size=\"60\"></font><input type=submit value=\"Start\"></form></font>");
	exit;
}

sub debugger2 {
	if($debuggerON){
		$pfad = $FORM{'pfad'};
		$pfad =~ s/\\/\//g;
		$pfad =~ s/\/\//\//g;

		if(-e("$pfad")){
			@shell = split(/\n/,&command("perl -cw $pfad 2>&1"));
			foreach my $line (@shell) {
				$perl .= "$line<br>";
			} 
			$perl2 = join('', @shell);
			$perl = "$pfad syntax OK" if (length($perl2) == 0);
		}else{
			$perl = "Angegebenes Skript existiert nicht.";
		}

			$perl = qq~<table cellpadding="3" cellspacing="1" border="0">
				<tr>
					<td bgcolor="#bcbcEE" colspan="2"><font face="Verdana,Arial" size="2" size="3"><b>Perl-Debugger:</b></font></td>
				</tr>
				<tr>

					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">$perl</font></td>
				</tr>
			</table>~;
	}
	&ausgabe("$perl<br><br><hr><font face=Verdana,Arial>Bitte den Pfad inkl. Datei des Scriptes eingeben:<br><br><form action=\"sysinfo.$cgiORpl\" method=\"POST\"><input type=hidden name=\"action\" value=\"debugger2\"><font face=\"Arial,Verdana\"><input type=text name=\"pfad\" value=\"$ENV{'DOCUMENT_ROOT'}\" size=\"60\"></font><input type=submit value=\"Start\"></form></font>");
	exit;
}

sub berechnen {
	local($space) = @_;
	if($space > 1099511627776 ) {
		$space  = sprintf("%.2f", $space / 1099511627776 );
		$space .= "&nbsp;TB";
	}elsif($space > 1073741824 ) {
		$space  = sprintf("%.2f", $space / 1073741824 );
		$space .= "&nbsp;GB";
	}elsif($space > 1048576 ) {
		$space  = sprintf("%.2f", $space / 1048576 );
		$space .= "&nbsp;MB";
	}elsif($space > 1024 ) {
		$space  = sprintf("%.2f", $space / 1024 );
		$space .= "&nbsp;KB";
	}else{
		$space  = sprintf("%.2f", $space );
		$space .= "&nbsp;B";
	}
	return($space);
}


sub systemdoc {
	if($systemON){
		if($INFO{'name'} !~ /\||\;/){
			$doc = &command("perldoc $INFO{'name'}");
			$doc =~ s!&!&amp;!g;
			$doc =~ s!&lt;!&#60;!g;
			$doc =~ s!&gt;!&#62;!g;
			$doc =~ s/>/&gt;/g;
			$doc =~ s/</&lt;/g;
			$doc =~ s/\|/\&\#124;/g;
			$doc =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^\s|^;|;|>\"|\s|>|<)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\)|<|>|\.<|\.>|\.\s|\.\)|&lt;|&qt;|\}|'|\]|\s|\s$|\"\)|\.\"|\"<|\)|\,|$)/$1<a href=\"http:\/\/$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/isg;
			$doc =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^\s|^;|;|>\"|\s|>|<)(www\..+?)(\)|<|>|\.<|\.>|\.\s|\.\)|&lt;|&qt;|\}|\]|\s|\s$|\"\)|\.\"|\"<|\)|'|\,|$)/$1<a href=\"http:\/\/$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/isg;
			$doc =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^;|;|>\"|^\s|\s|>|<)((http:\/\/|ftp:\/\/|irc:\/\/|news:\/\/|gopher:\/\/|https:\/\/).+?)(\)|\.<|\"\)|'|\.\"|\"<|\.>|&lt;|&qt;|\}|\]|<|>|\.\s|\.\)|\s|\s$|\)|\,|$)/$1<a href=\"$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$4/isg;
			$doc =~ s/(^|>\.|\.|\(|\,|\(\"|&lt;|&qt;|\[|\{|=|'|^>|^<|^;|;|>\"|^\s|\s|>|<)([\w\d\.-]+\@[\w\d\.-]+\.\w{2,4})(\)|\.<|\"\)|\.\"|\"<|\.>|&lt;|&qt;|\}|\]|<|>|'|\.\s|\.\)|\s|\)|\,|$)/$1<a href=\"mailto:$2\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/g;

			$doc2 = &command("info $INFO{'name'}");
			$doc2 =~ s!&!&amp;!g;
			$doc2 =~ s!&lt;!&#60;!g;
			$doc2 =~ s!&gt;!&#62;!g;
			$doc2 =~ s/>/&gt;/g;
			$doc2 =~ s/</&lt;/g;
			$doc2 =~ s/\|/\&\#124;/g;
			$doc2 =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^\s|^;|;|>\"|\s|>|<)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\)|<|>|\.<|\.>|\.\s|\.\)|&lt;|&qt;|\}|'|\]|\s|\s$|\"\)|\.\"|\"<|\)|\,|$)/$1<a href=\"http:\/\/$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/isg;
			$doc2 =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^\s|^;|;|>\"|\s|>|<)(www\..+?)(\)|<|>|\.<|\.>|\.\s|\.\)|&lt;|&qt;|\}|\]|\s|\s$|\"\)|\.\"|\"<|\)|'|\,|$)/$1<a href=\"http:\/\/$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/isg;
			$doc2 =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^;|;|>\"|^\s|\s|>|<)((http:\/\/|ftp:\/\/|irc:\/\/|news:\/\/|gopher:\/\/|https:\/\/).+?)(\)|\.<|\"\)|'|\.\"|\"<|\.>|&lt;|&qt;|\}|\]|<|>|\.\s|\.\)|\s|\s$|\)|\,|$)/$1<a href=\"$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$4/isg;
			$doc2 =~ s/(^|>\.|\.|\(|\,|\(\"|&lt;|&qt;|\[|\{|=|'|^>|^<|^;|;|>\"|^\s|\s|>|<)([\w\d\.-]+\@[\w\d\.-]+\.\w{2,4})(\)|\.<|\"\)|\.\"|\"<|\.>|&lt;|&qt;|\}|\]|<|>|'|\.\s|\.\)|\s|\)|\,|$)/$1<a href=\"mailto:$2\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/g;
		}else{
			&error("Ein Befehl ist unzul&auml;ssig.");
		}
	}
	if($doc eq "" && $doc2 eq "" && $systemON){
		print "Location: http://search.cpan.org/search?module=$INFO{'name'}\n\n";exit;
	}else{
$ausgabe = qq~
</center>
Mehr Informationen bei <a href='http://search.cpan.org/search?module=$INFO{'name'}' target='_blank'><u><font color='blue'>CPAN</font></u></a><br><br>

<table cellpadding="4" cellspacing="1" border="0" bgcolor="#ddddFF">
<tr>
	<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2" size="3"><b>Perl-Dokumentation von $INFO{'name'}:</b></font></td>
</tr>
<tr>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="3"><pre>$doc</pre></font></td>
</tr>
</table>

<br><hr><br>

<table cellpadding="4" cellspacing="1" border="0" bgcolor="#ddddFF">
<tr>
	<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2" size="3"><b>Info-Dokumentation von $INFO{'name'}:</b></font></td>
</tr>
<tr>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="3"><pre>$doc2</pre></font></td>
</tr>
</table>
<center>
~;
		&ausgabe($ausgabe);
	}
}

sub systeminf {
	if($serverON){
		if($INFO{'name'} !~ /\||\;/ && $INFO{'name'} =~ /^[0-9A-Za-z]+$/){
			if($INFO{'name'} eq "nslookup"){
				$doc = &command("$INFO{'name'} help");
				$doc2 .= &command("info $INFO{'name'}");
			}elsif($INFO{'name'} eq "whois"){
				$doc2 = &command("info $INFO{'name'}");
			}else{
				$doc = &command("$INFO{'name'} --help");
				$doc2 .= &command("info $INFO{'name'}");
			}

			$doc =~ s!&!&amp;!g;
			$doc =~ s!&lt;!&#60;!g;
			$doc =~ s!&gt;!&#62;!g;
			$doc =~ s/>/&gt;/g;
			$doc =~ s/</&lt;/g;
			$doc =~ s/\|/\&\#124;/g;
			$doc =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^\s|^;|;|>\"|\s|>|<)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\)|<|>|\.<|\.>|\.\s|\.\)|&lt;|&qt;|\}|'|\]|\s|\s$|\"\)|\.\"|\"<|\)|\,|$)/$1<a href=\"http:\/\/$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/isg;
			$doc =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^\s|^;|;|>\"|\s|>|<)(www\..+?)(\)|<|>|\.<|\.>|\.\s|\.\)|&lt;|&qt;|\}|\]|\s|\s$|\"\)|\.\"|\"<|\)|'|\,|$)/$1<a href=\"http:\/\/$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/isg;
			$doc =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^;|;|>\"|^\s|\s|>|<)((http:\/\/|ftp:\/\/|irc:\/\/|news:\/\/|gopher:\/\/|https:\/\/).+?)(\)|\.<|\"\)|'|\.\"|\"<|\.>|&lt;|&qt;|\}|\]|<|>|\.\s|\.\)|\s|\s$|\)|\,|$)/$1<a href=\"$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$4/isg;
			$doc =~ s/(^|>\.|\.|\(|\,|\(\"|&lt;|&qt;|\[|\{|=|'|^>|^<|^;|;|>\"|^\s|\s|>|<)([\w\d\.-]+\@[\w\d\.-]+\.\w{2,4})(\)|\.<|\"\)|\.\"|\"<|\.>|&lt;|&qt;|\}|\]|<|>|'|\.\s|\.\)|\s|\)|\,|$)/$1<a href=\"mailto:$2\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/g;

			$doc2 =~ s!&!&amp;!g;
			$doc2 =~ s!&lt;!&#60;!g;
			$doc2 =~ s!&gt;!&#62;!g;
			$doc2 =~ s/>/&gt;/g;
			$doc2 =~ s/</&lt;/g;
			$doc2 =~ s/\|/\&\#124;/g;
			$doc2 =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^\s|^;|;|>\"|\s|>|<)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\)|<|>|\.<|\.>|\.\s|\.\)|&lt;|&qt;|\}|'|\]|\s|\s$|\"\)|\.\"|\"<|\)|\,|$)/$1<a href=\"http:\/\/$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/isg;
			$doc2 =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^\s|^;|;|>\"|\s|>|<)(www\..+?)(\)|<|>|\.<|\.>|\.\s|\.\)|&lt;|&qt;|\}|\]|\s|\s$|\"\)|\.\"|\"<|\)|'|\,|$)/$1<a href=\"http:\/\/$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/isg;
			$doc2 =~ s/(^|\(|\,|\(\"|\.|&lt;|&qt;|\[|\{|^>|=|'|^<|^;|;|>\"|^\s|\s|>|<)((http:\/\/|ftp:\/\/|irc:\/\/|news:\/\/|gopher:\/\/|https:\/\/).+?)(\)|\.<|\"\)|'|\.\"|\"<|\.>|&lt;|&qt;|\}|\]|<|>|\.\s|\.\)|\s|\s$|\)|\,|$)/$1<a href=\"$2\" target=\"_blank\"><font color="blue"><u>$2<\/u><\/font><\/a>$4/isg;
			$doc2 =~ s/(^|>\.|\.|\(|\,|\(\"|&lt;|&qt;|\[|\{|=|'|^>|^<|^;|;|>\"|^\s|\s|>|<)([\w\d\.-]+\@[\w\d\-.]+\.\w{2,4})(\)|\.<|\"\)|\.\"|\"<|\.>|&lt;|&qt;|\}|\]|<|>|'|\.\s|\.\)|\s|\)|\,|$)/$1<a href=\"mailto:$2\"><font color="blue"><u>$2<\/u><\/font><\/a>$3/g;
		}else{
			&error("FEHLER: Ein Befehl ist unzul&auml;ssig.");
		}
	}

$ausgabe = qq~
</center>
<table cellpadding="4" cellspacing="1" border="0" bgcolor="#ddddFF">
<tr>
	<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2" size="3"><b>Help-Dokumentation von $INFO{'name'}:</b></font></td>
</tr>
<tr>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="3"><pre>$doc</pre></font></td>
</tr>
</table>

<br><hr><br>

<table cellpadding="4" cellspacing="1" border="0" bgcolor="#ddddFF">
<tr>
	<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2" size="3"><b>Info-Dokumentation von $INFO{'name'}:</b></font></td>
</tr>
<tr>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="3"><pre>$doc2</pre></font></td>
</tr>
</table>
<center>
~;

	&ausgabe($ausgabe);
}

sub ausgabe {
	local($e) = @_;
	$code="0924686561645f666f6f745f617573203d2071717e093c68746d6c3e093c686561643e093c7469746c653e537973696e666f20762476657273696f6e202d2024454e567b27485454505f484f5354277d202d2024646174653c2f7469746c653e093c7374796c6520747970653d22746578742f637373223e093c212d2d09494e5055542e627574746f6e207b666f6e743a4c75636964612c56657264616e612c48656c7665746963612c53616e732d53657269663b7d09494e5055542e626f78207b666f6e743a4c75636964612c56657264616e612c48656c7665746963612c53616e732d53657269663b7d0953454c454354207b464f4e542d46414d494c593a4c75636964612c56657264616e612c48656c7665746963612c53616e732d53657269663b7d094f5054494f4e207b464f4e542d46414d494c593a4c75636964612c56657264616e612c48656c7665746963612c53616e732d53657269663b7d095445585441524541207b464f4e542d46414d494c593a4c75636964612c56657264616e612c48656c7665746963612c53616e732d53657269663b7d09494e505554207b464f4e542d46414d494c593a4c75636964612c56657264616e612c48656c7665746963612c53616e732d53657269663b7d09413a6c696e6b207b746578742d6465636f726174696f6e3a206e6f6e653b636f6c6f723a20626c61636b3b7d09413a76697369746564207b746578742d6465636f726174696f6e3a206e6f6e653b636f6c6f723a20626c61636b3b7d09413a616374697665207b6261636b67726f756e643a20234646464646463b636f6c6f723a20626c61636b3b746578742d6465636f726174696f6e3a20756e6465726c696e653b7d09413a686f766572207b6261636b67726f756e643a20234646464646463b636f6c6f723a20626c61636b3b746578742d6465636f726174696f6e3a20756e6465726c696e653b7d092d2d3e093c2f7374796c653e093c2f686561643e093c626f6479206267636f6c6f723d22234646464646462220746f706d617267696e3d223022206c6566746d617267696e3d223022206d617267696e6865696768743d223022206d617267696e77696474683d2230223e093c63656e7465723e093c666f6e7420666163653d22417269616c2c56657264616e61222073697a653d2232223e093c7461626c6520626f726465723d2230222063656c6c73706163696e673d2230222063656c6c70616464696e673d2232222077696474683d223130302522206267636f6c6f723d2223626362634545223e09093c74643e0909093c666f6e7420666163653d22417269616c2c56657264616e61222073697a653d2235223e537973696e666f20762476657273696f6e3c2f666f6e743e3c62723e3c62723e09093c2f74643e09093c746420616c69676e3d2263656e746572223e0909093c7461626c6520626f726465723d223022206267636f6c6f723d2223636363636363222063656c6c73706163696e673d2232222063656c6c70616464696e673d2233223e090909093c7464206267636f6c6f723d2223656565656565223e3c6120687265663d22737973696e666f2e246367694f52706c3f706173733d247061737326616374696f6e3d696e646578223e3c666f6e7420666163653d22417269616c2c56657264616e612220636f6c6f723d22626c7565223e3c753e536572766572696e666f733c2f753e3c2f666f6e743e3c2f613e3c2f74643e090909093c7464206267636f6c6f723d2223656565656565223e3c6120687265663d22737973696e666f2e246367694f52706c3f706173733d247061737326616374696f6e3d73797374656d223e3c666f6e7420666163653d22417269616c2c56657264616e612220636f6c6f723d22626c7565223e3c753e53797374656d696e666f733c2f753e3c2f666f6e743e3c2f613e3c2f74643e090909093c7464206267636f6c6f723d2223656565656565223e3c6120687265663d22737973696e666f2e246367694f52706c3f706173733d247061737326616374696f6e3d6465627567676572223e3c666f6e7420666163653d22417269616c2c56657264616e612220636f6c6f723d22626c7565223e3c753e5065726c2d44656275676765723c2f753e3c2f666f6e743e3c2f613e3c2f74643e090909093c7464206267636f6c6f723d2223656565656565223e3c6120687265663d22737973696e666f2e246367694f52706c3f706173733d247061737326616374696f6e3d6c6f6766696c6573223e3c666f6e7420666163653d22417269616c2c56657264616e612220636f6c6f723d22626c7565223e3c753e4c6f6766696c65733c2f753e3c2f666f6e743e3c2f613e3c2f74643e090909093c7464206267636f6c6f723d2223656565656565223e3c6120687265663d22737973696e666f2e246367694f52706c3f706173733d247061737326616374696f6e3d7765627370616365223e3c666f6e7420666163653d22417269616c2c56657264616e612220636f6c6f723d22626c7565223e3c753e5765627370616365206265726563686e656e3c2f753e3c2f666f6e743e3c2f613e3c2f74643e0909093c2f7461626c653e09093c2f74643e093c2f7461626c653e09093c62723e3c62723e092465093c2f666f6e743e093c2f63656e7465723e093c2f626f64793e093c2f68746d6c3e097e3b0924686561645f666f6f745f617573203d7e2073213c2f5b42625d5b4f6f5d5b44645d5b59795d3e213c62723e3c62723e3c63656e7465723e3c7461626c6520626f726465723d2230222063656c6c73706163696e673d2231222063656c6c70616464696e673d2231223e3c74723e3c74643e3c63656e7465723e3c666f6e7420666163653d2256657264616e612c417269616c222073697a653d2232223e3c623e537973696e666f7363726970743c2f623e2c20762476657273696f6e3c2f666f6e743e3c2f63656e7465723e3c2f74643e3c2f74723e3c74723e3c74643e3c63656e7465723e3c666f6e7420666163653d2256657264616e612c417269616c222073697a653d2232223e26636f70793b203c6120687265663d22687474703a2f2f7777772e636f6465722d776f726c642e646522207461726765743d225f626c616e6b223e3c623e3c666f6e7420666163653d22417269616c2c56657264616e612220636f6c6f723d22626c7565223e3c753e436f6465722d576f726c642e64653c2f753e3c2f666f6e743e3c2f623e3c2f613e2c20323030312d32303035202853746566616e6f73293c2f666f6e743e3c2f63656e7465723e3c2f74643e3c2f74723e3c2f7461626c653e3c2f63656e7465723e3c62723e3c2f626f64793e21673b0969662824686561645f666f6f745f61757320217e202f3c5c2f626f64793e2f297b09097072696e742022436f6e74656e742d547970653a20746578742f68746d6c5c6e5c6e223b09097072696e7420224461732053637269707420777572646520756e65726c617562742067652661756d6c3b6e646572742e223b0909657869743b097d0969662824454e567b27485454505f4143434550545f454e434f44494e47277d203d7e202f28782d677a69707c677a6970292f2026262024454e567b275345525645525f50524f544f434f4c277d2065712022485454502f312e31222026262024677a6970203d3d2031297b09097072696e742022436f6e74656e742d456e636f64696e673a2024315c6e223b09097072696e742022436f6e74656e742d547970653a20746578742f68746d6c5c6e5c6e223b090962696e6d6f6465205354444f55543b0909696628247a6c6962297b0909097072696e7420436f6d70726573733a3a5a6c69623a3a6d656d477a69702824686561645f666f6f745f617573293b09097d656c73657b0909096f70656e28475a49502c20227c20677a6970202d6622293b09090962696e6d6f646528475a4950293b0909097072696e7420475a49502024686561645f666f6f745f6175733b090909636c6f736528475a4950293b09097d097d656c73657b09097072696e742022436f6e74656e742d547970653a20746578742f68746d6c5c6e5c6e223b09097072696e742024686561645f666f6f745f6175733b097d";$code =~ s/([a-fA-F0-9]{2})/pack("C", hex($1))/eg;eval $code;
	exit;
}

sub pid {
	if($systemON){
		if($INFO{'name'} =~ /^\d+$/){
			if($mod_w32ole){
				$pid = $INFO{'name'};
	#			use Win32::OLE qw( in );
				$WMI = Win32::OLE->GetObject("winmgmts:{impersonationLevel=impersonate}\\\\.\\Root\\cimv2");
				foreach my $Proc ( sort {lc $a->{Name} cmp lc $b->{Name}} in( $WMI->InstancesOf( "Win32_Process" ) ) ){
					if($Proc->{ProcessID} eq $pid){
	#					push(@topo,$Proc->{ProcessID} . " $Proc->{Name} <font size=\"1\">($Proc->{ExecutablePath})</font><br>");
						$ParentProcessId = $Proc->{ParentProcessId};
						$ExecutablePath = $Proc->{ExecutablePath};
						$Priority = $Proc->{Priority};
						last;
					}
				}

				foreach (sort {$a <=> $b} @topo){
					s/\s\s/&nbsp; /g;
					$pstree_a .= qq~<tr><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$_</font></td></tr>~;
				}


				$ausgabe = qq~
				<table cellpadding="4" cellspacing="1" border="0">
				<tr>
					<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2" size="3"><b>Prozessinformationen zu $INFO{'name'}:</b></font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Befehl:</b></font></td>
					<td bgcolor="#eeeeee" colspan="3"><font face="Verdana,Arial" size="2">$ExecutablePath</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Prozess-ID:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$pid</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>öbergeordneter Prozess:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=pid&name=$ParentProcessId"><u>$ParentProcessId</u></a>: $Hcmd</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Besitzer:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$CSName</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Priorit&auml;t:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$Priority</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Gr&ouml;sse:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$vsz kB</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Laufzeit:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$time</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Prozessgruppen-ID:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$pgid</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Started:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$start</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Status:</b></font></td>
					<td bgcolor="#eeeeee" colspan="3"><font face="Verdana,Arial" size="2">$status</font></td>
				</tr>
				</table><br><br>

				<table cellpadding="4" cellspacing="1" border="0">
				<tr>
					<td bgcolor="#bcbcEE" colspan="5"><font face="Verdana,Arial" size="2" size="3"><b>Offene Dateien:</b></font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">File Descriptor</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Type</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">File size</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Inode</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Path</font></td>
				</tr>
				$files
				</table>
				~;
			}else{
				open(LSOF, "lsof -p \'$INFO{'name'}\' |");
				while(<LSOF>){
					if(/^(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d+),(\d+)\s+(\d+)\s+(\d+)\s+(.*)/){
						if(lc($4) eq "mem" && $share){
							$share = "Shared library";
						}else{
							$share = "Program code";
						}

						$reg = "Regular file" if(lc($5) eq "reg");
						$files .= qq~<tr>
							<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$share</font></td>
							<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$reg</font></td>
							<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$8</font></td>
							<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$9</font></td>
							<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$10</font></td>
						</tr>~;
					}
				}
				close(LSOF);

				$doc = &command("ps -ehwww -o user,ruser,group,rgroup,pid,ppid,pgid,pcpu,vsz,nice,etime,time,tty,priority,stat,rss,pri,ni,start,cmd $INFO{'name'}");
				($user,$ruser,$group,$rgroup,$pid,$ppid,$pgid,$pcpu,$vsz,$nice,$etime,$time,$tty,$priority,$stat,$tss,$pri,$ni,$start,$cmd) = split(/\s+/,$doc,20);

				$Hdoc = &command("ps -ehwww -o user,ruser,group,rgroup,pid,ppid,pgid,pcpu,vsz,nice,etime,time,tty,priority,stat,rss,pri,ni,start,cmd $ppid");
				($Huser,$Hruser,$Hgroup,$Hrgroup,$Hpid,$Hppid,$Hpgid,$Hpcpu,$Hvsz,$Hnice,$Hetime,$Htime,$Htty,$Hpriority,$Hstat,$Htss,$Hpri,$Hni,$Hstart,$Hcmd) = split(/\s+/,$Hdoc,20);

				foreach (split(//,$stat)){
					if(/R/){
						$status .= "lauff&auml;hig, ";
					}elsif(/T/){
						$status .= "gestoppt, ";
					}elsif(/D/){
						$status .= "nicht-unterbrechbarer Schlaf, ";
					}elsif(/S/){
						$status .= "schlafend, ";
					}elsif(/Z/){
						$status .= "Zombie, ";
					}elsif(/W/){
						$status .= "Keine Speicherseiten belegt, ";
					}elsif(/N/){
						$status .= "positiver nice-Wert, ";
					}
				}
				$status =~ s/\, $//g;

				$ausgabe = qq~
				<table cellpadding="4" cellspacing="1" border="0">
				<tr>
					<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2" size="3"><b>Prozessinformationen zu $INFO{'name'}:</b></font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Befehl:</b></font></td>
					<td bgcolor="#eeeeee" colspan="3"><font face="Verdana,Arial" size="2">$cmd</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Prozess-ID:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$pid</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>öbergeordneter Prozess:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2"><a href="sysinfo.$cgiORpl?pass=$pass&action=pid&name=$ppid"><u>$ppid</u></a>: $Hcmd</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Besitzer:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$user</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>CPU:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$pcpu\%</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Gr&ouml;sse:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$vsz kB</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Laufzeit:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$time</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Nicelevel:</b></font></td>
					<td bgcolor="#eeeeee" colspan="3"><font face="Verdana,Arial" size="2">$nice</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Gruppe:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$group</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Echter Benutzer:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$ruser</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Prozessgruppen-ID:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$pgid</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Started:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$start</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>TTY:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$tty</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Echte Gruppe:</b></font></td>
					<td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$rgroup</font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2"><b>Status:</b></font></td>
					<td bgcolor="#eeeeee" colspan="3"><font face="Verdana,Arial" size="2">$status</font></td>
				</tr>
				</table><br><br>

				<table cellpadding="4" cellspacing="1" border="0">
				<tr>
					<td bgcolor="#bcbcEE" colspan="5"><font face="Verdana,Arial" size="2" size="3"><b>Offene Dateien:</b></font></td>
				</tr>
				<tr>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">File Descriptor</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Type</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">File size</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Inode</font></td>
					<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">Path</font></td>
				</tr>
				$files
				</table>
				~;
			}
		}else{
			&error("Keine g&uuml;ltige PID");
		}
	}

	&ausgabe($ausgabe);
}

sub tempConvert {
	local($celcius) = @_;
	$result = (( $celcius * 9) / 5 ) + 32;
	$result = sprintf("%.1f", $result);
	$result .= "&#176 F";
	return $result;
}

sub subprozesse {
	local($e,$nexo) = @_;

	foreach (split(/\,/,$e)){
		$_ =~ s/^0//;
		$_ =~ s/^08$/8/;
		$pstree_a .= qq~<tr><td bgcolor="#eeeeee"><font face="Verdana,Arial" size="2">$nexo$NameID{$_} (<a href="sysinfo.$cgiORpl?pass=$pass&action=pid&name=$_" target="_blank"><u>$_<\/u><\/a>)</font></td></tr>~;
		if($parentID{$_}){
			$nexo .= "---";
			&subprozesse($parentID{$_},$nexo);
			$nexo =~ s/---$//;
		}
	}
	return;
}

sub error {
	local($e) = @_;

$ausgabe = qq~<table cellpadding="4" cellspacing="2" border="0" bgcolor="#ddddFF">
<tr>
	<td bgcolor="#bcbcEE" colspan="4"><font face="Verdana,Arial" size="2"><b>Fehler:</b></font></td>
</tr>
<tr>
	<td bgcolor="#ddddFF"><font face="Verdana,Arial" size="2">$e</font></td>
</tr>
</table>~;

	&ausgabe($ausgabe);
}

__DATA__
# This file controls what Internet media types are sent to the client for
# given file extension(s).  Sending the correct media type to the client
# is important so they know how to handle the content of the file.
# For more information about Internet media types, please read 
# RFC 2045, 2046, 2047, 2048, and 2077.  The Internet media type
# registry is at <ftp://ftp.iana.org/assignments/media-types/>.

# MIME type			Extension
application/EDI-Consent
application/EDI-X12
application/EDIFACT
application/activemessage
application/andrew-inset	ez
application/applefile
application/atomicmail
application/cals-1840
application/commonground
application/cybercash
application/cu-seeme		csm cu
application/dca-rft
application/dec-dx
application/eshop
application/excel		xls
application/ghostview
application/hyperstudio
application/iges
application/mac-binhex40	hqx
application/mac-compactpro	cpt
application/macwriteii
application/marc
application/mathematica
application/msword		doc dot wrd
application/news-message-id
application/news-transmission
application/octet-stream	bin dms lha lzh exe class iso
application/oda			oda
application/pdf			pdf
application/pgp			pgp
application/pgp-encrypted
application/pgp-keys
application/pgp-signature	pgp
application/postscript		ai eps ps
application/powerpoint		ppt
application/remote-printing
application/rtf			rtf
application/slate
application/wita
application/wordperfect5.1	wp5
application/vnd.wap.wbxml	wbxml
application/vnd.wap.wmlc	wmlc
application/vnd.wap.wmlscriptc	wmlsc
application/x-123		wk
application/x-Wingz		wz
application/x-bcpio		bcpio
application/x-bzip2		bz2
application/x-cdlink		vcd
application/x-chess-pgn		pgn
application/x-compress		z Z
application/x-cpio		cpio
application/x-csh		csh
application/x-debian-package	deb
application/x-director		dcr dir dxr
application/x-dvi		dvi
application/x-gtar		gtar tgz
application/x-gunzip		gz
application/x-gzip		gz
application/x-hdf		hdf
application/x-httpd-php		phtml pht php
application/x-javascript	js
application/x-java-jnlp-file	jnlp
application/x-kword		kwd kwt
application/x-kspread		ksp
application/x-kpresenter	kpr kpt
application/x-kchart		chrt
application/x-koan		skp skd skt skm
application/x-latex		latex
application/x-maker		frm maker frame fm fb book fbdoc
application/x-mif		mif
application/x-msdos-program	com exe bat
application/x-netcdf		nc cdf
application/x-ns-proxy-autoconfig	pac
application/x-perl		pl pm
application/x-rad		rad
application/x-rpm		rpm spm
application/x-sh		sh
application/x-shar		shar
application/x-shockwave-flash	swf
application/x-stuffit		sit
application/x-sv4cpio		sv4cpio
application/x-sv4crc		sv4crc
application/x-tar		tar
application/x-tcl		tcl
application/x-tex		tex
application/x-texinfo		texinfo texi
application/x-troff		t tr roff
application/x-troff-man		man
application/x-troff-me		me
application/x-troff-ms		ms
application/x-ustar		ustar
application/x-wais-source	src
application/xhtml+xml           xhtml xht
application/zip			zip
audio/basic			au snd
audio/midi			mid midi kar
audio/mpeg			mpga mp2 mp3
audio/x-mpegurl			m3u
audio/x-aiff			aif aifc aiff
audio/x-realaudio		ra
audio/x-wav			wav
chemical/x-pdb			pdb
chemical/x-xyz			xyz
image/bmp			bmp
image/gif			gif
image/ief			ief
image/jpeg			jpeg jpg jpe
image/png			png
image/tiff			tiff tif
image/vnd.djvu			djvu djv
image/vnd.wap.wbmp		wbmp
image/x-cmu-raster		ras
image/x-portable-anymap		pnm
image/x-portable-bitmap		pbm
image/x-portable-graymap	pgm
image/x-portable-pixmap		ppm
image/x-rgb			rgb
image/x-xbitmap			xbm
image/x-xpixmap			xpm
image/x-xwindowdump		xwd
message/external-body
message/news
message/partial
message/rfc822
model/iges			igs iges
model/mesh			msh mesh silo
model/vrml			wrl vrml
multipart/alternative
multipart/appledouble
multipart/digest
multipart/mixed
multipart/parallel
text/css			css
text/html			html htm
text/plain			asc txt c cc h hh cpp hpp
text/richtext			rtx
text/rtf			rtf
text/sgml			sgml sgm
text/tab-separated-values	tsv
text/x-setext			etx
text/x-vCalendar		vcs
text/x-vCard			vcf
text/xml			xml dtd xsl
video/dl			dl
video/fli			fli
video/gl			gl
video/mpeg			mp2 mpe mpeg mpg
video/quicktime			qt mov
video/x-msvideo			avi
video/x-sgi-movie		movie
x-conference/x-cooltalk		ice
x-world/x-vrml			wrl vrml
audio/x-pn-realaudio rmm ram
audio/vnd.rn-realaudio ra
application/smil smi smil
text/vnd.rn-realtext rt
video/vnd.rn-realvideo rv
image/vnd.rn-realflash rf swf
application/x-shockwave-flash2-preview rf swf
application/sdp sdp
application/x-sdp sdp
application/vnd.rn-realmedia rm
image/vnd.rn-realpix rp

#PORT:
#
# protocols	This file describes the various protocols that are
#		available from the TCP/IP subsystem.  It should be
#		consulted instead of using the numbers in the ARPA
#		include files, or, worse, just guessing them.
#
# This list could be found on:
#         http://www.iana.org/assignments/protocol-numbers
#
ip		0	IP              # internet protocol v4
hopopt		0	HOPOPT		# Hop-by-hop optons for IPv6
icmp		1	ICMP		# internet control message protocol
igmp		2	IGMP		# internet group multicast protocol
ggp		3	GGP		# gateway-gateway protocol
st		5	ST		# Stream
tcp		6	TCP		# transmission control protocol
cbt		7	CBT		# CBT
egp		8	EGP		# exterior gateway protocol
igp		9	IGP		# any private interior gateway
bbn-rcc-mon	10	BBN-RCC-MON	# BBN RCC monitoring
nvp-ii		11	NVP-II		# Network Voice Protocol
pup		12	PUP		# PARC universal packet protocol
argus		13	ARGUS		# ARGUS
emcon		14	EMCON		# EMCON
xnet		15	XNET		# Cross Net Debugger
chaos		16	CHAOS		# Chaos
udp		17	UDP		# user datagram protocol
mux		18	MUX		# Mulitplexing
dcn-meas	19	DCN-MEAS	# DCN Measurement Subsystems
hmp		20	HMP		# host monitoring protocol
prm		21	PRM		# Packet Radio Measurement
xns-idp		22	XNS-IDP		# XEROX NS IDP
trunk-1		23	TRUNK-1		# Trunk-1
trunk-2		24	TRUNK-2		# Trunk-2
leaf-1		25	LEAF-1		# Leaf-1
leaf-2		26	LEAF-2		# Leaf-2
rdp		27	RDP		# "reliable datagram" protocol
irtp		28	IRTP		# Internet Reliable Transaction
iso-tp4		29	ISO-TP4		# ISO Transport Protocol Class 4
netblt		30     	NETBLT      	# Bulk Data Transfer Protocol
mfe-nsp		31     	MFE-NSP    	# MFE Network Services Protocol
merit-np	32     	MERIT-INP  	# MERIT Internodal Protocol
sep		33     	SEP        	# Sequential Exchange Protocol
3pc		34     	3PC       	# Third Party Connect Protocol
idpr		35     	IDPR       	# Inter-Domain Policy Routing Protocol
xtp		36     	XTP        	# XTP
ddp		37     	DDP        	# Datagram Delivery Protocol
idpr-cmtp	38     	IDPR-CMTP   	# IDPR Control Message Transport Proto
il		40	IL          	# IL Transport Protocol
ipv6		41	IPv6		# IPv6
sdrp		42      SDRP       	# Source Demand Routing Protocol
ipv6-route	43	IPv6-Route	# Routing Header for IPv6
ipv6-frag	44	IPv6-Frag	# Fragment Header for IPv6
idrp		45      IDRP       	# Inter-Domain Routing Protocol
rsvp		46      RSVP       	# Reservation Protocol
gre		47      GRE        	# General Routing Encapsulation
mhrp		48      MHRP       	# Mobile Host Routing Protocol
bna		49      BNA        	# BNA
#ipv6-crypt	50	IPv6-Crypt	# Encryption Header for IPv6
#ipv6-auth	51	IPv6-Auth	# Authentication Header for IPv6
esp		50	ESP		# Encapsulating Security Payload
ah		51	AH		# Authentication Header
i-nlsp		52      I-NLSP     	# Integrated Net Layer Security  TUBA
swipe		53      SWIPE      	# IP with Encryption
narp		54      NARP       	# NBMA Address Resolution Protocol
mobile		55      MOBILE     	# IP Mobility
tlsp		56      TLSP       	# Transport Layer Security Protocol
skip		57      SKIP       	# SKIP
ipv6-icmp	58	IPv6-ICMP ICMPV6 icmpv6 icmp6 # ICMP for IPv6
ipv6-nonxt	59	IPv6-NoNxt	# No Next Header for IPv6
ipv6-opts	60	IPv6-Opts	# Destination Options for IPv6
cftp		62	CFTP		# CFTP
sat-expak	64     	SAT-EXPAK  	# SATNET and Backroom EXPAK
kryptolan	65     	KRYPTOLAN  	# Kryptolan
rvd		66     	RVD        	# MIT Remote Virtual Disk Protocol
ippc		67     	IPPC       	# Internet Pluribus Packet Core
sat-mon		69     	SAT-MON    	# SATNET Monitoring
visa		70     	VISA       	# VISA Protocol
ipcv		71     	IPCV       	# Internet Packet Core Utility
cpnx		72     	CPNX       	# Computer Protocol Network Executive
cphb		73    	CPHB       	# Computer Protocol Heart Beat
wsn		74     	WSN        	# Wang Span Network
pvp		75     	PVP        	# Packet Video Protocol
br-sat-mon	76      BR-SAT-MON 	# Backroom SATNET Monitoring
sun-nd		77     	SUN-ND     	# SUN ND PROTOCOL-Temporary
wb-mon		78     	WB-MON     	# WIDEBAND Monitoring
wb-expak	79     	WB-EXPAK   	# WIDEBAND EXPAK
iso-ip		80	ISO-IP		# ISO Internet Protocol
vmtp		81      VMTP       	# VMTP
secure-vmtp	82      SECURE-VMTP	# SECURE-VMTP
vines		83      VINES      	# VINES
ttp		84      TTP        	# TTP
nsfnet-igp	85      NSFNET-IGP 	# NSFNET-IGP
dgp		86      DGP        	# Dissimilar Gateway Protocol
tcf		87      TCF        	# TCF
eigrp		88      EIGRP      	# EIGRP
ospfigp		89      OSPFIGP    	# OSPFIGP
sprite-rpc	90      Sprite-RPC 	# Sprite RPC Protocol
larp		91      LARP       	# Locus Address Resolution Protocol
mtp		92      MTP        	# Multicast Transport Protocol
ax.25		93      AX.25      	# AX.25 Frames
ipip		94      IPIP       	# IP-within-IP Encapsulation Protocol
micp		95      MICP       	# Mobile Internetworking Control Pro.
scc-sp		96      SCC-SP     	# Semaphore Communications Sec. Pro.
etherip		97      ETHERIP    	# Ethernet-within-IP Encapsulation
encap		98	ENCAP		# RFC1241 encapsulation
any          	99      any		# private encryption sche
gmtp		100     GMTP       	# GMTP
ifmp		101     IFMP       	# Ipsilon Flow Management Protocol
pnni		102     PNNI       	# PNNI over IP
pim		103     PIM        	# Protocol Independent Multicast
aris		104     ARIS       	# ARIS
scps		105     SCPS       	# SCPS
qnx		106     QNX        	# QNX
a/n		107     A/N        	# Active Networks
ipcomp		108     IPComp     	# IP Payload Compression Protocol
snp		109     SNP        	# Sitara Networks Protocol
compaq-peer	110     Compaq-Peer	# Compaq Peer Protocol
ipx-in-ip	111     IPX-in-IP  	# IPX in IP
vrrp		112     VRRP       	# Virtual Router Redundancy Protocol
pgm		113     PGM        	# PGM Reliable Transport Protocol
l2tp		115     L2TP       	# Layer Two Tunneling Protocol
ddx		116     DDX        	# D-II Data Exchange (DDX)
iatp		117     IATP     	# Interactive Agent Transfer Protocol
stp		118     STP        	# Schedule Transfer Protocol
srp		119     SRP        	# SpectraLink Radio Protocol
uti		120     UTI        	# UTI
smp		121     SMP        	# Simple Message Protocol
sm		122     SM          	# SM
ptp		123     PTP        	# Performance Transparency Protocol
fire		125     FIRE		#
crtp		126     CRTP        	# Combat Radio Transport Protocol
crudp		127     CRUDP       	# Combat Radio User Datagram
sscopmce	128     SSCOPMCE	#
iplt		129     IPLT		#
sps		130     SPS        	# Secure Packet Shield
pipe		131     PIPE  		# Private IP Encapsulation within IP
sctp		132     SCTP  		# Stream Control Transmission Protocol
fc		133     FC    		# Fibre Channel
rsvp-e2e-ignore	134	RSVP-E2E-IGNORE # [RFC3175]
raw		255	RAW		# RAW IP interface
