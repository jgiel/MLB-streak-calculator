# MLB-streak-calculator
Python program that creates a CSV containing MLB players' hit-streak and strikeout-streak data, which is calculated using data available on baseball-reference.com.  

A player is considered to have a hit-streak/strikeout-streak of size _n_ if they played _n_ consecutive games in which they had a hit/strikeout (or conversely, a no-hit-streak/no-strikeout-streak of size _n_ if they played _n_ consecutive games in which they had no hits/strikeouts).


# Execution
- Execute the program with `python3 main.py`  

- Then, you will have the option to enter the path to a .txt file containing MLB player names or to use the default list of names  
  - (If you choose to use your own .txt file, please be aware that data for rookie players may not be found because the CSV containing baseball reference IDs (`BR_id.csv`) has not been updated since 2022) 

- Players will then be processed and their data will be scraped from baseball-reference.com. Once finished processing, the streak data will be available on `streak_info(MM-DD-YYYY_HH:MM)`.


### Please be aware...
I have implemented a 1 second lag in between each player being processed in order to avoid overloading baseball-reference.com with HTTP requests, so processing times may be slow for large batches of players. 
