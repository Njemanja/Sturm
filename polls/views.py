import io
import math
import time
import matplotlib
from datetime import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpRequest
from math import floor
from numpy import ComplexWarning
from sympy import symbols, diff, div, rem, Poly, pi, expand, Rational, sympify, latex, E, solve, lambdify
import numpy as np
import warnings
from sympy.core.sympify import SympifyError
from django.shortcuts import render
from user.models import Student
from .models import *
import re
import wolframalpha
from django.utils.translation import activate, gettext as _
import matplotlib.pyplot as plt
from django.http import HttpResponse
import random
from django.utils import timezone
from django.shortcuts import redirect
import sys

sys.path.append("..")
warnings.filterwarnings("ignore", category=ComplexWarning)
x = symbols('x')
token_generator = PasswordResetTokenGenerator()
matplotlib.use('Agg')


def gcdEuclid(a, b):
    a, b = Poly(a), Poly(b)
    while b:
        a, b = b, a % b
    return a.monic()

def sturm(P0):
    P1 = diff(P0, x)
    i = 0
    polys = []
    while P1 != 0:
        Q = -rem(P0, P1)
        polys.append(P0)
        P0 = P1
        P1 = Q
        i += 1
    polys.append(P0)
    return polys

def numberOfZeros(polys, ab):
    cntAB = [0, 0]
    arr = ""
    for i in range(len(polys)):
        arr += "$\mathrm{ P_" + str(i) + "(x) = " + str(latex(polys[i].as_expr())) + "}$\n\n"
    inPoint = ["", ""]
    for iterator in range(2):
        prev = 0
        inPoint[iterator] += "$\mathrm{x = " + str(latex(ab[iterator])) + "}$\n\n"
        for i in range(len(polys)):
            if polys[i] != 0:
                value = polys[i].subs(x, ab[iterator])
                # ispravi
                inPoint[iterator] += "$\mathrm{P_" + str(i) + "(" + str(ab[iterator]) + ") = } \displaystyle "
                inPoint[iterator] += str(latex(value)) + " = "
                s = "{:2e}".format(float("{:.15f}".format(value.evalf())))
                s, e = s.split('e')
                s, d = s.split('.')
                for place in range(len(d)):
                   if not int(d[place:]): break
                   if place > 5: break
                if place >= 5:
                    s += "." + d[:5] + "..."
                elif place > 0:
                    s += "." + d[:place]
                if int(e[1:]):
                    s = f"{s} \\times 10^{{{int(e)}}}"
                inPoint[iterator] += (s + "$\n\n")
                if prev < 0 and value > 0 or prev > 0 and value < 0 or value == 0:
                    cntAB[iterator] += 1
                prev = value

    theory = _(
        "Neka je ξ ∈ [a, b] označimo V (ξ) broj promena znakova u nizu P0(ξ), P1(ξ), ..., Pr(ξ), ignorišući eventualno javljanje korena polinoma u tom nizu.") + "\n"
    theory += _("Tada razlika N = V (a) − V (b) određuje broj nula polinoma P(x) na segmentu [a, b].") + "\n"
    theory += "$\mathrm{V(" + str(ab[0]) + ") = " + str(cntAB[0]) + "}$\n"
    theory += "$\mathrm{V(" + str(ab[1]) + ") = " + str(cntAB[1]) + "}$\n"
    theory += "$\mathrm{V(" + str(ab[0]) + ") - " + "V(" + str(ab[1]) + ") = " + str(abs(cntAB[0] - cntAB[1])) + "}$\n"
    return abs(cntAB[0] - cntAB[1]), polys[0].subs(x, ab[1]), arr, theory, inPoint

def coefficients(coef, k):
    k = int(k)
    if (coef == 0): return 0
    exp = 0
    while abs(coef) < 1:
        coef *= 10
        exp += 1
    return (floor(coef * 10 ** k) / (10 ** k)) / (10 ** exp)

def coefficients1(coef, k):
    k = int(k)
    if (coef == 0): return 0
    exp = 0
    while abs(coef) < 1:
        coef *= 10
        exp += 1
    return (math.ceil(coef * 10 ** k) / (10 ** k)) / (10 ** (exp))


def graph(lower, upper, P0, id):
    X = np.linspace(lower, upper, 400)
    p = lambdify(x, P0, "numpy")
    Y = p(X)
    roots = solve(P0, x)
    plt.figure(figsize=(12, 9))
    plt.plot(X, Y)
    plt.axvline(lower, color='#897594', linestyle='--', linewidth=2, label=f'[{lower}, {upper}]')
    plt.axvline(upper, color='#897594', linestyle='--', linewidth=2)
    plt.plot(X, Y, color='black', label=f'P(x) = {P0}')
    for root in roots:
        if root.is_real:
            plt.plot(float(root), 0, 'ro', markersize=4, label=f'x = {round(float(root), 2)}')
    plt.xlabel("x")
    plt.ylabel("P(x)")
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.ylim(-5, 5)
    plt.legend()
    plt.show()
    plt.savefig(f'static/graph{id}.png', bbox_inches='tight')
    plt.close()

def index(request: HttpRequest, id=None):
    if not request.user.is_authenticated: return redirect('Login')

    if id:
        history = Searched.objects.filter(idHistory=id, idStudent=request.user.id)
        if not len(history):
            return redirect('Index')
        history = History.objects.get(id=id)
        return render(request, "result.html",
                      {"add1": history.add1, "add2": history.add2, "P0": history.P0, "P1": history.P1,
                       "G": history.G, "arr": history.arr, "theory": history.theory,
                       "firstPoint": history.firstPoint, "secondPoint": history.secondPoint, "edges": history.edges,
                       "numOfZeros": history.numOfZeros, "id": history.id})
    if request.method == 'POST':
        global res
        res = ""
        P0_original = poly = request.POST.get('hiddenPolinom', '')
        lower = request.POST.get('donjaGranica', '')
        upper = request.POST.get('gornjaGranica', '')
        k = request.POST.get('decimal', '')

        if poly == '':
            return render(request, "index.html", {'error': _("Unesite polinom.")})
        if not lower:
            return render(request, "index.html", {'error': _("Unesite donju granicu.")})
        if not upper:
            return render(request, "index.html", {'error': _("Unesite gornju granicu.")})
        if k == '':
            return render(request, "index.html", {'error': _("Unesite broj decimala.")})
        try:
            lower = float(lower)
            upper = float(upper)
            k = float(k)
        except ValueError:
            return render(request, "index.html",
                          {'error': _("Donja, gornja granica i koficijent moraju biti brojevi.")})
        if float(lower) >= float(upper):
            return render(request, "index.html", {'error': _("Donja granica mora biti strogo manja od gornje.")})
        if k < 0:
            return render(request, "index.html", {'error': _("Broj decimala mora biti jednak ili veći od 0.")})
        lower = float(request.POST.get('donjaGranica', ''))
        upper = float(request.POST.get('gornjaGranica', ''))

        try:
            P0 = sympify(poly)
            if not (sympify(poly).free_symbols == {x}):
                return render(request, "index.html", {'error': _("Polinom nije ispravan.")})
        except SympifyError:
            return render(request, "index.html", {'error': _("Polinom nije ispravan.")})

        coeffs = [expand(P0).coeff(x, n) for n in range(expand(P0).as_poly().degree(), -1, -1)]
        coefs = []

        for coeff in coeffs:
            expr = sympify(coeff)
            try:
                nil = Rational(expr)
            except:
                if not expr.is_rational:
                    if not (expr.has(pi) or expr.has(E)):
                        return render(request, "index.html", {'error': _("Polinom nije ispravan.")})

        P0_evalf = P0.evalf(20)
        P0u = P0 = Poly(P0_evalf, x)
        for coeff in P0.all_coeffs():
            coefs.append(coefficients(coeff, k))
        P0 = Poly(coefs, x)

        coefs2 = []
        for coeff in P0u.all_coeffs():
            coefs2.append(coefficients1(coeff, k))
        P0u = Poly(coefs2, x)
        if isinstance(P0u, Poly):
            P0u = P0u.args[0]
        Gu = gcdEuclid(P0u, diff(P0u, x))

        if isinstance(P0, Poly):
            P0 = P0.args[0]
        P1 = diff(P0, x)
        G = gcdEuclid(P0, P1)

        P0_res = "$\mathrm{ P(x) = " + latex(P0) + "}$"
        P1_res = "$\mathrm{ P'(x) = " + latex(P1) + "}$"
        G_res = "$\mathrm{ G(x) = " + latex(G.args[0]) + "}$"

        his = History.objects.filter(P0=P0_res, lower=lower, upper=upper )
        if len(his) != 0:
            searched = Searched()
            searched.idHistory = his[0].id
            searched.idStudent = request.user.id
            searched.save()
            return render(request, "result.html",
                          {"add1": his[0].add1, "add2": his[0].add2, "P0": his[0].P0, "P1": his[0].P1, "G": his[0].G,
                           "arr": his[0].arr, "theory": his[0].theory,
                           "firstPoint": his[0].firstPoint, "secondPoint": his[0].secondPoint, "edges": his[0].edges,
                           "numOfZeros": his[0].numOfZeros, "id": his[0].id})

        diver = 10
        while 1:
            if P0.subs(x, lower) == 0:
                edge = lower - 1 / diver
                diver *= 10
                numOfZeros, nil, nil, nil, nil = numberOfZeros(sturm(list(div(P0, G))[0]), [edge, lower])
                if numOfZeros == 0:
                    lower = edge
                    break
            else:
                break
        diver = 10
        while 1:
            if P0.subs(x, lower) == 0:
                edge = lower + 1 / diver
                diver *= 10
                numOfZeros, nil, nil, nil, nil = numberOfZeros(sturm(list(div(P0, G))[0]), [upper, edge])
                if numOfZeros == 0:
                    upper = edge
                    break
            else:
                break

        numOfZeros, positive, arr, theory, inPoint = numberOfZeros(sturm(list(div(P0, G))[0]), [lower, upper])

        add1 = ""
        if not numOfZeros:
            add1 += _("Polinom je uvek") + " " + (_("pozitivan") if positive else _("negativan"))

        history = History()
        history.save()
        graph(lower, upper, P0, history.id)

        edges = "$\mathrm{[" + str(lower) + "," + str(upper) + "]}$"
        numOfZeros_res = numOfZeros

        diver = 10
        while 1:
            if P0u.subs(x, lower) == 0:
                edge = lower - 1 / diver
                diver *= 10
                numOfZeros, nil, nil, nil, nil = numberOfZeros(sturm(list(div(P0u, Gu))[0]), [edge, lower])
                if numOfZeros == 0:
                    lower = edge
                    break
            else:
                break
        diver = 10
        while 1:
            if P0u.subs(x, lower) == 0:
                edge = lower + 1 / diver
                diver *= 10
                numOfZeros, nil, nil, nil, nil = numberOfZeros(sturm(list(div(P0u, Gu))[0]), [upper, edge])
                if numOfZeros == 0:
                    upper = edge
                    break
            else:
                break
        numOfZerosu, nil, nil, nil, nil = numberOfZeros(sturm(list(div(P0u, Gu))[0]), [lower, upper])
        add2 = ""
        if numOfZeros != numOfZerosu:
            add2 = "  *(" + _(
                "Broj nula je dobijen nanižom aproksimacijom koeficijenata, ukoliko se koristi navišna aproksimacija koeficijenata broj nula je") + ")" + str(
                numOfZerosu) + ")"

        history.P0 = P0_res
        history.P1 = P1_res
        history.G = G_res
        history.arr = arr
        history.theory = theory
        history.firstPoint = inPoint[0]
        history.secondPoint = inPoint[1]
        history.edges = edges
        history.numOfZeros = numOfZeros_res
        history.add1 = add1
        history.add2 = add2
        history.idStudent = request.user.id
        history.lower = lower
        history.upper = upper
        history.P0_original = P0_original
        history.save()
        searched = Searched()
        searched.idHistory = history.id
        searched.idStudent = request.user.id
        searched.save()
        return render(request, "result.html",
                      {"add1": add1, "add2": add2, "P0": P0_res, "P1": P1_res, "G": G_res, "arr": arr, "theory": theory,
                       "firstPoint": inPoint[0], "secondPoint": inPoint[1], "edges": edges,
                       "numOfZeros": numOfZeros_res, "id": history.id})
    return render(request, "index.html")

def help(request: HttpRequest):
    if not request.user.is_authenticated:  return redirect('Login')
    return render(request, "help.html")

def history(request, id=None):
    if not request.user.is_authenticated: return redirect('Login')
    if id:
        return pdf(request, id)
    histories = History.objects.filter(id__in=Searched.objects.filter(idStudent=request.user.id).values('idHistory')).order_by('-id')
    return render(request, 'history.html', {'histories': histories})

def pdf(request, id):
    language = request.path.split('/')[1]
    activate(language)

    history = History.objects.get(id=id)

    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    y_pos = 2
    spacing = 0.05
    ax.axis('off')

    ax.text(0.05, y_pos, _("Početni polinom P(x):"), fontsize=12, ha='left')
    y_pos -= spacing
    ax.text(0.05, y_pos, history.P0, fontsize=12, ha='left')
    y_pos -= spacing
    ax.text(0.05, y_pos, _("Prvi izvod početnog polinoma P'(x):"), fontsize=12, ha='left')
    y_pos -= spacing
    ax.text(0.05, y_pos, history.P1, fontsize=12, ha='left')
    y_pos -= spacing
    ax.text(0.05, y_pos, _("Najveći zajednički delilac polinoma P(x) i P'(x):"), fontsize=12, ha='left')
    y_pos -= spacing
    ax.text(0.05, y_pos, history.G, fontsize=12, ha='left')
    y_pos -= spacing

    ax.text(0.05, y_pos, _("Šturmov niz polinoma:"), fontsize=12, ha='left')
    y_pos -= spacing
    for line in history.arr.splitlines():
        if line:
            ax.text(0.05, y_pos, line, fontsize=12, ha='left')
            y_pos -= spacing

    ax.text(0.05, y_pos, _("Vrednost Šturmovog niza polinoma u tački:"), fontsize=12, ha='left')
    y_pos -= spacing

    first = history.firstPoint.replace(r'\displaystyle', '')
    ax.text(0.05, y_pos, _("Prva tačka: "), fontsize=12, ha='left')
    y_pos -= spacing
    for line in first.splitlines():
        if line:
            ax.text(0.05, y_pos, line, fontsize=12, ha='left')
            y_pos -= spacing

    second = history.secondPoint.replace(r'\displaystyle', '')
    ax.text(0.05, y_pos, _("Druga tačka: "), fontsize=12, ha='left')
    y_pos -= spacing
    for line in second.splitlines():
        if line:
            ax.text(0.05, y_pos, line, fontsize=12, ha='left')
            y_pos -= spacing

    ax.text(0.05, y_pos, _("Teorija"), fontsize=12, ha='left')
    y_pos -= spacing

    theory = _(
        "Neka je ξ ∈ [a, b] označimo V (ξ) broj promena znakova u nizu P0(ξ), P1(ξ), ..., Pr(ξ), ignorišući eventualno javljanje korena polinoma u tom nizu.")
    ax.text(0.05, y_pos, theory, fontsize=12, ha='left')
    y_pos -= spacing

    theory = _("Tada razlika N = V (a) − V (b) određuje broj nula polinoma P(x) na segmentu [a, b].")
    ax.text(0.05, y_pos, theory, fontsize=12, ha='left')
    y_pos -= spacing

    for line in history.theory.splitlines()[2:]:
        ax.text(0.05, y_pos, line, fontsize=12, ha='left')
        y_pos -= spacing

    ax.text(0.05, y_pos, _("Broj nula polinoma") + " " + history.P0 + " " + _("na segmentu") + " " + history.edges + " " + _("je") + " " + str(history.numOfZeros) + ".", fontsize=12, ha='left')
    y_pos -= spacing

    if history.add1:
        ax.text(0.05, y_pos, history.add1, fontsize=12, ha='left')
        y_pos -= spacing

    if history.add2:
        ax.text(0.05, y_pos, history.add2, fontsize=12, ha='left')
        y_pos -= spacing

    buf = io.BytesIO()
    plt.savefig(buf, format='pdf', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    response = HttpResponse(buf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="result.pdf"'
    return response

def contact(request):
    if not request.user.is_authenticated: return redirect('Login')
    context = {}
    if request.method == 'POST':
        message = request.POST.get('message')
        if message == "":
            context = {'error': _("Unesite poruku.")}
            return render(request, 'contact.html', context)

        email = request.user.email
        message = _(f'Email: {email}\n{message}')
        subject = _('Pomoć')
        send_mail(subject, message, 'kn233091m@student.etf.bg.ac.rs', ['kn233091m@student.etf.bg.ac.rs'])
        context = {'succ': _("Uspešno ste poslali poruku. Očekujte odgovor na email adresu.")}
    return render(request, 'contact.html', context)

def quiz(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    today = timezone.now().date()
    try:
        myScore = Scores.objects.get(idStudent=request.user.id)
        if myScore.time.date() != today:
            myScore.index = 0
            myScore.save()
        UnansweredQuestions.objects.filter(time__date__lt=timezone.now().date()).delete()
    except Scores.DoesNotExist:
        myScore = Scores(idStudent=request.user.id, points=0, index=0, time=timezone.now())
        myScore.save()

    if request.method == 'POST':
        time.sleep(3)
        selectedAnswer = int(request.POST.get('selected_answer'))
        correctAnswer = int(request.POST.get('correct_answer'))
        id = request.POST.get('id')

        if selectedAnswer == correctAnswer:
            myScore.points += 1
            questionAnswered = Questions()
            questionAnswered.idQuestion = id
            questionAnswered.idStudent = request.user.id
            questionAnswered.time = timezone.now()
            questionAnswered.save()
        else:
            myScore.points -= 1
            questionUnanswered = UnansweredQuestions()
            questionUnanswered.idQuestion = id
            questionUnanswered.idStudent = request.user.id
            questionUnanswered.time = timezone.now()
            questionUnanswered.save()

        myScore.index += 1
        myScore.time = timezone.now()
        myScore.save()

    scores = Scores.objects.all().order_by('-points')
    ranking = []
    prev_points = None
    rank = 0
    for score in scores:
        if score.points != prev_points:
            rank += 1
        student = Student.objects.get(id=score.idStudent)
        ranking.append({
            'username': student.username,
            'points': score.points,
            'rank': rank
        })
        prev_points = score.points

    if myScore.index != 10:
        answered = Questions.objects.filter(idStudent=request.user.id).values_list('idQuestion', flat=True)
        unanswered = UnansweredQuestions.objects.filter(idStudent=request.user.id).values_list('idQuestion', flat=True)
        unanswered = list(History.objects.exclude(id__in=answered).exclude(id__in=unanswered))
        random.shuffle(unanswered)
        unanswered = unanswered[0]
        numOfZeros = int(unanswered.numOfZeros)
        possibleAnswers = list(range(numOfZeros - 5, numOfZeros + 4))
        possibleAnswers = [answer for answer in possibleAnswers if answer >= 0]
        possibleAnswers.remove(numOfZeros)
        answers = random.sample(possibleAnswers, 2)
        answers = [{'value': numOfZeros, 'correct': True}, {'value': answers[0], 'correct': False},
                   {'value': answers[1], 'correct': False}]
        random.shuffle(answers)
        return render(request, 'quiz.html', {
            'ranking': ranking,
            'answers': answers,
            'myScore': myScore,
            'poly': unanswered.P0,
            'id': unanswered.id,
            'lower': unanswered.lower,
            'upper': unanswered.upper,
            'correct_answer': unanswered.numOfZeros
        })

    return render(request, 'quiz.html', {
        'ranking': ranking,
        'answers': [],
        'myScore': myScore,
        'poly': None,
        'id': None,
        'correct_answer': None
    })

def generate_polynomial():
    client = wolframalpha.Client('EPETLL-PEJQQH283Q')
    try:
        res = client.query("Give a number between 3 and 7.")
        dg = int(next(res.results).text)
        res = client.query(f"Give a list of {dg} numbers between -30 and 30.")
        coeffs = next(res.results).text
        coeffs = re.findall(r'-?\d+', coeffs)
        coeffs = [int(num) for num in coeffs]
        poly = Poly(coeffs, x)
        res = client.query("Give a two numbers between -100 and 100.")
        segment = next(res.results).text
        segment = re.findall(r'-?\d+', segment)
        segment = [int(num) for num in segment]
        segment = sorted(segment)
        real_zeros = poly.real_roots()
        numOfZeros = [root for root in real_zeros if segment[0] <= root <= segment[1]]
        numOfZeros = len(numOfZeros)
        return {"poly": poly, "segment": segment, "numOfZeros": numOfZeros}
    except Exception as e:
        print("Došlo je do greške")

