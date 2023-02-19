from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import ApplicationForm
from .forms import ConfirmationForm


def application_view(request):
    match request.method:
        case 'GET':
            form = ApplicationForm()
            return render(request, 'application.html', {'form': form})
        case 'POST':
            form = ApplicationForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(f'../confirmation/?email={form.cleaned_data["email"]}')
            else:
                return render(request, 'application.html', {'form': form})


def confirmation_view(request):
    match request.method:
        case 'GET':
            form = ConfirmationForm(initial=request.GET)
            return render(request, 'confirmation.html', {'form': form})
        case 'POST':
            form = ConfirmationForm(data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse(b'You did it')
            else:
                return render(request, 'confirmation.html', {'form': form})
