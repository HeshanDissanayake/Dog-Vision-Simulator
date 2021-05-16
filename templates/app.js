var xhttp = new XMLHttpRequest();


xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {

        console.log(xhttp.responseText);
    }
};





xhttp.open("GET", document.URL + 'search', true);
xhttp.send();



xhttp.open("POST", document.URL + 'submit_data', true);
xhttp.send("asdasd");