# -*- coding: utf-8 -*-
import pytest
import sys, os
from datetime import date
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
import wsfex
import wsaa
import files
import copy


class TestWsfe:
    
    @pytest.fixture(scope="module")
    def item_test(self):
        item = wsfex.invoice.ExportationElectronicInvoiceItem("Item")
        item.quantity = 2
        item.measurement_unit = 7
        item.unit_price = 2500
        item.bonification = 0.0

        return item
    
    @pytest.fixture
    def invoice_test(self):  
        invoice_test = wsfex.invoice.ExportationElectronicInvoice(19)     
        invoice_test.document_date = date.today()
        invoice_test.exportation_type = 1
        invoice_test.existent_permission = "N"
        invoice_test.destiny_country = 200
        invoice_test.destiny_country_cuit = 27252262070
        invoice_test.customer_name = "Perez Jose"
        invoice_test.customer_address = "Gualeno 3124, LLKK (3220)"
        invoice_test.document_language = 3        
        invoice_test.currency_id = "PES"
        invoice_test.currency_cotization = 1   
        invoice_test.incoterms = "CIF"         
        return invoice_test

    @pytest.fixture(scope="module")
    def wsfex_test(self):
        #Logeo
        token = wsaa.tokens.AccessRequerimentToken('wsfex')
        signed_tra = token.sign_tra(files.private_key, files.certificate) 
        wsaa_test = wsaa.wsaa.Wsaa()
        login_fault = wsaa_test.login(signed_tra)     

        #Token
        token = wsaa.tokens.AccessToken()
        token.create_token_from_login(login_fault)
        return wsfex.wsfex.Wsfex(token, '20311641531')
    
    def test_check_webservice_status(self, wsfex_test):
        wsfex_test.check_webservice_status()

    def test_get_measurement_units(self, wsfex_test):
        wsfex_test.get_measurement_units()

    def test_get_exportation_types(self, wsfex_test):
        wsfex_test.get_exportation_types()

    def test_get_point_of_sales(self, wsfex_test):
        wsfex_test.get_point_of_sales()

    def test_get_currencies(self, wsfex_test):
        wsfex_test.get_currencies()

    def test_get_incoterms(self, wsfex_test):
        wsfex_test.get_incoterms()

    def test_get_languages(self, wsfex_test):
        wsfex_test.get_languages()

    def test_get_countries(self, wsfex_test):
        wsfex_test.get_countries()

    def test_get_countries_cuit(self, wsfex_test):
        wsfex_test.get_countries_cuit()

    def test_currency_value(self, wsfex_test):
        wsfex_test.get_currency_value("DOL")
        wsfex_test.get_currency_value("023")

    def test_get_document_codes(self, wsfex_test):
        wsfex_test.get_document_codes()

    def test_get_last_id(self, wsfex_test):
        wsfex_test.get_last_id()

    def test_get_last_number(self, wsfex_test):
        wsfex_test.get_last_number(0001, '19')

    def test_invoice_no_items(self, wsfex_test, invoice_test):
        """ Buscamos que el codigo de error sea el 1666 que es de items invalidos """

        try:
            wsfex_test.get_cae([invoice_test], 0001)
        except Exception as e:
            assert '1666' == str(e)[-4:]

    def test_invoice(self, wsfex_test, invoice_test, item_test):
        invoice_test.add_item(item_test)
        wsfex_test.get_cae([invoice_test], 1)

    def test_invoice_multiple_items(self, wsfex_test, invoice_test, item_test):
        invoice_test.add_item(item_test)
        invoice_test.add_item(item_test)
        item_test2 = copy.copy(item_test)
        item_test2.quantity = 4
        item_test2.measurement_unit = 4
        item_test2.unit_price = 2300.32
        invoice_test.add_item(item_test2)
        wsfex_test.get_cae([invoice_test], 1)

    def test_multiple_invoices(self, wsfex_test, invoice_test, item_test):
        invoice_test.add_item(item_test)
        invoice_test2 = copy.copy(invoice_test)
        invoice_test2.add_item(item_test)
        wsfex_test.get_cae([invoice_test, invoice_test2], 1)
