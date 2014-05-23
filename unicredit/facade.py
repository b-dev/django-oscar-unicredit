"""
Responsible for briding between Oscar and the Unicredit gateway
"""
import hashlib
import urllib
import logging
import base64
from decimal import Decimal as D

from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings

API_VERSION = getattr(settings, 'UNICREDIT_API_VERSION', '2.5.0')
BASE_URL = getattr(settings, 'UNICREDIT_BASE_URL', 'https://pagamenti.unicredito.it/initInsert.do')

log = logging.getLogger('unicredit')

def get_unicredit_url(order_number, total, host=None, scheme='https'):
    """
    Return the URL for Unicredit transaction.
    """
    currency = getattr(settings, 'UNICREDIT_CURRENCY', '978')

    if host is None:
        host = Site.objects.get_current().domain
    return_url = '%s://%s%s' % (scheme, host, reverse('unicredit-confirm-response'))
    cancel_url = '%s://%s%s' % (scheme, host, reverse('unicredit-cancel-response'))

    totale_ordine = str(total.quantize(D('0.02'))).replace(".", "")

    url_parameters = (
        ("numeroCommerciante", settings.UNICREDIT_ID_ESERCENTE),
        ("userID", settings.UNICREDIT_USERID),
        ("password", settings.UNICREDIT_PASSWORD),
        ("numeroOrdine", order_number),
        ("totaleOrdine", totale_ordine),
        ("valuta", currency),
        ("flagDeposito", "Y"),
        ("urlOk", return_url),
        ("urlKo", cancel_url),
        ("tipoRispostaApv", getattr(settings, 'UNICREDIT_TIPO_RISPOSTA_APV', "wait")),
        ("flagRiciclaOrdine", "Y"),
        ("stabilimento", settings.UNICREDIT_STABILIMENTO),
    )

    # CALCOLO DEL MAC
    stringa_per_mac = ""
    for parametro in url_parameters:
        stringa_per_mac += "%s=%s&" % (parametro[0], parametro[1])
    stringa_per_mac += "b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1"
    mac = base64.b64encode(hashlib.md5(stringa_per_mac).digest())

    # La password reale viene usata solo per la generazione del mac. Nell'url finale va passata una password finta
    stringa_urlencodata = urllib.urlencode(url_parameters)
    stringa_urlencodata = stringa_urlencodata.replace("password=%s" % settings.UNICREDIT_PASSWORD, "password=xxxxx")

    # Genero l'url finale da chiamare aggiungendo l'urlencode del mac
    url_unicredit = stringa_urlencodata + "&mac=%s" % urllib.quote_plus(mac)
    url_to_call = '%s?%s' % (BASE_URL, url_unicredit)
    log.debug('CHIAMO URL : %s' % url_to_call)

    return url_to_call