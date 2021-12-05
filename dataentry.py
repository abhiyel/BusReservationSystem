#this program initializes the database
import random
import names
import pymongo
import datetime
def tripExists(id,date):
    for trip in db['trips'].find():
        if trip['bus_id']==id and trip['date']==date:
            return True
    return False
def scheduleTrip(id,date):
    if not tripExists(id,date):
        busid = int(id)
        tripid = random.randint(9000, 9999)
        collection = db['trips']
        buses = db['bus']
        for bus in buses.find():
            if bus['bus_id'] == busid:
                availSeats = bus['total_seats']
                break

        tripinput = {'bus_id': busid,
                     'date': date,
                     'trip_id': tripid,
                     'seats_available': availSeats}
        collection.insert_one(tripinput)


def bookTicket(tripid, passengername,n):
    collection = db['ticket']
    collection2 = db['trips']
    id = int(tripid)
    name = passengername

    for trip in collection2.find():
        if trip['trip_id'] == id:
            trip_availseats = trip['seats_available']
            date = trip['date']
            busidtobook = trip['bus_id']
            for bus in db['bus'].find():
                if bus['bus_id'] == busidtobook:
                    bus_maxseats = bus['total_seats']
            if trip_availseats != 0:
                ticketid = random.randint(1000, 4000)
                ticketinput = {'passenger_name': name,
                               'ticket_id': ticketid,
                               'trip_id': id,
                               'bus_id': busidtobook,
                               'seat_no': bus_maxseats - trip_availseats + 1,
                               'passenger_contact':n}
                collection.insert_one(ticketinput)
                old = {'seats_available': trip_availseats, 'trip_id': id}
                new = {'$set': {'seats_available': trip_availseats - 1}}
                collection2.update_one(old, new)
                for bus in db['bus'].find():
                    if bus['bus_id'] == busidtobook:
                        dep = bus['departure_time']
                        arr = bus['arrival_time']
                        busname = bus['bus_name']
                        src = bus['from_location']
                        dest = bus['to_location']
                ticketname = name.split(' ')[0] + str(ticketid)
                f = open("D:\\BUS_RESERVATION_MANAGEMENT_SYSTEM\\tickets\\" + ticketname + ".txt", "w+")
                f.write("***SUNSHINE TRAVELS**" + "\n")
                f.write("Passenger Name: " + name + "\n")
                f.write("Passenger Contact Number: " + n + "\n")
                f.write("Ticket ID: " + str(ticketid) + "\n")
                f.write("Bus Name: " + busname + "\n")
                f.write("Trip : " + src + " to " + dest + "\n")
                f.write("Trip ID: " + str(id) + "\n")
                f.write("Departure date and time: " + date + " " + dep + "\n")
                f.write("Trip duration: " + duration(dep, arr) + "\n")
                f.write("----------------------------------------\n")
                f.write("Trip Fare: INR " + str(int(duration(dep, arr).split('h')[0]) * 20) + " \n")
                f.write("----------------------------------------\n")
                f.write("\nNote: Please be ready at your bus station atleast 30 minutes before the scheduled departure time of the bus\n")
                f.close()



def duration(dep,arr):
    dep_h = int(dep.split(':')[0])
    dep_m = int(dep.split(':')[1])
    arr_h = int(arr.split(':')[0])
    arr_m = int(arr.split(':')[1])
    hd=0
    i = dep_h
    while True:
        if i==arr_h:
            break
        else:
            i = (i+1)%24
            hd = hd+1
    md=0
    i = dep_m
    while True:
        if i==arr_m:
            break
        else:
            i = (i+1)%60
            md = md+1
    if md==0:
        return str(hd)
    else:
        return str(hd)+"h"+str(md)+"m"
def addbus(a,b,c,d,e,f,h):
    collection=db['bus']
    businput = {'bus_id': int(a),
                'bus_name': b,
                'from_location': c,
                'to_location': d,
                'departure_time': e,
                'arrival_time': f,
                'total_seats': int(h)}
    collection.insert_one(businput)
client = pymongo.MongoClient("mongodb://localhost:27017/")
print("The database is being initialized.. do not close the program till done")
db = client['BUS_RESERVATION']
buses = db['bus']
tripses = db['trips']
tickets = db['ticket']

#drop the bus, trips and ticket collections if they exist
tripses.drop()
tickets.drop()
buses.drop()

#creating th bus collection
buses.insert_one({"bus_id":7000,"bus_name":"Rajya Sleeper","from_location":"Nagpur","to_location":"Shegaon","departure_time":"6:30","arrival_time":"13:45","total_seats":15})
buses.insert_one({"bus_id":5152,"bus_name":"Maharaja AC","from_location":"Nagpur","to_location":"Pune","departure_time":"18:00","arrival_time":"8:45","total_seats":45})
buses.insert_one({"bus_id":6232,"bus_name":"Rajya Sleeper","from_location":"Shegaon","to_location":"Nagpur","departure_time":"22:30","arrival_time":"5:30","total_seats":15})
buses.insert_one({"bus_id":6252,"bus_name":"Prithvi","from_location":"Aurangabad","to_location":"Nagpur","departure_time":"21:00","arrival_time":"7:30","total_seats":50})
buses.insert_one({"bus_id":8523,"bus_name":"Volvo 360","from_location":"Shirdi","to_location":"Nagpur","departure_time":"19:45","arrival_time":"8:00","total_seats":40})
buses.insert_one({"bus_id":8712,"bus_name":"Maharaja AC","from_location":"Pune","to_location":"Nagpur","departure_time":"17:30","arrival_time":"7:30","total_seats":45})
buses.insert_one({"bus_id":3724,"bus_name":"Surya Sleeper","from_location":"Nagpur","to_location":"Aurangabad","departure_time":"21:15","arrival_time":"7:00","total_seats":35})
buses.insert_one({"bus_id":3521,"bus_name":"Volvo 360","from_location":"Nagpur","to_location":"Shirdi","departure_time":"18:00","arrival_time":"5:59","total_seats":40})
buses.insert_one({"bus_id":2521,"bus_name":"Rajya Sleeper","from_location":"Shegaon","to_location":"Shirdi","departure_time":"7:00","arrival_time":"17:15","total_seats":15})
buses.insert_one({"bus_id":1531,"bus_name":"Surya Sleeper","from_location":"Aurangabad","to_location":"Pune","departure_time":"23:00","arrival_time":"4:35","total_seats":35})

#creating th trips collection
busids = []
for bus in buses.find():
    busids.append(bus['bus_id'])
for id in busids:
    for i in range(random.randint(0,10)):
        scheduleTrip(id,str(datetime.date.today() + datetime.timedelta(days=random.randint(0,10))))
tripids = []
for trip in tripses.find():
    tripids.append(trip['trip_id'])


#creating th ticket collection
fullnames = set()
contactnumbers = set()
for i in range(140):
    j = random.randint(0,len(tripids)-1)
    a = tripids[j]
    b = names.get_full_name()
    if b not in fullnames:
        fullnames.add(b)
        n = str(random.randint(9100000000,9999999999))
        if n not in contactnumbers:
            contactnumbers.add(n)
            bookTicket(a,b,n)
print("The database is now ready to use")