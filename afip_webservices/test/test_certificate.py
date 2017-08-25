# -*- coding: utf-8 -*-
import unittest
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))
from wsaa import certificate


class TestCertificate(unittest.TestCase):

    def test_key(self):
        key = certificate.WsaaPrivateKey()
        key.generate_rsa_key()

    def test_invalid_values(self):
        key = certificate.WsaaPrivateKey()
        key.generate_rsa_key()
        cert = certificate.WsaaCertificate(key)
        with self.assertRaises(AttributeError):
            cert.validate_values()

    def test_certificate_request(self):
        key = certificate.WsaaPrivateKey()
        key.generate_rsa_key()
        cert = certificate.WsaaCertificate(key.key)

        # Seteamos valores al certificado
        cert.country_code = 'AR'
        cert.state_name = 'Buenos Aires'
        cert.company_name = 'OpenPyme S.R.L.'
        cert.company_vat = '30709612312'
        cert.generate_certificate_request()

