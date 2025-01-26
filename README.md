# SA4E

Repo zur Übung Software Architecture for Enterprises WS24/25

## Hinweise zu Übung 2

### Docker Container mit XmasWishes (enhält Aufgaben 3 und 4)

Ich habe das Image in den Docker Hub gepusht.
Nutzen Sie folgenden Command um es zu clonen und den Container zu starten:

```bash
docker run -p 8085:8085 -p 8086:8086 marvinxmo/xmaswishes
```

Mit den oben spezifizierten Port-Bindings haben sie dann über folgende Links Zugriff auf XmasWishes:

[http://localhost:8086/submitwish](http://localhost:8086/submitwish) : Das GUI um einen einzelnen Wunsch zu übermitteln

[http://localhost:8086/uploadwish](http://localhost:8086/uploadwish) : Das GUI um mehrere Wünsche mit dem Upload von JSON Dateien zu übermittel (Aufgabe 4)

[http://localhost:8086/api/wish](http://localhost:8086/api/wish) : API-Endpoint für POST requests mit XmasWish-Objekten

[http://localhost:8085/h2-console](http://localhost:8085/h2-console) : (Achtung anderer Port!) Hier kann die Datenbank mithilfe von SQL Queries abgefragt werden. Login Daten:

|                       |                          |
| --------------------- | ------------------------ |
| Settings              | Generic H2               |
| Driver Class          | org.h2.Driver            |
| JDBC URL              | jdbc:h2:mem:wishdb       |
| User Name             | santa                    |
| Password              |                          |
| ------------          | -----------              |
| SQL Query zur Abfrage | SELECT \* FROM XMAS_WISH |
