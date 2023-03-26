import os
import pymongo
import json
import random
import psycopg2
import time
import requests

def sendsms(tonum, message):


    url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/sendsms"

    payload = json.dumps({
    "receiver": tonum,
    "message": message,
    "token": "GET YOUR OWN TOKEN"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)


def connector():
    cockroachstring = os.environ.get('COCKROACHSTR3')
    conn=psycopg2.connect(cockroachstring)
    return conn



def initialize(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INT PRIMARY KEY, username STRING, email STRING, userpassword STRING, useraddress STRING, userphone STRING, lat STRING, lon STRING)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS foods (id INT PRIMARY KEY, name STRING, userid STRING, calories STRING, time STRING)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS tasks (id INT PRIMARY KEY, name STRING, userid STRING, cost STRING, time STRING, place STRING, status STRING)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS readings (id INT PRIMARY KEY, name STRING, ownerid STRING, value STRING, time STRING)"
        )
        # cur.execute("UPSERT INTO users (id, email, userpassword, usertype, name) VALUES (1, 'jon@fisherman.com', 'password1', 'fisherman', 'jon stewart'), (2, 'joe@gmail.com', 'password1', 'customer', 'joe someone')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()



def add_tasks(conn, userid, cost, time, place, items, tname):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM tasks")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        i = 1
        for row in rows:
            i = i + 1
        i = str(i)
        # helperid = "-1"
        status = "created"
        cur.execute("UPSERT INTO tasks (id, name, userid, cost, time, place, status) VALUES (" + i +", '" + tname +"', '" + userid + "', '" + cost + "', '" + time +"', '" + place + "', '" + status +"')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    return i
    # print ("user added")



def pendingtask(conn, time, taskid):
    newstatus = "pending"
    with conn.cursor() as cur:
        cur.execute( "UPDATE tasks SET time = %s , status = %s WHERE id = %s", (time, newstatus, taskid));
        #  "UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, frm)
        conn.commit()

    return 0


def acceptedtask(conn, taskid):
    newstatus = "accepted"
    with conn.cursor() as cur:
        cur.execute( "UPDATE tasks SET status = %s WHERE id = %s", (newstatus, taskid));
        #  "UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, frm)
        conn.commit()

    return 0


def completedtask(conn, taskid):
    newstatus = "completed"
    with conn.cursor() as cur:
        cur.execute( "UPDATE tasks SET status = %s WHERE id = %s", (newstatus, taskid));
        #  "UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, frm)
        conn.commit()

    return 0





def add_readings(conn, name, ownerid, value, time):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM readings")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        i = 1
        for row in rows:
            i = i + 1
        i = str(i)
        
        cur.execute("UPSERT INTO readings (id, name, ownerid, value, time) VALUES (" + i +", '" + name + "', '" + ownerid + "', '" + value +"', '" + time +"')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    return i
    # print ("user added")



def add_users(conn, uname, pw, uphone, uemail, lat, lon, uaddress):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        i = 1
        for row in rows:
            i = i + 1
        i = str(i)
        
        cur.execute("UPSERT INTO users (id, email, userpassword, userphone, username, lat, lon, useraddress) VALUES (" + i +", '" + uemail + "', '" + pw + "', '" + uphone +"', '" + uname + "', '" + lat +"', '" + lon +"', '" + uaddress +"')")
        # logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    return i
    # print ("user added")


def login(conn, uemail, pw):
    with conn.cursor() as cur:
        cur.execute("SELECT id, email, userpassword, userphone, username, lat, lon, useraddress FROM users")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        for row in rows:
            # print(row)
            # print (type(row))
            if row[1] == uemail and row[2] == pw:
                # print ("found")
                return True, row[0], row[3], row[4], row[5], row[6], row[7]
        return False, 'none', 'none', '-1', '-1', '-1', '-1', '-1', '-1' 


def getuserbyid(conn, uid):
    with conn.cursor() as cur:
        cur.execute("SELECT id, email, userpassword, userphone, username, lat, lon, useraddress FROM users")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        for row in rows:
            # print(row)
            # print (type(row))
            if row[0] == int(uid):
                # print ("found")
                return True, row[0], row[1], row[3], row[4], row[5], row[6], row[7]
        return False, 'none', 'none', '-1', '-1', '-1', '-1', '-1', '-1' , '-1'


def gettasks(conn, userid):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, userid, cost, price, items, helperid, status FROM tasks")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        tasks = []

        for row in rows:
            if row[2] != userid:
                continue
             
            place = {}
            place['id'] = row[0]
            place['name'] = row[1]
            place['userid'] = row[2]
            place['cost'] = row[3]
            place['price'] = row[4]
            place['items'] = row[5]
            place['helperid'] = row[6]
            place['status'] = row[7]

            tasks.append(place)

        return tasks 




def getheartrateraw(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, ownerid, value, time FROM readings")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        readings = []

        for row in rows:
            if "Heart" in str(row[1]):
                return int(row[3])

            place = {}
            place['id'] = row[0]
            place['name'] = row[1]
            place['ownerid'] = row[2]
            place['value'] = row[3]
            place['time'] = row[4]


            readings.append(place)

        return 0






def getreadings(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, ownerid, value, time FROM readings")
        # logging.debug("print_balances(): status message: %s", cur.statusmessage)
        rows = cur.fetchall()
        conn.commit()
        # print(f"Balances at {time.asctime()}:")
        readings = []

        for row in rows:
            place = {}
            place['id'] = row[0]
            place['name'] = row[1]
            place['ownerid'] = row[2]
            place['value'] = row[3]
            place['time'] = row[4]


            readings.append(place)

        return readings 


def delete_users(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM hackabull2023.users")
        # logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    with conn.cursor() as cur:
        cur.execute("DROP TABLE users")
        # logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()

    print ("users table deleted")


def purgedb(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM defaultdb.users")
        # logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()
    with conn.cursor() as cur:
        cur.execute("DROP TABLE users")
        # logging.debug("delete_accounts(): status message: %s", cur.statusmessage)
    conn.commit()

    print ("users table deleted")



def dummy(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    }

    mongostr = os.environ.get('MONGOSTR')
    client = pymongo.MongoClient(mongostr)
    db = client["hackathon"]

    request_json = request.get_json()
    conn = connector()
    initialize(conn)

    retjson = {}

    action = request_json['action']
    if action == "createuser" :
        uname = request_json['name']
        pw = request_json['password']
        uphone = request_json['phone']
        uaddress = request_json['address']
        lat = request_json['lat']
        lon = request_json['lon']
        uemail = request_json['email']

        pid = add_users(conn, uname, pw, uphone, uemail, lat, lon, uaddress)

        retjson['status'] = "successfully added"
        retjson['id'] = pid

        return json.dumps(retjson)


    if action == "addreading" :
        name = request_json['name']
        ownerid = request_json['ownerid']
        value = request_json['value']
        time = request_json['time']


        pid = add_readings(conn, name, ownerid, value, time)

        retjson['status'] = "successfully added"
        retjson['id'] = pid

        return json.dumps(retjson)

    if action == "addsnore":
        col = db.snores

        found = 0
        count = 0
        id = "0" ##can change this

        id = request_json['dayid']

        for x in col.find():
            if x['id'] == id:
                found = 1
                id = x['id']
                count = x['count']

            break
        if found == 0:
            retjson['status'] = "unknown  id"

            return json.dumps(retjson)
        


        col.update_one({"id": id}, {"$set":{"count":count+1}})

        retjson['status'] = "snores updated"

        return json.dumps(retjson)


    if action == "populaterooms":
        col = db.rooms

        found = 0
        count = 0

        rooms = request_json['rooms']
        i = 0 ##can change this

        for r in rooms:
            col.update_one({"id": str(i)}, {"$set":{"population":r}})
            i+=1
        

        retjson['status'] = "rooms updated"

        return json.dumps(retjson)



    if action == "resetmedicine":
        col = db.pills

        found = 0
        count = 0

        i = 1 ##can change this

        for x in col.find():
            col.update_one({"userid": str(i)}, {"$set":{"taken":0}})
            i+=1
        

        retjson['status'] = "medicines reset"

        return json.dumps(retjson)



    if action == "takepill":
        col = db.pills

        found = 0
        count = 0
        id = "0" ##can change this

        id = request_json['patientid']

        for x in col.find():
            if x['userid'] == id:
                found = 1
                userid = x['userid']
                count = x['taken']

            break
        if found == 0:
            retjson['status'] = "unknown  id"

            return json.dumps(retjson)
        


        col.update_one({"userid": id}, {"$set":{"taken":count+1}})

        retjson['status'] = "medication updated"

        return json.dumps(retjson)




    if action == "getpillraw":
        col = db.pills

        found = 0
        count = 0
        id = "1" ##can change this

        id = request_json['patientid']

        for x in col.find():
            if x['userid'] == id:
                found = 1
                userid = x['userid']
                count = x['taken']

            break
        if found == 0:
            retjson['status'] = "unknown  id"

            return json.dumps(retjson)
        

        retjson['count'] = count

        return json.dumps(retjson)




    if action == "getrawlocation":
        
        col = db.rooms

        i = 0
        count = 0
        found = 0

        rooms = []

        for x in col.find():

            rooms.append(x['population'])
            if x['population'] > 0:
              found = 1
            i+=1
        
        if found >0:
            retjson['location'] = "living room"
        else:
            retjson['location'] = "bathroom"

        return json.dumps(retjson)




    if action == "getrooms":
        col = db.rooms

        i = 0
        count = 0

        rooms = []

        for x in col.find():

            rooms.append(x['population'])
            i+=1
        
        retjson['rooms'] = rooms

        return json.dumps(retjson)







    if action == "getsnores":
        col = db.snores

        found = 0
        count = 0
        id = "0" ##can change this

        id = request_json['dayid']

        for x in col.find():
            if x['id'] == id:
                found = 1
                id = x['id']
                count = x['count']

            break
        if found == 0:
            retjson['status'] = "unknown  id"

            return json.dumps(retjson)
        

        retjson['count'] = count

        return json.dumps(retjson)


    if action == "createtask" :
        userid = request_json['userid']
        cost = request_json['cost']
        price = request_json['price']
        placeid = request_json['placeid']
        items = request_json['items']
        tname= request_json['name']

        tid = add_tasks(conn, userid, cost, price, placeid, items, tname)
        
        

        retjson['status'] = "successfully added"
        retjson['id'] = tid

        return json.dumps(retjson)

    
    if action == "getreadings" :
        readings = getreadings(conn)
        
        retjson['status'] = "successfully retrieved"
        retjson['readings'] = readings

        return json.dumps(retjson)


    if action == "getvital" :
        reading = getheartrateraw(conn)
        
        retjson['status'] = "successfully retrieved"
        retjson['reading'] = reading

        return json.dumps(retjson)


    
    if action == "accepttask" :
        taskid = request_json['taskid']

        res = acceptedtask(conn, taskid)
        
        retjson['status'] = "task successfully accepted"

        return json.dumps(retjson)   


    if action == "completetask" :
        taskid = request_json['taskid']

        res = completedtask(conn, taskid)
        
        retjson['status'] = "task successfully accepted"

        return json.dumps(retjson)    

    

    if action == 'login':
        uemail = request_json['email']
        pw = request_json['password']

        res = login(conn, uemail, pw)

        retjson['status'] = str(res[0])
        retjson['id'] = str(res[1])
        retjson['type'] = str(res[2])
        retjson['name'] = str(res[3])
        retjson['lat'] = str(res[4])
        retjson['lon'] = str(res[5])
        retjson['address'] = str(res[6])
        

        return json.dumps(retjson)



    if action == 'getuserbyid':
        uid = request_json['uid']

        res = getuserbyid(conn, uid)

        retjson['status'] = str(res[0])
        retjson['id'] = str(res[1])
        retjson['email'] = str(res[2])
        retjson['type'] = str(res[3])
        retjson['name'] = str(res[4])
        retjson['lat'] = str(res[5])
        retjson['lon'] = str(res[6])
        retjson['address'] = str(res[7])
        

        return json.dumps(retjson)


    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr
