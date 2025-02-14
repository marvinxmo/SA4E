# SA4E

Repo zur Übung Software Architecture for Enterprises WS24/25

## Hinweise zu Übung 3

Steps to run the code for Uebung 3.

```bash
### Navigate to Uebung3 dir
cd Uebung3

### Create venv inside Uebung3
python -m venv .venv

### Activate .venv on Windows
.\.venv\Scripts\activate
### or macOS and Linux
source .venv/bin/activate

### Install dependencies from requirement.txt
pip install -r requirements.txt
```

Jede der Aufgaben 1 bis 3 hat eine eigene docker-compose.yaml

**Run Aufgabe1**

```bash
### Navigate to Aufgabe1 dir
cd Aufgabe1

### Start docker network with Kafka server and zookeeper
docker compose -f "docker-compose.yml" up -d --build

### Start the Race
python SectionInitializer.py

### Stop docker network to prevent port conflicts
docker compose -f "docker-compose.yml" down
```

**Run Aufgabe2**

```bash
### Navigate to Aufgabe2 dir
cd Aufgabe2

### Start docker network with three Kafka servers
docker compose -f "docker-compose.yml" up -d --build

### Start the Race (includes a wait to simulate outage of one of the kafka server)
python SectionInitializer.py

### Stop docker network to prevent port conflicts
docker compose -f "docker-compose.yml" down

```

**Run Aufgabe3**

```bash
### Navigate to Aufgabe3 dir
cd Aufgabe3

### Start docker network
docker compose -f "docker-compose.yml" up -d --build

### Create your own Track (saved to CuCuCo/MyTrackConfig.json)
python CuCuCo/TrackGenerator.py

### Visualize Track (either the MyTrackConfig.json or ExampleTrackConfig.json)
python CuCuCo/TrackVisualizer.py

### Start the Race
python SectionInitializer.py

### Stop docker network to prevent port conflicts
docker compose -f "docker-compose.yml" down

```

---

---

---

---

## Hinweise zu Übung 2

### Docker Container mit XmasWishes (enhält Aufgaben 3 und 4)

Ich habe das Image in Docker Hub gepusht.
Nutzen Sie folgenden Command um es zu clonen:

```bash
docker run -p 8085:8085 -p 8086:8086 marvinxmo/xmaswishes
```

Mit den oben spezifizierten Port-Bindings haben sie dann über folgende Links Zugriff auf XmasWishes:

[http://localhost:8086/submitwish](http://localhost:8086/submitwish) : Das GUI um einen einzelnen Wunsch zu übermitteln

[http://localhost:8086/uploadwish](http://localhost:8086/uploadwish) : Das GUI um mehrere Wünsche mit dem Upload von JSON Dateien zu übermittel (Aufgabe 4)

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
