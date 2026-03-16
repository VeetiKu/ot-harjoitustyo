import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):

    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_kassassa_rahaa_alussa_oikein(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_lounaita_ei_ole_myyty_alussa(self):
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_edullinen_kateisosto_toimii_oikein(self):
        vaihtoraha = self.kassa.syo_edullisesti_kateisella(400)
        self.assertEqual(vaihtoraha, 160)
        self.assertEqual(self.kassa.kassassa_rahaa, 100240)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_edullinen_kateisosto_ei_toimi_jos_raha_ei_riita(self):
        vaihtoraha = self.kassa.syo_edullisesti_kateisella(200)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(self.kassa.edulliset, 0)

    def test_maukas_kateisosto_toimii(self):
        vaihtoraha = self.kassa.syo_maukkaasti_kateisella(450)
        self.assertEqual(vaihtoraha, 50)
        self.assertEqual(self.kassa.kassassa_rahaa, 100400)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_maukas_kateisosto_ei_toimi_jos_raha_ei_riita(self):
        vaihtoraha = self.kassa.syo_maukkaasti_kateisella(300)
        self.assertEqual(vaihtoraha, 300)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_edullinen_korttiosto_toimii(self):
        onnistui = self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertTrue(onnistui)
        self.assertEqual(self.kortti.saldo, 760)
        self.assertEqual(self.kassa.edulliset, 1)

    def test_edullinen_korttiosto_ei_toimi_jos_saldo_ei_riita(self):
        kortti = Maksukortti(200)
        onnistui = self.kassa.syo_edullisesti_kortilla(kortti)
        self.assertFalse(onnistui)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(self.kassa.edulliset, 0)

    def test_maukas_korttiosto_toimii(self):
        onnistui = self.kassa.syo_maukkaasti_kortilla(self.kortti)
        self.assertTrue(onnistui)
        self.assertEqual(self.kortti.saldo, 600)
        self.assertEqual(self.kassa.maukkaat, 1)

    def test_maukas_korttiosto_ei_toimi_jos_saldo_ei_riita(self):
        kortti = Maksukortti(300)
        onnistui = self.kassa.syo_maukkaasti_kortilla(kortti)
        self.assertFalse(onnistui)
        self.assertEqual(kortti.saldo, 300)
        self.assertEqual(self.kassa.maukkaat, 0)

    def test_korttiosto_ei_muuta_kassan_rahaa(self):
        self.kassa.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)

    def test_kortille_lataaminen_kasvattaa_saldoa_ja_kassaa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kortti.saldo, 1500)
        self.assertEqual(self.kassa.kassassa_rahaa, 100500)
        
    def test_kortille_ei_voi_ladata_negatiivista_summaa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kortti.saldo, 1000)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        
    def test_kassassa_rahaa_euroina(self):
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1000.0)