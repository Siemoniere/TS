use strict;
use warnings;
use HTTP::Daemon;
use HTTP::Status;
use HTTP::Response; # Potrzebne do stworzenia własnej odpowiedzi

# Zmieniono 'lukim' na 'localhost' dla lepszej kompatybilności
my $d = HTTP::Daemon->new(
    LocalAddr => 'localhost',
    LocalPort => 4321,
) || die "Nie można uruchomić serwera: $!";

print "Serwer (echo nagłówków) uruchomiony pod adresem: ", $d->url, "\n";

while (my $c = $d->accept) {
    # Użycie fork() pozwala na obsługę wielu klientów jednocześnie (opcjonalne, ale dobra praktyka)
    if (my $pid = fork) {
        # Proces rodzica - zamyka połączenie i czeka na następne
        $c->close;
        next;
    }
    # Proces dziecka - obsługuje to konkretne połączenie
    
    while (my $r = $c->get_request) {
        if ($r->method eq 'GET') {
            # Pobierz nagłówki jako pojedynczy string
            my $headers_string = $r->headers->as_string;

            # Utwórz nową odpowiedź HTTP
            my $response = HTTP::Response->new(RC_OK); # Status 200 OK
            $response->header('Content-Type' => 'text/plain; charset=utf-8');
            $response->content("Oto nagłówki Twojego żądania:\n\n" . $headers_string);

            # Wyślij odpowiedź do klienta
            $c->send_response($response);
        }
        else {
            $c->send_error(RC_FORBIDDEN);
        }
    }
    $c->close;
    exit; # Zakończ proces dziecka
}