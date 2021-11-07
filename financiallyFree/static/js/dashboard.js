const exExpandButton = document.querySelector("#expenseEx");
const savExpandButton = document.querySelector("#savingEx");
const expenseForm = document.querySelector("#dashExpenseForm");
const savingForm = document.querySelector("#savingForm");
const expenseChart = document.querySelector("#expenseChart");
const budgetChart = document.querySelector("#budgetChart");
// * Expenses variables
const sumExAmount = document.querySelectorAll(".sumExAmount");
const expenseAmount = document.querySelector("#expenseAmount");
const cattName = document.querySelectorAll(".cattName")
// * Budget variables
const budName = document.querySelectorAll(".budName");
const budgetAmount = document.querySelectorAll(".budgetAmount");
const budgetsAmount = document.querySelector("#budgetsAmount");
const exAmountBud = document.querySelectorAll(".exAmountBud");
// * Bar chart variables
const barTitles = document.querySelectorAll(".barTitles");
const barSumTotal = document.querySelectorAll(".barSumTotal");
const monthlyBar = document.querySelector("#monthlyBar");
// * expandButtonVariables
const expenseExpand = document.querySelector("#expenseExpand")
const allExpenses = document.querySelector("#allExpensesCont")

// * Fixe Decimal Problem variables
const fixDec = document.querySelectorAll(".fixDec");
for(let i = 0; i < fixDec.length; i++){
    const deciNum = Number(fixDec[i].textContent);
    fixDec[i].textContent = deciNum.toFixed(2);
}





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
    if(amount.length === 0){
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
const createChart = (chart ,d, chartType = "pie")=>{ 
    let result = new Chart(chart, {
        type: chartType,
        data: {
            labels: d.exTitles,
            datasets: [{
                label: 'Expense Group by Month',
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

// ?Create stack bar chart for budget and expense data

const getBudgetExpense = (dataInfo)=>{
    const result = []
    dataInfo.forEach((d)=>{
        result.push(d.textContent)
    })
    return result
}
const createBarStack = (chartLocal)=>{
    const stackBar = retrieveExInfo(budgetAmount,budName)
    const data = {
        labels: stackBar.exTitles,
        datasets: [
          {
            label: 'Budget Amount',
            data: stackBar.expenseData,
            backgroundColor: ranColor(),
          },
          {
            label: 'Expense Amount',
            data: getBudgetExpense(exAmountBud),
            backgroundColor: ranColor(),
          },
        ]
      };
      let config = {
        type: 'bar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
      };
      let stack = new Chart(chartLocal, config);
}

// ? Declaring all the charts of the page
let myChart = createChart(expenseChart, retrieveExInfo(sumExAmount, cattName))
let budChart = createBarStack(budgetChart);
let monthBar = createChart(monthlyBar, retrieveExInfo(barSumTotal, barTitles), "bar")

// ?The sum of the aside expense and budget data
sumExAmount.forEach((d)=>{
    expenseAmount.textContent = Number(expenseAmount.textContent) + Number(d.textContent)
    expenseAmount.textContent = Number(expenseAmount.textContent).toFixed(2);
});
budgetAmount.forEach((d)=>{
    budgetsAmount.textContent = Number(budgetsAmount.textContent) + Number(d.textContent)
    budgetsAmount.textContent = Number(budgetsAmount.textContent).toFixed(2);
});

// ? Checks if the button has the - or + sign in the textcontent
const checkButton = (data)=>{
    if (data.textContent === "-"){
        data.textContent = "+";
        data.classList.toggle("greenButton")
    }else{
        data.textContent = "-";
        data.classList.toggle("redButton")
    }
}

// ? Events listeners to wait for the click of hiding info
exExpandButton.addEventListener('click', ()=>{
    expenseForm.classList.toggle("hideForm")
    checkButton(exExpandButton);
    
})

savExpandButton.addEventListener('click', ()=>{
    savingForm.classList.toggle("hideForm");
    checkButton(savExpandButton);
})

expenseExpand.addEventListener('click', ()=>{
    allExpenses.classList.toggle('hideDiv');
    checkButton(expenseExpand)
})