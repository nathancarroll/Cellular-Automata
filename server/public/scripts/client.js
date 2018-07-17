const app = angular.module('CA-app', []);

app.controller('CA-controller', function(){
    let self = this;

    self.rulebook = [];
    self.neighbors = 3;
    self.states = 2;
    self.currentRow = 0;

    c = document.getElementById('myCanvas');
    ctx = c.getContext('2d');
    console.log(screen.width);

    c.width = 1001;
    c.height = 600;

    self.generateRule = function(event, rule=90){
        console.log(`generate rule function called with ${self.neighbors} neighbors and ${self.states} states`);
        if (rule > self.states**(self.states**self.neighbors)){
            console.log('invalid rule number! try again');
            return;
        }
        const ruleString = self.leadingZeros(rule.toString(self.states), self.states**self.neighbors);
        self.rulebook = Array.from(ruleString);
        console.log(self.rulebook);
        console.log(self.nextRow(firstRow));
    }

    self.leadingZeros = function(numberString, desiredLength){
        while (numberString.length < desiredLength){
            numberString = '0' + numberString;
        }
        return numberString;
    }

    self.applyRule = function(){
        let codon = Array.from(arguments).join('');
        return self.rulebook[parseInt(codon, self.states)];
    }

    self.nextRow = function(previousRow){
        let nextRow = [];
        nextRow.push(self.applyRule(previousRow[previousRow.length-1], previousRow[0], previousRow[1]))
        for (i=1; i< previousRow.length-1; i++){
            nextRow.push(self.applyRule(previousRow[i-1], previousRow[i], previousRow[i+1]));
        }
        nextRow.push(self.applyRule(previousRow[previousRow.length-2], previousRow[previousRow.length-1], previousRow[0]));
        // console.log(nextRow);
        return nextRow;
    }

    self.drawRow = function(row){
        let rgbRow = ctx.createImageData(c.width, 1);
        for (let i=0; i<rgbRow.data.length; i+=4){
            rgbRow.data[i] = 255;
            rgbRow.data[i+1] = 0;
            rgbRow.data[i+2] = 0;
            rgbRow.data[i+3] = 255;
        }
        // for (let i=0; i < row.length; i++){
        //     if (row[i] === 0){
        //         // BLUE
        //         rgbRow[i*4+2] = 255;
        //     } else if (row[i] === 1){
        //         // RED
        //         rgbRow[i*4] = 255;
        //     } else if (row[i] === 2){
        //         // YELLOW
        //         rgbRow[i*4] = 255;
        //         rgbRow[i*4+1] = 255;
        //     } else if (row[i] = 3){
        //         // GREEN
        //         rgbRow[i*4+1] = 255;
        //         rgbRow[i*4+2] = 255;
        //     }
        //     rgbRow[i*4+3] = 255;
        // }

        ctx.putImageData(rgbRow,0,self.currentRow);
        self.currentRow++;
    }

    let firstRow = new Array(c.width).fill(0);
    firstRow[501] = 1;
    self.drawRow(firstRow);
    
})