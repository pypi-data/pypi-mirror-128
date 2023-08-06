
def Day(FullDate):
    '''
    Returns the day of the week for a date entered,using Zeller's Formula, if it falls between
    01/01/0001 and 31/12/9999 (yeah, thousands of years ).
    This is capable of Error handling.
    You may modify the source given below to your liking, (and may even publish it online, provided
    you abide by the MIT license.)
    '''
    DatePart = str(FullDate).split('/')
    Year = int(int(DatePart[2])%100)
    Century = int(int(DatePart[2])//100)
    Month = int(DatePart[1])
    Date = int(DatePart[0])
    if Date > 31: # Date cannot be greater than 31
        return "\t \n Date cannot exceed 31 \n "
    elif Date < 0: # negative dates not allowed
        return "\t \n Date cannot be Negative \n"
    if Month > 12: # Month numbers don't exceed 12
        return "\t \n Month cannot exceed 12 \n "
    elif Month < 0: # Months are numbered from 1 to 12
        return "\t \n Month cannot be negative \n"

    #Zeller's formula requires these conversions.        
    if Month == 1:
        Year -= 1
        Month = 13
    elif Month == 2:
        Year -= 1
        Month = 14

    # errors relating to February's last dates        
    if (Month == 2 or Month == 14) and Date >= 30:
        return "\n February\'s days are only till 28 or 29 on leap years \n'"
    if (Month == 2 or Month == 14) and Date >= 29 and (Year+1) % 4 != 0:
        return "\n February 29 does not exist for non-leap years \n"

    condition = Month == 9 or Month == 6 or Month == 4 or Month == 13
    if bool(condition) == 1 and Date > 30:
        return "\n April, June, September and November have only 30 Days \n"


    Result = Date + ((13*(Month + 1))//5) + Year + (Year//4) + (Century//4) - 2*Century
    Weekday = Result % 7
    WeekDict = {1:'Sunday',2:'Monday',3:'Tuesday',4:'Wednesday',5:'Thursday',6:'Friday',7:'Saturday'}
    return(f"{WeekDict[Weekday]}\n")
