import datetime
import random
import pymongo
from tkinter import ttk, messagebox
from dateutil import parser
from tkinter import *

def doSomething(event):
    print("Mouse coordinates: " + str(event.x)+","+str(event.y))
def viewGivenTrips(window,src,dest):
    window.destroy()
    ws = Tk()
    ws.title('View trips')
    ws.geometry('800x500')
    ws['bg'] = '#AC99F2'

    trip_frame = Frame(ws)
    trip_frame.pack()

    trips = ttk.Treeview(trip_frame)

    trips['columns'] = ("TRIP ID", "BUS ID", "FROM", "TO", "DATE", "DEPARTURE", "ARRIVAL", "SEATS AVAILABLE","FARE (in ₹)")

    trips.column("#0", width=0, stretch=NO)
    trips.column("TRIP ID", anchor=CENTER, width=80)
    trips.column("BUS ID", anchor=CENTER, width=80)
    trips.column("FROM", anchor=CENTER, width=80)
    trips.column("TO", anchor=CENTER, width=80)
    trips.column("DATE", anchor=CENTER, width=80)
    trips.column("DEPARTURE", anchor=CENTER, width=80)
    trips.column("ARRIVAL", anchor=CENTER, width=80)
    trips.column("SEATS AVIALABLE", anchor=CENTER, width=110)
    trips.column("FARE (in ₹)", anchor=CENTER, width=110)
    trips.heading("#0", text="", anchor=CENTER)
    trips.heading("TRIP ID", text="TRIP ID", anchor=CENTER)
    trips.heading("BUS ID", text="BUS ID", anchor=CENTER)
    trips.heading("FROM", text="FROM", anchor=CENTER)
    trips.heading("TO", text="TO", anchor=CENTER)
    trips.heading("DATE", text="DATE", anchor=CENTER)
    trips.heading("DEPARTURE", text="DEPARTURE", anchor=CENTER)
    trips.heading("ARRIVAL", text="ARRIVAL", anchor=CENTER)
    trips.heading("SEATS AVIALABLE", text="SEATS AVIALABLE", anchor=CENTER)
    trips.heading("FARE (in ₹)", text="FARE (in ₹)", anchor=CENTER)
    from_loc = src
    to_loc = dest
    i = 0
    for trip in db['trips'].find():
        busid = trip['bus_id']
        for bus in db['bus'].find():
            if bus['bus_id'] == busid and bus['from_location'] == from_loc and bus['to_location'] == to_loc:
                trips.insert(parent='', index='end', iid=i, text='',
                             values=(
                             str(trip['trip_id']), str(busid), from_loc, to_loc, trip['date'], bus['departure_time'],
                             bus['arrival_time'], trip['seats_available'],str(int(duration(bus['departure_time'], bus['arrival_time']).split('h')[0])*20)))
                i = i+1
    trips.pack()
    tripid = Entry(ws)
    tripid.place(x=435, y=300)
    Label(ws, text='ID of trip to book', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=300, y=300)
    Label(ws, text='Passenger\'s full name', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=265,y=352)
    passengername = Entry(ws)
    passengername.place(x=437, y=352)
    Label(ws, text='Passenger\'s contact no.', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=242, y=396)
    passengercontact = Entry(ws)
    passengercontact.place(x=435,y=391)
    Button(ws, text='Book ticket', bg='#C1CDCD', font=('arial', 12, 'normal'),
           command=lambda: bookTicket(tripid.get().lower().capitalize(),
                                      passengername.get().lower().capitalize(),passengercontact.get())).place(x=360, y=450)
    ws.mainloop()
def bookTicket(tripid,passengername,passengercontact):
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
                if bus['bus_id']==busidtobook:
                    bus_maxseats = bus['total_seats']
            if trip_availseats != 0:
                ticketid = random.randint(1000, 4000)
                ticketinput = {'passenger_name': name,
                               'ticket_id': ticketid,
                               'trip_id': id,
                               'bus_id': busidtobook,
                               'seat_no': bus_maxseats - trip_availseats + 1,
                               'passenger_contact':passengercontact}
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
                f.write("Passenger Contact Number: " + passengercontact + "\n")
                f.write("Ticket ID: " + str(ticketid) + "\n")
                f.write("Bus Name: " + busname + "\n")
                f.write("Trip : " + src + " to " + dest + "\n")
                f.write("Trip ID: " + str(id) + "\n")
                f.write("Departure date and time: " + date + " " + dep + "\n")
                f.write("Trip duration: " + duration(dep, arr) + "\n")
                f.write("----------------------------------------\n")
                f.write("Trip Fare: INR " + str(int(duration(dep, arr).split('h')[0])*20) + "\n")
                f.write("----------------------------------------\n")
                f.write("\nNote: Please be ready at your bus station atleast 30 minutes before the scheduled departure time of the bus\n")
                f.close()
                messagebox.showinfo(title="ticket booked", message="the ticket is booked with your ticket at "+"D:\\" + ticketname + ".txt")
            else:
                messagebox.showinfo(title="ticket not booked", message="the seats are full for the trip")


def ticketbooking():
    ticketbookingwindow = Tk()
    ticketbookingwindow.geometry('649x402')
    ticketbookingwindow.configure(background='#F0F8FF')
    ticketbookingwindow.title('Book ticket')
    tripid = Entry(ticketbookingwindow)
    tripid.place(x=326, y=82)
    Label(ticketbookingwindow, text='ID of trip to book', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=192, y=83)
    Label(ticketbookingwindow, text='Passenger\'s full name', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=155,
                                                                                                                y=132)
    passengername = Entry(ticketbookingwindow)
    passengername.place(x=326, y=129)
    Button(ticketbookingwindow, text='Book ticket', bg='#C1CDCD', font=('arial', 12, 'normal'),
           command=lambda:bookTicket(tripid.get().lower().capitalize(),passengername.get().lower().capitalize())).place(x=275, y=227)
    ticketbookingwindow.mainloop()


def buttonBook():
    root.destroy()
    bookingswindow = Tk()
    bookingswindow.geometry('559x361')
    bookingswindow.configure(background='#F0F8FF')
    bookingswindow.title('trips')
    source = Entry(bookingswindow)
    source.place(x=250, y=104)
    Label(bookingswindow, text='Source city', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=157, y=105)
    destination = Entry(bookingswindow)
    destination.place(x=250, y=153)
    Label(bookingswindow, text='Destination city', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=130, y=153)
    Button(bookingswindow, text='View trips', bg='#C1CDCD', font=('arial', 12, 'normal'), command=lambda:viewGivenTrips(bookingswindow,source.get().lower().capitalize(),destination.get().lower().capitalize())).place(
        x=234, y=216)
    bookingswindow.mainloop()


def cancelTicket(id):
    collection = db['ticket']
    collection2 = db['trips']
    id = int(id)
    query1 = {"ticket_id": id}
    seats = 0
    for ticket in collection.find():
        if ticket['ticket_id'] == id:
            tripid = ticket['trip_id']
            for trip in collection2.find():
                if trip['trip_id'] == tripid:
                    seats = trip['seats_available']
                    break
            oldseats = {'trip_id': tripid, 'seats_available': seats}
            newseats = {'$set': {'seats_available': seats + 1}}
            collection2.update_one(oldseats, newseats)
            collection.delete_one(query1)
    messagebox.showinfo(title="ticket cancelled", message="the ticket is cancelled")



def buttonCancelBooking():
    window = Tk()

    window.geometry('557x460')
    window.configure(background='#F0F8FF')
    window.title('Cancel ticket')
    id = Entry(window)
    id.place(x=250, y=150)
    Label(window, text='4-digit ticket ID', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=138, y=150)
    Button(window, text='CANCEL BOOKING', bg='#C1CDCD', font=('arial', 12, 'normal'),
           command=lambda: cancelTicket(id.get())).place(x=200, y=200)
    window.mainloop()
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
    messagebox.showinfo(title="bus added", message="the bus is added")
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


def deletebus(id):
    id = int(id)
    collection = db['bus']
    collection2 = db['trips']
    collection3 = db['ticket']
    for trip in collection2.find():
        if trip['bus_id']==id:
            tripid = trip['trip_id']
            collection3.delete_many({'trip_id':int(tripid)})
    collection2.delete_many({'bus_id': id})
    collection.delete_one({'bus_id': id})
    messagebox.showinfo(title="bus deleted", message="the bus is deleted")


def scheduleTrip(id,date):
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
    messagebox.showinfo(title="trip scheduled", message="Trip scheduled with trip id "+str(tripid))


def deleteTrip(tripid):
    collection = db['trips']
    collection.delete_one({"trip_id": int(tripid)})
    collection2 = db['ticket']
    collection2.delete_many({'trip_id':int(tripid)})
    messagebox.showinfo(title="trip deleted", message="Trip deleted")

def viewTrips():
    ws = Tk()
    ws.title('View trips')
    ws.geometry('800x300')
    ws['bg'] = '#F0F8FF'

    trip_frame = Frame(ws)
    trip_frame.pack()

    trips = ttk.Treeview(trip_frame)

    trips['columns'] = ("TRIP ID", "BUS ID", "FROM", "TO", "DATE", "DEPARTURE", "ARRIVAL", "SEATS AVIALABLE","FARE (in ₹)")

    trips.column("#0", width=0, stretch=NO)
    trips.column("TRIP ID", anchor=CENTER, width=80)
    trips.column("BUS ID", anchor=CENTER, width=80)
    trips.column("FROM", anchor=CENTER, width=80)
    trips.column("TO", anchor=CENTER, width=80)
    trips.column("DATE", anchor=CENTER, width=80)
    trips.column("DEPARTURE", anchor=CENTER, width=80)
    trips.column("ARRIVAL", anchor=CENTER, width=80)
    trips.column("SEATS AVIALABLE", anchor=CENTER, width=110)
    trips.column("FARE (in ₹)", anchor=CENTER, width=110)

    trips.heading("#0", text="", anchor=CENTER)
    trips.heading("TRIP ID", text="TRIP ID", anchor=CENTER)
    trips.heading("BUS ID", text="BUS ID", anchor=CENTER)
    trips.heading("FROM", text="FROM", anchor=CENTER)
    trips.heading("TO", text="TO", anchor=CENTER)
    trips.heading("DATE", text="DATE", anchor=CENTER)
    trips.heading("DEPARTURE", text="DEPARTURE", anchor=CENTER)
    trips.heading("ARRIVAL", text="ARRIVAL", anchor=CENTER)
    trips.heading("SEATS AVIALABLE", text="SEATS AVIALABLE", anchor=CENTER)
    trips.heading("FARE (in ₹)", text="FARE (in ₹)", anchor=CENTER)
    i = 0
    for trip in db['trips'].find():
        busid = trip['bus_id']
        for bus in db['bus'].find():
            if bus['bus_id'] == busid:
                trips.insert(parent='', index='end', iid=i, text='',
                             values=(
                             str(trip['trip_id']), str(busid), bus['from_location'], bus['to_location'], trip['date'],
                             bus['departure_time'], bus['arrival_time'], trip['seats_available'],str(int(duration(bus['departure_time'], bus['arrival_time']).split('h')[0])*20)))
                i = i + 1
    trips.pack()
    ws.mainloop()

def sel(window,var):
    window.destroy()
    if var.get()==1:
        addbuswindow = Tk()

        addbuswindow.geometry('557x460')
        addbuswindow.configure(background='#F0F8FF')
        addbuswindow.title('Add a bus')

        busid = Entry(addbuswindow)
        busid.place(x=270, y=20)
        Label(addbuswindow, text='4-digit bus ID', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=170, y=20)

        busname = Entry(addbuswindow)
        busname.place(x=270, y=70)
        Label(addbuswindow, text='bus name', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=170, y=70)

        src = Entry(addbuswindow)
        src.place(x=270, y=120)
        Label(addbuswindow, text='Source City', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=170, y=120)

        dest = Entry(addbuswindow)
        dest.place(x=270, y=170)
        Label(addbuswindow, text='Destination City', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=150, y=170)

        dep = Entry(addbuswindow)
        dep.place(x=300, y=220)
        Label(addbuswindow, text='Departure Time (HH:MM)', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=110,
                                                                                                             y=220)

        arr = Entry(addbuswindow)
        arr.place(x=300, y=270)
        Label(addbuswindow, text='Arrival Time (HH:MM)', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=110, y=270)

        seats = Entry(addbuswindow)
        seats.place(x=270, y=320)
        Label(addbuswindow, text='Total seats', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=170, y=320)

        Button(addbuswindow, text='ADD BUS', bg='#C1CDCD', font=('arial', 12, 'normal'), command=lambda:addbus(busid.get(),busname.get(),src.get().lower().capitalize(),dest.get().lower().capitalize(),dep.get(),arr.get(),seats.get())).place(x=280,y=354)

        addbuswindow.mainloop()
    elif var.get()==2:
        deletebuswindow = Tk()
        deletebuswindow.geometry('557x460')
        deletebuswindow.configure(background='#F0F8FF')
        deletebuswindow.title('Source city')

        busid = Entry(deletebuswindow)
        busid.place(x=250, y=150)
        Label(deletebuswindow, text='4-digit bus ID', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=138, y=150)


        Button(deletebuswindow, text='DELETE BUS', bg='#C1CDCD', font=('arial', 12, 'normal'),
               command=lambda: deletebus(busid.get())).place(x=200, y=200)
        deletebuswindow.mainloop()
    elif var.get()==3:
        scheduleTripwindow = Tk()
        scheduleTripwindow.geometry('557x460')
        scheduleTripwindow.configure(background='#F0F8FF')
        scheduleTripwindow.title('Schedule trip')
        busid = Entry(scheduleTripwindow)
        busid.place(x=270, y=120)
        Label(scheduleTripwindow, text='4-digit bus ID', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=170, y=120)
        tripdate = Entry(scheduleTripwindow)
        tripdate.place(x=270, y=170)
        Label(scheduleTripwindow, text='Date of trip (YYYY-MM-DD)', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=70, y=170)
        Button(scheduleTripwindow, text='SCHEDULE TRIP', bg='#C1CDCD', font=('arial', 12, 'normal'),command=lambda: scheduleTrip(busid.get(),tripdate.get())).place(x=200,y=200)
        scheduleTripwindow.mainloop()
    elif var.get()==4:
        deleteTripwindow = Tk()
        deleteTripwindow.title('View trips')
        deleteTripwindow.geometry('800x400')
        deleteTripwindow['bg'] = '#F0F8FF'

        trip_frame = Frame(deleteTripwindow)
        trip_frame.pack()

        trips = ttk.Treeview(trip_frame)

        trips['columns'] = ("TRIP ID", "BUS ID", "FROM", "TO", "DATE", "DEPARTURE", "ARRIVAL", "SEATS AVIALABLE")

        trips.column("#0", width=0, stretch=NO)
        trips.column("TRIP ID", anchor=CENTER, width=80)
        trips.column("BUS ID", anchor=CENTER, width=80)
        trips.column("FROM", anchor=CENTER, width=80)
        trips.column("TO", anchor=CENTER, width=80)
        trips.column("DATE", anchor=CENTER, width=80)
        trips.column("DEPARTURE", anchor=CENTER, width=80)
        trips.column("ARRIVAL", anchor=CENTER, width=80)
        trips.column("SEATS AVIALABLE", anchor=CENTER, width=110)

        trips.heading("#0", text="", anchor=CENTER)
        trips.heading("TRIP ID", text="TRIP ID", anchor=CENTER)
        trips.heading("BUS ID", text="BUS ID", anchor=CENTER)
        trips.heading("FROM", text="FROM", anchor=CENTER)
        trips.heading("TO", text="TO", anchor=CENTER)
        trips.heading("DATE", text="DATE", anchor=CENTER)
        trips.heading("DEPARTURE", text="DEPARTURE", anchor=CENTER)
        trips.heading("ARRIVAL", text="ARRIVAL", anchor=CENTER)
        trips.heading("SEATS AVIALABLE", text="SEATS AVIALABLE", anchor=CENTER)
        i = 0
        for trip in db['trips'].find():
            busid = trip['bus_id']
            for bus in db['bus'].find():
                if bus['bus_id'] == busid:
                    trips.insert(parent='', index='end', iid=i, text='',
                                 values=(
                                     str(trip['trip_id']), str(busid), bus['from_location'], bus['to_location'],
                                     trip['date'],
                                     bus['departure_time'], bus['arrival_time'], trip['seats_available']))
                    i = i + 1
        trips.pack()
        tripid = Entry(deleteTripwindow)
        tripid.place(x=270, y=240)
        Label(deleteTripwindow, text='4-digit trip ID', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=160, y=240)
        Button(deleteTripwindow, text='CANCEL TRIP', bg='#C1CDCD', font=('arial', 12, 'normal'),
               command=lambda: deleteTrip(tripid.get())).place(x=260, y=290)
        deleteTripwindow.mainloop()
    else:
        viewTrips()

def adminloggedinwindow():
    adminMenu = Tk()
    Label(adminMenu, text='Select function', bg='#F0F8FF',borderwidth=2,relief="groove", font=('arial', 12, 'normal')).place(x=50, y=145)
    adminMenu.geometry('200x200')
    adminMenu.title('Admin function')
    adminMenu.configure(background='#F0F8FF')
    var = IntVar()
    R1 = Radiobutton(adminMenu, text="Add bus", variable=var, value=1,
                     command=lambda:sel(adminMenu,var),bg='#F0F8FF')
    R1.pack(anchor=W)

    R2 = Radiobutton(adminMenu, text="Delete bus", variable=var, value=2,
                     command=lambda:sel(adminMenu,var),bg='#F0F8FF')
    R2.pack(anchor=W)

    R3 = Radiobutton(adminMenu, text="Schedule a trip", variable=var, value=3,
                     command=lambda:sel(adminMenu,var),bg='#F0F8FF')
    R3.pack(anchor=W)
    R4 = Radiobutton(adminMenu, text="Cancel a trip", variable=var, value=4,
                     command=lambda: sel(adminMenu,var),bg='#F0F8FF')
    R4.pack(anchor=W)
    R5 = Radiobutton(adminMenu, text="View all trips", variable=var, value=5,
                     command=lambda: sel(adminMenu,var),bg='#F0F8FF')
    R5.pack(anchor=W)

    label = Label(adminMenu)
    label.pack()
    adminMenu.mainloop()


def adminlogin(window,p):
    window.destroy()
    if p=="123":
        adminloggedinwindow()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['BUS_RESERVATION']
for trip in db['trips'].find():
    if parser.parse(trip['date']).date()<datetime.date.today():
        db['trips'].delete_one(trip)
root = Tk()
root.geometry('829x516')
root.configure(background='#F0F8FF')
root.title('Bus Reservation window')

canvas = Canvas(root, width=350, height=200)
canvas.pack()
img = PhotoImage(file="D:\\BUS_RESERVATION_MANAGEMENT_SYSTEM\\busimage.png")
canvas.create_image(20, 20, anchor=NW, image=img)
label = Label(root,
              text="WELCOME TO SUNSHINE TRAVELS",
              font=('Arial',20,'bold'),
              fg='#00FF00',
              bg='black',
              relief=RAISED,
              bd=10,
              padx=20,
              pady=20,
              compound='bottom')
label.pack()
passwordbox=Entry(root)
passwordbox.place(x=270, y=427)
Label(root, text='Enter Admin Password', bg='#F0F8FF', font=('arial', 12, 'normal')).place(x=93, y=425)
Button(root, text='LOGIN AS ADMIN', bg='#C1CDCD', font=('arial', 12, 'normal'), command=lambda:adminlogin(root,passwordbox.get())).place(x=419,y=415)
Button(root, text='BOOK TICKET', bg='#C1CDCD', font=('arial', 12, 'normal'),command=buttonBook).place(x=234, y=327)
Button(root, text='CANCEL BOOKING', bg='#C1CDCD', font=('arial', 12, 'normal'), command=buttonCancelBooking).place(x=462, y=327)
root.mainloop()