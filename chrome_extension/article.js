var host = window.location.host;

if (host == "www.nytimes.com"){
  text_chunks = document.getElementsByClassName("g-body");
  for (let index = 0; index < text_chunks.length; index++) {
    var element = text_chunks[index].innerText;

    console.log(element);

    // // Send element by http post request
    // var xmlHttp = new XMLHttpRequest();
    // xmlHttp.onreadystatechange = function() { 
    //     if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
    //         callback(xmlHttp.responseText);
    // }
    // const request_url = "http://IP:PORT/path?" + element
    // xmlHttp.open("GET", request_url, true);
    // xmlHttp.send();
    
    // // Get processed JSON
    // const Http = new XMLHttpRequest();
    // const get_request_url = 'http://IP:PORT/path';
    // Http.open("GET", get_request_url);
    // Http.send();

    // Http.onreadystatechange = (e) => {
    //   console.log(Http.responseText)
    // }

    text_chunks[index].innerText = 'hello hello hello hello';
  }

}
if (host == "www.ledevoir.com" || host == "time.com"){
  text_chunks = document.getElementsByTagName('p');
  for (let index = 0; index < text_chunks.length; index++) {
    var element = text_chunks[index].innerText;
    console.log(element);

    obj = JSON

    text_chunks[index].innerText = 'hello hello hello hello';
  }
}