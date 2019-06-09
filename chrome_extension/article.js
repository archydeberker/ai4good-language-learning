var learning_enabled = true;
var host = window.location.host;

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
  bienvenue_yes.setAttribute("style", "cursor: pointer;");
  bienvenue_yes.textContent = "👍";
  bienvenue_header.append(bienvenue_yes);

  // Empty divider span
  var divider_span = document.createElement("SPAN");
  divider_span.setAttribute("style", "padding-left:20px;");
  bienvenue_header.append(divider_span);

  // Assessement no button
  var bienvenue_no = document.createElement("SPAN");
  bienvenue_no.id = "bienvenue_no";
  bienvenue_no.setAttribute("style", "cursor: pointer;");
  bienvenue_no.textContent = "👎";
  bienvenue_header.append(bienvenue_no);


  // Level counter
  var assessment_quiz_level_span = document.createElement("SPAN");
  assessment_quiz_level_span.textContent = "Level: " + 16;
  assessment_quiz_level_span.setAttribute("style", "float:right;");
  bienvenue_header.append(assessment_quiz_level_span);

  // Actual assessement quizz
  var assessment_quiz_dict = {
    "bonjour": "easy",
    "ecole": "med",
    "marche": "high",
    "dehors": "easy"
  }

  for (var word in assessment_quiz_dict) {
    console.log(assessment_quiz_dict[word]);
    assessment_quiz_span.innerText = word;
  }
}

if (host == "www.nytimes.com"){
  text_chunks = document.getElementsByClassName("g-body");
  for (let index = 0; index < text_chunks.length; index++) {
    var element = text_chunks[index].innerText;
    console.log(element);

    const Http = new XMLHttpRequest();
    const url = "http://662f13f9.ngrok.io/query-example?text=" + element;
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
      console.log(Http.responseText)
    }

    //text_chunks[index].innerText = 'hello hello hello hello';
  }
}

if (host == "www.ledevoir.com" || host == "time.com"){
  text_chunks = document.getElementsByTagName('p');
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
        console.log(Http.responseText);
        text_resampled = Http.responseText;
      }
    };

    // text_chunks[index].innerText ="";
    // for (var word in text_resampled) {
    //   console.log(word)
    //   //console.log("hello");
    //   // text_chunks[index].innerText += text_resampled[word];
    //   // console.log( word + "  " + text_resampled[word])
    // }
  }
}