var learning_enabled = true;
var host = window.location.host;
max_level = ["Easy"];
bienvenues_text = ["Bienvenue", "Welcome", "Ahlan wa sahlan", "Bienvenido", "Danke", "Grazie", "Obrigado", "Cпасибо"];
var score = {
  "Easy": 0,
  "Medium": 0,
  "Hard": 0
};

// Actual assessement quizz
const assessment_quiz_dict = [["bonjour", "Easy"],["ecole", "Medium"],["marche", "Medium"],["dehors", "Hard"]];
var assessment_idx = 0;

var current_bienvenue = 0;
const bienvenue_header = document.createElement("div");

function display() {
    if (learning_enabled){

	// Bienvenue header div creation
	var str = bienvenues_text[current_bienvenue] + " ��";
	bienvenue_header.textContent = bienvenues_text[current_bienvenue] + " 🤗";
	bienvenue_header.setAttribute("style", "background-color:#42a4f4; color:white; font-weight:bold; padding:5px;");
	document.body.insertBefore(bienvenue_header, document.body.firstChild);
	current_bienvenue += 1;
	current_bienvenue = current_bienvenue % bienvenues_text.length;

	if (assessment_idx <  assessment_quiz_dict.length) {
	    // Initial quiz text
	    const head_text = document.createElement("span");
	    head_text.textContent = "How familiar are you with this word ? ";
	    head_text.setAttribute("style", "padding-left:5cm; font-style:normal;");
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
	    bienvenue_yes.onclick = function() {
		var level_known = assessment_quiz_dict[assessment_idx][1]
		score[level_known] += 1;
		assessment_idx += 1;
		//alert(JSON.stringify(score));
		display();
	    }
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
	    bienvenue_no.onclick = function() {
		assessment_idx += 1;
		display();
	    }
	    bienvenue_header.append(bienvenue_no);

	    assessment_quiz_span.innerText = assessment_quiz_dict[assessment_idx][0];
	    //console.log(Object.values(assessment_quiz_dict[assessment_idx]))
	}// end show quiz
	function getMaxLevel() {
	    max_score = -1;
	    max_level = "None";
	    for (var level in score) {
		if (score[level] > max_score) {
		    max_score = score[level];
		    max_level = level;
		}
	    }
	    return max_level;
	}

	// Level counter
	var assessment_quiz_level_span = document.createElement("SPAN");
	assessment_quiz_level_span.textContent = "Level: " + getMaxLevel();
	assessment_quiz_level_span.setAttribute("style", "float:right;");
	bienvenue_header.append(assessment_quiz_level_span);
    }//end if
    setTimeout(display, 3000);
}//end display function

display();

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

if (host == "www.ledevoir.com" || host == "time.com" || host == "en.wikipedia.org" || host == "" || host == "www.newyorker.com" || true){
  text_chunks = document.getElementsByTagName('p');
  console.log(text_chunks);
  for (let index = 0; index < 2; index++) {
    var element = text_chunks[index].innerText;
    console.log(element);

    var Http = new XMLHttpRequest();
    var url = "http://ai4good-translation.herokuapp.com/query-example?text=" + element;
    Http.open("GET", url);
    Http.send();

    text_chunks[index].innerText ="";
    Http.onreadystatechange = function () {
      if(Http.readyState === 4 && Http.status === 200) {
        console.log(text_chunks[index]);
        console.log(text_chunks[index].innerText);
        obj = JSON.parse(Http.responseText);
        console.log(obj[0]);
        for (let resp_index = 2; resp_index < obj.length; resp_index++) {
          console.log(obj[resp_index]);
          if(obj[resp_index].original)
          {
            text_chunks[index].innerHTML += "<b>" + obj[resp_index].text + "</b>";
          }
          else
            text_chunks[index].innerHTML += " " + obj[resp_index].text;
        }
      }
    }
  }
}
