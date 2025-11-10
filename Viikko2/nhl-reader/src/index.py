from rich.console import Console
from rich.table import Table

import player_reader
import player_stats

def create_table(top_players,wanted_nationality,wanted_season):

    table = Table(title=f"Top Scorers from {wanted_nationality} in {wanted_season}")
    table.add_column("Player", justify="right", style="cyan")
    table.add_column("Teams", style="magenta")
    table.add_column("Goals", justify="right", style="green")
    table.add_column("Assists", justify="right", style="green")
    table.add_column("Total Points", justify="right", style="green")

    for player in top_players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.points))
    return table

def questions():

    print("Give 3 letter acronym (ALL CAPS) for nationality (FIN, SWE, CAN etc.) of players you want to find")
    wanted_nationality = input("Nationality:")
    print("Give a season you want to find players from (e.g., 2024-25), only following seasons available 2018-19, 2019-20, 2020-21, 2021-22, 2022-23, 2023-24, 2024-25, 2025-26")
    wanted_season = input("Season:")
    return wanted_nationality, wanted_season

def main():

    wanted_nationality,wanted_season = questions()

    url = f"https://studies.cs.helsinki.fi/nhlstats/{wanted_season}/players"
    reader = player_reader.PlayerReader(url)

    players = reader.get_players()
    stats = player_stats.PlayerStats()
    top_players = stats.top_scorers_by_nationality(players, wanted_nationality)

    table = create_table(top_players,wanted_nationality,wanted_season)
    console = Console()
    console.print(table)

if __name__ == "__main__":
    main()
