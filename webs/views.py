from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from random import randint
from django import template


#---Lottozahlen_generieren----------------------------------
zahlen = [] #Generierte Zahlen

def checknum(num):
    for i in range(len(zahlen)):
        if zahlen[i] == num:    #checkt ob die gegebene Zahl in der Liste (zahlen) ist
            return True         #gibt True zurück wenn Zahl bereits exsistiert.

def gen_num():
    zahlen = []
    for i in range(6):          #6 Zzahlen sollen generiert werden.
        randnum = randint(1,49)
        while checknum(randnum) == True: # Solange die Zufällige Zahl bereits exsistiert wird
            randnum = randint(1,49)      # eine neue Zahl generiert und die schleife wiederholt sich.
        zahlen.append(randnum)
    return zahlen                        # Gibt die Liste der generierten Zahlen zurück.

def checkwins(lottozahlen):
    while len(lottozahlen) < 12 or len(lottozahlen) > 18: # Prüft ob der string die minimal und maximale
        return 'Fehler1, länge der Strings stimmt nicht.'  # länge nicht überschreitet.
    komma_check = 0
    for kommas in range(len(lottozahlen)):
        if lottozahlen[kommas] == ",":         # Zählt die kommas im sting.
            komma_check += 1
    while komma_check != 6:             # Kann auch ein 'If' sein, checkt ob die vorgegebene Komma anzahl stimmt.
        return 'Fehler2, {} von 6 kommas erkannt.'.format(komma_check)
    zahlenliste = []
    winzahlen = []           # Vorgegebener string sieht so aus '1,2,3,4,5,6,'
    komma = 0                # Der string ist dafür da das sich das programm ausserhalb der schleife merken kann an welcher stelle das letzte komma war.
    for nums in range(len(lottozahlen)):    # schleife geht jede stelle des strings durch, die jeweilige stelle ist 'nums'. Überprüft jz die einzelnen Zahlen
        if lottozahlen[nums] == ",":        # wenn es ein komme gefunden hat 1, <-- letztes komma ist an stelle 0 und aktuelles komma (nums) ist an stelle 1.
            if komma == 0:                  # wenn noch kein letztes komma exsistiert also die Variable komma = 0/False ist
                try:                  # \/-----------------------------------\/------------------------------I
                    if int(lottozahlen[komma:nums]) <= 0 or int(lottozahlen[komma:nums]) >= 50: # muss auf 'komma' keine 1 drauf gerechnet werden,
                        return 'Fehler3, die Zahl {} ist nicht im bereich 1-49.'.format(lottozahlen[komma:nums]) # weil die Zahl ja schon bei stelle 0 beginnt.
                except Exception as e:
                    return 'Fehler4'

                if int(lottozahlen[komma:nums]) not in zahlenliste:
                    zahlenliste.append(int(lottozahlen[komma:nums]))
                else:
                    return 'Fehler5, sie haben die Zahl {} mehr als 1 mal eingetragen.'.format(int(lottozahlen[komma:nums]))
            else:
                try:
                    if int(lottozahlen[komma+1:nums]) <= 0 or int(lottozahlen[komma+1:nums]) >= 50:  # Hier muss auf 'komma' +1 gerechnet werden weil die Zahl erst eine Stelle nach dem
                        return 'Fehler3, die Zahl {} ist nicht im bereich 1-49.'.format(lottozahlen[komma:nums]) # komma beginnt.
                except Exception as e:
                    return 'Fehler4'

                if int(lottozahlen[komma+1:nums]) <= 0 or int(lottozahlen[komma+1:nums]) >= 50:
                    return 'Fehler3, die Zahl {} ist nicht im bereich 1-49.'.format(lottozahlen[komma+1:nums]) #Bis hier hin war es alles nur prüfung des Strings.Hätte man um einiges Leichter
                   
                if int(lottozahlen[komma+1:nums]) not in zahlenliste:                        #machen können, ich wollts aber auf manuellen wege zeigen, wie is es früher gemacht hab.
                    zahlenliste.append(int(lottozahlen[komma+1:nums]))     # Wenn der Code dann bist hier hin gekommen ist, ist der string richtig weil 
                else:
                    return 'Fehler5, sie haben die Zahl {} mehr als 1 mal eingetragen.'.format(int(lottozahlen[komma+1:nums]))
            komma = nums                                               # der Befehl 'return' ein abbruch der kompletten Definition ist.
    while len(lottozahlen) < 12 or len(lottozahlen) > 18: # Prüft ob der string die minimal und maximale
        return 'Fehler5, doppelte Zahl.'  # länge nicht überschreitet.
    gen_zahlen = gen_num()  #Die funktion 'gen_nums()' wird benutzt um eine liste mir zufälligen Zahlen zu generieren.
    winzahlen_string = ""
    gen_zahlen_string = ""
    anzahl_richtig = 0
    for number in gen_zahlen:   # Liste 'gen_zahlen' wird in einen string umgewandelt (kann man einfacher machen)
        gen_zahlen_string += str(number) + ','
    for number in zahlenliste:  # Checkt welche Zahl vom User in den zufälligen Zahlen ist.
        if number in gen_zahlen:
            winzahlen.append(number)
            winzahlen_string += str(number) + ','
            anzahl_richtig += 1
    #server_send = str(','.join(winzahlen))
    #return server_send
    final_string = 'Zufällige Lotto Zahlen: ' + gen_zahlen_string[:-1] + ' sie haben ' + str(anzahl_richtig) + ' Zahlen richtig: ' + winzahlen_string[:-1]
    return final_string

def home_view(request):
    return render(request, 'index.html')


def login_view(request):    #Die definiton für die seite '/login'
    if request.user.is_authenticated:
        redirect('webs:lotto')

    if request.method == 'POST':    # Wenn die anfrage vom browser POST ist
        form = AuthenticationForm(data=request.POST) #Django Login Form
        if form.is_valid():   # Ist die form gültig
            user = form.get_user()
            login(request, user)    #User einloggen
            return redirect('webs:lotto')   #Weiterleiten auf Lotto seite
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})    #Gibt die HTML datei zurück.

def register_view(request):
    if request.user.is_active:
        redirect('webs:lotto')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)   #Django Register Form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('webs:lotto')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request) #Der User der den request macht wird ausgeloggt
    messages.info(request,'Erfolgreich ausgeloggt')
    return redirect('webs:home')

def about_view(request):
    return render(request, 'about.html')    # Hier wird einfach nur die 'about.html' datei gerendert.

@login_required(login_url='/login/')    # Dieser request kann nur gemacht werden wenn ein User eingeloggt ist.
def lotto_view(request):                # Wenn man nicht eingeloggt ist wir man zu '/login/' weitergeleitet.
    if request.method == 'POST':
        lt1 = request.POST.get('lt1')   # Die werte bei einem POST request, der Zahlen
        lt2 = request.POST.get('lt2')
        lt3 = request.POST.get('lt3')
        lt4 = request.POST.get('lt4')
        lt5 = request.POST.get('lt5')
        lt6 = request.POST.get('lt6')
        user_name = request.user.username
        user_id = request.user.id
        register_date = request.user.date_joined
        lotto_nums = checkwins(lt1 + ',' + lt2 + ',' + lt3 + ',' + lt4 + ',' + lt5 + ',' + lt6 + ',') # Zahlen werden zur definition weitergegeben.
        print(lt1,lt2,lt3,lt4,lt5,lt6)                                       # das was die def 'checkwins()' zurückgibt wird in 'lotto_nums' gespeichtert.
        print(lotto_nums)
    else:
        user_name = request.user.username   # Wenn es kein POST request ist müssen alle Variablen trotzdem belegt sein.
        user_id = request.user.id
        register_date = request.user.date_joined
        print(user_id)
        print(register_date)
        lotto_nums = ""

    return render(request, 'lotto.html',    # Rendert html seite und schickt die werte zur Html datei.
    {
        'user_name': user_name,             #Variablen die an den browser(an die lotto.html) datei übermittelt werden.
        'lotto_nums': lotto_nums,           
        'user_id': user_id,
        'register_date': register_date
       })
