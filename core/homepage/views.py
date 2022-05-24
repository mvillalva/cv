import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.template.loader import render_to_string
from django.shortcuts import render
from core.homepage.forms import HomeForm
from config import settings


class IndexView(FormView):
    form_class = HomeForm
    template_name = 'homepage/index.html'
    

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def send_email_messages(self, form):
        data = {}
        try:
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']            

            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to = settings.EMAIL_HOST_USER_TO
            mensaje = MIMEMultipart()
            mensaje['From'] = form.data['email'].strip()
            mensaje['To'] = email_to
            mensaje['Subject'] = form.data['asunto'].strip()

            content = render_to_string('homepage/send_email.html', {
                'nombre': form.data['nombre'].strip(),                
                'email' : form.data['email'].strip(),                
                'mensaje': form.data['mensaje'].strip(),
                'link_home': 'http://{}'.format(URL)
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = HomeForm(request.POST)
            if form.is_valid():                
                data = self.send_email_messages(form)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

def page_not_found_404(request, exception):
    return render(request, '404.html')