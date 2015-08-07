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
                              (The appointment “evolves”.)
```

###“Specials”
Now for the interesting part. Specials are intended to be used as a method to highlight special information
about an appointment. Thus, if written as plain text, specials would be those parts of the subject that are
prepended by special characters as `#`, `$`, `|`, `@`, etc.

An object of the `special` class, implemented in the file `special.py`, contains a dictionary that
defines the special parts to be considered. Further, it contains dictionaries that define the behavior
of those special parts when a corresponding appointment is output or evolves.

Duplicate special parts may cause undefined behavior.

By default, the following specials are used:
```
Char  Meaning     Default print behavior      Default evolution behavior

 @    Location    @<value>                    @<value> → @<value>
 #    Number      #<value>  (No | present)    #<value> → #<value + 1>     (No $ present)
                  <nothing> (else)            #<value> → #<value + step>  (step = value of $)
                                              Note: Evolution fails if the resulting new value is greter than
                                                the value of a present “Count” special part
 |    Count       <nothing> (No # present)    |<value> → |<value>
                  <num> of <value> 
                        (num = value of #)
 $    Step        <nothing>                   $<value> → $<value>
```

To change the default behavior, dictionaries different from the default ones can be passed
during the object construction. The values of the different specials are stored in a dictionary
`tokens`.
```
 Dict [Source]                    Entry
 
 token_map [char]                 unique string
 evolution_map [token_map[char]]  function taking the tokens and returning the new value
 print_map [token_map[char]]      function taking the tokens and returning a string
 
 tokens [token_map[char]]         value of the special;
                                  can be passed as tokens [char], but will then be converted 
```
It is also possible to replace only some of the dictionaries' ertries.

Methods for `special` objects include:
```
has_next() : bool     Checks whether the corresponding appoint object can evolve
evolve() : special    Returns the special object obtained by applying the evolution_map on every entry in tokens
print() : string      Returns the string obtained by applying the print_map on every entry in tokens
```

Examples can be found in the `examples` folder.

###Input/ Output
Input and output routines are implemented in the file `io.py`.
####File IO

