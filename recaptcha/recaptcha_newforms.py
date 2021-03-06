# This code is public domain.
# Thanks to SmileyChris for the original implementation

import django.forms as forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
import librecaptcha


# Do you want to bypass reCAPTCHA validation while in DEBUG mode?
SKIP_IF_IN_DEBUG_MODE = False

RECAPTCHA_LANG = settings.LANGUAGE_CODE[:2]
RECAPTCHA_THEME = getattr(settings, 'RECAPTCHA_THEME', 'red')


### ERROR_CODES
ERROR_CODES = {
    "unknown" :	_("Unknown error."),
    "invalid-site-public-key" :	_("We weren't able to verify the public key. Please try again later."),
    "invalid-site-private-key" : _("We weren't able to verify the private key. Please try again later."),
    "invalid-request-cookie" : _("The challenge parameter of the verify script was incorrect."),
    "incorrect-captcha-sol" : _("The CAPTCHA solution was incorrect."),
    "verify-params-incorrect" : _("The parameters to /verify were incorrect, make sure you are passing all the required parameters.  Please try again later."),
    "invalid-referrer" : _("reCAPTCHA API keys are tied to a specific domain name for security reasons.  Please try again later."),
    "recaptcha-not-reachable" :	_("Unable to contact the reCAPTCHA verify server.  Please try again later.")
}


class RecaptchaWidget(forms.Widget):
    def __init__(self):
       super(RecaptchaWidget, self).__init__()

    def render(self, name, value, attrs=None):
        html = librecaptcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY,
                                        theme=RECAPTCHA_THEME,
                                        lang=RECAPTCHA_LANG)
        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        challenge = data.get('recaptcha_challenge_field')
        response = data.get('recaptcha_response_field')
        return (challenge, response)

    def id_for_label(self, id_):
        return None


class RecaptchaField(forms.Field):
    widget = RecaptchaWidget

    def __init__(self, remote_ip, *args, **kwargs):
        self.remote_ip = remote_ip
        super(RecaptchaField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        if SKIP_IF_IN_DEBUG_MODE and settings.DEBUG:
            return True
        value = super(RecaptchaField, self).clean(value)
        challenge, response = value
        
        if not challenge:
            raise forms.ValidationError(_('An error occured with the CAPTCHA service. Please try again.'))
        if not response:
            raise forms.ValidationError(_('Please enter the CAPTCHA solution.'))

        rc = librecaptcha.submit(challenge, response,
                              settings.RECAPTCHA_PRIVATE_KEY,
                              self.remote_ip)
        if not rc.is_valid:
            msg = ERROR_CODES.get(rc.error_code, ERROR_CODES['unknown'])
            raise forms.ValidationError(msg)
       
        # reCAPTCHA validates!
        return True




