from datetime import timedelta
from django.utils.translation import gettext as _
from polls.views import *
from polls.models import *
from user.models import *

def myadmin(request: HttpRequest):
    if not request.user.is_authenticated:return redirect('Login')
    if request.user.username != "admin1":return redirect('Index')
    users = Student.objects.filter().order_by('id')
    if request.method == "POST":
        if 'delete_user' in request.POST:
            try:
                id = int(request.POST.get('user'))
            except Exception:
                return render(request, "admin.html", {"users" : users,"error": _("ID korisnika nije u ispravnom obliku.")})
            try:
                user = Student.objects.get(id=id)
            except Exception:
                return render(request, "admin.html", {"users" : users, "error": _("ID korisnika ne postoji.")})
            try:
                History.objects.get(idStudent=request.user.id).delete()
            except Exception:
                pass
            try:
                PasswordResetToken.objects.get(user_id=id).delete()
            except Exception:
                pass
            try:
                Scores.objects.get(idStudent=request.user.id).delete()
            except Exception:
                pass
            user.delete()
            return render(request, "admin.html", {"users" : users, "succ": _("Uspešno ste obrisali korisnika.")})

        if 'generate_questions' in request.POST:
            try:
                number = int(request.POST.get('number'))
            except Exception:
                return render(request, "admin.html", {"users": users, "error": _("Broj novih pitanja nije u ispravnom obliku.")})
            for i in range(number):
                question = generate_polynomial()
                poly = question['poly']
                lower = question['segment'][0]
                upper = question['segment'][1]
                k = 2

                P0_original = poly = str(poly.as_expr())
                P0 = sympify(poly)
                coefs = []
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

                P0_res = "$\mathrm{ P_0(x) = " + latex(P0) + "}$"
                P1_res = "$\mathrm{ P_1(x) = " + latex(P1) + "}$"
                G_res = "$\mathrm{ G(x) = " + latex(G.args[0]) + "}$"

                his = History.objects.filter(P0=P0_res)
                if len(his) != 0:
                    continue

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
                history.P0_original = P0_original
                history.lower = question['segment'][0]
                history.upper = question['segment'][1]
                history.save()
            return render(request, "admin.html", {"users": users, "succ": _("Baza znanja dopunjena.")})

        if 'reset' in request.POST:
            date = timezone.now() - timedelta(days=4 * 30)
            olds = Questions.objects.filter(time__lt=date)
            olds.delete()
            return render(request, "admin.html", {"users": users, "succ": _("Tabela tačnih odgovora ažurirana.")})

        if 'test' in request.POST:
            histories = History.objects.filter(idStudent=3)
            errors = []
            for history in histories:
                poly = Poly(history.P0_original)
                real_zeros = poly.real_roots()
                numOfZeros = [root for root in real_zeros if history.lower <= root <= history.upper]
                numOfZeros = len(numOfZeros)
                if numOfZeros != int(history.numOfZeros):
                    errors.append({
                        "Poly": history.P0_original,
                        "Lower": history.lower,
                        "Upper": history.upper,
                        "Expected": numOfZeros,
                        "Got": history.numOfZeros
                    })
            if len(errors):
                with open("errors.txt", "w") as file:
                    for error in errors:
                        file.write(f"Polynomial: {error['Poly']}\n")
                        file.write(f"Segment: [{error['Lower']}, {error['Upper']}] \n")
                        file.write(f"Expected: {error['Expected']}\n")
                        file.write(f"Got: {error['Got']}\n")
                        file.write("\n")
                return render(request, "admin.html", {"users": users, "error": _("Testiranje neuspešno.")})
            return render(request, "admin.html", {"users": users, "succ": _("Testiranje uspešno.")})
    return render(request, "admin.html", {"users" : users})