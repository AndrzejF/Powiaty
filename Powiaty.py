# -*- coding: utf-8 -*-
# ./Powiaty.py

# -*- coding: utf-8 -*-
import pyodbc
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash

def OpenMSSQLDatabase(Server,
                      Database,
                      Driver,
                      Username=None,
                      Password=None):  # Otwiera połaczenie do bazy MS SQL
    if Username is None:
        LoginType = ';Trusted_Connection=yes'
    else:
        LoginType = ';UID=' + Username + ';PWD=' + Password
    return pyodbc.connect('DRIVER=' + Driver + '; SERVER=' + Server + '; DATABASE=' + Database + LoginType)


def OpenSQL(Plik, Parametr):  # Otwiera z pliku skrypt SQL i podstawia parametr do filtra WHERE
    f = open(Plik, 'r')
    SQL = (f.read())
    f.close()
    return SQL.replace("Parametr", Parametr)

def GetWOJ():
    # Odczytywanie danych logowania z pliku LOGIN.txt
    with open('LOGIN.txt', 'r') as f:
        L = f.read().split(':')
    LOGIN = L[0]
    PASSWORD = L[1].strip()

    # Połaczenie do bazy
    cnxn = OpenMSSQLDatabase('192.168.1.12,1433',
                             'SPDS_ST_STP',
                             '{SQL Server Native Client 11.0}',
                             Username = LOGIN,
                             Password = PASSWORD)
    cursor = cnxn.cursor()
    # Zapytanie SQL
    cursor.execute(OpenSQL("WOJEWODZTWA.sql", ""))
    row = cursor.fetchone()
    dict_woj = {'':''}
    while row:  # Wpisywanie województw do słownika
        dict_woj.update({row[0]: row[1]})
        row = cursor.fetchone()
    # for x in dict_woj.items():
    #     print(x)
    return dict_woj

def GetPOWIAT(wybrany_powiat):
    # Połaczenie do bazy
    cnxn = OpenMSSQLDatabase('192.168.1.12,1433',
                             'SPDS_ST_STP',
                             '{SQL Server Native Client 11.0}',
                             Username='AF',
                             Password='tomasz')
    cursor = cnxn.cursor()
    # Zapytanie SQL
    cursor.execute(OpenSQL("POWIATY.sql", wybrany_powiat))
    row = cursor.fetchone()
    powiaty = []
    while row:  # Wpisywanie powiatów do słownika
        powiaty.append((row[0], row[1]))

        row = cursor.fetchone()
    return powiaty

app = Flask(__name__)

# konfiguracja aplikacji
app.config.update(dict(
    SECRET_KEY='bradzosekretnawartosc',
))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        wybor=''
        WOJ = request.form.get('wybor')
        flash('Powiaty dla województwa: {0}'.format(DANE[WOJ]))
        for i,j in GetPOWIAT(WOJ):
            #print(j.strip(),'-',i.strip())
            flash('{0:<23} - {1}'.format( j.strip(), i.strip()))  # Formatowanie nie działa
            # print('{0:<23} - {1}'.format( j.strip(), i.strip()))
        return redirect(url_for('index'))
    return render_template('index.html', lista=DANE.items())

if __name__ == '__main__':
    DANE=GetWOJ()   # pobranie listy województw
    app.run(debug=True, host="192.168.1.10", port=5000)