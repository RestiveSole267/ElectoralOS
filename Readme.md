# ElectoralOS 

ElectoralOS is a voting operating system for different types of ranked-choice voting systems (IRV, STV, PBV). This was orignially a personal project created by me a year ago originally named Election Alpha.

## Ranking Methods
**Instant runoff voting (IRV):** A single candidate election method that elects the candidate with majority support (≥ 50% of the votes).

```os
# INSTANT RUNOFF VOTING

ROUND 1
Candidate                 Votes Status 
-------------------- ---------- ------------
Juan Simon Angel             11 In 
Yezarel Prieto                7 In
Cameron White                 3 Out

FINAL ROUND
Candidate                 Votes Status 
-------------------- ---------- ------------
Juan Simon Angel             12 Elected 
Yezarel Prieto                9 Runnerup
Cameron White                 0 Out
```

**Single transferable vote (STV):** A multiple candidate election method that elects candidates based on proportional representation.
Voters rank candidates and are granted one vote each. If a candidate gets more votes than the threshold for being elected, the candidate is the winner. This type of voting uses the Droop quota,

```python
droop_quota = votes/(seats + 1) + 1
```

If one candidate gets more votes than the threshold the extra votes are transferred to the voter's 2nd, 3rd, and etc choice. If no candidates gets over the threshold, the candidate with the fewest votes is removed, and the votes are transferred to the next choice of the voter.

```os
# SINGLE TRANSFFERABLE VOTE
# EXAMPLE IS FOR THREE SEATS

ROUND 1
Candidate                 Votes Status 
-------------------- ---------- ------------
Juan Simon Angel             25 In 
Yezarel Prieto               17 In
Cameron White                14 In
Jazmyn Gregory               11 In 
Isabel Kassum                 9 Out

ROUND 2
Candidate                 Votes Status 
-------------------- ---------- ------------
Juan Simon Angel             25 In 
Yezarel Prieto               19 In
Cameron White                18 In
Jazmyn Gregory               16 Out 
Isabel Kassum                 0 Out

FINAL ROUND
Candidate                 Votes Status 
-------------------- ---------- ------------
Yezarel Prieto             28 Elected 
Cameron White              26 Elected
Juan Simon Angel           25 Elected
Jazmyn Gregory              0 Out
Isabel Kassum               0 Out
```
**Preferential block vote (PBV):** A multiple candidate election method that elects candidates that obtain a majority support (≥ 50% of the votes).
Voters rank candidates and are granted one vote. The candidate with fewest votes is removed and the candidate's votes are transferred according to the voters 2nd choice or 3rd and etc.

```os
# PREFERENTIAL BLOCK VOTING
# EXAMPLE IS FOR TWO SEATS

FINAL ROUND
Candidate                           Votes Status 
------------------------------ ---------- ------------
Maksim Malanchunk, Libertarian         28 Elected
Maxwell Paradis, Libertarian           26 Elected
Jean-Paul Absi, Republican             21 Out
William Arnold, Democrat               15 Out
```

## Versions
- v1.0 (2020-04-07) - Pre-release:
This is the beta release that test the operating systems function in whether or not the operating system that can handle parsing data and printing it down into a file of the users choice.
- v2.0 (2021-09-02) - Alpha Build:
  - Google Forms is connected to the operating system. 
  - The system can parse results from .csv or .json file. 
