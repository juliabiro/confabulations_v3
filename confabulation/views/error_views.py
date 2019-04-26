from django.shortcuts import render
from .context_helpers import setup_page_context


def error_404(request, exception):
        context = setup_page_context()
        return render(request,'confabulation/error_404.html', context, status=404)

def error_500(request):
        context = setup_page_context()
        return render(request,'confabulation/error_500.html',context, status=500)
