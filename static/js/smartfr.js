const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");

const form = document.getElementById("uploadForm");
const button = document.getElementById("submitBtn");

fileInput.addEventListener("change", function(){

    if(this.files.length){

        fileName.innerHTML = "📷 " + this.files[0].name;

    }

});

form.addEventListener("submit", function(){

    button.disabled = true;

    button.innerHTML = "Analyzing...";

});