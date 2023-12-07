const serverURL = "http://localhost:8000"
// const serverURL = "http://192.168.208.29:8000"
// const serverURL = "http://192.168.208.145:8000"

const socket = io(serverURL);

let host_id = document.getElementById("host_id").value;
let quiz_id = document.getElementById("quiz_id").value;

let room = `${host_id} ${quiz_id}`

socket.on("connect", ()=>{
    console.log("connected!")
    socket.emit("join", {"room": room});
})

// socket.on("disconnect", ()=>{
//     console.log("disconnected!");
//     navigator.sendBeacon(leaveRoomURL, JSON.stringify({room: room, sid: socket.id}));
// })

// window.addEventListener("beforeunload", ()=>{
//     socket.emit("leave", {"room": room});
//     // navigator.sendBeacon(leaveRoomURL, JSON.stringify({room: room, sid: socket.id}));
// })

window.addEventListener("unload", (e)=>{
    navigator.sendBeacon(leaveRoomURL, JSON.stringify({room: room, sid: socket.id}));
})



let timer;
function startTimer(){
    timer = setInterval(() => {
        // let destination = new Date("Oct 8, 2023 22:10:00+5:30").getTime();
        totalSeconds -= 1;

        let minutes = Math.floor(totalSeconds / 60);
        let seconds = Math.floor(totalSeconds % 60);
        
        timerString = `${(minutes<10)?(0):("")}${minutes}:${(seconds<10)?(0):("")}${seconds}`;
        document.getElementById("timer").innerHTML = timerString;
    }, 1000);
}

function stopTimer(){
    clearInterval(timer);
}



socket.on("start_quiz", (data)=>{
    // console.log(data);
    
    document.getElementById("mainContent").style.display = "block";

    document.getElementById("nextBtn").disabled = false;
    document.getElementById("submitBtn").disabled = false;
    quiz_start_time = data.quiz_start_time;

    // socket.emit("startTimerHost", {"started": true});

    // displaying timer
    startTimer();

    // displaying alert
    document.getElementById("beforeStartAlert").style.display = "none";
    document.getElementById("afterStartAlert").style.display = "block";
});


socket.on("stop_timer", ()=>{
    // console.log("Stop")
    stopTimer();
})

socket.on("submit_quiz", ()=>{
    stopTimer();
    submitQuiz();

    document.getElementById("user_quizzes_joined").innerHTML = parseInt(document.getElementById("user_quizzes_joined").innerHTML)+1;
})

socket.on("visibility_changed", (data)=>{
    if(!data.quiz_visible){
        window.location.href = homeURL;
    }
})