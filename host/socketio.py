import socketio
from datetime import datetime
from django.utils import timezone
import eventlet

# store timer states for each room
timer_states = {}

sio = socketio.Server()

@sio.event
def check_timer(sid, data):
    room = data["room"]

    
    while timer_states.get(room, {}).get("running", False):
        # print("timer running...")
        if(timezone.now()>=datetime.fromisoformat(data.get("quiz_end_time", 0))):
            break
        
        eventlet.sleep(1)

    # print("timer stopped...")
    sio.emit("stop_timer", data={"stop": True}, room=room)
    if(timezone.now()>=datetime.fromisoformat(data.get("quiz_end_time", 0))):
        sio.emit("stop_timer_host", data={"stop": True})


# @sio.event
# def startTimerHost(sid, data):
#     sio.emit("start_timer_host", data={"start": True})



def update_room_count(room):
    room_count = len(sio.manager.rooms.get('/', {}).get(room, {}))
    # print(sio.manager.rooms)
    sio.emit("room_count", data={"room_count": room_count, "room": room})

@sio.event
def fetch_room_count(sid, data):
    room = data["room"]
    update_room_count(room)


@sio.event
def join(sid, data):
    room = data["room"]

    sio.enter_room(sid, room)
    # print(room)
    update_room_count(room)