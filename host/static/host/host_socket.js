const serverURL = "https://kwizz.adaptable.app"
// const serverURL = "http://192.168.208.29:8000"
// const serverURL = "http://192.168.208.145:8000"

const socket = io(serverURL);

socket.on("connect", (data)=>{
    console.log("connected!");

    // socket.emit("host_join", {room: host_username});
})


socket.on("room_count", (data)=>{
    // console.log("hi")
    if(document.getElementById("quizCodeForStart").value == data["room"]){
        document.getElementById("room_count").innerHTML = data["room_count"];
        // console.log(data["room_count"])
    }
});

function quizInfoModal(){

    let quizCodeElem = document.getElementById("quizCodeForStart");
    quizCodeElem.value = this.children[0].value;

    let room = quizCodeElem.value;
    let host_id = quizCodeElem.value.split(' ')[0];
    let quiz_id = quizCodeElem.value.split(' ')[1];

    const quiz_code = `${host_id} ${quiz_id}`;

    socket.emit("fetch_room_count", {room: room});

    let quizPK = this.children[1].value;

    document.getElementById("quizPKField").value = quizPK;

    // console.log(toBeHeldData)

    document.getElementById("loader").style.display = "block";
    fetch(getTimerValueURL)
    .then(response=>response.json())
    .then(responseData=>{

      if(responseData.time_seconds!=false){
        totalSeconds = Math.floor(parseInt(responseData.time_seconds));
        document.getElementById("startBtn").style.display = "none";
        document.getElementById("stopBtn").style.display = "block";
        document.getElementById("quizStartModalCloseBtn").disabled = true;
        
        timer = setInterval(() => {
          // let destination = new Date("Oct 8, 2023 22:10:00+5:30").getTime();
          totalSeconds -= 1;
  
          let minutes = Math.floor(totalSeconds / 60);
          let seconds = Math.floor(totalSeconds % 60);
          
          timerString = `${(minutes<10)?(0):("")}${minutes}:${(seconds<10)?(0):("")}${seconds}`;
          document.getElementById("timer").innerHTML = timerString;
        }, 1000);

      }

      else{
        // console.log(quizPK)
        totalSeconds = (toBeHeldData[quizPK].quiz_timer_minutes)*60;
        // console.log(totalSeconds);
        document.getElementById("startBtn").innerHTML = "Start";
        document.getElementById("startBtn").disabled = false;
      }
      
      
      let minutes = Math.floor(totalSeconds / 60);
      let seconds = Math.floor(totalSeconds % 60);

      timerString = `${(minutes<10)?(0):("")}${minutes}:${(seconds<10)?(0):("")}${seconds}`;
      document.getElementById("timer").innerHTML = timerString;

      return fetch(`${getQuizTitleURL}?quiz_code=${quiz_code}`)
    })
    .then(response=>response.json())
    .then(fetchedData=>{

      document.getElementById("active_quiz_title_display").innerHTML = fetchedData.quiz_title;
      document.getElementById("toBeHeldModalTitle").innerHTML = quizCodeElem.value;
      // quizPK = parseInt(quizPK)+1;
      // console.log(`pk -> ${quizPK}`)
      document.getElementById("active_totalQuestions").innerHTML = toBeHeldData[quizPK].question_set.length;
      
      if(typeof modalAfterRefresh == "function"){
        document.getElementById("editQuizBtn").style.display = "none";
        document.getElementById("quizLinkContainer").style.display = "flex";

        document.getElementById("connectedUserContainer").style.display = "flex";

        document.getElementById("quizInfoModalAlert").style.display = "none";

        document.getElementById("quizVisibilityContainer").style.display = "none";
        document.getElementById("previewBtn").style.display = "none";
      }
      
      else{
        document.getElementById("quizVisibilityCheckbox").checked = toBeHeldData[quizPK].quiz_visible;
        // console.log(`=> ${toBeHeldData[quizPK].quiz_visible}`)
        if(toBeHeldData[quizPK].quiz_visible){
          document.getElementById("editQuizBtn").style.display = "none";
          document.getElementById("quizLinkContainer").style.display = "flex";
  
          document.getElementById("connectedUserContainer").style.display = "flex";
          document.getElementById("startBtn").style.display = "block";
  
          document.getElementById("quizInfoModalAlert").style.display = "none";
        }
        else{
          document.getElementById("editQuizBtn").style.display = "inline-block";
          document.getElementById("quizLinkContainer").style.display = "none";
  
          document.getElementById("connectedUserContainer").style.display = "none";
          document.getElementById("startBtn").style.display = "none";
  
          document.getElementById("quizInfoModalAlert").style.display = "block";
        }
      }
      
      // setting link
      let host_id = quiz_code.split(" ")[0];
      let quiz_id = quiz_code.split(" ")[1];
      let quizLinkURL = clientJoinURL.replace("host_id", host_id);
      quizLinkURL = quizLinkURL.replace("123", quiz_id);
      document.getElementById("quizLink").value = `${window.location.host}${quizLinkURL}`;

      const myModal = new bootstrap.Modal(document.getElementById('quizInfoModal'));
      myModal.show();

      document.getElementById("loader").style.display = "none";
    })
}

let timer;
function startQuiz(){
    let quizCodeElem = document.getElementById("quizCodeForStart");
    let room = quizCodeElem.value;

    document.getElementById("total_seconds").value = totalSeconds;

    let myForm = new FormData(document.getElementById("quiz_start_form"));
    this.style.display = "none";
    document.getElementById("stopBtn").style.display = "block";
    document.getElementById("quizStartModalCloseBtn").disabled = true;
    
    document.getElementById("quizVisibilityContainer").style.display = "none";
    document.getElementById("previewBtn").style.display = "none";

    fetch(startQuizURL, {
      method: "POST",
      body: myForm
    })
    .then(response=>response.json())
    .then(data=>{

      socket.emit("check_timer", {"room": room, "quiz_start_time": data.quiz_start_time, "quiz_end_time": data.quiz_end_time});

      // console.log("hiiiii")
      timer = setInterval(() => {
        // let destination = new Date("Oct 8, 2023 22:10:00+5:30").getTime();
        totalSeconds -= 1;

        let minutes = Math.floor(totalSeconds / 60);
        let seconds = Math.floor(totalSeconds % 60);
        
        timerString = `${(minutes<10)?(0):("")}${minutes}:${(seconds<10)?(0):("")}${seconds}`;
        document.getElementById("timer").innerHTML = timerString;
      }, 1000);

      // console.log("done");

    })

}


socket.on("stop_timer_host", (data)=>{
  stopQuizBtnClick();
})



function stopQuiz(){

  document.getElementById("stopBtn").style.display = "none";
  document.getElementById("startBtn").style.display = "block";
  document.getElementById("quizStartModalCloseBtn").disabled = false;

  clearInterval(timer);

  fetch(clearQuizSessionURL)
  .then(response=>response.json())
  .then(data=>{
    // console.log("quiz start end session cleared!")
    submitQuiz();
  })

}

function stopQuizBtnClick(){
  stopQuiz();
}

function submitQuiz(){
  let quizCodeElem = document.getElementById("quizCodeForStart");
  let room = quizCodeElem.value;

  fetch(`${submitQuizURL}?room=${room}`)
  .then(response=>response.json())
  .then(data=>{
    // console.log("quiz submitted!")

    document.getElementById("user_quizzes_hosted").innerHTML = parseInt(document.getElementById("user_quizzes_hosted").innerHTML)+1;
    document.getElementById("quizStartModalCloseBtn").click();

    fetchInitialPreviouslyHeldQuiz();
    fetchInitialToBeHeldQuiz();

  })
}