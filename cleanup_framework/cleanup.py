#TODO:
#      -maybe handle sheltering in init_db. but need to store final location somewhere
#            -shelter table includes final location
#            -table of individual requests includes offset from beginning of series, not
#             absolute block #
#      -write near & thresh cleanup fxns
#      -prettify/make it conform to python convention
#      -encapsulate SQL queries in fxns? (low priority)
#      -initdb, sheltering_and_cleanup, and db_to_trace should be the public methods.
"""Framework to simulate I/O sheltering with a variety of cleanup policies.

"""

import sqlite3
import csv
import glob
import cleanup_config as conf
from cleanup_policies import get_cleanup_class

class DataExistsError(Exception):
    def __init__(self, tbl, layout, code):
        self.tbl = tbl
        self.layout = layout
        self.code = code

def get_x_and_y(layout):
    #1 MB in sectors
    one_MB = 2 * 1024

    if layout == 1:
        x = 1 * one_MB
    elif layout == 2:
        x = 5 * one_MB
    elif pre == 3:
        x = 10 * one_MB
    else:
        raise Exception("Invalid shelter layout: {}".format(string(pre))) 
    y = x * 10
    return (x, y)

def round_down(num, divisor):
    return num - (num%divisor)

#return 1st block number of next shelter after block_num
def get_next_shelter (block_num, x, y):
    shelter = round_down(block_num, y) + (x * 9)
    #If shelter starts before block_num, last write must have been sheltered too
    #That's okay--we just want beginning of shelter
    return shelter

#given a request, break it into a list of requests 
#none of which overlaps with a shelter
def dodge_shelters(req, x, y):
    start = req[2]
    size = req[3]
    next_shelter = get_next_shelter(start, x, y)
    if start + size <= next_shelter:
        return [req]
    else:
        overlap = start + size - next_shelter
        new_req = copy(req)
        new_req[3] = size - overlap
        next_req = copy(req)
        next_req[2] = next_shelter + x
        next_req[3] = overlap
        new_reqs = dodge_shelters(next_req, x, y)
        new_reqs.append(new_req)
        return new_reqs

class CurrentReq:
    """Keep track of information about current sequential series of writes."""
    def __init__(self, request, layout):
        #total size of current series of requests
        self.size = request[3]
        #the requests themselves
        self.requests = [request]
        #are these reads or writes?
        self.flag = request[4]
        (self.x, self.y) = get_x_and_y(layout)
        return
    #the next sequential block in this series
    def get_next_blk(self):
        #we just look at last block; after shifting, this series may no longer be sequential
        return self.requests[-1][2] + self.requests[-1][3]
    def is_sequential(self, req):
        #the next request is sequential IF we have some requests already, 
        #AND its starting block comes after the tail of these requests, AND it's the same
        #type of I/O (i.e. read or write)
        return (self.requests and self.get_next_blk() == req[2] and self.flag == req[4])
    def add_req(self, request):
        assert(self.is_sequential(request))
        self.size += request[3]
        self.requests.append(request)
        return
    def should_shelter(self):
        return (self.size <= conf.cutoff and self.flag == 0)
    def shift_requests(self):
        new_reqs = []
        for req in self.requests:
            start_blk = req[2]
            size = req[3]
            #num_shelters is number of shelters that END behind the FIRST 
            #block of the request
            num_shelters = start_blk / self.y
            shift = num_shelters * self.x
            new_start = start_blk + shift
            next_shelter = get_next_shelter(new_start, self.x, self.y)
            if new_start >= next_shelter:
                #new_start is inside a shelter, shift it to just after shelter
                new_start = next_shelter + self.x
                next_shelter = get_next_shelter(new_start, self.x, self.y)
            req[2] = new_start
            #split up request as needed so it doesn't run into a shelter
            split_reqs = dodge_shelters(req, self.x, self.y)
            split_reqs.reverse()
            if not split_reqs:
                print "no split_reqs!"
            new_reqs.extend(split_reqs)
            self.requests = new_reqs
            return

#Add a sequential series of requests to the database
#Shift unshelter requests first!
def add_to_db(cursor, current_reqs, layout, tail):
    #First, shift as needed
    current_reqs.shift_requests()
    if current_reqs.should_shelter():
        shelter_flag = 1
    else:
        shelter_flag = 0

    #first we add an entry representing all these requests to seq_req_series table
    first = current_reqs.requests[0]
    series_start_time = first[0]
    series_disk = first[1]
    series_start_block = first[2]
    series_flag = first[4]
    series_total_size = sum([req[3] for req in current_reqs.requests])

    query = "INSERT INTO " + conf.series_t + \
            "(init_time, disk_num, total_start, total_size, flag, shelter, layout)" + \
            "VALUES(?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (series_start_time, series_disk, series_start_block, 
                           series_total_size, series_flag, shelter_flag, layout))
    id = cursor.lastrowid

   #Now we insert a row for each request into reqs_table
    query = "INSERT INTO " + conf.reqs_t + \
            "(time, start, size, elapsed, series_id)" +  \
            "VALUES(?, ?, ?, ?, ?)"
    req_table_rows = [ (req[0], req[2], req[3], req[5], id) for req in current_reqs.requests ]
    cursor.executemany(query, req_table_rows)

#initialize db
def init_db (layout):
    conn = sqlite3.connect(conf.db)
    curs = conn.cursor()

    #each entry represents one sequential series of requests

    #flag is 1 for read, 0 for write.
    #time is in seconds, and gives start time of first request in series
    #total_start is in sectors, and gives start of first request in series
    #total_size is in sectors, and gives total size of all requests in series
    #shelter is 1 if the request should be sheltered, 0 o/w
    #layout is code for layout of preallocated shelters: 1, 2, or 3
    query = "CREATE TABLE IF NOT EXISTS " + conf.series_t + \
            "(series_id INTEGER PRIMARY KEY, " + \
            "init_time REAL NOT NULL, " + \
            "disk_num INTEGER NOT NULL, " + \
            "total_start INTEGER NOT NULL, " + \
            "total_size INTEGER NOT NULL, " + \
            "flag INTEGER NOT NULL, " + \
            "shelter INTEGER NOT NULL, " + \
            "layout INTEGER NOT NULL)"
    curs.execute(query)

    #make sure data from this layout isn't in this table already
    query = "SELECT * FROM " + conf.series_t + " WHERE layout=?"
    curs.execute(query, (layout))
    if curs.fetchone():
        raise DataExistsError(conf.series_t, layout, None)

    #each entry represents one request
    #elapsed and time are in seconds
    #start_offset and size are in sectors
    #start_offset gives offset from beginning of this series of requests
    query = "CREATE TABLE IF NOT EXISTS " + conf.reqs_t + \
            "(req_id INTEGER PRIMARY KEY, " + \
            "time REAL NOT NULL, " + \
            "start_offset INTEGER NOT NULL, " + \
            "size INTEGER NOT NULL, " + \
            "elapsed REAL NOT NULL, " + \
            "series_id INTEGER NOT NULL, " + \
            "FOREIGN KEY(series_id) REFERENCES "+ conf.series_t +"(series_id)" + \
            ")"
    curs.execute(query)


    #create a table for keeping track of cleanup information for sheltered requests:
    #final_loc is final location to write to on cleanup (blk #)
    #clean_time is time scheduled for cleanup
    #code indicates cleanup policy
    query = "CREATE TABLE IF NOT EXISTS " + conf.cleanup_t + \
            "(id INTEGER PRIMARY KEY, " + \
            "series_id INTEGER NOT NULL, " + \
            "final_loc INTEGER NOT NULL, " + \
            "clean_time REAL, " + \
            "code CHAR, " + \
            "FOREIGN KEY (series_id) REFERENCES " + conf.series_t + "(series_id)" + \
            ")"

    curs.execute(query)

    #store all traces in table, shifting/sheltering as we go
    traces = glob.glob(conf.num+"_disk*")

    for trace in traces:
        print trace

        current_reqs = None
        with open(trace, "r") as input:
            tail = None
            reader = csv.reader(input, delimiter=' ')
            for row in reader:

                time = float(row[0])
                disk_num = row[1]
                block_num = int(row[2])
                block_size = int(row[3])
                flag = int(row[4])
                elapsed = float(row[5])

                #set row entries to casted values now so we don't have to deal with it later
                row[0] = time
                row[2] = block_num
                row[3] = block_size
                row[4] = flag
                row[5] = elapsed

                if not current_reqs:
                    #this is the first row!
                    current_reqs = CurrentReq(row, layout)
                    continue

                if current_reqs.is_sequential(row):
                    #this is a continuation of the current request
                    current_reqs.add_req(row)
                else:
                    #Now we add these requests to the database, sheltering if needed
                    tail = add_to_db(curs, current_reqs, layout, tail)
                    #And reset current_reqs
                    current_reqs = CurrentReq(row)

            #Now flush any remaining requests to database
            add_to_db(curs, current_reqs, layout, tail)
#    calculate_queue_lengths(curs)
    conn.commit()
    conn.close()


#Given a shelter start, get tail within shelter at a given time
def get_shelter_tail(cursor, shelt_start, time, layout, code):
    #get the shelter start block and size of all requests that are:
    # -in this shelter
    # -not cleaned up before this time
    #sort them in descending order by shelter start block
    #get the tail of the one
    query = "SELECT shelt_blk, total_size" + \
            "FROM " + shelter_t + \
            " WHERE ((clean_time IS NULL) OR " + \
            "(clean_time <  ? ))" + \
            "AND layout = ? AND code = ? "
            "ORDER BY shelt_blk DESC"
    cursor.execute(query, (time, layout, code))
    row = cursor.fetchone()
    return row['shelt_blk'] + row['total_size']


#Given a series of requests that needs to be sheltered, figure out where to shelter it
def shelter_request(cursor, row, layout, code):
    (x, y) = get_x_and_y(layout)
    #get the series of requests just before this one; i.e. the latest series for this layout
    #and this disk that isn't later than the current one
    prev_query = "SELECT init_time, total_start, total_size, shelter FROM " + series_t + \
        "WHERE layout=? AND disk_num=? AND init_time < ? ORDER BY init_time DESC"
    
    cursor.execute(prev_query, (layout, row['disk_num'], row['init_time']))
    prev_req = cursor.fetchone()
    if prev_req['shelter']:
        #these requests are sheltered. figure out where.
        prev_sheltered_query = "SELECT shelt_id FROM " + shelter_t + \
                               "WHERE series_id=?"
        cursor.execute(prev_sheltered_query, (prev_id))
        prev_shelt = cursor.fetchone()
        shelter = prev_shelt['shelt_id']

    else:
        #this request isn't sheltered so we just get the next shelter after its tail
        tail = prev_row['total_start'] + prev_row['total_size']
        shelter = get_next_shelter(tail, x, y)
        shelter_tail = get_shelter_tail(cursor, shelter, row['init_time'], layout, code)


    #make sure this shelter has enough space. if it doesn't, keep looking until we
    #find one that does        
    while True:
        shelter_tail = get_shelter_tail(cursor, shelter, row['init_time'], layout, code)
        shelter_end = shelter + x
        if shelter_end - shelter_tail > = row['total_size']:
            #we have enough space
            break
        else:
            print "Warning: shelter out of space, trying next one."
            shelter += y

    return (shelter, shelter_tail)



#shelter requests and handle cleanup
def sheltering_and_cleanup (cleanup_code, layout, start, end):

    starttime = start * 60 * 60
    endtime = end * 60 * 60

    cleanup_class = get_cleanup_class(cleanup_code)

    conn = sqlite3.connect(conf.db)
    #first cursor for fetching all requests in the table
    curs = conn.cursor()
    #second cursors for other queries we need to make along the way
    curs2 = conn.cursor()

    #make sure data from this layout/code isn't in this table already
    query = "SELECT * FROM " + conf.shelter_t + " WHERE layout=? AND code=?"
    curs.execute(query, (layout, code))
    if curs.fetchone():
        raise DataExistsError(conf.series_t, layout, None)

    query = "SELECT * FROM " + series_t + "WHERE layout=? AND init_time > ? " + \
        "AND init_time < ? + ORDER BY init_time ASC"

    for row in curs.execute(query, (layout, starttime, endtime)):
        if row['shelter'] == 1:
            #first, figure out where to shelter these requests
            (shelter_start, shelter_tail) = shelter_request(curs2, row)
            #now actually shelter them
            query = "INSERT INTO " + shelter_t + \
                "(series_id, shelt_id, shelt_blk, layout, code) " + \
                "VALUES(?, ?, ?)"
            values = (row['series_id'], shelter_start, shelter_tail, layout, cleanup_code)
            curs2.execute(query, values)
        #now we ask our cleanup policy what requests to cleanup, and when
        #cleanup_fxn should take the id of the request that's just been cleaned
        #and a cursor, and return a list of (series_id, time) pairs
        #we give our cleanup policy a chance to run after every request, not just sheltered ones
        scheduled_cleanings = cleanup_class.clean(curs2, row)
        #for each scheduled cleaning, updated table with cleanup time
        query = "UPDATE " + shelter_req_table + \
            "SET clean_time = ? WHERE series_id = ?"
        curs2.executemany(query, scheduled_cleanings)
    
    conn.commit()
    conn.close()

#output script suitable for replay tool
#(almost) same format as preprocess.py outputs:
#time, disk num, blk num, size, flag (read or write)
def db_to_trace (cleanup_code, layout, start, end, outfile):
    conn = sqlite3.connect(conf.db)
    curs = conn.cursor()

    #time interval to output, in seconds
    starttime = start * 60 * 60
    endtime = end * 60 * 60

    #All non-sheltered requests
    query = "(SELECT req.time as time, series.disk_num, req.start as start, req.size, series.flag " + \
        "FROM " + series_t + "AS series NATURAL JOIN  " + \
        reqs_t + "AS req WHERE series.shelter=0 AND series.layout=:layout AND time >:start AND time <:end)" + \
        "UNION " + \
        #All sheltered requests
    "(SELECT req.time as time, series.disk_num, " + \
        "(shelt.shelt_blk + req.start - series.total_start) as start, req.size, series.flag " + \
        "FROM " + series_t + "AS series NATURAL JOIN " + \
        reqs_t + "AS req NATURAL JOIN " + \
        shelter_t + "AS shelt WHERE series.shelter=1 AND series.layout=:layout AND shelt.code=:code AND time > :start AND time < :end)"
    "UNION " + \
        #Cleanup of all sheltered requests
    "(SELECT shelt.clean_time as time, series.disk_num, req.start as start, req.size, series.flag " + \
        "FROM " + series_t + "AS series NATURAL JOIN " + \
        reqs_t + "AS req NATURAL JOIN " + \
        shelter_t + "AS shelt WHERE series.shelter=1 AND series.layout=:layout AND shelt.code=:code AND time > :start AND time < :end)" + \
        "ORDER BY time ASC"
    
    with open(outfile, 'w') as f:
        writer = csv.writer(f, delimiter=' ')
        for row in curs.execute(query, {"layout" : layout, "code" : code, "start" : starttime, "end" : endtime})
            write.writerow(row)

    conn.close()



            
    

        

        

