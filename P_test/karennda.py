import sys
import string

def Week():
    dayOfTheWeek = []
    for i in string.ascii_uppercase:
        dayOfTheWeek.append(i)

    return dayOfTheWeek

def y_m(daysInYear, daysInMonth):
    one_Yesr = daysInYear / daysInMonth
    Day_excess = daysInYear % daysInMonth

    return one_Yesr, Day_excess

def date_factor(date):
    date_YMW = date.split('-')
    date_Year = int(date_YMW[0])
    date_Month = int(date_YMW[1])
    date_Day = int(date_YMW[2])

    return date_Year, date_Month, date_Day

def leap_month(Day_excess, daysInMonth, daysInWeek,dayOfTheWeek):
    list_1 = []
    day_leap = int(0)
    for l in range(1, 201):
        day_leap = int(day_leap) + Day_excess
        if int(day_leap) >= int(daysInMonth):
            #print(i)
            list_1.append(l)
            day_leap = day_leap - int(daysInMonth)


def main_can(Day_excess, date_Day, daysInWeek, dayOfTheWeek):
    while date_Day > daysInWeek:
        date_Day = date_Day - daysInWeek
    print(dayOfTheWeek[date_Day - 1])

def main_cannt(Day_excess, date_Day, daysInWeek, dayOfTheWeek,days_gap):
    while date_Day > daysInWeek:
        date_Day = date_Day - daysInWeek
    print(dayOfTheWeek[date_Day - (1 + days_gap)])


def qq_month(daysInWeek, dayOfTheWeek, date_Day, date_Month, daysInMonth, date_Year, one_Yesr):
    list_week = []
    for w in range(daysInWeek):
        list_week.append(dayOfTheWeek[w])


    while date_Day > daysInWeek:
        date_Day = date_Day - daysInWeek
    
    if date_Year == 1:
        gap_week = daysInWeek - date_Month  
        print(list_week[date_Day - (1)])
    
    elif daysInMonth < daysInWeek:
        if daysInWeek % daysInMonth == 0:
            gap_week = daysInMonth * (date_Year / one_Yesr)
        print(gap_week)
        #print(list_week[int(date_Day - (1 + gap_week))])
        print(list_week[int(gap_week - date_Day)])



if __name__ == '__main__':
    daysInYear, daysInMonth, daysInWeek, date = input().split()
    dayOfTheWeek = Week()
    one_Yesr, Day_excess = y_m(int(daysInYear), int(daysInMonth))
    date_Year, date_Month, date_Day = date_factor(date)
    date_Year, date_Month, date_Day = int(date_Year), int(date_Month), int(date_Day)
        
    if(date_Day <= int(daysInMonth) and date_Month <= one_Yesr and one_Yesr < 99 and Day_excess == 0):
        main_can(int(Day_excess), int(date_Day), int(daysInWeek), dayOfTheWeek)

    elif(date_Day <= int(daysInMonth) and date_Month <= one_Yesr + 1 and one_Yesr < 99 and Day_excess >0):
        main_can(int(Day_excess), int(date_Day), int(daysInWeek), dayOfTheWeek)

    elif(date_Day <= int(daysInMonth) and date_Month <= one_Yesr and one_Yesr == 99):
        main_can(int(Day_excess), int(date_Day), int(daysInWeek), dayOfTheWeek)
        qq_month(int(daysInWeek),dayOfTheWeek,int(date_Day),int(date_Month),int(daysInMonth), int(date_Year), one_Yesr)

    else:
        print(-1)