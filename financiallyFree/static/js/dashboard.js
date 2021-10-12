const exExpandButton = document.querySelector("#expenseEx");
const savExpandButton = document.querySelector("#savingEx");
const expenseForm = document.querySelector("#dashExpenseForm");
const savingForm = document.querySelector("#savingForm");
const expenseChart = document.querySelector("#expenseChart");
const savingChart = document.querySelector("#savingsChart");
const sumExAmount = document.querySelectorAll(".sumExAmount");
const expenseAmount = document.querySelector("#expenseAmount");
const cattName = document.querySelectorAll(".cattName")
// * Function in charge of creating rgb random colors
const ranColor = ()=>{
    rgb = []
    for(let i = 0; i < 3; i++){
        rgb.push(Math.floor(Math.random() * 255 ))
    }
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
}
const expenseByCatt = []
const rgbColors = []
const labels = []
// ? Retreive the written info from the data injected by jinja to format the 
const retrieveExInfo = (amount, titles)=>{
    
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
const createChart = (chart)=>{
    const d = retrieveExInfo(sumExAmount, cattName)
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
let myChart = createChart(expenseChart)

sumExAmount.forEach((d)=>{
    expenseAmount.textContent = Number(expenseAmount.textContent) + Number(d.textContent)
    expenseAmount.textContent = Number(expenseAmount.textContent).toFixed(2);
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