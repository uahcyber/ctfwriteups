from flask import jsonify, request, Flask, abort
import uuid
from itertools import product
import arrow
import logging

logging.basicConfig(level=logging.DEBUG)

knownMinions = {}
codes = []
workingCodes = {}

doDie = False

app = Flask(__name__)

def gen_codes():
    # YYMMDD
    global codes
    years = [str(i).zfill(2) for i in range(100)]
    months = [str(i).zfill(2) for i in range(1,13)]
    days = [str(i).zfill(2) for i in range(1,32)]
    codes = [''.join(x) for x in list(product(years,months,days))]
    logging.info(f"Generated {len(codes)} possible codes")
    codes.reverse()

@app.before_request
def before_it():
    global doDie
    if doDie:
        return jsonify({"cmd":"die"})

@app.route('/')
def root():
    return 'bingus'

@app.route('/register',methods=["GET"])
def register():
    global knownMinions
    alreadyKnown = True if request.remote_addr in knownMinions.values() else False
    if alreadyKnown:
        abort(403)
    thisUUID = str(uuid.uuid4())
    knownMinions[thisUUID] = request.remote_addr
    return jsonify({"uuid": thisUUID, "cmd":"continue"})

@app.route('/<uuid>/check',methods=['GET'])
def check(uuid):
    global knownMinions
    if uuid in knownMinions.keys():
        return jsonify({"status":"success", "cmd":"getNew"})
    return jsonify({"status":"error","cmd":"die"})

@app.route('/<uuid>/giveCode',methods=["GET"])
def give_code(uuid):
    global knownMinions
    if uuid not in knownMinions.keys():
        abort(403)
    global codes
    global workingCodes
    toGive = codes.pop()
    # add to workingCodes along with a timestamp.
    # this way, we can check to see if any working codes have been out for too long, indicated failure of the minion script
    while toGive in workingCodes.keys():
        toGive = codes.pop() # lock-ish
    workingCodes[toGive] = {uuid: arrow.utcnow()}
    return jsonify({"code": toGive, "cmd":"try"})

@app.route('/<uuid>/codeResponse',methods=["POST"])
def submit_code(uuid):
    global knownMinions
    if uuid not in knownMinions.keys():
        abort(403)
    global codes
    global workingCodes
    data = dict(request.get_json())
    if 'code' not in data or 'status' not in data:
        abort(500)
    code = data['code']
    status = data['status']
    del workingCodes[code]
    # check for expired codes from crashed minions
    toDel = []
    for k,v in workingCodes.items():
        if arrow.utcnow().timestamp() - list(v.values())[0].timestamp() > 180:
            # past 180 second expiration
            toDel.append(k)
            codes.append(k)
            logging.info(f"Cleaning code {code} from expired workingCodes")
    for k in toDel:
        del workingCodes[k]
    # check status of passcode trial
    if status == 'success':
        # we got em
        logging.info(f"SUCCESS!!!!!!: {code}")
        global doDie
        doDie = True # tell all minions to die on next connection
        return jsonify({"cmd":"die"})
    # failure
    logging.info(f"fail: {code}")
    return jsonify({"cmd":"getNew"}) # tell minions to get a new code

if __name__ == '__main__':
    gen_codes()
    app.run(host="0.0.0.0",port="18337")