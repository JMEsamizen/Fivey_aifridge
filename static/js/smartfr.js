document.addEventListener("DOMContentLoaded",()=>{

const inputs=document.querySelectorAll("#fileInput");

inputs.forEach(input=>{

    input.addEventListener("change",()=>{

        const fileName=input.files[0]?.name;
        const label=input.parentElement.querySelector("#fileName");

        if(fileName && label){
            label.textContent=fileName;
        }

    });

});


const buttons=document.querySelectorAll(".primary-button");

buttons.forEach(button=>{

    button.addEventListener("click",()=>{

        button.textContent="Analyzing...";

    });

});

});