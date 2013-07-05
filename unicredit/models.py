from django.db import models

class UnicreditTransactionLog(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=128, db_index=True)
    datacreazione = models.CharField(max_length=100) # 'datacreazione': [u'11.03.2013 10:47:13'],
    numeroCommerciante = models.CharField(max_length=50) # 'numeroCommerciante': [u'9999888'],
    stabilimento = models.CharField(max_length=50) # 'stabilimento': [u'99888'],
    numeroOrdine = models.CharField(max_length=50) # 'numeroOrdine': [u'PRD000000000016018'],
    statoprecedente = models.CharField(max_length=10) # 'statoprecedente': [u'RO'],
    statoattuale = models.CharField(max_length=10) # 'statoattuale': [u'AB'],
    descrizione = models.CharField(max_length=100) # 'descrizione': [u'CAMBIO DI STATO'],
