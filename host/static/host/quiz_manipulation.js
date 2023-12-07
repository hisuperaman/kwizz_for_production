function askDelete(e){
    document.getElementById("loader").style.display = "block";

    e.stopPropagation();

    const myModal = new bootstrap.Modal(document.getElementById('deleteQuizModal'));
    myModal.show();

    quiz_code = this.parentElement.parentElement.children[0].value;
    document.getElementById("quizCodeForStart").value = quiz_code;

    document.getElementById("deleteQuizModalLabel").innerHTML = quiz_code;

    document.getElementById("loader").style.display = "none";
    
}

function deleteQuiz(){

    document.getElementById("deleteQuizCloseBtn").click();

    document.getElementById("loader").style.display = "block";

    let quizCode = document.getElementById("quizCodeForStart").value;
    fetch(deleteQuizURL, {
        method: "POST",
        body: JSON.stringify({"quizCode": quizCode})
    })
    .then(response=>response.json())
    .then(data=>{

        document.getElementById("deleteQuizAlertModalLabel").innerHTML = quizCode;
        document.getElementById("deleteQuizAlertModalMessage").innerHTML = data.message;
        
        
        document.getElementById("loader").style.display = "none";

        const myModal = new bootstrap.Modal(document.getElementById('deleteQuizAlertModal'));
        myModal.show();

        quiz_table_body.innerHTML = "";
    
        if(toBeHeld_btn.classList.contains("active")){
            fetchInitialToBeHeldQuiz();
        }
        else{
            fetchInitialPreviouslyHeldQuiz();
        }

    })
}

function editQuiz(){
    let quizCode = document.getElementById("quizCodeForStart").value;
    const host_id = quizCode.split(" ")[0]
    const quiz_id = quizCode.split(" ")[1]
    window.location.href = `${editQuizURL}?host_id=${host_id}&quiz_id=${quiz_id}`;
}

// quiz visibility
let quizVisibilityCheckbox = document.getElementById("quizVisibilityCheckbox")
quizVisibilityCheckbox.addEventListener("change", (e)=>{
    document.getElementById("loader").style.display = "block";

    let quizPK = document.getElementById("quizPKField").value;

    let quiz_code = document.getElementById("quizCodeForStart").value;

    if(quizVisibilityCheckbox.checked){
        document.getElementById("editQuizBtn").style.display = "none";
        document.getElementById("quizLinkContainer").style.display = "flex";
        document.getElementById("connectedUserContainer").style.display = "flex";
        document.getElementById("startBtn").style.display = "block";
        document.getElementById("quizInfoModalAlert").style.display = "none";

        fetch(changeQuizVisibilityURL, {
            method: "POST",
            body: JSON.stringify({"quizCode": quiz_code, "quiz_visible": true})
        })
        .then(response=>response.json())
        .then(data=>{
            toBeHeldData[quizPK].quiz_visible = true;

            document.getElementById("loader").style.display = "none";
        })
    }
    else{
        document.getElementById("editQuizBtn").style.display = "inline-block";
        document.getElementById("quizLinkContainer").style.display = "none";
        document.getElementById("connectedUserContainer").style.display = "none";
        document.getElementById("startBtn").style.display = "none";
        document.getElementById("quizInfoModalAlert").style.display = "block";

        fetch(changeQuizVisibilityURL, {
            method: "POST",
            body: JSON.stringify({"quizCode": quiz_code, "quiz_visible": false})
        })
        .then(response=>response.json())
        .then(data=>{
            toBeHeldData[quizPK].quiz_visible = false;

            document.getElementById("loader").style.display = "none";
        })
    }
})