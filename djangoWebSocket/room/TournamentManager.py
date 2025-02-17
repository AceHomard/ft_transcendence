from room.Tournament import Tournament


class TournamentManager:
    def __init__(self):
        self.tournaments = []

    def createTournament(self):
        tournament = Tournament()
        self.tournaments.append(tournament)
        return tournament.getId()

    def removeTournamentById(self, tournamentId):
        if self.isTournamentIdExist(tournamentId):
            self.getTournamentById(tournamentId).leaveAllPlayers()
        initial_len = len(self.tournaments)
        self.tournaments = [tournament for tournament in self.tournaments if tournament.getId() != tournamentId]
        if len(self.tournaments) == initial_len:
            return False
        return True

    def getTournaments(self):
        return self.tournaments

    def isTournamentIdExist(self, tournamentId):
        for tournament in self.tournaments:
            if tournament.getId() == tournamentId:
                return True
        return False

    def getTournamentById(self, tournamentId):
        for tournament in self.tournaments:
            if tournament.getId() == tournamentId:
                return tournament
        return False

    def getWaitingTournament(self):
        for tournament in self.tournaments:
            if tournament.isWaiting():
                return tournament.getId()
        return False


tournament_manager = TournamentManager()
