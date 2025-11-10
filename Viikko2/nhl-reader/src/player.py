class Player:
    def __init__(self, data):

        self.name = data['name']
        self.nationality = data['nationality']
        self.assists = data['assists']
        self.goals = data['goals']
        self.team = data['team']
        self.points = data['assists'] + data['goals']

    def __str__(self):
        return f"{self.name} Team: {self.team} Goals: {self.goals} Assists: {self.assists} ,Points: {self.points}"
    def wtf_do_i_need_forced_amount_of_methods_for(self):
        print("this is dumb AF")
