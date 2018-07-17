const app = angular.module('CA-app', []);

app.controller('CA-controller', function(){
    console.log('ca-controller started');
    let self=this;

    c = document.getElementById('myCanvas');
    ctx = c.getContext('2d');
    console.log(screen.width);

    c.width = screen.width / 1.4;
    c.height = screen.height / 1.4;

    let imgData = ctx.createImageData(c.width, 1);
    console.log(imgData.data.length);

    for (let i=0; i<imgData.data.length; i+=4){
        imgData.data[i] = 0;
        imgData.data[i+1] = 0;
        imgData.data[i+2] = 255;
        imgData.data[i+3] = 255;
    }

    ctx.putImageData(imgData,0,0);

    document.getElementById('goButton').addEventListener('click', generateRule);

    let rulebook = [];
    let neighbors = 3;
    let states = 2;

    function generateRule(event, rule=90){
        console.log(`generate rule function called with ${neighbors} neighbors and ${states} states`);
        console.log(states**(states**neighbors));
        if (rule > states**(states**neighbors)){
            console.log('invalid rule number! try again');
            return;
        }
        const ruleString = leadingZeros(rule.toString(states), states**neighbors);
        rulebook = Array.from(ruleString);
        console.log(rulebook);
        console.log(nextRow([0,0,0,0,0,1,0,0,0,0,0]));
    }

    function leadingZeros(numberString, desiredLength){
        while (numberString.length < desiredLength){
            numberString = '0' + numberString;
        }
        return numberString;
    }

    function applyRule(){
        let codon = Array.from(arguments).join('');
        return rulebook[parseInt(codon, states)];
    }

    function nextRow(previousRow){
        let nextRow = [];
        nextRow.push(applyRule(previousRow[previousRow.length-1], previousRow[0], previousRow[1]))
        for (i=1; i< previousRow.length-1; i++){
            nextRow.push(applyRule(previousRow[i-1], previousRow[i], previousRow[i+1]));
        }
        nextRow.push(applyRule(previousRow[previousRow.length-2], previousRow[previousRow.length-1], previousRow[0]));
        // console.log(nextRow);
        return nextRow;
    }
})