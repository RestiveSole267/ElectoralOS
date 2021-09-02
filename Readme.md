# ElectoralOS 

ElectoralOS is a voting operating system for different types of ranked-choice voting systems (IRV, STV, PBV)

## Ranking Methods
**Instant runoff voting (IRV):** A single candidate election method that elects the candidate with majority support (≥ 50% of the votes).

**Single transferable vote (STV):** A multiple candidate election method that elects candidates based on proportional representation.
Voters rank candidates and are granted one vote each. If a candidate gets more votes than the threshold for being elected, the candidate is the winner. This type of voting uses the Droop quota,

```python
droop_quota = votes/(seats + 1) + 1
```

If one candidate gets more votes than the threshold the extra votes are transferred to the voter's 2nd, 3rd, and etc choice. If no candidates gets over the threshold, the candidate with the fewest votes is removed, and the votes are transferred to the next choice of the voter.

**Preferential block vote (PBV):** A multiple candidate election method that elects candidates that obtain a majority support (≥ 50% of the votes).
Voters rank candidates and are granted one vote. The candidate with fewest votes is removed and the candidate's votes are transferred according to the voters 2nd choice or 3rd and etc.

## Versions
- v1.0 (2020-04-07) - Pre-release:
This is the beta release that test the operating systems function in whether or not the operating system that can handle parsing data and printing it down into a file of the users choice.
- v2.0 (2021-09-02) - Alpha Build:
  - Google Forms is connected to the operating system. 
  - The system can parse results from .csv or .json file. 
