import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
    
    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 11.0)
        
    def test_rahan_ottaminen_vahentaa_saldoa_jos_rahaa_on_tarpeeksi(self):
        onnistuu = self.maksukortti.ota_rahaa(400)
        self.assertTrue(onnistuu)
        self.assertEqual(self.maksukortti.saldo_euroina(), 6.0)

    def test_rahan_ottaminen_ei_vahenna_saldoa_jos_rahaa_ei_ole_tarpeeksi(self):
        onnistuu = self.maksukortti.ota_rahaa(2000)
        self.assertFalse(onnistuu)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
