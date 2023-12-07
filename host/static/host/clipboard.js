function copyText(){
    let text = document.getElementById("quizLink").value;
    document.getElementById("quizLink").select();

    navigator.clipboard.writeText(text);
}