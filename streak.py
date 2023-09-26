import urllib.request
import csv

#application takes an MLB player's name and displays their average streak (either games w/ hits or strikeouts) and dry streak lengths (games w/o hits or strikeouts)
#player information scraped from baseball-reference.com

year = 2023

#returns name from user input
def user_input_player_name():
    return input("\nEnter player name (case sensitive): ") #test

#takes player's name
#returns player's (baseball reference) id, found by searching csv. returns null string if not found
def get_player_id(player_name):
    br_id = ""
    #open player csv
    player_csv = open("BR_id.csv", "rt")
    reader = csv.reader(player_csv, delimiter=',')

    #parse through csv
    for row in reader:
        #id is first element, name is second
        if row[0] and row[1] and row[1]==player_name and br_id == "":
            br_id = row[0]
            print("\nFound "+player_name+"'s Baseball Reference ID: "+br_id)
        #if another player w/ name is found after id has been updated
        elif row[0] and row[1] and row[1]==player_name and br_id != "":
            raise Exception("Another player with name "+player_name+" found. Baseball Reference ID: " + row[4])
            #print("Another player with name "+player_name+" found. Baseball Reference ID: " + row[4])
            return ""
    if br_id=="":
        raise Exception("Player ID not found.")
    return br_id
        

# takes player's id and the desired year
# returns html contents of player's data baseball-reference.com 
def get_html(player_id, year):
    #headers for url method
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    url_string = "https://www.baseball-reference.com/players/gl.fcgi?id="+player_id+"&t=b&year="+str(year)+"#all_batting_gamelogs"
    #create request to html
    req = urllib.request.Request(url=url_string,headers=headers)
    
    #return string from request
    print("Player's Baseball Reference URL: "+url_string)
    return urllib.request.urlopen(req).read().decode("utf-8")


# takes html and desired stat type from baseball-reference.com
# returns list of # of occurences of desired event
def parse_html(html_string, stat_type):
    if (stat_type!= "H" and stat_type!="SO"):
        raise Exception("Invalid stat type. Must be 'H' for hits or 'SO' for strikeouts.")
    
    #if need to see what html it scrapes
    # full_html = open('full_html.txt', 'w')
    # full_html.write(html_string)
    # full_html.close()

    # trim html string by using larger sequential unique strings
    modded_html_string = html_string[html_string.find('Batting Game Log</caption>'):] #trim off front
    modded_html_string = modded_html_string[modded_html_string.find('<tbody>'):modded_html_string.find('</tbody>')]

    #save for testing
    trimmed_html = open('trimmed_html.txt', 'w')
    trimmed_html.write(modded_html_string)
    trimmed_html.close()

    #extract event count data
    counts = []
    while modded_html_string.find('data-stat="'+stat_type+'" >') != -1:
        count = modded_html_string[ modded_html_string.find('data-stat="'+stat_type+'" >')+len('data-stat="'+stat_type+'" >') ] #assumes number is 0-10
        counts.append(int(count))
        modded_html_string = modded_html_string[ modded_html_string.find('data-stat="'+stat_type+'" >')+len('data-stat="'+stat_type+'" >'):] #trims the string to go to next number
    
    #if event not found on player's baseball reference
    if len(counts)==0:
        raise Exception("Event data not found on player's Baseball Reference page")
    return counts

# takes count of event per game per game
# returns list containing the length of each streak of event occurences
def find_streak_lengths(counts):
    streaklengths = [0] #initial streak starts at 0
    idx = 0
    for count in counts: 
        if count!=0: #if a hit, increase current streak
            streaklengths[idx] = streaklengths[idx]+1
        elif count==0 and streaklengths[idx]!=0:#if no event occurence and current streak is not 0, go to next streak
            idx+=1
            streaklengths.append(0) #create new streak
        #if no event occurence and current streak is 0, do nothing
    
    #remove possible trailing 0 (if most recent game has no event occurence)
    if streaklengths[idx]==0:
        del streaklengths[idx]

    return streaklengths

# takes event count per game
# returns list containing the length of each dry streak 
def find_drystreak_lengths(counts):
    streaklengths = [0] #initial streak starts at 0
    idx = 0
    for count in counts: 
        if count==0: #if not a hit, increase current streak
            streaklengths[idx] = streaklengths[idx]+1
        elif count!=0 and streaklengths[idx]!=0:#if event occurs and current streak is not 0, go to next streak
            idx+=1
            streaklengths.append(0) #create new streak
        #if event occurs and current streak is 0, do nothing

    #remove possible trailing 0 (if last game has a hit)
    if streaklengths[idx]==0:
        del streaklengths[idx]

    return streaklengths

# takes array containing streak lengths
# returns average streak length
def avg_streak_length(streak_lengths):
    return sum(streak_lengths)/len(streak_lengths)
