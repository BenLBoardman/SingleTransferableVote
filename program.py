#-------------------------------------
# Single Transferable Vote Calculator
#             Version 1.2.2
#         Ben Boardman (@Benjome)
#            13 April 2022
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
    def getAllVotes():
        candStr = ""
        for i in range(len(Candidate.allCandidates)):
            candStr += str(i + 1) + ". " + str(Candidate.allCandidates[i]) + "\n"
        return candStr

    #List all non-eliminated candidates, including vote tallies
    def getCandVotes():
        candStr = ""
        for i in range(Candidate.numCands):
            candStr += str(i + 1) + ". " + str(Candidate.candidates[i]) + "\n"
        return candStr
    
    #List all non-eliminated candidates
    def getAllCandidates():
        candStr = ""
        for i in range(Candidate.numCands):
            candStr += str(i + 1) + ". " + Candidate.candidates[i].getName() + "     "
        return candStr
    
    #Gets the final printout of votes
    def finalPrint():
        printout = "The final tally of the election is:\n"
        Candidate.allCandidates.sort(key=lambda x: x.isElected(), reverse=True)
        for candidate in Candidate.allCandidates:
            printout += candidate.getName()
            if candidate.isElected():
                printout += ":\t ELECTED\n"
            if candidate.isEliminated():
                printout += ":\t ELIMINATED\n"
        printout += "\nCandidates "
        for candidate in Candidate.candidates:
            if candidate == Candidate.candidates[Candidate.numCands - 1]:
                printout += "and " + candidate.getName()
            else:
                printout += candidate.getName() + ", "
        printout += " have been elected. Thank you for using this Single Transferable Vote simulator."
        return printout

#Represents a ballot in memory
class Ballot:
    totalBallots = 0
    ballots = list()

    #Initializes a ballot given a list of candidate names
    def __init__(self, votes):
        self.__candidate = None
        self.__votes = votes
        self.__rank = 0
        self.__voteRemaining = 1.0
        Ballot.totalBallots += 1
        Ballot.ballots.append(self)
    
    #Sets the current candidate to which the ballot is located
    def setCandidate(self, candidate):
        self.__candidate = candidate
    
    #Returns the first non-eliminated, non-elected candidate 
    def get(self):
        return self.__votes[self.__rank]

    #Increments the ballot to look at the next candidate in rank
    def increment(self):
        self.__rank += 1

    #Returns the current candidate to which the ballot is located
    def getCandidate(self):
        return self.__candidate

    #Returns the list of votes in order
    def getTally(self):
        return self.__votes
    
    #Return the voting power the ballot has remaining
    def getRemaining(self):
        return self.__voteRemaining
    
    #Set the voting power the ballot has remaining
    def setRemaining(self, f):
        self.__voteRemaining = f

    #Checks whether a ballot lists valid candidates
    def checkValid():
        for candidate in Ballot.ballots[Ballot.totalBallots - 1].getTally():
            if Candidate.searchCandidates(candidate) == False: 
                return False
            return True
    
    #Add a ballot, given a string representation of the ballot's votes
    def addBallot(ballot):
        Ballot(ballot.split(', '))
        while not Ballot.checkValid():
            Ballot.ballots.pop(Ballot.totalBallots - 1)
            Ballot.totalBallots -= 1
            print("Your ballot has an error, please re-enter your votes:")
            ballot = str(input()).lower()
            Ballot(ballot.split(', '))
        log.write("{:n}.\t{:s}\n".format(Ballot.totalBallots, ballot))

    #Collects votes until told to stop
    def getVotes():
        log.write("\n\n~~~~~BALLOTS~~~~~\n")
        print("\n\n~~~~~ENTER VOTES~~~~~")
        print("Each candidate is listed here by name. Please list as many candidates as you wish separated by commas, in order of most desired to least. For example, a ballot might look like this for an election with five candidates:\nJohn Doe, James Roe, Theodore Roosevelt, Steve Jobs, Albert Einstein")
        print("To stop entering ballots, enter 'QUIT'. To enter multiple ballot mode, enter 'BLOCK'.")
        while True:
            print(Candidate.getAllCandidates())
            ballot = str(input()).lower()
            if ballot == "'block'":
                print("You have entered multiple ballot mode. The next input window will allow you to enter as many ballots as you like. Separate ballots using the TAB key.")
                ballots = str(input()).lower().split("\t")
                for ballot in ballots:
                    Ballot.addBallot(ballot)
            elif ballot == "'quit'":
                break
            else:
                Ballot.addBallot(ballot)

#Tallies all votes and runs the single transferable vote process
def tallyVotes():
    print("\n\n~~~~~VOTE TABULATION~~~~~")
    log.write("\n\n~~~~~VOTE TABULATION~~~~~")
    electThreshold = float(Ballot.totalBallots * electPercent)
    print("Ballots will now be tabulated. In order to be elected, a candidate must recieve at least {:2f} votes. {:n} ballots have been cast.".format(electThreshold, Ballot.totalBallots))
    log.write("\nBallots will now be tabulated. In order to be elected, a candidate must recieve at least {:2f} votes. {:n} ballots have been cast.".format(electThreshold, Ballot.totalBallots))

    candidatesElected = 0
    candidatesRemaining = Candidate.numCands
    round = 1
    while candidatesRemaining > 0:
        for ballot in Ballot.ballots:
            while True:
                candidate = Candidate.searchCandidates(ballot.get())
                if candidate.isEliminated():
                    ballot.increment()
                elif candidate.isElected():
                    ballot.setRemaining(candidate.getExtraVotePercent(electThreshold))
                    ballot.increment()
                else:
                    break
            if not ballot.getCandidate() == candidate:
                ballot.setCandidate(candidate)
                candidate.addVotes(ballot.getRemaining())  
             
               
        Candidate.sort()
        print("\n~~~ROUND {:n} VOTES~~~".format(round))
        log.write("\n~~~ROUND {:n} VOTES~~~".format(round))
        print("{:n} candidates have been elected. There are {:n} candidates remaining.".format(candidatesElected, candidatesRemaining))
        log.write("\n{:n} candidates have been elected. There are {:n} candidates remaining.\n".format(candidatesElected, candidatesRemaining))
        log.write(Candidate.getCandVotes())
        print(Candidate.getCandVotes())
        round += 1
        for candidate in Candidate.allCandidates:
            if candidatesElected < seatNum and not candidate.isElected() and candidate.checkElected(electThreshold):
                print("{:s} has been elected with {:2f} votes. Their {:2f} surplus votes will be redistributed to other candidates in later rounds.".format(candidate.getName(), candidate.getVotes(), candidate.getVoteSurplus(electThreshold)))
                log.write("\n{:s} has been elected with {:2f} votes. Their {:2f} surplus votes will be redistributed to other candidates in later rounds.".format(candidate.getName(), candidate.getVotes(), candidate.getVoteSurplus(electThreshold)))
                candidate.setDisplayVotes(electThreshold)
                candidatesElected += 1
                candidatesRemaining -= 1
                break
            if not candidate.isElected() and not candidate.isEliminated() and (candidate == Candidate.candidates[Candidate.numCands - 1] or candidatesElected == seatNum):
                candidate.eliminate()
                candidatesRemaining -=1
                print("{:s} has been eliminated. Their {:2f} votes will be redistributed to other candidates in later rounds.".format(candidate.getName(), candidate.getVotes()))
                log.write("\n{:s} has been eliminated. Their {:2f} votes will be redistributed to other candidates in later rounds.".format(candidate.getName(), candidate.getVotes()))
        input("Press any key to advance to the next round of vote tabulation.") 
    return 0

if __name__ == "__main__":
    print("Welcome to @Benjome's Single Transferable Vote calculator!")
    print("~~~~~ELECTION SETUP~~~~~")
    name = str(input("Give a Name for this Election: \n"))
    filename = 'SingleTransferableVote\elections\{:s}.txt'.format(name.lower())
    with open(filename, 'w') as log:
        numCands = int(input("Enter Number of Candidates: \n"))
        seatNum = int(input("Enter Number of Seats: \n"))
        log.write("ELECTION " + name.upper() + "\n")
        log.write("{:n} candidates      {:n} seats\n".format(numCands, seatNum))
        electPercent = 1 / (float)(seatNum + 1)
    
        for i in range(numCands):
            Candidate(input("Enter name of candidate " + str(i + 1) + "\n"))
        log.write("Candidates:\t\t{:s}".format(Candidate.getAllCandidates()))
        Ballot.getVotes()
        tallyVotes()

        log.write("\n" + Candidate.finalPrint())
        print(Candidate.finalPrint())
