import unittest
from unittest.mock import Mock
from kauppa import Kauppa
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()

        
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10

        
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "juusto", 3)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

    def test_yhden_tuotteen_ostos(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_kaksi_eri_tuotetta(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("eki", "12323")

        
        self.pankki_mock.tilisiirto.assert_called_with("eki", 42, "12323", "33333-44455", 8)

    def test_kaksi_samaa_tuotetta(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("olli", "99999")

        
        self.pankki_mock.tilisiirto.assert_called_with("olli", 42, "99999", "33333-44455", 10)

    def test_yksi_tuote_loppu_yhta_loytyy(self):
        
        def varasto_saldo_override(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0

        self.varasto_mock.saldo.side_effect = varasto_saldo_override

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("jori", "12345")

        
        self.pankki_mock.tilisiirto.assert_called_with("jori", 42, "12345", "33333-44455", 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen(self):
       
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("asiakas1", "tili1")

        
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("asiakas2", "tili2")

        
        self.pankki_mock.tilisiirto.assert_called_with("asiakas2", 42, "tili2", "33333-44455", 3)

    def test_uusi_viite_jokaiselle_maksutapahtumalle(self):
        
        self.viitegeneraattori_mock.uusi.side_effect = [101, 102]

        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("eka", "t1")

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("toka", "t2")

        
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

        # 001 -> ekan kutsun toinen parametri, 101 -> toisen kutsun toinen parametri
        # call_args_list -> kutsujen lista
        calls = self.pankki_mock.tilisiirto.call_args_list
        self.assertEqual(calls[0][0][1], 101)
        self.assertEqual(calls[1][0][1], 102)

    def test_poista_korista_palauttaa_varastoon(self):
        kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.poista_korista(1)
        self.varasto_mock.palauta_varastoon.assert_called_with(Tuote(1, "maito", 5))
