#-------------------------------------
# Single Transferable Vote Calculator
#             Version 1.1
#         Ben Boardman (@Benjome)
#            12 April 2022
#-------------------------------------

#A memory object to store a candidate
class Candidate:
    # Initializes candidate with a name, all other values set to defaults
    def __init__(self, name):
        self.__name = name.lower()
        self.__votes = 0.0
        self.__isElected = False
        self.__isEliminated = False
        self.__displayVotes = 0.0

    # Get the candidate's name
    def getName(self):
        return self.__name
    
    #Get the candidate's current vote tally
    def getVotes(self):
        return self.__votes

    #Resets the candidate's vote tally. Used between tabulation rounds.
    def resetVotes(self):
        self.__votes = 0

    #Adds a single vote to the candidate's vote tally
    def addVote(self):
        self.__votes += 1
        self.__displayVotes = self.__votes
    
    #Adds a variable number of votes to a candidate's tally. Intended for use with fractional votes.
    def addVotes(self, f):
        self.__votes += f
        self.__displayVotes = self.__votes
    
    #Sets the displayed vote tally for a candidate, if needs to be different from the actual vote tally.
    def setDisplayVotes(self, f):
        self.__displayVotes = f

    #Shows the displayed vote tally for a candidate, if needs to be different from the actual vote tally.
    def getDisplayVotes(self):
        return self.__displayVotes
    
    #Reflects whether a candidate is elected or not.
    def isElected(self):
        return self.__isElected

    #Checks whether a candidate has reached the required threshold of votes to be elected. Returns true if they have and false otherwise.
    def checkElected(self, electThreshold):
        if self.__votes > electThreshold or self.__isElected:
            self.__isElected = True
            return True
        return False
    
    #Determines the number of surplus votes that the candidate has above the election threshold
    def getVoteSurplus(self, electThreshold):
        return self.__votes - electThreshold

    # Returns the percentage of an elected candidate's votes that should be redistributed to the next candodate
    def getExtraVotePercent(self, electThreshold): 
        redistPercent = float(self.getVoteSurplus(electThreshold) / self.__votes)
        return redistPercent

    #Eliminates the candidate
    def eliminate(self):
        self.__isEliminated = True
        candidates.remove(self)
    
    #Reflect whether the candidate is eliminated
    def isEliminated(self):
        return self.__isEliminated

    #Displays the candidate in the following format
    # Name: votes   ELECTED   ELIMINATED
    def __str__(self):
        returnstr =  "{:s}: {:2f}".format(self.getName(), self.getDisplayVotes())
        if self.isElected():
            returnstr += "\t ELECTED"
        if self.isEliminated():
            returnstr += "\t ELIMINATED"
        return returnstr

#List all non-eliminated candidates
def printAllCandidates():
    candStr = ""
    for i in range(numCands):
        candStr += str(i + 1) + ". " + candidates[i].getName() + "     "
    print(candStr)

#List all non-eliminated candidates, including vote tallies
def printCandidateVotes():
    candStr = ""
    for i in range(len(candidates)):
        candStr += str(i + 1) + ". " + str(candidates[i]) + "\n"
    print(candStr)

#List all  candidates, including vote tallies
def printAllCandidateVotes():
    candStr = ""
    for i in range(numCands):
        candStr += str(i + 1) + ". " + str(allCandidates[i]) + "\n"
    print(candStr)

#Seach candidates for one with a specific name
def searchCandidates(name):
    for candidate in candidates:
        if name == candidate.getName(): 
            return candidate
    return False

#Checks to make sure that all rankings in a ballot correspond to a candidate
def checkValidBallot(ballot):
    ranking = ballot.split(', ')
    for candidate in ranking:
        if searchCandidates(candidate) == False: 
            return False
    return True

#Tallys all votes and runs the single transferable vote process
def tallyVotes(totalVotes):
    print("\n\n~~~~~VOTE TALLIES~~~~~")
    electThreshold = float(totalVotes * electPercent)
    print("Ballots will now be tabulated. In order to be elected, a candidate must recieve at least {:2f} votes. {:n} ballots have been cast.".format(electThreshold, totalVotes))
    with open(filename, 'r') as ballots:
        votes = ballots.readlines()
    candidatesElected = 0
    candidatesRemaining = len(candidates)
    round = 1
    while candidatesRemaining > 0:
        for candidate in candidates:
            if not candidate.isElected():
                candidate.resetVotes()
        for ballot in votes:
            fraction = 1.0
            for rank in ballot.split(', '):
                candidate = searchCandidates(rank)
                if candidate != False and not candidate.isElected() and not candidate.isEliminated():
                    if fraction != 1.0:
                        candidate.addVotes(fraction)
                    else:
                        candidate.addVote()
                    break
                elif candidate != False and candidate.isElected() and fraction == 1.0:
                    fraction = candidate.getExtraVotePercent(electThreshold)
                    
        candidates.sort(key=lambda x: x.getVotes(), reverse=True)
        allCandidates.sort(key=lambda x: x.getVotes(), reverse=True)
        print("ROUND {:n} VOTES:".format(round))
        print("{:n} candidates have been elected. There are {:n} candidates remaining.".format(candidatesElected, candidatesRemaining))
        printCandidateVotes()
        round += 1
        for candidate in allCandidates:
            if candidatesElected < seatNum and not candidate.isElected() and candidate.checkElected(electThreshold):
                print("{:s} has been elected with {:2f} votes. Their {:2f} surplus votes will be redistributed to other candidates in later rounds.".format(candidate.getName(), candidate.getVotes(), candidate.getVoteSurplus(electThreshold)))
                candidate.setDisplayVotes(electThreshold)
                candidatesElected += 1
                candidatesRemaining -= 1
                break
            if not candidate.isElected() and not candidate.isEliminated() and candidate == candidates[len(candidates)-1]:
                candidate.eliminate()
                candidatesRemaining -=1
                print("{:s} has been eliminated. Their {:2f} votes will be redistributed to other candidates in later rounds.".format(candidate.getName(), candidate.getVotes()))
        input("Press any key to advance to the next round of vote tabulation.\n") 

#Collects votes until told to stop
def getVotes():
    totalVotes = 0
    print("\n\n~~~~~ENTER VOTES~~~~~")
    print("Each candidate is listed here by name. Please list as many candidates as you wish separated by commas, in order of most desired to least. For example, a ballot might look like this for an election with five candidates:\nJohn Doe, James Roe, Theodore Roosevelt, Steve Jobs, Albert Einstein")
    with open(filename, 'w', newline='') as ballots:
        while True:
            printAllCandidates()
            ballot = str(input()).lower()
            while not checkValidBallot(ballot) and not ballot == "quit":
                print("Your ballot has an error, please re-enter your votes:")
                ballot = str(input()).lower()
            if ballot == "quit":
                break
            ballots.write(ballot + "\n")
            totalVotes += 1
    return totalVotes

#Gets the final printout of votes
def getFinalPrintout():
    printout = "Candidates "
    for candidate in candidates:
        if candidate == candidates[len(candidates) - 1]:
            printout += "and " + candidate.getName()
        else:
            printout += candidate.getName() + ", "
    printout += " have been elected. Thank you for using this Single Transferable Vote simulator."
    return printout

if __name__ == "__main__":
    print("Welcome to @Benjome's Single Transferable Vote calculator!")
    print("~~~~~ELECTION SETUP~~~~~")
    name = str(input("Give a Name for this Election: \n"))
    filename = "elections/" +  name.lower() + ".csv"
    numCands = int(input("Enter Number of Candidates: \n"))
    seatNum = int(input("Enter Number of Seats: \n"))
    candidates = list()
    
    electPercent = 1 / (float)(seatNum + 1)
    
    for i in range(numCands):
        candidates.append(Candidate(input("Enter name of candidate " + str(i + 1) + "\n")))
    allCandidates = candidates.copy()

    totalVotes = getVotes()

    tallyVotes(totalVotes)
    allCandidates.sort(key=lambda x: x.getVotes(), reverse=True)
    print("The final tally of the election is:")
    printAllCandidateVotes()
    print(getFinalPrintout())
    
    

         