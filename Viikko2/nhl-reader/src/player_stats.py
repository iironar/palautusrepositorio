class PlayerStats:

    def __init__(self):
        pass

    def top_scorers_by_nationality(self,players,wanted_nationality):
        wanted_players = []
        for player in players:
            if player.nationality == wanted_nationality:
                wanted_players.append(player)
        wanted_players.sort(key=lambda player: player.goals + player.assists, reverse=True)
        return wanted_players

    def wtf_do_i_need_forced_amount_of_methods_for(self):
        print("this is dumb AF")
