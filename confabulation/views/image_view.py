from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from .context_helpers import setup_page_context
from ..utils.s3_helpers import get_signed_photo_url
import re

def image_view(request, image_name):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    prefix = re.search('[A-Z]+', image_name).group()
    try:
        image_url = get_signed_photo_url(prefix+'/i/'+image_name+'.jpg',
                                     raise_error=True)

        context = {'image_url':image_url, 'image_name':image_name+'.jpg'}
        setup_page_context(context)
        return render(request, 'confabulation/imageView.html', context)
    except Exception as e:
        raise  Http404

