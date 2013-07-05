===================================
Unicredit package for django-oscar
===================================

This package provides integration between django-oscar_ and `Unicredit`_.

.. _django-oscar: https://github.com/tangentlabs/django-oscar

Support
-------

Having problems or got a question?

* write to me an email info@marcominutoli.it

---------------
Getting started
---------------

Add 'unicredit' in your INSTALLED_APPS::


Add the following settings using the details from your sandbox buyer account::

    UNICREDIT_ID_ESERCENTE = 'XXXXXX'
    UNICREDIT_STABILIMENTO = 'XXXXX'
    UNICREDIT_USERID = 'XXXXX'
    UNICREDIT_PASSWORD = 'XXXXXX'
    UNICREDIT_STRINGA_SICUREZZA = 'XXXXXXXX'


Next, you need to add the Unicredit URLs to your URL config.  This can be done as
follows::

    from django.contrib import admin
    from oscar.app import shop

    urlpatterns = patterns('',
        (r'^admin/', include(admin.site.urls)),
        (r'^checkout/unicredit/', include('unicredit.urls')),
        (r'', include(shop.urls)),


To insert the UNICREDIT button in your template ``templates/oscar/checkout/preview.html`` aggiungendo::

    <form method="post" action="{% url 'unicredit-direct-payment' %}" id="place-order-form-unicredit">
        {% csrf_token %}
        <input type="hidden" name="action" value="place_order"/>

        <div class="form-actions">
            <button id='place-order' type="submit" class="pull-right btn btn-primary btn-large js-disable-on-click"
                    data-loading-text="{% trans 'Submitting...' %}">Paga con unicredit
            </button>
        </div>
    </form>
