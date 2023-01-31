# Rooster-Rats

# Lectures & Lesroosters

Het inroosteren van lessen is een ingewikkeld probleem. In deze case moet een weekrooster gemaakt worden voor een vakkenlijst op Science Park. 

Hiervoor moeten 131 activiteiten ingepland worden. Dit kunnen hoorcolleges, werkcolleges en practica zijn.
· Een activiteit duurt 2 uur (= tijdslot)
· Maximale groepsgrootte bij werkcolleges en practica

Verder zijn er 7 zalen waarin de activiteiten kunnen plaatsvinden.
· Alle zalen zijn voor alle soorten activiteiten geschikt
· Capaciteit verschilt per zaal

Elk van de vakken kan worden ingedeeld in een van de 145 tijdsloten. Dit zijn periodes van 2 uur.

· Elke zaal heeft vier tijdsloten overdag (9-11u, 11-13u, 13-15u, 15-17u)

· Grootste zaal heeft ook een avondslot (17-19u)

We hebben te maken met 609 Studenten.
· Elke student volgt maximaal 5 vakken


## Constraints

De hard constraints van onze case zijn als volgt:
· Alle activiteiten moeten worden ingeroosterd
· Maximaal één activiteit per tijdslot per zaal
· Student mag maximaal twee tussenuren na elkaar hebben
· Maximumgrootte van werkcolleges en practica
· Zo min mogelijk werkcolleges en practica

Naast het genereren van een geldige oplossing wordt er gekeken naar de kwaliteit van het rooster. Er wordt een aantal maluspunten toegekend bij het overtreden van de volgende soft constraints:
· Studenten met tussenuren (α = een tussenuur per dag per student, β = twee tussenuren per dag per student)
· Studenten met twee activiteiten in hetzelfde tijdslot (γ = # lessen die overlappen per student)
· Gebruik van avondslot (δ = # gebruikte avondsloten per lokaal)
· Studenten die niet in het lokaal passen (ε = # studenten die niet in lokaal passen)

## Doel:
De kwaliteit van het rooster wordt gemeten aan de hand van de volgende objective function, die geminimaliseerd moet worden:
f(α, β, γ, δ, ε) = α + 3⋅β + γ + 5⋅δ + ε

## State space:
Om een idee te krijgen van de grootte van het probleem, hebben wij de state space berekend.



## Aan de slag

### Vereisten

Deze codebase is volledig geschreven in Python 3.9.13 en we gaan ervan uit dat er een Proglab environment aanwezig is. Hieronder staan alle benodigde packages om de code succesvol te draaien. Deze zijn gemakkelijk te installeren via pip, zoals hieronder aangegeven:

```
python3 -m pip install pdfschedule
```
```
pip install pyyaml
```

### Gebruik

Een voorbeeldje kan gerund worden door aanroepen van:

```
python main.py
```

Het bestand geeft een voorbeeld voor gebruik van de verschillende functies.

### Structuur

De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

- **/code**: bevat alle code van dit project
  - **/code/algorithms**: bevat de code voor algoritmes
  - **/code/classes**: bevat de drie benodigde classes voor deze case
  - **/code/visualisation**: bevat de code voor de visualisatie
- **/data**: bevat de verschillende csv bestanden die nodig zijn om de roosters te vullen en te visualiseren

## Auteurs
- Martijn Kievit
- Kiki van Gerwen
- Melanie Messih
