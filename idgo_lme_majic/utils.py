import logging
import mimetypes

from datetime import date

from django.apps import apps
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives

from idgo_admin.models import Mail
from idgo_admin.models.mail import get_admins_mails
from idgo_admin.utils import PartialFormatter
from idgo_admin import DEFAULT_FROM_EMAIL
from idgo_admin import ENABLE_SENDING_MAIL

logger = logging.getLogger('idgo_admin')

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return date(d.year + years, 3, 1)

def sender(template_name, to=None, cc=None, bcc=None, attach_files=[], **kvp):
    try:
        tmpl = Mail.objects.get(template_name=template_name)
    except Mail.DoesNotExist:
        return

    if to and cc:
        for v in to:
            try:
                cc.remove(v)
            except ValueError:
                continue

    if to and bcc:
        for v in to:
            try:
                bcc.remove(v)
            except ValueError:
                continue

    subject = tmpl.subject.format(**kvp)
    body = PartialFormatter().format(tmpl.message, **kvp)
    from_email = DEFAULT_FROM_EMAIL
    connection = get_connection(fail_silently=False)

    mail = EmailMultiAlternatives(
        subject=subject, body=body,
        from_email=from_email, to=to,
        cc=cc, bcc=bcc, connection=connection)

    for attach_file in attach_files:
        # mail.attach_file(attach_file)
        mail.attach(attach_file.name, attach_file.file.getvalue(), mimetypes.guess_type(attach_file.name)[0])

    if ENABLE_SENDING_MAIL:
        try:
            mail.send()
        except Exception as e:
            logger.exception(e)
            # Activer l'exception lorsque gérée par l'application.
            # return MailError()
    else:
        logger.warning("Sending mail is disable.")


# Pour une demande d'une extraction MAJIC/LME
def send_demande_extraction_majic_lme(user, type_ext, organisation, url, attach_files):
    JurisdictionCommune = apps.get_model(
        app_label='idgo_admin', model_name='JurisdictionCommune')
    communes = [
        instance.commune for instance
        in JurisdictionCommune.objects.filter(jurisdiction=organisation.jurisdiction)]
    return sender(
        'demande_extraction_majic_lme',
        to=get_admins_mails(),
        attach_files= attach_files,
        email=user.email,
        fullname=user.get_full_name(),
        type_ext = type_ext,
        communes=','.join([commune.code for commune in communes]),
        organisation=organisation.legal_name,
        organisation_pk=organisation.pk,
        url=url,
        username=user.username,
        website=organisation.website or '- adresse url manquante -')