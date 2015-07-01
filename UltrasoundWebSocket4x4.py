# This code reads 4 Ultrasound Sonar( Really Echolocation ) sensors
# To run on a Raspberry Pi.
# Current Author is John Leone ( Gibbloggen@gmail.com )
# Date 6/30/2015

# The code is in part my design,
# Another part author of SocketIO, Miguel Grinberg
# Another Part Matt from the Raspberrypi-spy.co.uk
# This is as is, in the public domain.  It would be nice if you
# gave me, and the two others a footnote or something.  I can't speak for
# them, but their code is out there.


from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit
import gevent
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


#changed formula to add a cm to compensate for the ultrasound
#also round to the nearest cm.
import datetime

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/sonar/')
def index():
    return render_template('sonar.html')



@socketio.on('my event', namespace='/test')
def test_message(message):
    while True:
        
	TRIG1 = 23 
	ECHO1 = 24
	FACTOR1 = 17450
	
	TRIG2 = 20 
	ECHO2 = 21
	FACTOR2 = 17450
	
	TRIG3 = 5 
	ECHO3 = 6
	FACTOR3 = 17450

	TRIG4 = 26 
	ECHO4 = 19
	FACTOR4 = 17450
	

	
	print "Distance Measurement In Progress"
	
	GPIO.setup(TRIG1,GPIO.OUT)
	GPIO.setup(ECHO1,GPIO.IN)
	
	GPIO.setup(TRIG2,GPIO.OUT)
	GPIO.setup(ECHO2,GPIO.IN)

	GPIO.setup(TRIG3,GPIO.OUT)
	GPIO.setup(ECHO3,GPIO.IN)

	GPIO.setup(TRIG4,GPIO.OUT)
	GPIO.setup(ECHO4,GPIO.IN)
	
	GPIO.output(TRIG1, False)
	GPIO.output(TRIG2, False)
        GPIO.output(TRIG3, False)
        GPIO.output(TRIG4, False)

	print "Waiting For Sensor To Settle"
	#time.sleep(1)

        gevent.sleep(0.5)

	pulse_start2 = time.time()
	print "time"
	print pulse_start2
	
	GPIO.output(TRIG2, True)
	#time.sleep(0.0001)
        gevent.sleep(0.0001)
	GPIO.output(TRIG2, False)
	
	while GPIO.input(ECHO2)==0:
	  pulse_start2 = time.time()	
	 # print "Waiting For Goudo"
	while GPIO.input(ECHO2)==1:
	  pulse_end2 = time.time()
	
	pulse_duration2 = pulse_end2 - pulse_start2
	
	distance2 = pulse_duration2 * FACTOR2
	
	distance2 = round(distance2, 0) + 1
	
	print "Distance2:",distance2,"cm"

        gevent.sleep(0.5)

	
	
	pulse_start1 = time.time()
        print "time"
	print pulse_start1
	
	GPIO.output(TRIG1, True)
	gevent.sleep(0.0001)
	GPIO.output(TRIG1, False)

	while GPIO.input(ECHO1)==0:
	  pulse_start1 = time.time()	
	 # print "Waiting For Goudo"
	while GPIO.input(ECHO1)==1:
	  pulse_end1 = time.time()
	
	pulse_duration1 = pulse_end1- pulse_start1
	
	distance1 = pulse_duration1 * FACTOR1
	
	
	distance1 = round(distance1, 0) + 1
	
	print "Distance1:",distance1,"cm"

        gevent.sleep(0.5)

	pulse_start3 = time.time()
        print "time"
	print pulse_start3
	
	GPIO.output(TRIG3, True)
	gevent.sleep(0.0001)
	GPIO.output(TRIG3, False)

	while GPIO.input(ECHO3)==0:
	  pulse_start3 = time.time()	
	 # print "Waiting For Goudo"
	while GPIO.input(ECHO3)==1:
	  pulse_end3 = time.time()
	
	pulse_duration3 = pulse_end3- pulse_start3
	
	distance3 = pulse_duration3 * FACTOR3
	
	
	distance3 = round(distance3, 0) + 1
	
	print "Distance3:",distance3,"cm"

        gevent.sleep(0.5)
	pulse_start4 = time.time()
        print "time"
	print pulse_start4
	
	GPIO.output(TRIG4, True)
	gevent.sleep(0.0001)
	GPIO.output(TRIG4, False)

	while GPIO.input(ECHO4)==0:
	  pulse_start4 = time.time()	
	 # print "Waiting For Goudo"
	while GPIO.input(ECHO4)==1:
	  pulse_end4 = time.time()
	
	pulse_duration4 = pulse_end4- pulse_start4
	
	distance4 = pulse_duration4 * FACTOR4
	
	
	distance4 = round(distance4, 0) + 1
	
	print "Distance4:",distance4,"cm"

	

        emit('DistancesReceived', {'distance1': distance1,'distance2': distance2,'distance3': distance3,'distance4': distance4})





@socketio.on('connect', namespace='/test')
def test_connect():
    #emit('my response', {'data': 'Connected'})

    # I just send values of 100, so I know it connected.
    # largest it can really handle is 91...
    emit('DistancesReceived', {'distance1': 100,'distance2':100,'distance3':100,'distance4':100})



@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80)
