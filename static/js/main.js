// ==============================
// GLOBAL QUIZ DATA
// ==============================

let quizData = [];

// ==============================
// GENERATE QUIZ
// ==============================

function generateQuiz(){

let topic = document.getElementById("topic").value;
let level = document.getElementById("level").value;

fetch("/generate-quiz",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({topic:topic,level:level})
})
.then(res=>res.json())
.then(data=>{

quizData = data.quiz;

let container=document.getElementById("quiz-Container");
container.innerHTML="";

quizData.forEach((q,index)=>{

let html=`<h4>${q.question}</h4>`;

q.options.forEach(opt=>{
html+=`<input type="radio" name="q${index}" value="${opt}"> ${opt}<br>`;
});

container.innerHTML+=html;

});

});

}

// ==============================
// SUBMIT QUIZ
// ==============================

async function submitQuiz(){

// check if quiz generated
if(quizData.length === 0){
alert("Generate quiz first!")
return
}

let score = 0

quizData.forEach((q,index)=>{

let selected = document.querySelector(`input[name="q${index}"]:checked`)
let questionCard = document.querySelectorAll(".card")[index]

// find correct option from options
let correctOption = q.options.find(opt =>
opt.toLowerCase().includes(q.answer.toLowerCase())
)

// check answer
if(selected){

if(selected.value.toLowerCase().includes(q.answer.toLowerCase())){

score++
selected.parentElement.style.color = "green"

}else{

selected.parentElement.style.color = "red"

}

}

// show correct answer
let answerHTML = `<p style="color:blue"><b>Correct Answer:</b> ${correctOption}</p>`

questionCard.innerHTML += answerHTML

})

// disable quiz after submit
document.querySelectorAll("input[type=radio]").forEach(r=>{
r.disabled = true
})

// send score to backend
let res = await fetch("/submit-quiz-score",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
score:score,
total:quizData.length
})
})

let data = await res.json()

// show result
document.getElementById("result").innerText =
"Score: "+data.score+" / "+data.total+" ("+data.percentage.toFixed(2)+"%)"

// update progress bar
document.getElementById("progressBar").style.width = data.percentage + "%"

}
// ==============================
// GENERATE NOTES
// ==============================

async function generateNotes(){

let topic = document.getElementById("topic").value
let level = document.getElementById("level").value

let res = await fetch("/generate-notes",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
topic:topic,
level:level
})
})

let data = await res.json()

document.getElementById("notesBox").innerText = data.notes

}

// ==============================
// GENERATE STUDY PLAN
// ==============================
function generatePlan(){

let topic = document.getElementById("topic").value
let days = document.getElementById("days").value

fetch("/generate-studyplan",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
topic:topic,
days:days
})

})

.then(res=>res.json())

.then(data=>{

document.getElementById("plan").innerHTML = data.study_plan.replace(/\n/g,"<br>") 

})

}
// ==============================
// AI CHAT
// ==============================

function sendChat(){

let msg=document.getElementById("message").value;

fetch("/ai-chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:msg})
})
.then(res=>res.json())
.then(data=>{

document.getElementById("chatBox").innerHTML+=
`<p><b>AI:</b> ${data.reply}</p>`;

});

}

// ==============================
// PDF UPLOAD
// ==============================

function uploadPDF(){

let file=document.getElementById("pdfFile").files[0];

let formData=new FormData();
formData.append("file",file);

fetch("/upload-pdf",{
method:"POST",
body:formData
})
.then(res=>res.json())
.then(data=>{
alert("PDF uploaded successfully");
});

}

// ==============================
// ASK QUESTION FROM PDF
// ==============================

function askPDF(){

let filename=document.getElementById("pdfFile").files[0].name;
let question=document.getElementById("pdfQuestion").value;

fetch("/ask-pdf",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({filename:filename,question:question})
})
.then(res=>res.json())
.then(data=>{

document.getElementById("pdfAnswer").innerText=data.answer;

});

}

// ==============================
// AI TUTOR LESSON
// ==============================

function generateTutor(){

let topic = document.getElementById("topic").value;
let level = document.getElementById("level").value;

fetch("/generate-tutor",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
topic:topic,
level:level
})
})
.then(res=>res.json())
.then(data=>{

document.getElementById("lessonBox").innerText = data.lesson;

});

}

// ==============================
// LIVE DOUBT CHAT
// ==============================
async function askDoubt(){

let question = document.getElementById("question").value

let res = await fetch("/ai-chat",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
question:question
})
})

let data = await res.json()

let chatbox = document.getElementById("chatbox")

chatbox.innerHTML += `
<div class="card p-2 mb-2">
<b>You:</b> ${question} <br>
<b>AI:</b> ${data.answer}
</div>
`

document.getElementById("question").value = ""

}
// ==============================
// GENERATE AI VIDEO
// ==============================

function generateVideo(){

let topic = document.getElementById("topic").value;
let level = document.getElementById("level").value;

fetch("/generate-ai-video",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
topic:topic,
level:level
})
})
.then(res=>res.json())
.then(data=>{

let video = document.getElementById("lessonVideo");
video.src = "/" + data.video_path;

});

}
//===============================
// PROGRESS
//================================

function loadProgress(){

fetch("/get-progress")

.then(res=>res.json())

.then(data=>{

document.getElementById("totalQuiz").innerText =
data.total_quizzes

document.getElementById("avgScore").innerText =
data.average_score + "%"

})

}
loadProgress()