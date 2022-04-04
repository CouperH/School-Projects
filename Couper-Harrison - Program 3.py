# --------------------------------------
# CSCI 127, Program 3                  |
# October, 18th, 2021                  |
# Couper Harrison                      |
# --------------------------------------
import csv
import os

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'covid.csv') # I had to add this because I was having directory errors. this is used to look for covid.csv in the directory that the python file is in.

with open(filename,newline='') as csvfile:
    reader = csv.reader(csvfile)
    global data # global so i can use this elsewhere, rather than processing the file at the start of every function. reduction of redundancies
    data = list(reader)
    data.remove(data[0])

def ave_infection_rate():
    infection = 0.0
    for i in data:
        infection += float(i[-1]) # accumulates infection rates
    infection = infection/float(len(data)) # calculates data from sum of all infection rates divided by length of data AKA amount of entries
    return infection

def countries_in_study(filename):
    file_name = os.path.join(here, filename)
    previous = []
    populations = {} # using dictionary so i dont have a jumbled mess of printing
    with open(file_name, "w") as output: # "w" creates the file if it is not already there. if it is there, it just opens it.
        for i in data:
            if i[7] != '-1': # i found "-1" in the data for some certain countries. this was causing the total number to be 213 instead of 211. 
                if i[5] not in previous:
                    previous.append(i[5]) # append country to previous to handle repeated entries
                    populations.update({i[5]: int(i[7])}) # append to dictionary, makes it easier to print
        sorteddict = dict(sorted(populations.items(), key=lambda item: item[1], reverse=True)) # sorted works the same as sort, but with more parameters available
                                                                                               # lambda allows me to write a "function" in one line, sorting the values of the dict rather than attempting to sort the dict, which would error
                                                                                               # reverse=True sorts by descending, highest values first
                                                                                               # dict() keeps it in a dictionary, since sorted() returns a list by default
        for i in sorteddict:
            rank = (list(sorteddict.keys()).index(i))+1 # returns index of current key, list() needs to be used because you cant find index of a key in dict without converting it
            to_be_written = ((str(rank)).ljust(5) + i.ljust(50) + (str(sorteddict[i])).ljust(20)+ " \n") # using ljust() to have spaces inbetween values
            output.write(to_be_written)
            
def deaths_in_country(country):
    
    previous = []
    deaths = {}
    for i in data: # this for loop initializes the deaths dictionary. have to do separate for loops because you are cumulating for every country, rather than the whole data set
        if i[5] not in previous:
            previous.append(i[5])
            deaths.update({((i[5]).upper()): 0}) # .upper() added for sake of handling

    current_country = data[0][5] # initializes the starting country
    for x in data:
        if x[5] == current_country:
            deaths[((x[5]).upper())] += int(x[4]) # adds deaths to key 
            current_country = x[5] # sets current country to current iteration
        else:
            current_country = x[5] # sets current country to current iteration. it is done here too to continue the loop
        
    return deaths[country] # dictionaries made this way easier, allows me to return the deaths in just a simple line

        

def continental_death_tolls():
    pass

# --------------------------------------

def main():

    print("Global data collected between Jan 1 - Nov 5, 2020".center(50))
    infections = ave_infection_rate() 
    print('*' * 50)
    print("Fortnightly cases reported per 100,000 people,\n(global average): ", end="")
    print(infections)

    print('*' * 50)
    user_input = input("Save list countries? ('y' for yes) : ")
    if user_input.lower() == 'y':
        save_as = input("Save File As: ")
        save_as += ".txt"
        countries_in_study(save_as)
        print("File saved as", save_as)

    print('*' * 50)
    country = input("Enter a country in the dataset: ")
    num = deaths_in_country((country.upper())) # .upper() added for ease of handling. assignment did not say to assume that user input was correctly formatted, so i added this
    print("The data reports {:d} covid deaths in {}.".format(num, country))

    print('*' * 50)
    continental_death_tolls()

# --------------------------------------

main()
