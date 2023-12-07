let newQuizData = null;

function fetchQuiz(host_id, quiz_id){
    

    let quiz_data = {host_id: host_id, quiz_id: quiz_id};

    let form = document.createElement("form");
    let host_id_elem = document.createElement("input");
    host_id_elem.type = "hidden";
    host_id_elem.value = host_id;

    let quiz_id_elem = document.createElement("input");
    quiz_id_elem.type = "hidden";
    quiz_id_elem.value = quiz_id;

    form.appendChild(host_id_elem);
    form.appendChild(quiz_id_elem);

    let formData = new FormData(form);

    for(let key in quiz_data){
        formData.append(key, quiz_data[key]);
    }

    fetch(getQuizURL, {
        method: "POST",
        body: formData
    })
    .then(response=>response.json())
    .then(data=>{
        // console.log(data);

        // saving data
        saveData(data);

        // displaying data
        // for(let i=0; i<data.question_set.length; i++){
        //     displayQuizData(i);
        // }

        editQuizDisplay();
    });

}

function saveData(fetchedData){
    newQuizData = fetchedData;
}

function createClick(){

    let quiz_code = this.parentElement.parentElement.children[0].value;
    let host_id = quiz_code.split(" ")[0];
    let quiz_id = quiz_code.split(" ")[1];

    fetchQuiz(host_id, quiz_id);
    
}

function editQuizDisplay(){
    document.getElementById("quiz_title").value = newQuizData.quiz_title;

    emptyNewQuiz();

    let timer_select_elem = document.getElementById("quiz_timer_minutes");

    let optionPresent = false;
    for(let i=0; i<timer_select_elem.options.length; i++){
        let option = timer_select_elem.options[i];
        if(newQuizData.quiz_timer_minutes == option.value){
            option.selected = true;
            showOtherOption.bind(timer_select_elem).call();
            document.getElementById("timerOther").value = "";

            optionPresent = true;
            break;
        }
    }

    if(!optionPresent){
        timer_select_elem.options[timer_select_elem.options.length-1].selected = true;
        
        showOtherOption.bind(timer_select_elem).call();

        document.getElementById("timerOther").value = newQuizData.quiz_timer_minutes;

    }

    let question_block;
    let latest_question;
    let choice_block;
    let latest_choice;

    for(let i=0; i<newQuizData.question_set.length; i++){
        question_block = document.getElementById("latest_question_no").parentElement;
        latest_question = question_block.children[1].children[0];
        latest_question.value = newQuizData.question_set[i].question_text;

        
        
        for(let j=0; j<newQuizData.question_set[i].choice_set.length; j++){
            let choice = newQuizData.question_set[i].choice_set[j];

            choice_block = question_block.parentElement.lastElementChild;
            latest_choice = choice_block.children[1].children[1];

            latest_choice.value = choice.choice_text;

            let correct_choice_radio = choice_block.children[1].children[0].children[0];
            if(choice.is_correct_choice){
                correct_choice_radio.checked = true;
            }

            if(j<newQuizData.question_set[i].choice_set.length-1){
                let new_choice_btn = choice_block.children[1].children[2];
                new_choice_btn.dispatchEvent(new Event("click"));
            }
        }

        if(i<newQuizData.question_set.length-1){
            new_question_click();
        }
    }


    const myModal = document.getElementById('previousModalCloseBtn');
    myModal.click();

    
}

function emptyNewQuiz(){
    document.getElementById("no_of_questions").value = 1;
    document.getElementById("question_field").innerHTML = `<div class="container-fluid" class="questions">
                                                                <h5 class="my-0">Q.<span id="latest_question_no">1</span>.
                                                                    <div class="input-group mb-3 w-75" style="display: inline-flex;">
                                                                        <input type="text" name="question1" class="form-control" placeholder="question title goes here">
                                                                        
                                                                        <button type="button" class="input-group-text" id="new_question_btn" onclick="new_question_click(event)">
                                                                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-plus-square-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                                                                                <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/>
                                                                            </svg>
                                                                        </button>
                                                                    </div>
                                                                </h5>

                                                                <h6 class="container"><span class="choice_no">1</span>.
                                                                    <div class="input-group mb-3 w-75" style="display: inline-flex;">
                                                                        <div class="input-group-text">
                                                                            <input class="form-check-input mt-0" type="radio" name="question1_choice_correct" value="0" checked>
                                                                        </div>
                                                                        <input type="text" name="question1_choice" class="form-control" placeholder="choice goes here">
                                                                        <button type="button" class="input-group-text" onclick="new_choice_click(event)">
                                                                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-plus-square-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                                                                                <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/>
                                                                            </svg>
                                                                        </button>
                                                                    </div>
                                                                </h6>
                                                            </div>`;
}