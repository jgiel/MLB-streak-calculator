#TODO:
# find adequate lag time
# put date of most recent game
# if pitcher, just skip
# upload error code to csv

import streak
import csv
import time
from datetime import datetime
from pathlib import Path


def main():
    #get file of players
    playername_file_name = input("Enter the path to a .txt file containing player names separated by newlines (or press enter to use default): ")
    if not playername_file_name:
        playername_file_name = str(Path().absolute())+"/data/MLB-Player-Names-(trimmed).txt" #trimmed version removes players that could not be found in original MLB-Player-Names.csv
    playername_file = open(playername_file_name)
    player_names = playername_file.readlines()
    
    #create output csv
    output_csv_title = "streak_info("+datetime.now().strftime("%m-%d-%Y_%H:%M")+").csv"
    output_csv = open(output_csv_title, "w")
    csv_writer = csv.writer(output_csv)
    fields = ['Name', 'BR ID', 'Hit streaks (old to new)', 'No hit streaks (old to new)', 'Avg. hit streak-length',\
               'Avg. no-hit streak-length', 'Current hit streak type', 'Current hit streak', 'Strikeout streaks (old to new)',\
                  'No strikeout streaks (old to new)', 'Avg. strikeout streak length', 'Avg. no strikeout streak length',\
                    'Current strikeout streak type', 'Current strikeout streak', 'Exception Message']
    csv_writer.writerow(fields)

    for player_name in player_names:
        time.sleep(.5) #avoid overloading http requests
        player_name = player_name.strip() #remove newline char

        #catch errors from streak.py
        try:
            player_id = streak.get_player_id(player_name)

            #exception handle for not found id?
            if player_id != "":
                #get baseball reference page as html string
                html_string = streak.get_html(player_id, year=2023)

                #Get hit data:
                hit_counts = streak.parse_html(html_string, stat_type="H") #get amount of hits for each game

                hit_streaklengths = streak.find_streak_lengths(hit_counts) #find hit streaks / no hit streaks
                nohit_streaklengths = streak.find_drystreak_lengths(hit_counts)

                avg_hit_streaklength = streak.avg_streak_length(hit_streaklengths) #calculate averages
                avg_nohit_streaklength = streak.avg_streak_length(nohit_streaklengths)

                current_hit_streaktype = "" #find current hit-streak type by checking most recent game
                current_hit_streak = 0
                if hit_counts[-1] != 0:
                    current_hit_streaktype = "hit streak"
                    current_hit_streak = hit_streaklengths[-1]
                else:
                    current_hit_streaktype = "dry streak"
                    current_hit_streak = nohit_streaklengths[-1]
                

                #Get strikeout data
                strikeout_counts = streak.parse_html(html_string, stat_type="SO") #get amount of strikeouts for each game

                strikeout_streaklengths = streak.find_streak_lengths(strikeout_counts) #find strikeout / no strikeout streaks
                nostrikeout_streaklengths = streak.find_drystreak_lengths(strikeout_counts)

                avg_strikeout_streaklength = streak.avg_streak_length(strikeout_streaklengths) #calculate averages
                avg_nostrikeout_streaklength = streak.avg_streak_length(nostrikeout_streaklengths)

                current_strikeout_streaktype = "" #find current strikeout streak type by checking most recent game
                current_strikeout_streak = 0
                if strikeout_counts[-1] != 0:
                    current_strikeout_streaktype = "strikeout streak"
                    current_strikeout_streak = strikeout_streaklengths[-1]
                else:
                    current_strikeout_streaktype = "no strikeout streak"
                    current_strikeout_streak = nostrikeout_streaklengths[-1]
                
                #Write to array (name, id, h streak, n-h streak, avg h streak, avg n-h streak, current h streak type, current h streak, so streak, n-so streak, avg so streak, avg n-so streak, current so streak type, current so streak, exception message)
                data = [player_name, player_id, str(hit_streaklengths), str(nohit_streaklengths), str(avg_hit_streaklength),\
                         str(avg_nohit_streaklength), current_hit_streaktype, current_hit_streak, str(strikeout_streaklengths),\
                              str(nostrikeout_streaklengths), str(avg_strikeout_streaklength), str(avg_nostrikeout_streaklength),\
                                  current_strikeout_streaktype, str(current_strikeout_streak), ""]
                
                #Write array to csv
                csv_writer.writerow(data)
            else:
                raise Exception("ID not found for "+player_name)
            
        #if exception, write exception info to csv
        except Exception as e:
            print("\nError uploading data for "+player_name+" ("+str(e)+")")
            csv_writer.writerow([player_name, "", "", "", "", "", "", "", "", "", "", "","","", str(e)])
    output_csv.close()
    
if __name__ == "__main__":       
    main()
