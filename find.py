import json
import requests
import threading
# import required module
from playsound import playsound
from datetime import date, timedelta

 
# for playing note.mp3 file

runCount = 0
locations = []
zipcode = input("Enter ZipCode \n")
print("searching within 10 miles")
# this uses DMV built in API which defaults to 10 miles, if you were to search within a bigger range, such as 25 miles, use the coordinates given-
# -in branches = requests.get("https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/") or zipcode and find
# the distance between that and your input zipcode. If less than 25 miles (or whatever # u use) than add that DMV id to the locations list


searchWindow = int(input("Within how many days do you need an appointment? \n"))
lastDay = (date.today()+timedelta(days=searchWindow)).isoformat()
print(lastDay)


search = requests.get("https://www.dmv.ca.gov/portal/wp-json/dmv/v1/field-offices?q="+zipcode)
list = search.json()

if len(list)==0:
    print("No nearby DMV found")
    exit()

# creates locations list with location name and id used for DMV API
for i in range(len(list)):
    if i >1:
        print("searching " + list[i]["slug"])
        locations.append([list[i]["slug"],list[i]["meta"]["dmv_field_office_public_id"]])





def scan():
    # looping process
    global runCount
    runCount += 1
    print("iteration: " + str(runCount))
    threading.Timer(40, scan).start()

    for i in locations:
        global found
        cLocation = i[1]
        response = requests.get('https://www.dmv.ca.gov/portal/wp-json/dmv/v1/appointment/branches/'+cLocation+'/dates?services[]=DT!1857a62125c4425a24d85aceac6726cb8df3687d47b03b692e27bd8d17814&numberOfCustomers=1')
        data = response.json()
        found = False
        for cday in data:
            # checks if availible appointments are in an earlier month than final day or in an earlier day and same month
            if(cday[5:7]<lastDay[5:7]) or (cday[8:10]<=lastDay[8:10] and cday[5:7]==lastDay[5:7]):
                found = True
                print("FOUND DATE AT " + i[0] + ": "+ cday)
                playsound('vine-boom.mp3')
        if(found==False):
            print("No dates found... rerunning in 40 sec")

    

    
    

scan()


