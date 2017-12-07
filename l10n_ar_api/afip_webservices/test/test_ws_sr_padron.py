# -*- coding: utf-8 -*-
import pytest
import sys
sys.path.append("..")
import ws_sr_padron
import wsaa
import files


class TestWsSrPadron:

    @pytest.fixture(scope="module")
    def ws_sr_padron_test(self):
        # Logeo
        token = wsaa.tokens.AccessRequerimentToken('ws_sr_padron_a4')
        signed_tra = token.sign_tra(files.private_key, files.certificate)
        wsaa_test = wsaa.wsaa.Wsaa()
        login_fault = wsaa_test.login(signed_tra)

        # Token
        token = wsaa.tokens.AccessToken()
        token.create_token_from_login(login_fault)
        return ws_sr_padron.ws_sr_padron.WsSrPadron(token, '20362889406')

    def test_get_persona(self, ws_sr_padron_test):
        #response = ws_sr_padron_test.get_partner_data('30712097953')
        #1assert response.getPersonaResponse.persona.idPersona == '30712097953'
        response = ws_sr_padron_test.get_partner_data(20000000516)
        assert response.persona
