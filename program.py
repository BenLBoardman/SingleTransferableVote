#-------------------------------------
# Single Transferable Vote Calculator
#             Version 1.0
#         Ben Boardman (@Benjome)
#            12 April 2022
#-------------------------------------

class Candidate:
    def __init__(self, name):
        self.__name = name.lower()
        self.__votes = 0.0
        self.__isElected = False
        self.__isEliminated = False
        self.__displayVotes = 0.0

    def getName(self):
        return self.__name
    
    def getVotes(self):
        return self.__votes

    def resetVotes(self):
        self.__votes = 0

    def addVote(self):
        self.__votes += 1
        self.__displayVotes = self.__votes
    
    def addVotes(self, f):
        self.__votes += f
        self.__displayVotes = self.__votes
    
    def setDisplayVotes(self, f):
        self.__displayVotes = f

    def getDisplayVotes(self):
        return self.__displayVotes
    
    def isElected(self):
            return self.__isElected

    def checkElected(self, electThreshold):
        if self.__votes > electThreshold or self.__isElected:
            self.__isElected = True
            return True
    
    def getVoteSurplus(self, electThreshold):
        return self.__votes - electThreshold

    # Returns the percentage of an elected candidate's votes that should be redistributed to the next candodate
    def getExtraVotePercent(self, electThreshold): 
        redistPercent = float(self.getVoteSurplus(electThreshold) / self.__votes)
        return redistPercent

    def eliminate(self):
        self.__isEliminated = True
        candidates.remove(self)
    
    def isEliminated(self):
        return self.__isEliminated

    def __str__(self):
        returnstr =  "{:s}: {:2f}".format(self.getName(), self.getDisplayVotes())
        if self.isElected():
            returnstr += "\t ELECTED"
        if self.isEliminated():
            returnstr += "\t ELIMINATED"
        return returnstr

def printAllCandidates():
    candStr = ""
    for i in range(numCands):
        candStr += str(i + 1) + ". " + candidates[i].getName() + "     "
    print(candStr)

def printCandidateVotes():
    candStr = ""
    for i in range(len(candidates)):
        candStr += str(i + 1) + ". " + str(candidates[i]) + "\n"
    print(candStr)

def printAllCandidateVotes():
    candStr = ""
    for i in range(numCands):
        candStr += str(i + 1) + ". " + str(allCandidates[i]) + "\n"
    print(candStr)


def searchCandidates(name):
    for candidate in candidates:
        if name == candidate.getName(): 
            return candidate
    return False

def checkValidBallot(ballot):
    ranking = ballot.split(', ')
    for candidate in ranking:
        if searchCandidates(candidate) == False: 
            return False
    return True

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
        print("ROUND {:n} VOTES:".format(round))
        print("{:n} candidates have been elected. There are {:n} candidates remaining.".format(candidatesElected, candidatesRemaining))
        printCandidateVotes()
        round += 1
        for candidate in candidates:
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
    
    

         