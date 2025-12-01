class TennisGame:
    #tämän idean sain AI:lta, scoret listassa mistä niitä voi hakea listan indeksien avulla
    Score_names = ["Love", "Fifteen", "Thirty", "Forty"]

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.m_score1 += 1
        else:
            self.m_score2 += 1

    def get_score(self):
        if self.m_score1 == self.m_score2:
            return self.equal_score()

        if self.m_score1 >= 4 or self.m_score2 >= 4:
            return self.advantage_or_win()

        return f"{self.Score_names[self.m_score1]}-{self.Score_names[self.m_score2]}"

    def equal_score(self):
        if self.m_score1 < 3:
            return f"{self.Score_names[self.m_score1]}-All"
        return "Deuce"

    def advantage_or_win(self):
        score_diff = self.m_score1 - self.m_score2
        if score_diff == 1:
            return "Advantage " + self.player1_name
        if score_diff == -1:
            return "Advantage " + self.player2_name
        if score_diff >= 2:
            return "Win for " + self.player1_name
        return "Win for " + self.player2_name