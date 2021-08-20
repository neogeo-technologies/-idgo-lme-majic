
from datetime import date

from idgo_admin.models import Mail
from idgo_admin.models.mail import sender
from idgo_admin.models.mail import get_admins_mails

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




# Pour une demande d'une extraction MAJIC/LME
def send_demande_extraction_majic_lme(user, type_ext, organisation, url, attach_files):
    JurisdictionCommune = apps.get_model(
        app_label='idgo_admin', model_name='JurisdictionCommune')
    communes = [
        instance.commune for instance
        in JurisdictionCommune.objects.filter(jurisdiction=organisation.jurisdiction)]
    return sender(
        'demande_extraction_majic_lme',
        # to=get_admins_mails(),
        to=['lalmada@neogeo.fr',],
        attach_files= attach_files,
        email=user.email,
        full_name=user.get_full_name(),
        type_ext = type_ext,
        communes=','.join([commune.code for commune in communes]),
        organisation=organisation.legal_name,
        organisation_pk=organisation.pk,
        url=url,
        username=user.username,
        website=organisation.website or '- adresse url manquante -')