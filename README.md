appoints
=
A library for managing appointments
-

###Overview
The appoints lib helps organize appointments. (Surprise)
It is capable of reckoning whether an appointment _or, in case of recurring appointments,
whether a future of these_ is on a given day or not.

The lib can parse the appointments from files; consult the section Input/ Output for further details.

###Appointments
Appointments are stored in objects of the `appoint` class, which is implemented in the file `appoint.py`.

Appoint objects strore what you'd expect:
```
start : datetime            The appointment's start date
end   : datetime            The appointment's end date
inc   : [int,int,int,int]   The time after start until the appointment repeats,
                              given as list of exactly 4 values: [#years, #days, #hours, #minutes]
                            Note: #years describes the number of years, i.e. one year may equal to 365 or 366 days
                            Note: To have an appointment happen every month (e.g. every 1st), simply create
                                  12 appointments that repeat every year
                            Note: To not have an appointment repeat, simply set all values to 0
prio  : int                 The appointment's priority
text  : string              The appointment's subject
spec  : special             See the section special for details
```                            

Methods for appoint objects include:
```
is_present( curr_time : datetime ) : boolean
                            Checks whether the appointment is on the date given through curr_time
is_past( curr_time : datetime ) : boolean     
                            Checks whether the appointment is before the date given through curr_time
is_future( curr_time : datetime ) : boolean     
                            Checks whether the appointment is after the date given through curr_time

is_present( curr_time : datetime, time_eps : timedelta ) : boolean     
                            Checks whether the appointment is after the date given through curr_time
                              but before the date curr_time + time_eps

evolve( ) : appoint         Generates the next occurance of the appointment or None if there's none
```

###“Specials”


###Input/ Output
Input and output routines are implemented in the file `io.py`.
####File IO

