import csv
import sys

#how to use the program:
#python dna.py databases/large.csv sequences/1.txt


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py databases/data.csv sequences/number.txt")

    # Read database file into a variable
    persons = []
    #dictionary as [{"name" : "Albus" , "AGAT" : int("27") , ... }{...}{...}]
    with open (sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            int_row = {}
            for column in row:
                if column == "name" : #exclude names column or values from being converted from strings to ints
                    int_row[column] = row[column]
                else: 
                    int_row[column] = int(row[column])
            persons.append(int_row)

    # Read DNA sequence file into a variable
    with open (sys.argv[2] , "r") as file:
        text = file.read()
    STRs = extract_STR() #array of STRs names ['AGATC', 'TTTTTTCT', 'AATG', 'TCTAG', 'GATA', 'TATC', 'GAAA', 'TCTG']

    # Find longest match of each STR in DNA sequence
    dict_text = {} #dict of STR : longest match
    for i in range (len(STRs)): #{'AGATC': 4, 'TTTTTTCT': 0, 'AATG': 1, 'TCTAG': 0, 'GATA': 1, 'TATC': 5, 'GAAA': 1, 'TCTG': 0}
        dict_text[STRs[i]] = longest_match(text,STRs[i])

    # Check database for matching profiles
    matching = 0
    for i in range(len(persons)):
        matching = 0
        for j in range(len(STRs)): 
            if dict_text[STRs[j]] == persons[i][STRs[j]]: #lw longest match of that particular STRs = person number1,strs , then increase matching by 1 if matching reaches the len(STR)"all strs are matched" retrun name of that person
                matching += 1
        if matching == len(STRs):
            print(persons[i]["name"])
        elif i == len(persons) - 1 : #reached end of loop , then print
            print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


def extract_STR(): #goes through csv and extracts keys(texts) and puts them to a list
    with open (sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames #must be used with same naming, returns all keys with commas between them
        STRs = [] # empty list to append text to
        for i in range(1 , len(fieldnames)): #start from i = 1 because we don't need text(name)
            STRs.append(fieldnames[i]) #['AGATC', 'TTTTTTCT', 'AATG', 'TCTAG', 'GATA', 'TATC', 'GAAA', 'TCTG']
        return STRs


main()
