from django.conf import settings
import os

class ThemeMiddleware(object):
    def process_request(self, request):
#        try:
#            future_messages = request.session['future_site_messages']
#        except KeyError:
#            future_messages = {'errors':[],'notices':[]}
#        request.session['future_site_messages'] = {
#            'errors': [],
#            'notices': []}
#        request.session['site_messages'] = {
#            'errors': future_messages['errors'],
#            'notices': future_messages['notices']}
        settings.TEMPLATE_DIRS = [os.path.join(settings.PROJECT_ROOT, 'templates', 'themes', settings.THEME)] +\
                [tdir for tdir in list(settings.TEMPLATE_DIRS) if tdir.find('themes')==-1]
        
        
        
        return None

