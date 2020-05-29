# Generiere Kalender = Liste mit Tuple (Tag, Monat, Wochentag)
def gen_cal(is_leap, start_day):
    cal = []
    l_mon = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] if is_leap else \
            [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    weekdays = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    curr_day = 0
    for mon in range(12):
        for day in range(l_mon[mon]):
            cal.append((day + 1, mon + 1, weekdays[(curr_day + start_day) % 7]))
            curr_day += 1
    return cal

# Bestimme den ersten Wochentag des nächsten Jahres
def next_start_day(is_leap, old_start_day):
    return (old_start_day + (2 if is_leap else 1)) % 7 # 2 % 7 == 366 % 7

def is_leap_year(year):
    return True if (year % 4 == 0 and year % 100 != 0 or year % 400 == 0) \
                else False

# a)
# Es gibt 14 verschiedene Fälle, da das Jahr mit 7 Wochentage beginnen kann und
# es entweder ein Schaltjahr oder nicht ist.

for weekday in range(7):
    for leap in range(2):
        cal = gen_cal(leap, weekday)
        for day in cal:
            if day[0] == 13 and day[2] == "fri":
                print(f"Start weekday: {weekday+1}    Is leap year: {leap}    "
                      f"Date: {day}")

# Ergebniss:
#
# |------------+------------------------+------------------------|
# | erster Tag | Schaltjahr             | kein Schaltjahr        |
# |------------+------------------------+------------------------|
# | Montag     | 2: 13.09, 13.12        | 2: 13.04, 13.07        |
# | Dienstag   | 1: 13.06               | 2: 13.09, 13.12        |
# | Mittwoch   | 2: 13.03, 13.11        | 1: 13.06               |
# | Donnerstag | 2: 13.02, 13.08        | 3: 13.02, 13.03, 13.11 |
# | Freitag    | 1: 13.05               | 1: 13.10               |
# | Samstag    | 1: 13.10               | 1: 13.05               |
# | Sonntag    | 3: 13.01, 13.04, 13.07 | 2: 13.01, 13.10        |
# |------------+------------------------+------------------------|


# b)

black_fridays = []

# 1998 startete mit einem Do
start_day = 3
for year in range(1998, 2021):
    cal = gen_cal(is_leap_year(year), start_day)
    for date in cal:
        if date[0] == 13 and date[2] == "fri":
            black_fridays.append(date + (year,))
    start_day = next_start_day(is_leap_year(year), start_day)

# Die ersten 2 und der letzte Eintrag werden weggesliced da sie vor meinem
# Geburstag (14.07.1998) oder nach heute sind
print(len(black_fridays[2:-1])) 

# Ergebniss: Es gab 38 mal einen "Freitag den Dreizehnten" seit meinem
#            Geburtstag.


