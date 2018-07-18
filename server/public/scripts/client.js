const app = angular.module('CA-app', []);

app.controller('CA-controller', function(){
    let self = this;

    // Neighbors and states are hardcoded for now, will be variables in the future
    self.ruleString = '';
    self.neighbors = 0;
    self.states = 0;
    self.rowNumber = 0;
    self.currentRow = '';

    // Initialize your canvas object
    c = document.getElementById('myCanvas');
    ctx = c.getContext('2d');

    // Canvas size is also hardcoded, this can be adjusted to a % of window width later
    c.width = 1001;
    c.height = 600;

    // The first row is currently hardcoded to be all zeroes except for the center unit
    // self.currentRow = new Array(c.width).fill('0');
    // for (let i=450; i<550; i++){
    //     if (i % 2 === 0) self.currentRow[i] = '1';
    // }

    // self.currentRow = self.currentRow.join('');
    // console.log(self.currentRow);

    self.generateRule = function(){
        console.log(`generate rule function called for rule ${self.rule} with ${self.neighbors} neighbors and ${self.states} states`);
        if (self.rule > self.states**(self.states**self.neighbors)){
            console.log('invalid rule number! try again');
            return;
        }
        self.ruleString = self.leadingZeros(self.rule.toString(self.states), self.states**self.neighbors);
        console.log(self.ruleString, self.ruleString.length);
    }

    self.leadingZeros = function(numberString, desiredLength){
        while (numberString.length < desiredLength){
            numberString = '0' + numberString;
        }
        return numberString;
    }

    self.applyRule = function(){
        let codon = Array.from(arguments).join('');
        return self.ruleString.charAt(parseInt(codon, self.states));
    }

    self.nextRow = function(previousRow){
        // console.log('current row', previousRow);
        // console.log(self.currentRow.length);
        let nextRow = '';
        console.log(previousRow.charAt(0), previousRow.charAt(1));
        nextRow += self.applyRule(previousRow.charAt(previousRow.length-1), previousRow.charAt(0), previousRow.charAt(1));
        for (i=1; i< previousRow.length-1; i++){
            nextRow += self.applyRule(previousRow.charAt(i-1), previousRow.charAt(i), previousRow.charAt(i+1))
        }
        nextRow += self.applyRule(previousRow.charAt(previousRow.length-2), previousRow.charAt(previousRow.length-1), previousRow.charAt(0));
        // console.log('next row:', nextRow);
        // console.log(self.currentRow.length);
        return nextRow;
    }

    self.drawRow = function(row){
        let rgbRow = ctx.createImageData(c.width, 1);
        // console.log(rgbRow.data);
        // for (let i=0; i<rgbRow.data.length; i+=4){
        //     rgbRow.data[i] = 255;
        //     rgbRow.data[i+1] = 0;
        //     rgbRow.data[i+2] = 0;
        //     rgbRow.data[i+3] = 255;
        // }
        // row = Array.from(row);
        // console.log(row, row.length);
        for (let i=0; i < row.length; i++){
            if (row[i] === '0'){
                // BLUE
                rgbRow.data[i*4+2] = 255;
            } else if (row[i] === '1'){
                // RED
                rgbRow.data[i*4] = 255;
            } else if (row[i] === '2'){
                // YELLOW
                rgbRow.data[i*4] = 255;
                rgbRow.data[i*4+1] = 255;
            } else if (row[i] = '3'){
                // GREEN
                rgbRow.data[i*4+1] = 255;
                rgbRow.data[i*4+2] = 255;
            }
            rgbRow.data[i*4+3] = 255;
        }
        // console.log(rgbRow.data);
        ctx.putImageData(rgbRow,0,self.rowNumber);
    }

    // self.drawRow(firstRow);

    self.populate = function(){
        self.clearCanvas();
        self.currentRow = self.randomizeRow();
        self.generateRule();
        while (self.rowNumber < c.height){
            self.drawRow(self.currentRow);
            self.currentRow = self.nextRow(self.currentRow)
            self.rowNumber++;
        }
        self.rowNumber = 0;
        // console.log(self.currentRow);
    }

    self.randomizeRow = function(){
        // console.log(self.states);
        let row = '';
        while (row.length < c.width){
            // console.log(Math.floor(Math.random()*self.states));
            row += Math.floor(Math.random()*self.states)
        }
        console.log(row);
        return row;
    }

    self.clearCanvas = function(){
        ctx.clearRect(0,0, c.width, c.height);
    }
})