# **Handlinger** (i 2D tetris...)


## Rotasjon

- Selvbestemt retning, med to ulike knapper, en for høyre, en for venstre
- Roterer 90 grader om sentrum i blokken for ett trykk
- Definerer for hver enkelt type figur hvilken blokk som er rotasjonssentrum
- Figuren roterer kun dersom blokkene dens ikke kolliderer med andre figurers blokker


## Sidelengs bevegelse

- To retninger, høyre og venstre, med to ulike knapper
- Figuren beveger seg hele blokker bortover av gangen
- Figuren beveger seg en blokk for ett trykk
- Stopper ved veggene


## Hard drop

- Slippes helt ned og låses med en gang, no going back
- Egen knapp for hard drop


## Soft drop

- Slippes fortere ned (kanskje selvbestemt hvor mye fortere? Hvis vi vil fikse sånt)
- Faller kun fortere mens knappen holdes inne
- Egen knapp for soft drop


## Standard nedover bevegelse

- Øker hastighet desto lengre man spiller
- Hastighet øker med nivå
- Kan låses med en gang den treffer bunnen, kan ha delay, opp til oss


## Nivå

- Styrt av linjer ryddet, ikke poengsum