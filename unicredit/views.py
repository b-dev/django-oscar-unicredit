import logging
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from django.views.generic import RedirectView, View
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import get_model

from oscar.apps.checkout.views import RedirectRequired, PaymentError, OrderPlacementMixin
from oscar.apps.checkout.views import PaymentDetailsView, ThankYouView

from oscar.apps.payment.models import SourceType, Source
from oscar.core.loading import get_class, get_classes

from unicredit.facade import get_unicredit_url
from unicredit.models import UnicreditTransactionLog
from unicredit.exceptions import UnicreditError

Country = get_model('address', 'Country')
Basket = get_model('basket', 'Basket')
pre_payment, post_payment = get_classes('checkout.signals', ['pre_payment', 'post_payment'])

log = logging.getLogger('unicredit')

class PaymentView(PaymentDetailsView):
    """
    Initiate the transaction with Unicredit and redirect the user
    to Unicredit site to perform the transaction.
    """
    preview = True

    def handle_payment(self, order_number, total, **kwargs):
        """
        Handle any payment processing.

        This method is designed to be overridden within your project.  The
        default is to do nothing.
        """
        try:
            url = self._get_redirect_url(order_number, total, **kwargs)
            raise RedirectRequired(url)
        except UnicreditError:
            raise PaymentError("Attenzione. C'e' stato un errore dutante la comunicazione con Unicredit")


    def _get_redirect_url(self, order_number, total, **kwargs):
        if settings.DEBUG:
            # Determine the localserver's hostname to use when
            # in testing mode
            kwargs.update({'host':self.request.META['HTTP_HOST']})
            kwargs.update({'scheme':'http'})

        return get_unicredit_url(order_number, total, **kwargs)


class CancelResponseView(OrderPlacementMixin, View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CancelResponseView, self).dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        self.restore_frozen_basket()
        messages.error(self.request, "Transazione Unicredit Cancellata")
        return HttpResponseRedirect(reverse('basket:summary'))


class ListenerPayment(OrderPlacementMixin, View):
    """
    Questi i parametri in get che arrivano ad ogni richiesta:
    u'tipomessaggio': [u'PAYMENT_STATE'],
    u'datacreazione': [u'11.03.2013 10:47:13'],
    u'numeroCommerciante': [u'9999888'],
    u'stabilimento': [u'99888'],
    u'numeroOrdine': [u'PRD000000000016018'],
    u'statoprecedente': [u'RO'],
    u'statoattuale': [u'AB'],
    u'descrizione': [u'CAMBIO DI STATO'],
    u'MAC': [u'K1NJth37DHS1FCHdhh+jxg=='],
    """

    def get(self, request, *args, **kwargs):
        log.debug("ListenerPayment : inizio chiamata asicrona")

        datacreazione = request.GET['datacreazione']
        numeroCommerciante = request.GET['numeroCommerciante']
        stabilimento = request.GET['stabilimento']
        numeroOrdine = request.GET['numeroOrdine']
        statoprecedente = request.GET['statoprecedente']
        statoattuale = request.GET['statoattuale']
        descrizione = request.GET['descrizione']
        MAC = request.GET['MAC']

        order_number = self.checkout_session.get_order_number()
        log.debug("Session Order Number : %s", order_number)
        log.debug("REQUEST GET : %s", request.GET)

        log.debug("Creo UnicreditTransactionLog")
        utl = UnicreditTransactionLog()
        utl.order_number = order_number
        utl.datacreazione = datacreazione
        utl.numeroCommerciante = numeroCommerciante
        utl.stabilimento = stabilimento
        utl.numeroOrdine = numeroOrdine
        utl.statoprecedente = statoprecedente
        utl.statoattuale = statoattuale
        utl.descrizione = descrizione
        utl.save()
        log.debug("UnicreditTransactionLog Creata")

        if statoattuale == 'IC':
            log.debug("Transazione eseguita. Salvo l'ordine")
            basket = request.basket
            self.handle_order_placement(basket)
            log.debug("Ordine salvato correttamente")

        log.debug("UNICREDIT ListenerPayment : fine chiamata asicrona")
        return HttpResponse('OK')


    def handle_order_placement(self, basket):
        order_number = self.checkout_session.get_order_number()

        total_incl_tax = basket.total_incl_tax
        total_excl_tax = basket.total_excl_tax
        log.debug("Salvo ordine n. %s. Totale ordine : %s", order_number, total_incl_tax)

        # Record payment source
        source_type, is_created = SourceType.objects.get_or_create(name='Unicredit')
        source = Source(source_type=source_type,
            currency='EUR',
            amount_allocated=total_incl_tax,
            amount_debited=total_incl_tax)
        self.add_payment_source(source)

        # Place order
        super(ListenerPayment, self).handle_order_placement(order_number,
                                                            basket,
                                                            total_incl_tax,
                                                            total_excl_tax)


class ThankYouView(ThankYouView):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(ThankYouView, self).dispatch(*args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('checkout:thank-you'))
