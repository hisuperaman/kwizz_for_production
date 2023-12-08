const new_question_click = (e)=>{
    let new_question_btn = document.getElementById('new_question_btn');
    let question_field = document.getElementById('question_field')

    let latest_question_no = document.getElementById('latest_question_no')
    let question_no = parseInt(latest_question_no.innerHTML);

    latest_question_no.removeAttribute("id");
    new_question_btn.remove();
    question_no += 1;

    try {
        let remove_question_btn = document.getElementById("remove_question_btn");
        remove_question_btn.remove();
    } 
    catch (error) {
        // console.log('nothing');
    }
    
    let question_elem = document.createElement("div");
    question_elem.setAttribute("class", "container-fluid questions");


    let html = `
                    <h5 class="my-0">Q.<span id="latest_question_no">${question_no}</span>.
                        <div class="input-group mb-3 w-75" style="display: inline-flex;">
                            <input type="text"  name="question${question_no}" class="form-control" placeholder="question title goes here" required>
                            
                            <button type="button" class="input-group-text" id="new_question_btn" onclick="new_question_click(event)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-plus-square-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                                    <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/>
                                </svg>
                            </button>
                            <button type="button" class="input-group-text" id="remove_question_btn" onclick="remove_question_click(event)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                                    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                                </svg>
                            </button>
                        </div>
                    </h5>

                    <h6 class="container" style="display: flex-block;"><span class="choice_no">1</span>.
                        <div class="input-group mb-3 w-75" style="display: inline-flex;">
                            <div class="input-group-text" onclick="this.children[0].checked=true;" onmouseover="this.style.cursor='pointer';">
                                <input onmouseover="this.style.cursor='inherit';" class="form-check-input mt-0" type="radio" name="question${question_no}_choice_correct" value="0" checked>
                            </div>
                            <input type="text" name="question${question_no}_choice" class="form-control" placeholder="choice goes here" required>
                            <button type="button" class="input-group-text" onclick="new_choice_click(event)">
                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-plus-square-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                                    <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/>
                                </svg>
                            </button>
                        </div>
                    </h6>`

    document.getElementById("no_of_questions").value = parseInt(document.getElementById("no_of_questions").value)+1;

    question_elem.innerHTML = html;
    question_field.appendChild(question_elem);
}

const new_choice_click = (e)=>{
    let new_choice_btn = e.target;

    let latest_choice_no = new_choice_btn.parentElement.parentElement.childNodes[0];
    let choice_no = parseInt(latest_choice_no.innerHTML);

    let choice_field = new_choice_btn.parentElement.parentElement.parentElement;

    let latest_question_no = choice_field.children[0].children[0];
    let question_no = parseInt(latest_question_no.innerHTML);

    latest_choice_no.removeAttribute('id');
    
    choice_no += 1;
    
    try {
        let remove_choice_btn = new_choice_btn.parentElement.lastElementChild;
        remove_choice_btn.remove();
    } 
    catch (error) {
        // console.log('nothing');
    }
            
    new_choice_btn.remove();
    let choice_elem = document.createElement('h6');
    choice_elem.setAttribute("class", "container")
    choice_elem.setAttribute("style", "display: flex-block;")

    let html = `<span class="choice_no">${choice_no}</span>.
                <div class="input-group mb-3 w-75" style="display: inline-flex;">
                    <div class="input-group-text" onclick="this.children[0].checked=true;" onmouseover="this.style.cursor='pointer';">
                        <input onmouseover="this.style.cursor='inherit';" class="form-check-input mt-0" type="radio" name="question${question_no}_choice_correct" value="${choice_no-1}">
                    </div>
                    <input type="text" name="question${question_no}_choice" class="form-control" placeholder="choice goes here" required>
                    <button type="button" class="input-group-text" onclick="new_choice_click(event)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-plus-square-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                            <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/>
                        </svg>
                    </button>
    
                    <button type="button" class="input-group-text" id="remove_choice_btn" onclick="remove_choice_click(event)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                        </svg>
                    </button>
                </div>
            `

    choice_elem.innerHTML = html;
    
    // choice_field.innerHTML += html;
    choice_field.appendChild(choice_elem);
}

function createElementFromHTML(htmlString){
    const parser = new DOMParser();
    const parsedHTML = parser.parseFromString(htmlString, "text/html")
    return parsedHTML.body.firstChild;
}

const remove_question_click = (e)=>{
    let remove_question_btn = e.target;
    remove_question_btn.parentElement.parentElement.parentElement.remove();

    let questions = document.getElementById("question_field");
    questions = questions.children;

    let latest_question_field = questions[questions.length-1];

    let latest_question = latest_question_field.childNodes[1];
    // let latest_question = latest_question_field.childNodes;

    let btns_html;
    if(latest_question_field==questions[0]){
        btns_html = `<button type="button" class="input-group-text" id="new_question_btn" onclick="new_question_click(event)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-plus-square-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                            <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/>
                        </svg>
                    </button>`
        latest_question.children[1].appendChild(createElementFromHTML(btns_html));
    }
    else{
        btns_html = `<button type="button" class="input-group-text" id="new_question_btn" onclick="new_question_click(event)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-plus-square-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                        <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/>
                    </svg>
                    </button>`
        latest_question.children[1].appendChild(createElementFromHTML(btns_html));
        btns_html = `<button type="button" class="input-group-text" id="remove_question_btn" onclick="remove_question_click(event)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                    </svg>
                    </button>`
        latest_question.children[1].appendChild(createElementFromHTML(btns_html));
    }

    document.getElementById("no_of_questions").value = parseInt(document.getElementById("no_of_questions").value)-1;

    latest_question.children[0].setAttribute("id", "latest_question_no");
    // console.log(questions)
}

const remove_choice_click = (e)=>{
    let remove_choice_btn = e.target;
    // console.log(remove_choice_btn)
    let latest_question_field = remove_choice_btn.parentElement.parentElement.parentElement;

    remove_choice_btn.parentElement.parentElement.remove();

    let latest_choice = latest_question_field.lastElementChild;
    // console.log(latest_choice)

    let btns_html;
    if(latest_choice==latest_question_field.children[1]){
        btns_html = `<button type="button" class="input-group-text" onclick="new_choice_click(event)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-plus-square-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                            <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/>
                        </svg>
                    </button>`
        latest_choice.children[1].appendChild(createElementFromHTML(btns_html));
    }
    else{
        btns_html = `<button type="button" class="input-group-text" onclick="new_choice_click(event)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-plus-square-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                            <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/>
                        </svg>
                    </button>`
        latest_choice.children[1].appendChild(createElementFromHTML(btns_html));
        btns_html = `<button type="button" class="input-group-text" id="remove_choice_btn" onclick="remove_choice_click(event)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="30" fill="currentColor" class="bi bi-x-circle-fill" viewBox="0 0 16 16" style="pointer-events: none;">
                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/>
                        </svg>
                    </button>`
        latest_choice.children[1].appendChild(createElementFromHTML(btns_html));
    }

    // latest_question.children[0].setAttribute("id", "latest_question_no");
}