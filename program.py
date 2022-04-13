#-------------------------------------
# Single Transferable Vote Calculator
#             Version 1.1
#         Ben Boardman (@Benjome)
#            12 April 2022
#-------------------------------------

#A memory object to store a candidate
class Candidate:
    candidates = list()
    allCandidates = list()
    numCands = 0

    # Initializes candidate with a name, all other values set to defaults
    def __init__(self, name):
        self.__name = name
        self.__votes = 0.0
        self.__isElected = False
        self.__isEliminated = False
        self.__displayVotes = 0.0
        Candidate.candidates.append(self)
        Candidate.allCandidates.append(self)
        Candidate.numCands += 1

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
        Candidate.candidates.remove(self)
        Candidate.numCands -= 1
    
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

    #Seach candidates for one with a specific name
    def searchCandidates(name):
        for candidate in Candidate.candidates:
            if name == candidate.getName().lower(): 
                return candidate
        return False
    
    #Sorts all candidates by total votes, from most to least
    def sort():
        Candidate.candidates.sort(key=lambda x: x.getVotes(), reverse=True)
        Candidate.allCandidates.sort(key=lambda x: x.getVotes(), reverse=True)
    
    #List all candidates, including vote tallies
    def printAllVotes():
        candStr = ""
        for i in range(len(Candidate.allCandidates)):
            candStr += str(i + 1) + ". " + str(Candidate.allCandidates[i]) + "\n"
        print(candStr)

    #List all non-eliminated candidates, including vote tallies
    def printVotes():
        candStr = ""
        for i in range(Candidate.numCands):
            candStr += str(i + 1) + ". " + str(Candidate.candidates[i]) + "\n"
        print(candStr)

        #Gets the final printout of votes
    
    #List all non-eliminated candidates
    def printAllCandidates():
        candStr = ""
        for i in range(Candidate.numCands):
            candStr += str(i + 1) + ". " + Candidate.candidates[i].getName() + "     "
        print(candStr)
    
    def finalPrint():
        printout = "Candidates "
        for candidate in Candidate.candidates:
            if candidate == Candidate.candidates[Candidate.numCands - 1]:
                printout += "and " + candidate.getName()
            else:
                printout += candidate.getName() + ", "
        printout += " have been elected. Thank you for using this Single Transferable Vote simulator."
        print(printout)

class Ballot:
    totalBallots = 0
    ballots = list()

    def __init__(self, votes):
        self.__votes = votes
        self.__rank = 0
        self.__voteRemaining = 1.0
        Ballot.totalBallots += 1
        Ballot.ballots.append(self)
    
    def getTally(self):
        return self.__votes
    
    def checkValid():
        for candidate in Ballot.ballots[Ballot.totalBallots - 1].getTally():
            if Candidate.searchCandidates(candidate) == False: 
                return False
            return True
    
    #Collects votes until told to stop
    def getVotes():
        print("\n\n~~~~~ENTER VOTES~~~~~")
        print("Each candidate is listed here by name. Please list as many candidates as you wish separated by commas, in order of most desired to least. For example, a ballot might look like this for an election with five candidates:\nJohn Doe, James Roe, Theodore Roosevelt, Steve Jobs, Albert Einstein")
        print("To stop entering ballots, enter 'QUIT'")
        while True:
            Candidate.printAllCandidates()
            ballot = str(input()).lower()
            Ballot(ballot.split(', '))
            while not Ballot.checkValid() and not ballot == "\'quit\'":
                Ballot.ballots.pop(Ballot.totalBallots - 1)
                Ballot.totalBallots -= 1
                print("Your ballot has an error, please re-enter your votes:")
                ballot = str(input()).lower()
                Ballot(ballot.split(', '))
            if ballot == "\'quit\'":
                Ballot.ballots.pop(Ballot.totalBallots - 1)
                Ballot.totalBallots -= 1
                break


#Tallys all votes and runs the single transferable vote process
def tallyVotes():
    print("\n\n~~~~~VOTE TALLIES~~~~~")
    electThreshold = float(Ballot.totalBallots * electPercent)
    print("Ballots will now be tabulated. In order to be elected, a candidate must recieve at least {:2f} votes. {:n} ballots have been cast.".format(electThreshold, Ballot.totalBallots))
    
    candidatesElected = 0
    candidatesRemaining = Candidate.numCands
    round = 1
    while candidatesRemaining > 0:
        for candidate in Candidate.candidates:
            if not candidate.isElected():
                candidate.resetVotes()
        for ballot in Ballot.ballots:
            fraction = 1.0
            for rank in ballot.getTally():
                candidate = Candidate.searchCandidates(rank)
                if candidate != False and not candidate.isElected() and not candidate.isEliminated():
                    if fraction != 1.0:
                        candidate.addVotes(fraction)
                    else:
                        candidate.addVote()
                    break
                elif candidate != False and candidate.isElected() and fraction == 1.0:
                    fraction = candidate.getExtraVotePercent(electThreshold)
                    
        Candidate.sort()
        print("ROUND {:n} VOTES:".format(round))
        print("{:n} candidates have been elected. There are {:n} candidates remaining.".format(candidatesElected, candidatesRemaining))
        Candidate.printVotes()
        round += 1
        for candidate in Candidate.allCandidates:
            if candidatesElected < seatNum and not candidate.isElected() and candidate.checkElected(electThreshold):
                print("{:s} has been elected with {:2f} votes. Their {:2f} surplus votes will be redistributed to other candidates in later rounds.".format(candidate.getName(), candidate.getVotes(), candidate.getVoteSurplus(electThreshold)))
                candidate.setDisplayVotes(electThreshold)
                candidatesElected += 1
                candidatesRemaining -= 1
                break
            if not candidate.isElected() and not candidate.isEliminated() and candidate == Candidate.candidates[Candidate.numCands - 1]:
                candidate.eliminate()
                candidatesRemaining -=1
                print("{:s} has been eliminated. Their {:2f} votes will be redistributed to other candidates in later rounds.".format(candidate.getName(), candidate.getVotes()))
        input("Press any key to advance to the next round of vote tabulation.\n") 
    return 0

if __name__ == "__main__":
    print("Welcome to @Benjome's Single Transferable Vote calculator!")
    print("~~~~~ELECTION SETUP~~~~~")
    name = str(input("Give a Name for this Election: \n"))
    filename = "elections/" +  name.lower() + ".csv"
    numCands = int(input("Enter Number of Candidates: \n"))
    seatNum = int(input("Enter Number of Seats: \n"))
    
    electPercent = 1 / (float)(seatNum + 1)
    
    for i in range(numCands):
        Candidate(input("Enter name of candidate " + str(i + 1) + "\n"))

    Ballot.getVotes()
    tallyVotes()
    Candidate.sort()
    print("The final tally of the election is:")
    Candidate.printAllVotes()
    Candidate.finalPrint()