# -*- coding: utf-8 -*-
import pytest
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
import wsfex
import copy

class TestExportationElectronicInvoice:

    @pytest.fixture(scope="module")
    def item_test(self):
        item = wsfex.invoice.ExportationElectronicInvoiceItem("Item")
        item.quantity = 2
        item.measurement_unit = "UN"
        item.unit_price = 2500
        item.bonification = 0.0
         
        return item
    
    @pytest.fixture
    def invoice_test(self):  
        invoice_test = wsfex.invoice.ExportationElectronicInvoice(19)        
        invoice_test.exportation_type = 2
        invoice_test.existent_permission = "S"
        invoice_test.destiny_country = 250.0
        invoice_test.destiny_country_cuit = 30709653542
        invoice_test.customer_name = "Perez Jose"
        invoice_test.customer_address = "Gualeno 3124, LLKK (3220)"
        invoice_test.document_language = 3        
        invoice_test.currency_id = "PES"
        invoice_test.currency_cotization = "1"            

        return invoice_test   

    
    def test_validate_invoice(self, invoice_test):
        wsfex.invoice.ExportationElectronicInvoiceValidator.validate_invoice(invoice_test)         
        
    def test_invoice_invalid_exportation_type(self, invoice_test):
        with pytest.raises(AttributeError): 
            invoice_test.exportation_type = 3
            wsfex.invoice.ExportationElectronicInvoiceValidator.validate_invoice(invoice_test)         

    def test_invoice_invalid_document_language(self, invoice_test):
        with pytest.raises(AttributeError): 
            invoice_test.document_language = 9
            wsfex.invoice.ExportationElectronicInvoiceValidator.validate_invoice(invoice_test)         

    def test_invoice_invalid_existent_permission(self, invoice_test):
        with pytest.raises(AttributeError): 
            invoice_test.existent_permission = 'J'
            wsfex.invoice.ExportationElectronicInvoiceValidator.validate_invoice(invoice_test)   

    def test_invoice_invalid_document_code(self, invoice_test):
        with pytest.raises(AttributeError): 
            invoice_test.document_code = '22'
            wsfex.invoice.ExportationElectronicInvoiceValidator.validate_invoice(invoice_test)

    def test_total_item(self, invoice_test, item_test):
        item_test2 = copy.copy(item_test)
        item_test2.measurement_unit = "KG"
        item_test2.quantity = 0.8
        item_test2.unit_price = 500
        invoice_test.add_item(item_test)
        invoice_test.add_item(item_test2)
        wsfex.invoice.ExportationElectronicInvoiceValidator.validate_invoice(invoice_test)         

        assert invoice_test.array_items[0].total_price == 5000
        assert invoice_test.array_items[1].total_price == 400
        assert invoice_test.get_total_amount() == 5400