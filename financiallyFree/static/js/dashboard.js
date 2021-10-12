const exExpandButton = document.querySelector("#expenseEx");
const savExpandButton = document.querySelector("#savingEx");
const expenseForm = document.querySelector("#dashExpenseForm");
const savingForm = document.querySelector("#savingForm");
const expenseChart = document.querySelector("#expenseChart");
const savingChart = document.querySelector("#savingsChart");
const sumExAmount = document.querySelectorAll(".sumExAmount");
const expenseAmount = document.querySelector("#expenseAmount");
const cattName = document.querySelectorAll(".cattName")
const savName = document.querySelectorAll(".savName");
const sumSavAmount = document.querySelectorAll(".sumSavAmount");
const savingsAmount = document.querySelector("#savingsAmount");

// * Function in charge of creating rgb random colors
const ranColor = ()=>{
    rgb = []
    for(let i = 0; i < 3; i++){
        rgb.push(Math.floor(Math.random() * 255 ))
    }
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
}

// ? Retreive the written info from the data injected by jinja to format the 
const retrieveExInfo = (amount, titles)=>{
    const expenseByCatt = []
    const rgbColors = []
    const labels = []
    if(expenseAmount.length === 0){
        return false
    }else{
        amount.forEach((d)=>{
            expenseByCatt.push(Number(d.textContent))
        });
        titles.forEach((d)=>{
            labels.push(d.textContent)
        });
        for(let i = 0; i < expenseByCatt.length; i++){
            rgbColors.push(ranColor());
        }
        data = {
            expenseData: expenseByCatt,
            exTitles: labels,
            bg: rgbColors
        }
        return data
    }
}
//? Created the pie chart with the database info
const createChart = (chart ,d)=>{ 
    let result = new Chart(chart, {
        type: 'doughnut',
        data: {
            labels: d.exTitles,
            datasets: [{
                label: '# of Votes',
                data: d.expenseData,
                backgroundColor: d.bg,
                borderColor: d.bg,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
    return result
}
let myChart = createChart(expenseChart, retrieveExInfo(sumExAmount, cattName))
let savChart = createChart(savingChart, retrieveExInfo(sumSavAmount, savName))
sumExAmount.forEach((d)=>{
    expenseAmount.textContent = Number(expenseAmount.textContent) + Number(d.textContent)
    expenseAmount.textContent = Number(expenseAmount.textContent).toFixed(2);
});
sumSavAmount.forEach((d)=>{
    savingsAmount.textContent = Number(savingsAmount.textContent) + Number(d.textContent)
    savingsAmount.textContent = Number(savingsAmount.textContent).toFixed(2);
});



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