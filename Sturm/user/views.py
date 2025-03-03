from datetime import timedelta
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _
from .models import *
from polls.views import *
from polls.models import *


def register(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        email = request.POST.get('email')
        status = request.POST.get('status')
        reason = request.POST.get('reason')
        institution = request.POST.get('institution')
        password1 = request.POST.get('password1')

        if len(username) == 0:
            error = _("Unesite korisničko ime.")
        elif len(name) == 0:
            error = _("Unesite ime.")
        elif len(surname) == 0:
            error = _("Unesite prezime.")
        elif len(password) == 0:
            error = _("Unesite lozinku.")
        elif len(password1) == 0:
            error = _("Unesite lozinku i u drugo polje.")
        elif len(email) == 0:
            error = _("Unesite email.")
        elif not re.match(r'^(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{6,}$', password):
            error = _("Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.")
        elif password != password1:
            error = _("Unete lozinke nisu iste.")
        elif not re.match('^[A-Za-z\d]{6,25}$', username):
            error = _("Korisničko ime mora imati između 6 i 25 karaktera  i može sadržati samo slova i cifre.")
        elif len(Student.objects.filter(username=username)) != 0:
            error = _("Korisničko ime već postoji.")
        elif len(Student.objects.filter(email=email)) != 0:
            error = _("Email već postoji.")
        elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            error = _("Email nije ispravan.")
        else:
            student = Student()
            student.username = username
            student.set_password(password)
            student.name = name
            student.surname = surname
            student.email = email
            student.status = status
            student.institution = institution
            student.reason = reason
            student.save()
            return redirect('Login')

    context = {'error': error}
    return render(request, 'register.html', context)

def log(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "" and password == "":
            error = _("Unesite korisničko ime i lozinku.")
        elif username == "":
            error = _("Unesite korisničko ime.")
        elif password == "":
            error = _("Unesite lozinku.")
        else:
            try:
                student = Student.objects.get(username=username)
                if check_password(password, student.password):
                    student = authenticate(username=username, password=password)
                    auth_login(request, student)
                    return redirect('Index')
            except Exception as e:
                error = _("Korisničko ime ili lozinka nisu ispravni.")

    context = {'error': error}
    return render(request, 'login.html', context)

def logoutt(request):
    logout(request)
    return redirect('../login/')

def forgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email == "":
            error = _("Unesite email.")
            context = {'error': error}
            return render(request, 'forgotPassword.html', context)

        try:
            student = Student.objects.get(email=email)
        except Student.DoesNotExist:
            error = _("Korisnik sa datom email adresom ne postoji.")
            context = {'error': error}
            return render(request, 'forgotPassword.html', context)

        token = token_generator.make_token(student)
        uid = urlsafe_base64_encode(force_bytes(student.pk))
        token = f"{uid}|{token}"
        reset_link = request.build_absolute_uri(f'/newPassword/{token}/')
        with open('token.txt', 'w') as token_file:
            token_file.write(token)
        try:
            PasswordResetToken.objects.filter(user_id=student.id).delete()
        except Exception:
            pass

        resetToken = PasswordResetToken()
        resetToken.user = student
        resetToken.token = token
        resetToken.created_at = timezone.now()
        resetToken.save()

        subject = _('Promena lozinke')
        message = _(f'Kliknite na sledeći link da promenite lozinku: {reset_link}')
        send_mail(subject, message, 'kn233091m@student.etf.bg.ac.rs', [email])
        context = {'succ': _("Uspešno ste poslali zahtev za promenu lozinke.")}
        return render(request, 'forgotPassword.html', context)

    return render(request, 'forgotPassword.html', None)

def newPassword(request, token):
    error = ""

    try:
        uidb64, token = token.split('|', 1)
        id = force_str(urlsafe_base64_decode(uidb64))
        student = Student.objects.get(pk=id)
        token = PasswordResetToken.objects.get(user_id=id)
    except PasswordResetToken.DoesNotExist:
        return redirect('forgotPassword.html')

    if timezone.now() - token.created_at > timedelta(minutes=30):
        return redirect('../../forgotPassword/')

    if request.method == "POST":
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if len(password) == 0:
            error = _("Unesite lozinku.")
        elif len(password1) == 0:
            error = _("Unesite lozinku i u drugo polje.")
        elif not re.match(r'^(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{6,}$', password):
            error = _("Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.")
        elif password != password1:
            error = _("Unete lozinke nisu iste.")

        if error:
            return render(request, 'newPassword.html', {'error': error, 'token': token})

        student.set_password(password)
        student.save()
        token = PasswordResetToken.objects.get(user_id=id)
        token.delete()
        return redirect('Login')

    return render(request, 'newPassword.html', {'token': token})

def profile(request):
    error = ""

    if not request.user.is_authenticated:
        return redirect('Login')
    user = Student.objects.get(username=request.user.username)

    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if len(username) == 0:
            error = _("Unesite korisničko ime.")
        elif len(name) == 0:
            error = _("Unesite ime.")
        elif len(surname) == 0:
            error = _("Unesite prezime.")
        elif len(email) == 0:
            error = _("Unesite email.")
        elif not re.match('^[A-Za-z\d]{6,25}$', username):
            error = _("Korisničko ime mora imati između 6 i 25 karaktera  i može sadržati samo slova i cifre.")

        if error != "":
            context = {'error': error}
            return render(request, 'profile.html', context)

        if user.username != username:
            try:
                Student.objects.get(username=username)
                error = _("Korisnik sa datim korisničkim imenom postoji.")
                context = {'error': error}
                return render(request, 'profile.html', context)
            except Student.DoesNotExist:
                pass

        if user.email != email:
            try:
                Student.objects.get(email=email)
                error = _("Korisnik sa datim emailom već postoji.")
                context = {'error': error}
                return render(request, 'profile.html', context)
            except Student.DoesNotExist:
                pass

        if error != "":
            context = {'error': error}
            return render(request, 'profile.html', context)

        if password:
            if password1 == "":
                error = _("Unesite lozinku i u drugo polje.")
            elif not re.match(r'^(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{6,}$', password):
                error = _("Lozinka mora imati minimalno 6 karaktera, barem jednu cifru i barem jedan specijalni znak.")
            elif password != password1:
                error = _("Unete lozinke nisu iste.")

            if error != "":
                context = {'error': error}
                return render(request, 'profile.html', context)

            user.set_password(password)

        user.username = username
        user.email = email
        user.name = name
        user.surname = surname
        user.save()

        context = {'succ': _("Uspešno ste promenili podatke.")}
        return render(request, 'profile.html', context)

    else:
        context = {'user': user}
    return render(request, 'profile.html', context)
