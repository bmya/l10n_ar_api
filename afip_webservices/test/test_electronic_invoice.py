# -*- coding: utf-8 -*-
import pytest
import sys, os
from datetime import date
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from odoo_openpyme_api import documents
import wsfe

class TestElectctronicInvoice:

    @pytest.fixture(scope="module")
    def invoice_test(self):
        
        invoice_test = wsfe.invoice.ElectronicInvoice(001)
        invoice_test.document_date = date.today() - relativedelta(days=2)        
        invoice_test.service_from = date.today() + relativedelta(days=3)
        invoice_test.service_to = date.today()
        invoice_test.payment_due_date = date.today() - relativedelta(days=5)
        invoice_test.taxed_amount = 10000
        invoice_test.untaxed_amount = 150
        invoice_test.exempt_amount = 200
                
        return invoice_test   

    @pytest.fixture(scope="module")
    def invoice_validator_test(self):    
        invoice_validator_test = wsfe.invoice.ElectronicInvoiceValidator()

        return invoice_validator_test   
        
    def test_invoice_bad_concept(self, invoice_test, invoice_validator_test):
        with pytest.raises(AttributeError): 
            invoice_test.concept = 4
            invoice_validator_test.validate_invoice(invoice_test)        

    def test_invoice_document_date(self, invoice_test, invoice_validator_test):
        
        invoice_test.concept = 1
        invoice_test.document_date = (date.today() - relativedelta(days=2))
        invoice_validator_test.validate_invoice(invoice_test)
        with pytest.raises(AttributeError):
            invoice_test.document_date = (date.today() + relativedelta(days=6))
            invoice_validator_test.validate_invoice(invoice_test)
            
        invoice_test.concept = 2
        invoice_test.document_date = (date.today() - relativedelta(days=8))
        invoice_validator_test.validate_invoice(invoice_test)        
        with pytest.raises(AttributeError):
            invoice_test.document_date = (date.today() - relativedelta(days=12))
            invoice_validator_test.validate_invoice(invoice_test)
    
    def test_invoice_dates(self, invoice_test):

        assert len(invoice_test.document_date) == 8
        assert len(invoice_test.service_from) == 8
        assert len(invoice_test.service_to) == 8
        
    def test_invoice_tax(self, invoice_test):
                
        invoice_tax = documents.tax.Iva(5, 2100, 10000)
        invoice_test.add_iva(invoice_tax)
        assert invoice_test.get_total_amount() == 12450
        
        invoice_tax_2 = documents.tax.Iva(4, 1050, 10000)
        invoice_test.add_iva(invoice_tax_2)
        assert invoice_test.get_total_amount() == 13500
        
    def test_invoice_tributes(self, invoice_test):
                
        invoice_tax = documents.tax.Tribute(02, 500, 10000, 5)
        invoice_test.add_iva(invoice_tax)
        assert invoice_test.get_total_amount() == 14000
