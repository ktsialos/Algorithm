import csv
import numpy as np
import pandas as pd
from random import choices
import random


hourly_energy_consumption = {}
sum_hourly_energy_consumption = {}
c1 = 0
c2 = 0
month_count = -1
year_count = -1
day = 0
month = 0
hour = 0
year = 2020
number_of_cars = 2272
number_of_cars2 = 2272



#συνάρτηση εύρεσης χρόνων φόρτισης και κατανάλωσης την εκάστοτε ώρα για οικιακές φορτίσεις τις καθημερινές
def find_charging_times_and_consumption(hourly_energy_consumption, charging_started, capacity_to_charge, charging_speed, charging_ended, c_id):
    global data
    
    #full_hours: πλήρες ώρες φόρτισης, partially_charged_capacity είναι η υπολοιπόμενη τιμή της φόρτισης, η οποία μοιράζεται στην πρώτη ώρα και στην τελευταία ώρα εφόσον υπάρχουν. Charging_started/ended_akeraio είναι η πρώτη/τελευταία πλήρης ώρα φόρτισης
    (full_hours , partially_charged_capacity) = divmod(capacity_to_charge,0.9*charging_speed) #το 0.9 αντιστοιχεί στις 10% απώλειες κατά την φόρτιση
    (charging_started_akeraio,first_hour) = divmod(charging_started, 1)
    (charging_ended_akeraio,last_hour) = divmod(charging_ended, 1)
   
    #αν ο συνολικός διαθέσιμος χρόνος απο την στιγμή που το αυτοκίνητο φτάνει στο σπίτι έως την αναχώρηση του το πρωί είναι μεγαλύτερος απο τον χρόνο που απαιτείται για να φορτίσει
    if (24-charging_started)+charging_ended>full_hours+partially_charged_capacity/(charging_speed*0.9):
        #αν η πρώτη ώρα είναι γεμάτη και άν το άθροισμα του χρόνου εκκίνησης φόρτισης και των πλήρων ωρών φόρτισης που απαιτούνται δεν ξεπερνούν τις 24 ώρες(το εύρος του πίνακα) γέμισε τις ώρες απο το charging_started_akeraio έως το charging_started_akeraio + full_hours με charging speed(3.6,7.2) και την τελευταία ώρα με το partially_charged_capacity
        if first_hour==0: 
            if (int(charging_started_akeraio)+ int(full_hours)) < 24: 
                hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = charging_speed
                hourly_energy_consumption[int(charging_started_akeraio) + int(full_hours)] = partially_charged_capacity/0.9
            else: #αν το άθροισμα του χρόνου εκκίνησης φόρτισης και των πλήρων ωρών φόρτισης που απαιτούνται ξεπερνάνε το εύρος του πίνακα βάλε charging speed απο το charging_started_akeraio έως τις 23:00 και συνέχισε μετά απο τις 0:00
                hourly_energy_consumption[int(charging_started_akeraio):24] = charging_speed 
                hourly_energy_consumption[0:(int(full_hours)) - abs(int(charging_started_akeraio)-24)] = charging_speed
                hourly_energy_consumption[(int(full_hours)) - abs(int(charging_started_akeraio)-24)] = partially_charged_capacity/0.9
        else: #εφόσον η πρώτη ώρα δεν είναι γεμάτη(δηλαδή ξεκινάει και 15,30,45) αντιστοίχισε το ποσό φόρτισης αναλόγως στην πρώτη ώρα και κάνε τα ίδια με παραπάνω για τις υπόλοιπες
            hourly_energy_consumption[int(charging_started_akeraio)] = (1-float(first_hour))*charging_speed
            capacity_to_charge = capacity_to_charge - (1-float(first_hour))*charging_speed*0.9 #άλλαξε το capacity_to_charge και δούλεψε με το καινούργιο παρακάτω
            (full_hours , partially_charged_capacity) = divmod(capacity_to_charge,0.9*charging_speed)
            charging_started_akeraio = int(charging_started_akeraio) + 1 #ξεκίνα απο την επόμενη ώρα και κάνε ότι έκανες και στα προηγούμενα
    
            if (int(charging_started_akeraio) + int(full_hours)) < 24: #δες σειρά 36
                hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = charging_speed
                hourly_energy_consumption[int(charging_started_akeraio)+ int(full_hours)] = partially_charged_capacity/0.9
            else: #δες σειρά 41
                hourly_energy_consumption[int(charging_started_akeraio):24] = charging_speed 
                hourly_energy_consumption[0:(int(full_hours)) - abs(int(charging_started_akeraio)-24)] = charging_speed
                hourly_energy_consumption[(int(full_hours)) - abs(int(charging_started_akeraio)-24)] = partially_charged_capacity/0.9
        #εφόσον τρέξει την συγκεκριμένη υπόθεση σημαίνει ότι οι διαθέσιμες ώρες φόρτισης είναι αρκετές ώστε να φορτίσει πλήρως η μπαταρία μας.
        data.at[i, ' Battery State (%)'] = 100
    else: #στην περίπτωση που ο συνολικός διαθέσιμος χρόνος δεν επαρκεί για πλήρη φόρτιση της μπαταρίας όρισε τις πλήρες ώρες φόρτισης ανάλογα με τον διαθέσιμο χρόνο μέχρι την επόμενη αναχώρηση
        full_hours= 24 - int(charging_started_akeraio) + int(charging_ended_akeraio)
        if first_hour == 0: #ίδια με σειρές 38-43
            if (int(charging_started_akeraio)+ int(full_hours)) < 24: 
                hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = charging_speed
            else:
                hourly_energy_consumption[int(charging_started_akeraio):24] = charging_speed 
                hourly_energy_consumption[0:(int(full_hours))-abs(int(charging_started_akeraio)-24)] = charging_speed
        else: #σειρά 45
            hourly_energy_consumption[int(charging_started_akeraio)] = (1-float(first_hour))*charging_speed 
            #άλλαξε τις πλήρες ώρες φόρτισης καθώς η πρώτη(μη γεμάτη) ώρα γέμισε
            full_hours-=1 
            charging_started_akeraio = int(charging_started_akeraio)+1

            if (int(charging_started_akeraio) + int(full_hours)) < 24: 
                hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = charging_speed
            else:
                hourly_energy_consumption[int(charging_started_akeraio):24] = charging_speed 
                hourly_energy_consumption[0:(int(full_hours))-abs(int(charging_started_akeraio)-24)] = charging_speed
        #αντίστοιχα με την πρώτη ώρα, αν υπάρχει τελευταία(μη ολόκληρη) ώρα γέμιση το κελί της με το ποσό που της αντιστοιχεί    
        hourly_energy_consumption[int(charging_ended_akeraio)] += (float(last_hour))*charging_speed   #βαλαμε το + στην περίπτωση επικάλυψης φορτίσεων
        #Αφότου τρέξουν τα παραπάνω άλλαξε το data[' Battery State (%)'] ανάλογα με την περίπτωση ύπαρξης πρώτης(μη γεμάτης) ώρας.
        if first_hour == 0 :
            data.at[i, ' Battery State (%)'] = int(data.at[i, ' Battery State (%)']) + full_hours*charging_speed*90/data.at[i, 'Battery Capacity'] + hourly_energy_consumption[int(charging_ended_akeraio)]*90/data.at[i, 'Battery Capacity']
        else :
            data.at[i, ' Battery State (%)'] = int(data.at[i, ' Battery State (%)']) + (full_hours+(1-first_hour))*charging_speed*90/data.at[i, 'Battery Capacity'] + hourly_energy_consumption[int(charging_ended_akeraio)]*90/data.at[i, 'Battery Capacity']

        
#συνάρτηση εύρεσης χρόνων φόρτισης και κατανάλωσης την εκάστοτε ώρα για οικιακές φορτίσεις τα σαββατοκύριακα          
def find_charging_times_and_consumption_wkn(hourly_energy_consumption, charging_started, capacity_to_charge, charging_speed, charging_ended, c_id):
    global data
    
    #Θεωρούμε έναρξη και λήξη εξωτερικής φόρτισης +-2 ώρες σε σχέση με τις αντίστοιχες ώρες τις καθημερινές. Στην περίπτωση που ξεπεραστεί το εύρος μας αφαίρεσε 24 ώρες ώστε να μετρήσει ώρες απο την αρχή του πίνακα μας.(πχ 25->1:00 , 26->2:00)
    if charging_started+2>24:
        charging_started+=2
        charging_started-=24
    else: 
        charging_started+=2
    charging_ended +=2
    #ίδια με την αντίστοιχη συνάρτηση για καθημερινές
    (full_hours , partially_charged_capacity) = divmod(capacity_to_charge,0.9*charging_speed)
    (charging_started_akeraio,first_hour) = divmod(charging_started, 1)
    (charging_ended_akeraio,last_hour) = divmod(charging_ended, 1)
   

    if (24-charging_started)+charging_ended>full_hours+partially_charged_capacity/(charging_speed*0.9):
        if first_hour==0:
            if (int(charging_started_akeraio)+ int(full_hours)) < 24: 
                hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = charging_speed
                hourly_energy_consumption[int(charging_started_akeraio) + int(full_hours)] = partially_charged_capacity/0.9
            else:
                hourly_energy_consumption[int(charging_started_akeraio):24] = charging_speed 
                hourly_energy_consumption[0:(int(full_hours)) - abs(int(charging_started_akeraio)-24)] = charging_speed
                hourly_energy_consumption[(int(full_hours)) - abs(int(charging_started_akeraio)-24)] = partially_charged_capacity/0.9
        else:
            hourly_energy_consumption[int(charging_started_akeraio)] = (1-float(first_hour))*charging_speed
            capacity_to_charge = capacity_to_charge - (1-float(first_hour))*charging_speed*0.9
            (full_hours , partially_charged_capacity) = divmod(capacity_to_charge,0.9*charging_speed)
            charging_started_akeraio = int(charging_started_akeraio) + 1
    
            if (int(charging_started_akeraio) + int(full_hours)) < 24: 
                hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = charging_speed
                hourly_energy_consumption[int(charging_started_akeraio)+ int(full_hours)] = partially_charged_capacity/0.9
            else:
                hourly_energy_consumption[int(charging_started_akeraio):24] = charging_speed 
                hourly_energy_consumption[0:(int(full_hours)) - abs(int(charging_started_akeraio)-24)] = charging_speed
                hourly_energy_consumption[(int(full_hours)) - abs(int(charging_started_akeraio)-24)] = partially_charged_capacity/0.9
        
        data.at[i, ' Battery State (%)'] = 100
    else:
        full_hours= 24 - int(charging_started_akeraio) + int(charging_ended_akeraio)
        if first_hour == 0:
            if (int(charging_started_akeraio)+ int(full_hours)) < 24: 
                hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = charging_speed
            else:
                hourly_energy_consumption[int(charging_started_akeraio):24] = charging_speed 
                hourly_energy_consumption[0:(int(full_hours))-abs(int(charging_started_akeraio)-24)] = charging_speed
        else:
            hourly_energy_consumption[int(charging_started_akeraio)] = (1-float(first_hour))*charging_speed
            full_hours-=1
            charging_started_akeraio = int(charging_started_akeraio)+1

            if (int(charging_started_akeraio) + int(full_hours)) < 24: 
                hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = charging_speed
            else:
                hourly_energy_consumption[int(charging_started_akeraio):24] = charging_speed 
                hourly_energy_consumption[0:(int(full_hours))-abs(int(charging_started_akeraio)-24)] = charging_speed
            
        hourly_energy_consumption[int(charging_ended_akeraio)] = (float(last_hour))*charging_speed            
        if first_hour == 0 :
           data.at[i, ' Battery State (%)'] = int(data.at[i, ' Battery State (%)']) + full_hours*charging_speed*90/data.at[i, 'Battery Capacity'] + hourly_energy_consumption[int(charging_ended_akeraio)]*90/data.at[i, 'Battery Capacity']
        else :
            data.at[i, ' Battery State (%)'] = int(data.at[i, ' Battery State (%)']) + (full_hours+(1-first_hour))*charging_speed*90/data.at[i, 'Battery Capacity'] + hourly_energy_consumption[int(charging_ended_akeraio)]*90/data.at[i, 'Battery Capacity']

            
#συνάρτηση εύρεσης χρόνων φόρτισης και κατανάλωσης την εκάστοτε ώρα για εξωτερικές φορτίσεις τις καθημερινές          
def find_charging_times_and_consumption_outdoors(hourly_energy_consumption, charging_started, capacity_to_charge, charging_ended, c_id):
    global data
    
    (full_hours , partially_charged_capacity) = divmod(capacity_to_charge,0.9*22)
    #Θεωρούμε έναρξη και λήξη εξωτερικής φόρτισης +-0.5 ώρες απο την στιγμή αναχώρησης/άφιξης.Υπάρχει μια περίπτωση στις ώρες ,25 να υπάρχει πρόβλημα επικάλυψης εσωτερικών και εξωτερικών φορτίσεων.
    charging_started += 0.5 
    charging_ended -= 0.5
    (charging_started_akeraio,first_hour) = divmod(charging_started, 1)
   
    #αν η πρώτη ώρα είναι γεμάτη κάνε ότι εκάνες με 22kW φόρτιση
    if first_hour==0:
        hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = 22
        hourly_energy_consumption[int(charging_started_akeraio) + int(full_hours)] = partially_charged_capacity/0.9
    else: #αλλιώς αν η υπολοιπόμενη τιμή φόρτισης είναι μεγαλύτερη απο την τιμή που μπορεί να αντιστοιχιστεί για το χρονικό διάστημα που απομένει την πρώτη ώρα 
        if partially_charged_capacity > (1-float(first_hour))*22*0.9 :
            #βάλε στην πρώτη ώρα την τιμή που αντιστοιχεί για το εναπομείναντα χρονικό διάστημα
            hourly_energy_consumption[int(charging_started_akeraio)] = (1-float(first_hour))*22
            capacity_to_charge = capacity_to_charge - (1-float(first_hour))*22*0.9 #αλλαξε το capacity to charge τώρα που τελείωσες με την πρώτη ώρα
            (full_hours , partially_charged_capacity) = divmod(capacity_to_charge,0.9*22)
            charging_started_akeraio=int(charging_started_akeraio)+1
            hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] =22
            hourly_energy_consumption[int(charging_started_akeraio)+ int(full_hours)] = partially_charged_capacity/0.9
        else:
            hourly_energy_consumption[int(charging_started_akeraio)] = partially_charged_capacity/0.9
    data.at[i, ' Battery State (%)'] = 100


#συνάρτηση εύρεσης χρόνων φόρτισης και κατανάλωσης την εκάστοτε ώρα για εξωτερικές φορτίσεις τα σαββατοκύριακα  
def find_charging_times_and_consumption_outdoors_wkn(hourly_energy_consumption, charging_started, capacity_to_charge, charging_ended, c_id):
    global data
    #δες σειρά 93
    if charging_started+2>24:
        charging_started+=2
        charging_started-=24
    else: 
        charging_started+=2
    charging_ended +=2
    
    (full_hours , partially_charged_capacity) = divmod(capacity_to_charge,0.9*22)
    charging_started += 1.5
    charging_ended -= 1.5
    (charging_started_akeraio,first_hour) = divmod(charging_started, 1)
   
    #ίδια με την αντίστοιχη συνάρτηση για καθημερινές

    if first_hour==0:
        hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] = 22
        hourly_energy_consumption[int(charging_started_akeraio) + int(full_hours)] = partially_charged_capacity/0.9
    else:
        if partially_charged_capacity > (1-float(first_hour))*22*0.9 :
            hourly_energy_consumption[int(charging_started_akeraio)] = (1-float(first_hour))*22
            capacity_to_charge = capacity_to_charge - (1-float(first_hour))*22*0.9
            (full_hours , partially_charged_capacity) = divmod(capacity_to_charge,0.9*22)
            charging_started_akeraio=int(charging_started_akeraio)+1
            hourly_energy_consumption[int(charging_started_akeraio):(int(charging_started_akeraio) + int(full_hours))] =22
            hourly_energy_consumption[int(charging_started_akeraio)+ int(full_hours)] = partially_charged_capacity/0.9
        else:
            hourly_energy_consumption[int(charging_started_akeraio)] = partially_charged_capacity/0.9
    data.at[i, ' Battery State (%)'] = 100

#συνάρτηση που υπολογίζει το άθροισμα των καταναλώσεων ανά ώρα κάθε μέρας
def  find_sum_hourly_energy_consumption(sum_hourly_energy_consumption, hourly_energy_consumption):
    global hour 
    for hour in range(0,24):
        sum_hourly_energy_consumption[hour] += hourly_energy_consumption[hour]



#παίρνει σαν είσοδο το .csv  αρχείο    
data = pd.read_csv('modified_data.csv')
data[' Battery State (%)'] = data[' Battery State (%)'].astype(float)
scenario = pd.read_csv('scenario24.csv')
#η πρώτη for  είναι για ποσες μέρες θα τρέχει το πρόγραμμα
for day in range(0,3652):
    if day < 3600:
        if day % 30 == 0:
            month_count += 1
            number_of_cars = number_of_cars2
            if month_count % 12 == 0:
                year_count += 1
                year += 1
            number_of_cars2 = number_of_cars + scenario.loc[year_count, 'Monthly imported EVs']

        
    sum_hourly_energy_consumption[day] = np.zeros(24) 
    #αυτή η for τρεχει ολο τον dict .csv και υπολογιζει για καθε αυτοκινητο τι καταναλωση που εκανε εκεινη την ημερα
    for i in data.index:  
        
        #gia tin miosi tis mpatarias ana xrono 
        if month_count % 12 == 0 and day != 0: #na to kita3oume
            data.at[i,'State of Health'] = 1 - (year - data.at[i,'Import Year'])*0.02025
    
        #το If εδώ ειναι για να ξεχωριζουμε τις καθημερινες με τα σκ (παιρνει αναλογος τι σωστη στηλη του .csv)
        if day % 7 != 5 and day % 7 != 6:
            #οι επομενες 2 if ειναι για να τα 2 ειδη αυτοκινητου που επιλεξαμε
            if data.at[i, 'Type of EV'] == "BEV":
               # daily_total_consumption = float(row[5]) * consumption_per_km[car_id]
                data.at[i, ' Battery State (%)'] -= data.at[i, 'Daily consumption(%)']/2 
                data.at[i, 'Capacity to full charge'] = (100 - data.at[i, ' Battery State (%)'])*data.at[i,  'Battery SOH']/100
            
            if data.at[i, 'Type of EV'] == "PHEV":
                #daily_total_consumption = float(row[5]) * consumption_per_km[car_id]
                #αν δεν φτανει η μπαταρια να παει μεχρι την δουλεια κανε το data[' Battery State (%)']=0 αλλιως αν δεν φτανει μεχρι το σπιτι κανε το ποσο ξοδεψε σημερα οσο μπαταρια του εχει απομεινει 
                if data.at[i, 'Daily consumption(%)']/2 > data.at[i, ' Battery State (%)']:
                    data.at[i, ' Battery State (%)'] = 0
                elif data.at[i, 'Daily consumption(%)'] >  data.at[i, ' Battery State (%)']:
                    data.at[i, 'Daily consumption(%)'] = data.at[i, ' Battery State (%)'] # λόγω της δυαδικότητας του προβλήματος θεωρούμε ότι καταναλώνεται το ίδιο ποσό ενέργειας στο πήγαινε-έλα(υπάρχει ενα μικρό ποσοστό σφάλματος)
                
                #αν εχει φτασει η μπαταρια μεχρι την δουλεια αφειρει απο την μπαταρια ποσο ξοδεψε να  φτασει στην δουλεια
                if data.at[i, ' Battery State (%)'] !=0:
                    data.at[i, ' Battery State (%)'] -= data.at[i, 'Daily consumption(%)']/2  
                
                data.at[i, 'Capacity to full charge'] = (100 - data.at[i, ' Battery State (%)']) * data.at[i,  'Battery SOH']/100
            #αρχικοποιει το dictionary 
            hourly_energy_consumption[i] = np.zeros(24)

            # einai gia melontika ama baloume pano apo 160 km max
            if data.at[i, ' Battery State (%)'] < data.at[i, 'Daily consumption(%)']/2 and data.at[i, 'Type of EV'] == "BEV" :
                find_charging_times_and_consumption_outdoors(hourly_energy_consumption[i], data.at[i, 'Departure Time'],  data.at[i, 'Capacity to full charge'], data.at[i, 'Arrival Time'],  i)
            #αν οταν φτασει στην δουλεια εχει λιγοτερο απο 50% μπαταρια μετρα τα αυτοκινητα
            if data.at[i, ' Battery State (%)'] < 50 and data.at[i, 'Type of EV'] == "BEV":
                c1 += 1
                #το ενα στα 8 αυτοκιητα BEV που πρεπει να φορτιστουν στην δουλεια να φορτιζονται οντως 
                if int(c1) % 8 == 0:
                    find_charging_times_and_consumption_outdoors(hourly_energy_consumption[i], data.at[i, 'Departure Time'],  data.at[i, 'Capacity to full charge'],  data.at[i, 'Arrival Time'],  i)
                
            #αν οταν φτασει στην δουλεια εχει λιγοτερο απο 50% μπαταρια μετρα τα αυτοκινητα
            if data.at[i, ' Battery State (%)'] < 50 and data.at[i, 'Type of EV'] == "PHEV":
                c2 += 1
                #το ενα στα 4 αυτοκιητα PHEV που πρεπει να φορτιστουν στην δουλεια να φορτιζονται οντως 
                if int(c2) % 4 == 0:
                    find_charging_times_and_consumption_outdoors(hourly_energy_consumption[i], data.at[i, 'Departure Time'],  data.at[i, 'Capacity to full charge'],  data.at[i, 'Arrival Time'],  i)
            #παει και αφερει απο την μπαταρια την επιστροφη στο σπιτι    
            if data.at[i, 'Type of EV'] == "BEV":
                data.at[i, ' Battery State (%)'] -= data.at[i, 'Daily consumption(%)']/2
                data.at[i, 'Capacity to full charge'] = (100 - data.at[i, ' Battery State (%)'])*data.at[i,  'Battery SOH']/100
            
            if data.at[i, 'Type of EV'] == "PHEV":
                if data.at[i, ' Battery State (%)'] !=0:
                    data.at[i, ' Battery State (%)'] -= data.at[i, 'Daily consumption(%)']/2
                data.at[i, 'Capacity to full charge'] = (100 - data.at[i, ' Battery State (%)'])*data.at[i,  'Battery SOH']/100
            #ελενχει αμα θελει φορτιση 
            if data.at[i, ' Battery State (%)'] < 50 :
                find_charging_times_and_consumption(hourly_energy_consumption[i],  data.at[i, 'Arrival Time'], data.at[i, 'Capacity to full charge'], data.at[i, 'Charging Speed [kW]'],  data.at[i, 'Departure Time'], i)
            
        
        #το else ειναι τα σκ (κανει ακριβως τα ιδια με πανω)   
        else:
            
            if data.at[i, 'Type of EV'] == "BEV":
                #data.at[i, 'Daily consumption wkn(%)'] = d * consumption_per_km[car_id]
                data.at[i, ' Battery State (%)'] = data.at[i, ' Battery State (%)']-data.at[i, 'Daily consumption wkn(%)']/2
                data.at[i, 'Capacity to full charge'] = (100 - data.at[i, ' Battery State (%)'])*data.at[i,  'Battery SOH']/100
                

            if data.at[i, 'Type of EV'] == "PHEV":
                #data.at[i, 'Daily consumption wkn(%)'] = float(row[6]) * consumption_per_km[car_id]
                
                if data.at[i, 'Daily consumption wkn(%)']/2 > data.at[i, ' Battery State (%)']:
                    data.at[i, ' Battery State (%)'] = 0
                elif data.at[i, 'Daily consumption wkn(%)'] >  data.at[i, ' Battery State (%)']:
                    data.at[i, 'Daily consumption wkn(%)'] = data.at[i, ' Battery State (%)'] # λόγω της δυαδικότητας του προβλήματος θεωρούμε ότι καταναλώνεται το ίδιο ποσό ενέργειας στο πήγαινε-έλα(υπάρχει ενα μικρό ποσοστό σφάλματος)
                
                
                if data.at[i, ' Battery State (%)'] !=0:
                    data.at[i, ' Battery State (%)'] = data.at[i, ' Battery State (%)']-data.at[i, 'Daily consumption wkn(%)']/2
                
                data.at[i, 'Capacity to full charge'] = (100 - data.at[i, ' Battery State (%)']) * data.at[i,  'Battery SOH']/100
            
            hourly_energy_consumption[i] = np.zeros(24)
            
            if data.at[i, ' Battery State (%)'] < 50 and data.at[i, 'Type of EV'] == "BEV":
                c1 += 1
                if int(c1) % 8 == 0:
                    find_charging_times_and_consumption_outdoors_wkn(hourly_energy_consumption[i], data.at[i, 'Departure Time'],  data.at[i, 'Capacity to full charge'],  data.at[i, 'Arrival Time'],  i)
            
            if data.at[i, ' Battery State (%)'] < 50 and data.at[i, 'Type of EV'] == "PHEV":
                c2 += 1
                if int(c2) % 4 == 0:
                    find_charging_times_and_consumption_outdoors_wkn(hourly_energy_consumption[i], data.at[i, 'Departure Time'],  data.at[i, 'Capacity to full charge'],  data.at[i, 'Arrival Time'],  i)
                
            if data.at[i, 'Type of EV'] == "BEV":
                data.at[i, ' Battery State (%)'] -= data.at[i, 'Daily consumption wkn(%)']/2
                data.at[i, 'Capacity to full charge'] = (100 - data.at[i, ' Battery State (%)'])*data.at[i,  'Battery SOH']/100
            
            if data.at[i, 'Type of EV'] == "PHEV":
                if data.at[i, ' Battery State (%)'] !=0:
                    data.at[i, ' Battery State (%)'] -= data.at[i, 'Daily consumption wkn(%)']
                data.at[i, 'Capacity to full charge'] = (100 - data.at[i, ' Battery State (%)'])*data.at[i,  'Battery SOH']/100
            
            if data.at[i, ' Battery State (%)'] < 50 :
                find_charging_times_and_consumption_wkn(hourly_energy_consumption[i],  data.at[i, 'Arrival Time'], data.at[i, 'Capacity to full charge'], data.at[i, 'Charging Speed [kW]'],  data.at[i, 'Departure Time'], i)
            
        find_sum_hourly_energy_consumption(sum_hourly_energy_consumption[day], hourly_energy_consumption[i])
        if i == number_of_cars2 :
            break
        #car_id += 1
    #για κάθε 30 μερες δημιουργει 1 αρχειο .csv που μεσα εχει την καταναλωση του εκαστοτε αυτοκινητου για καθε ωρα της μερας
    if day % 360 == 0  : 
        hourly_consumption = pd.DataFrame(hourly_energy_consumption).T
        hourly_consumption.to_csv("dedomenaday" + str(day) + ".csv")
        #print(data[' Battery State (%)'])
           
   
#η εξοδος μας που ειναι η συνολικη καταναλωσει ανα μερα ολων τον αυτοκινητων 

sum_consumption = pd.DataFrame(sum_hourly_energy_consumption).T
sum_consumption.to_csv('sum_consumption.csv')