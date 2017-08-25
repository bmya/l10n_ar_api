# -*- coding: utf-8 -*-
import unittest
import files
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from wsaa import wsaa
from wsaa.tokens import AccessRequerimentToken, AccessToken


class TestWsaa(unittest.TestCase):

    @staticmethod
    def _create_wsfe_tra():
        token = AccessRequerimentToken('wsfe')
        signed_tra = token.sign_tra(files.private_key, files.certificate) 
        
        return signed_tra
    
    def test_tra(self):
        self._create_wsfe_tra()
    
    def test_access_token(self):
        
        # Logeo
        tra = self._create_wsfe_tra()
        wsaa_test = wsaa.Wsaa()
        login_fault = wsaa_test.login(tra)     

        # Token
        token = AccessToken()
        token.create_token_from_login(login_fault)
