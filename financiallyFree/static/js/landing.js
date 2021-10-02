const expenseTitle = document.getElementById('expenseTitle');
const expenseCost = document.getElementById('expenseCost');
const expenseForm = document.getElementById('expenseForm');

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

let expensePi = document.getElementById('expensePi');
let myChart = createChart()
// *Event listener that is waiting on user to hit confirm, data user input data is then added to the chart dynamically
expenseForm.addEventListener('submit',(e)=>{
    e.preventDefault();
    data.push(Number(expenseCost.value))
    labels.push(expenseTitle.value)
    backgroundColor.push(ranColor())
    myChart.destroy()
    myChart = createChart()
});


