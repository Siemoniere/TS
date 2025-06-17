use strict;
use warnings;
use HTTP::Daemon;
use HTTP::Status;
use File::Spec;
use Cwd 'abs_path';
use FindBin; # <-- DODAJ TEN MODUŁ

# Użyj $FindBin::Bin, aby ścieżka była zawsze poprawna,
# niezależnie od tego, skąd uruchamiamy skrypt.
my $web_root = File::Spec->catfile($FindBin::Bin, 'www');

# Reszta kodu pozostaje bez zmian...
my $d = HTTP::Daemon->new(
    LocalAddr => 'localhost',
    LocalPort => 4321,
) || die "Nie można uruchomić serwera: $!";

print "Serwer plików statycznych uruchomiony pod adresem: ", $d->url, "\n";
print "Katalog główny serwisu: ", abs_path($web_root), "\n";

while (my $c = $d->accept) {
    while (my $r = $c->get_request) {
        if ($r->method eq 'GET') {
            my $uri = $r->uri;
            my $path = $uri->path;

            if ($path =~ m{/$}) {
                $path .= "index.html";
            }
            
            # Usuwamy początkowy '/' ze ścieżki, żeby File::Spec działał poprawnie
            $path =~ s{^/}{}; 
            
            my $file_path = File::Spec->catfile($web_root, $path);

            my $abs_filepath = abs_path($file_path);
            my $abs_webroot = abs_path($web_root);
            
            if (!$abs_filepath || index($abs_filepath, $abs_webroot) != 0) {
                print "ODMOWA: Próba dostępu poza katalog główny: $path\n";
                print "  (Ścieżka pliku: $abs_filepath, Root: $abs_webroot)\n"; # Dodatkowe info do debugowania
                $c->send_error(RC_FORBIDDEN, "Access Denied");
                next;
            }

            if (-f $file_path && -r _) { # Sprawdzamy też, czy plik jest odczytywalny
                print "Wysyłanie pliku: $file_path\n";
                $c->send_file_response($file_path);
            } else {
                print "BŁĄD: Nie znaleziono pliku lub brak praw odczytu: $file_path\n";
                $c->send_error(RC_NOT_FOUND, "File not found");
            }
        }
        else {
            $c->send_error(RC_METHOD_NOT_ALLOWED);
        }
    }
    $c->close;
    undef($c);
}