import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]
        
        
class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_pelaajan_etsintä_toimii(self):
        player = self.stats.search("Kurri")
        self.assertEqual(player.name, "Kurri")

    def test_pelaajan_etsintä_palauttaa_none(self):
        player = self.stats.search("oasdasd")
        self.assertIsNone(player)

    def test_joukkueen_pelaajien_haku_toimii(self):
        joukkue = self.stats.team("EDM")
        pelaajat = [pelaaja.name for pelaaja in joukkue]
        
        self.assertCountEqual(pelaajat, ["Semenko", "Kurri", "Gretzky"])

    def test_joukkuehaku_palauttaa_tyhjän(self):
        joukkue = self.stats.team("3saasdasd")
        self.assertEqual(joukkue, [])

    def test_top_pisteet_toimii_oikein(self):

        top_viisi = self.stats.top(4, SortBy.POINTS)
        self.assertEqual([pelaaja.name for pelaaja in top_viisi], ["Gretzky", "Lemieux", "Yzerman", "Kurri", "Semenko"])

    def test_top_järjestetään_tarkoituksenmukaisesti_goals(self):
       
        top_viisi = self.stats.top(4,SortBy.GOALS)
        self.assertEqual([pelaaja.name for pelaaja in top_viisi], ["Lemieux", "Yzerman", "Kurri", "Gretzky", "Semenko"])

    def test_top_järjestetään_tarkoituksenmukaisesti_assists(self):
        
        top_viisi = self.stats.top(4, SortBy.ASSISTS)
        self.assertEqual([pelaaja.name for pelaaja in top_viisi], ["Gretzky", "Yzerman", "Lemieux", "Kurri", "Semenko"])


