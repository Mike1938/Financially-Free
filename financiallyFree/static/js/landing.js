const expenseTitle = document.getElementById('expenseTitle');
const expenseCost = document.getElementById('expenseCost');
const expenseForm = document.getElementById('expenseForm');
const totalExpenses = document.querySelector('#totalExpenses')
const errorChecking = document.querySelectorAll('.errorChecking')

// * Function in charge of creating rgb random colors
const ranColor = ()=>{
    rgb = []
    for(let i = 0; i < 3; i++){
        rgb.push(Math.floor(Math.random() * 255 ))
    }
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`
}
// *Chart data
let data = [12, 19, 3, 5, 2, 3]
let labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
let backgroundColor = [
    'rgb(255, 99, 132)',
    'rgb(54, 162, 235)',
    'rgb(255, 206, 86)',
    'rgb(75, 192, 192)',
    'rgb(153, 102, 255)',
    'rgb(255, 159, 64)'
]

// * Function in charge of creating pie chart
const createChart = ()=>{
    let result = new Chart(expensePi, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: '# of Votes',
                data: data,
                backgroundColor: backgroundColor,
                borderColor: backgroundColor,
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

// *Function capable of doin the sum of all the expenses
const sumExpenses = (data)=>{
    let sum = 0;
    data.forEach((d)=>{
        sum += d;
    })
    return `$${sum}`
}

totalExpenses.textContent = sumExpenses(data);


let expensePi = document.getElementById('expensePi');
let myChart = createChart()
// *Event listener that is waiting on user to hit confirm, data user input data is then added to the chart dynamically
expenseForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    // *Verification of user inputs   
    let title = expenseTitle.value.trim()
    let cost = Number(expenseCost.value)
    if(title === ""){
        errorChecking[0].classList.add('error')
        errorChecking[0].textContent = "Title cannot be left empty"
    }
    if(isNaN(cost)){
        errorChecking[1].classList.add('error')
        errorChecking[1].textContent = "Cannot be text, must be number"
    }
    else if(cost <= 0){
        errorChecking[1].classList.add('error')
        errorChecking[1].textContent = "Cannot less or equal to 0"
    }
    // * After verification of input if both are true then all data is push to chart
    if(title && cost){
        if(errorChecking[0].textContent || errorChecking[1].textContent){
            errorChecking[0].classList.remove('error')
            errorChecking[1].classList.remove('error')
        }
        data.push(Number(expenseCost.value))
        labels.push(title)
        backgroundColor.push(ranColor())
        myChart.destroy()
        myChart = createChart()
        totalExpenses.textContent = sumExpenses(data);
    }
    expenseCost.value = ""
    expenseTitle.value = ""
});


