# Datenstruktur

simulation.csv:

agent: Individuum
x: x Koordinate
y: y Koordinate
t: timestep
State: Krankheitsstatus {0: unbekannt, 1: Gesund/nicht infiziert, 2: Corona Fall, 3: Geheilt}


AgentMaster.csv:

agent: Individuum,
state: Anfangsstatus (Test um Seed-Personen zu finden, generell unbekannt)
diffusion_rate: Bewegungsgeschwindigkeit (generell unbekannt, muss aus daten ermittelt werden)
