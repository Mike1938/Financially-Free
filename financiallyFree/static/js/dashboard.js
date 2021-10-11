const exExpandButton = document.querySelector("#expenseEx");
const savExpandButton = document.querySelector("#savingEx");
const expenseForm = document.querySelector("#dashExpenseForm");
const savingForm = document.querySelector("#savingForm");

const checkButton = (data)=>{
    if (data.textContent === "-"){
        data.textContent = "+";
    }else{
        data.textContent = "-";
    }
    data.classList.toggle("greenButton")
}

exExpandButton.addEventListener('click', ()=>{
    expenseForm.classList.toggle("hideForm")
    checkButton(exExpandButton);
    
})

savExpandButton.addEventListener('click', ()=>{
    savingForm.classList.toggle("hideForm");
    checkButton(savExpandButton);
})