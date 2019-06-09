var learning_enabled = true;
var host = window.location.host;
max_level = ["Easy"];
var score = {
  "Easy": 0,
  "Medium": 0,
  "Hard": 0
};

function getMaxScore() {
  max_score = 0;
  max_level = ["Easy"];
  for (var level in score) {
    if (score[level] > max_score) {
      max_score = score[level];
      max_level = level;
    }
  }
}

if (learning_enabled){

  // Bienvenue header div creation
  const bienvenue_header = document.createElement("div");
  bienvenue_header.textContent = "Bienvenue 🤗";
  bienvenue_header.setAttribute("style", "background-color:#42a4f4; color:white; font-weight:bold; padding:5px;");
  document.body.insertBefore(bienvenue_header, document.body.firstChild);

  // Initial quiz text
  const head_text = document.createElement("span");
  head_text.textContent = "How familiar are you with this word ? ";
  head_text.setAttribute("style", "padding-left:25%; font-style:normal;");
  bienvenue_header.append(head_text);

  // Assessement quizz span
  var assessment_quiz_span = document.createElement("SPAN");
  assessment_quiz_span.id = "assessment_quiz_span";
  assessment_quiz_span.setAttribute("style", "padding-left:40px; padding-right:40px; text-transform:capitalize; font-style:italic;");
  bienvenue_header.append(assessment_quiz_span);

  // Assessement yes button
  var bienvenue_yes = document.createElement("SPAN");
  bienvenue_yes.id = "bienvenue_yes";
  bienvenue_yes.textContent = "👍";
  bienvenue_header.append(bienvenue_yes);

  // Empty divider span
  var divider_span = document.createElement("SPAN");
  divider_span.setAttribute("style", "padding-left:20px;");
  bienvenue_header.append(divider_span);

  // Assessement no button
  var bienvenue_no = document.createElement("SPAN");
  bienvenue_no.id = "bienvenue_no";
  bienvenue_no.textContent = "👎";
  bienvenue_header.append(bienvenue_no);

  // Actual assessement quizz
  var assessment_quiz_dict = [{"bonjour": "easy"},{"ecole": "medium"},{"marche": "hard"},{"dehors": "easy"}];

  word_count = 0;
  getMaxScore()

  assessment_quiz_span.innerText = Object.keys(assessment_quiz_dict[word_count]);

  to_do_onclick = 'score[' + Object.values(assessment_quiz_dict[word_count]) + '++];'
  bienvenue_yes.setAttribute('onclick', to_do_onclick)
  console.log(Object.values(assessment_quiz_dict[word_count]))

  // Level
  var assessment_quiz_level_span = document.createElement("SPAN");
  assessment_quiz_level_span.textContent = "Level: " + max_level;
  assessment_quiz_level_span.setAttribute("style", "float:right;");
  bienvenue_header.append(assessment_quiz_level_span);
}

// if (host == "www.nytimes.com"){
//   text_chunks = document.getElementsByClassName("p");
//   for (let index = 0; index < text_chunks.length; index++) {
//     var element = text_chunks[index].innerText;
//     console.log(element);

//     const Http = new XMLHttpRequest();
//     const url = "http://662f13f9.ngrok.io/query-example?text=" + element;
//     Http.open("GET", url);
//     Http.send();

//     Http.onreadystatechange = (e) => {
//       obj = JSON.parse(Http.responseText);
//       console.log(obj[0]);
//       obj = JSON.parse(json);
//       for (let index = 2; index < obj.length; index++) {
//         console.log(obj[index]);
//       //   const element = array[index];
//       //   if(element.text)
//       //   {
//       //     console.log(element.original) 
//       //   }
//       //   else console.log(element.text);
//       // }
//     }

//     //text_chunks[index].innerText = 'hello hello hello hello';
//   }
// }

if (host == "www.ledevoir.com" || host == "time.com" || host == "en.wikipedia.org" || host == ""){
  text_chunks = document.getElementsByTagName('p');
  console.log(text_chunks);
  for (let index = 0; index < text_chunks.length; index++) {
    var element = text_chunks[index].innerText;
    console.log(element);

    var Http = new XMLHttpRequest();
    var url = "https://846006a2.ngrok.io/query-example?text=" + element;
    Http.open("GET", url);
    Http.send();

    text_resampled = {};

    Http.onreadystatechange = function () {
      if(Http.readyState === 4 && Http.status === 200) {
        obj = JSON.parse(Http.responseText);
        console.log(obj[0]);
        for (let index = 2; index < obj.length; index++) {
          console.log(obj[index]);
          // const element = array[index];
          // if(element.text)
          // {
          //   console.log(element.original) 
          // }
          // else console.log(element.text);
        }
      }
    }
  }

    // text_chunks[index].innerText ="";
    // for (var word in text_resampled) {
    //   console.log(word)
    //   //console.log("hello");
    //   // text_chunks[index].innerText += text_resampled[word];
    //   // console.log( word + "  " + text_resampled[word])
    // }
}