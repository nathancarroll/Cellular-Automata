let rulebook = [];
let neighbors = 3;
let states = 2;

function generateRule(event, rule=300){
    console.log(`generate rule function called with ${neighbors} neighbors and ${states} states`);
    console.log(states**(states**neighbors));
    if (rule > states**(states**neighbors)){
        console.log('invalid rule number! try again');
        return;
    }
    const ruleString = leadingZeros(rule.toString(states), states**neighbors);
    rulebook = Array.from(ruleString);
    console.log(rulebook); 
}

function leadingZeros(numberString, desiredLength){
    while (numberString.length < desiredLength){
        numberString = '0' + numberString;
    }
    return numberString;
}

function applyRule(){
    let codon = Array.from(arguments).join('');
    return ruleBook[parseInt(codon, states)];
}

