
let devices = null
let response = null
var xhttp = new XMLHttpRequest();



xhttp.open("GET", document.URL + 'search', true);
xhttp.send();




xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        response = xhttp.responseText;
        console.log(response)
    }
};

document.getElementById("blur").addEventListener('change',()=>{
    xhttp.open("POST", document.URL + 'submit_data', true);    
    xhttp.send( JSON.stringify({"blur": document.getElementById("blur").value}));

} )


document.getElementById("record").addEventListener("click", ()=>{
    let state = document.getElementById("record").checked
    console.log("record", state)
    if(state){
        document.getElementById("label").textContent = "Recording"
    }else{
        document.getElementById("label").textContent = "Record"
    }
    xhttp.open("GET", document.URL + 'record', true);
    xhttp.send();

})
