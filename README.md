# Uruchamianie
Najpierw trzeba zedytować plik `run_single_test.sh` tak, aby przekierowywał stdin na program kandydata i wypluwał wynik na stdout.

Testerkę uruchamia się w następujący sposób:
```bash
python3 run.py
```
Możemy także odpalić tylko niektóre testy (bo np. jest stanowczo za dużo błędów) wpisując podsłowo z nazwy testu:
```bash
python3 run.py ICE
```
# Pliki testów
1. Można dodawać komentarze do testów `#` lub opis `##`, który zostanie wypisany w wypadku błędu:
```python
## jeżeli w linii 6 quantity=2500 zamiast 10000 to znaczy, że agresywny iceberg zachowuje sie jak pasywny
{"sellOrders": [{"id": 1, "price": 101, "quantity": 20000}], "buyOrders": []}
{"sellOrders": [{"id": 1, "price": 101, "quantity": 20000}], "buyOrders": [{"id": 2, "price": 99, "quantity": 50000}]}
{"sellOrders": [{"id": 3, "price": 100, "quantity": 10000}, {"id": 1, "price": 101, "quantity": 20000}], "buyOrders": [{"id": 2, "price": 99, "quantity": 50000}]}
{"sellOrders": [{"id": 3, "price": 100, "quantity": 10000}, {"id": 4, "price": 100, "quantity": 7500}, {"id": 1, "price": 101, "quantity": 20000}], "buyOrders": [{"id": 2, "price": 99, "quantity": 50000}]}
{"sellOrders": [{"id": 3, "price": 100, "quantity": 10000}, {"id": 4, "price": 100, "quantity": 7500}, {"id": 1, "price": 101, "quantity": 20000}], "buyOrders": [{"id": 2, "price": 99, "quantity": 50000}, {"id": 5, "price": 98, "quantity": 25000}]}
# teraz wchodzi agresywny Iceberg
# zjadł wszystkie sell po cenie 100 i ustawia się teraz z maksymalnym peakiem
{"sellOrders": [{"id": 1, "price": 101, "quantity": 20000}], "buyOrders": [{"id": 6, "price": 100, "quantity": 10000}, {"id": 2, "price": 99, "quantity": 50000}, {"id": 5, "price": 98, "quantity": 25500}]}
{"buyOrderId": 6, "price": 100, "quantity": 10000, "sellOrderId": 3}
{"buyOrderId": 6, "price": 100, "quantity": 7500, "sellOrderId": 4}
```
2. Niektóre testy trzeba zweryfikować i są one oznaczone opisem `## niezweryfikowany test`.
3. Nie można dzielić JSONa enterami :(
# PDFy
Jest załączony pdf z zadaniem dla kandydata oraz pdf z (również udostępnionym dla kandydata) dokładniejszym opisem Iceberga.
# Sugerowane pytania
1. Testy:
    1. Czy przechodzi załączone testy
    2. Czy przechodzi test z drugiego PDFa (4-2-3-1-AGGRESSIVE)
    3. Czy są własne testy
        1. Ile
        2. Ile sensownych
        3. Czy był test integracyjny
2. Kod:
    1. Czy JSONy są generowane na piechotę
    2. Czy jest jakiś rodzaj pomocnego README
    3. Czy uruchamianie jest trywialne
    4. Czy zmienne mają sensowne nazwy
    5. Czy w kodzie są asercje
    6. Czy kod jest miejscami rozdmuchany (np. przez złudną obiektowość, rozdzielanie na pliki), podczas gdy rzeczy, które rzeczywiście powinny być wydzielone, wcale nie są.
    7. Jeżeli w języku jest opcjonalne typowanie (python) - czy są typy
    8. Inne
3. Program:
    1. Czy program dla poprawnego wejścia kończy się błędem
    2. Czy program dla poprawnego wejścia się zapętla
    3. Czy program wypisuje czysty stdout
4. Zadanie:
    1. Jak zostało zinterpretowane (zapytać o sensowność założeń podczas rozmowy). _Motywacja:
      Widzimy stan giełdy przed dodaniem orderu i możemy dostosować cenę, by była korzystna.
      Jeżeli nie zapewnimy poniższych właściwości, to użytkownik giełdy musiałby emulować te rzeczy poprzez aktywne czekanie._
        1. Kupno/Sprzedarz po korzystnej cenie dla wchodzącego orderu.
        2. Ustawianie maksymalnego quantity po relaksacji AGRESYWNEGO iceberga (tak powinno być)
        3. Ustawianie maksymalnego quantity po relaksacji PASYWNEGO iceberga (tak nie powinno być)
        4. Agresywny iceberg pomija swój peak (powinien - jeżeli nie, to peak będzie ujawniony, bo zobaczymy w logach kilka transakcji o identycznej cenie oraz quantity, a następnie zaksięgowaną niepełną kolejną)
        5. Podczas inicjalizacji ustawia quantity=peak (bład w wypadku, gdy quantity < peak)
        6. Czy obie kolejli są posortowane w odpowiednią stronę
    2. Czy wg ww. założeń (tj. przyjetych przez kandydata) kod jest poprawny
