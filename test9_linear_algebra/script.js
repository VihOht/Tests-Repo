const logsDiv = document.getElementById("logs");
const displayDiv = document.getElementById("display");

function logMessage(message, style="") {
    const p = document.createElement("p");
    p.textContent = message;

    if (style === "comment") {
        p.style.color = "#6a9955";
    }
    if (style === "information") {
        p.style.color = "#569cd6";
        p.style.fontWeight = "bold";
        p.style.border = "1px solid #569cd6";
        p.style.padding = "2px 4px";
    }
    logsDiv.appendChild(p);
}

function clearLogs() {
    logsDiv.innerHTML = "";
}

const canvas = document.getElementById("canvas1");
const ctx = canvas.getContext("2d");

canvas.width = 400;
canvas.height = 400;

function drawLine(x1, y1, x2, y2) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
}

const versorsLength = {
    i: 20,
    j: 20
}


function createGrid(cartesian=false, hasDashes=true, dashLength=5) {
    ctx.strokeStyle = "#e0e0e0";
    for (let x = 0; x <= canvas.width; x += versorsLength.i) {
        drawLine(x, 0, x, canvas.height);
    }
    for (let y = 0; y <= canvas.height; y += versorsLength.j) {
        drawLine(0, y, canvas.width, y);
    } 
    if (cartesian) {
        cartesianPlane(hasDashes, dashLength);
    }
}

function cartesianPlane(hasDashes=true, dashLength=5) {
    ctx.strokeStyle = "#000000";
    middleAxisX = Math.floor(Math.floor(canvas.width / versorsLength.i) / 2) * versorsLength.i;
    middleAxisY = Math.floor(Math.floor(canvas.height / versorsLength.j) / 2) * versorsLength.j;
    drawLine(middleAxisX, 0, middleAxisX, canvas.height);
    drawLine(0, middleAxisY, canvas.width, middleAxisY);

    // Draw Arrows
    const arrowSize = 7;
    // X Axis Arrow
    ctx.beginPath();
    ctx.moveTo(canvas.width - arrowSize, middleAxisY - arrowSize);
    ctx.lineTo(canvas.width, middleAxisY);
    ctx.lineTo(canvas.width - arrowSize, middleAxisY + arrowSize);
    ctx.fill();
    // Y Axis Arrow
    ctx.beginPath();
    ctx.moveTo(middleAxisX - arrowSize, arrowSize);
    ctx.lineTo(middleAxisX, 0);
    ctx.lineTo(middleAxisX + arrowSize, arrowSize);
    ctx.fill();

    // Draw dashes
    if (hasDashes) {
        for (let x = 0; x <= canvas.width; x += versorsLength.i) {
            if (x === middleAxisX) continue;
            for (let y = middleAxisY - dashLength; y <= middleAxisY + dashLength; y += dashLength * 2) {
                drawLine(x, y, x, y + dashLength);
            }
        }
        for (let y = 0; y <= canvas.height; y += versorsLength.j) {
            if (y === middleAxisY) continue;
            for (let x = middleAxisX - dashLength; x <= middleAxisX + dashLength; x += dashLength * 2) {
                drawLine(x, y, x + dashLength, y);
            }
        }
    }

}

class Vector2D {
    constructor(x, y, color="#ff0000", originX=0, originY=0, legend="") {
        this.x = x;
        this.y = y;
        this.originX = originX;
        this.originY = originY;
        this.color = color;
        this.legend = legend || `(${Math.round(this.x * 100) / 100}, ${Math.round(this.y * 100) / 100})`;
    }

    add(other, color="") {
        return new Vector2D(this.x + other.x, this.y + other.y, color === "" ? this.color : color, this.originX, this.originY);
    }

    subtract(other, color="") {
        const subV2 = new Vector2D(this.x - other.x, this.y - other.y, color === "" ? this.color : color, other.x, other.y);
        subV2.changeLegend(`\n${subV2.legend}`);
        return subV2;
    }

    scale(scalar, color="") {
        return new Vector2D(this.x * scalar, this.y * scalar, color === "" ? this.color : color, this.originX, this.originY);
    }

    dot(other) {
        return this.x * other.x + this.y * other.y;
    }

    matrixTransform(matrix) {
        const newX = matrix[0][0] * this.x + matrix[0][1] * this.y;
        const newY = matrix[1][0] * this.x + matrix[1][1] * this.y;
        return new Vector2D(newX, newY, this.color, this.originX, this.originY);
    }

    magnitude() {
        return Math.sqrt(this.x ** 2 + this.y ** 2);
    }

    normalize() {
        const mag = this.magnitude();
        return new Vector2D(this.x / mag, this.y / mag, this.originX, this.originY);
    }
    resetOrigin(newOriginX=0, newOriginY=0) {
        this.originX = newOriginX;
        this.originY = newOriginY;
    }
    changeColor(newColor) {
        this.color = newColor;
    }
    changeLegend(newLegend) {
        this.legend = newLegend;
    }
}

class Matrix2x2 {
    constructor(a, b, c, d) {
        this.matrix = [
            [a, b],
            [c, d]
        ];
    }
    subtract(other) {
        const result = new Matrix2x2(
            this.matrix[0][0] - other.matrix[0][0],
            this.matrix[0][1] - other.matrix[0][1],
            this.matrix[1][0] - other.matrix[1][0],
            this.matrix[1][1] - other.matrix[1][1]
        );
        return result;
    }
    multiply(other) {
        const result = new Matrix2x2(
            this.matrix[0][0] * other.matrix[0][0] + this.matrix[0][1] * other.matrix[1][0],
            this.matrix[0][0] * other.matrix[0][1] + this.matrix[0][1] * other.matrix[1][1],
            this.matrix[1][0] * other.matrix[0][0] + this.matrix[1][1] * other.matrix[1][0],
            this.matrix[1][0] * other.matrix[0][1] + this.matrix[1][1] * other.matrix[1][1]
        );
        return result;
    }
    determinant() {
        return this.matrix[0][0] * this.matrix[1][1] - this.matrix[0][1] * this.matrix[1][0];
    }
}


class RangeControler {
    constructor(labelText, x, y, min=0, max=10, initial=0, step=0.5, orientation="horizontal") {
        this.id = `range_${Math.random().toString(36).substr(2, 9)}`;
        this.label = document.createElement("label");
        this.label.textContent = labelText;
        this.label.htmlFor = this.id;
        this.label.style.fontFamily = "Arial, sans-serif";
        this.label.style.fontSize = "12px";

        this.input = document.createElement("input");
        this.input.id = this.id;
        this.input.style.width = "100px";
        this.input.value = initial;
        this.input.type = "range";
        this.input.min = min;
        this.input.max = max;
        this.input.step = step;
        
        this.x = x;
        this.y = y;
    }
    getValue() {
        this.label.textContent = `${this.label.textContent.split(":")[0]}: ${this.input.value}`;
        return parseFloat(this.input.value);
    }
    setValue(newValue) {
        this.input.value = newValue;
    }
    draw() {
        const div = document.createElement("div");
        div.style.position = "absolute";
        div.style.left = `${this.x}px`;
        div.style.top = `${this.y}px`;
        div.id = this.id;
        div.style.display = "flex";
        div.style.alignItems = "center";
        div.style.gap = "5px";
        
        div.appendChild(this.label);
        div.appendChild(this.input);
        displayDiv.appendChild(div);
    }
}

function drawVector(vector, showLegend=true) {
    const centralPointX = Math.floor(canvas.width / versorsLength.i / 2);
    const centralPointY = Math.floor(canvas.height / versorsLength.j / 2);


    const rOriginX = (vector.originX + centralPointX) * versorsLength.i;
    const rOriginY = (centralPointY - vector.originY) * versorsLength.j;

    const rVectorX = vector.x * versorsLength.i;
    const rVectorY = vector.y * versorsLength.j;

    const color = vector.color;

    // Drawing line
    ctx.strokeStyle = color;
    ctx.strokeWidth = 2;
    ctx.beginPath();
    ctx.moveTo(rOriginX, rOriginY);
    ctx.lineTo(rOriginX + rVectorX, rOriginY - rVectorY);
    ctx.stroke();
    ctx.closePath();

    // Drawing arrowhead
    const arrowSize = 7;
    const angle = Math.atan2(vector.y, vector.x);
    ctx.beginPath();
    ctx.moveTo(rOriginX + rVectorX, rOriginY - rVectorY);
    ctx.lineTo(rOriginX + rVectorX - arrowSize * Math.cos(angle - Math.PI / 6), rOriginY - rVectorY + arrowSize * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(rOriginX + rVectorX - arrowSize * Math.cos(angle + Math.PI / 6), rOriginY - rVectorY + arrowSize * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();

    // Drawing legend
    ctx.fillStyle = color;
    ctx.font = "12px Arial";
    if (showLegend) {
        vectorLegendParts = vector.legend.split("\n");
        for (let i = 0; i < vectorLegendParts.length; i++) {
            ctx.fillText(vectorLegendParts[i], rOriginX + rVectorX + 5, rOriginY - rVectorY - 5 + i * 14);
        }
    }
}


function animationLoop(script) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    createGrid(20, true);
    clearLogs();
    script();
    requestAnimationFrame(() => animationLoop(script));
}




function script1() {
    // Create a vector (3, 4)
    const v1 = new Vector2D(3, 4, "#0000ff");
    drawVector(v1);

    // Create another vector (1, 2)
    const v2 = new Vector2D(-2, 2, "#00ff00");
    drawVector(v2);


    const v3 = v1.add(v2, "#ff0000");
    drawVector(v3);

    const v4 = v1.subtract(v2, "#a35e59ff");

    drawVector(v4);

    logMessage(`v1: (${JSON.stringify(v1)})`);
    logMessage(`v2: (${JSON.stringify(v2)})`);
    logMessage(`v1 + v2 = v3: (${JSON.stringify(v3)})`);
}




const v1 = new Vector2D(5, 3, "#0000ff");  
const v2 = new Vector2D(2, 4, "#00ff00");

function script2() {
    drawVector(v1);
    drawVector(v2);
    
    // Increase v1 sinotically
    const time = Date.now() * 0.002;
    v1.x = 5 + Math.sin(time) * 3;
    v1.y = 3 + Math.cos(time) * 3;

    v2.x = 2 + Math.cos(time) * 2;
    v2.y = 4 + Math.sin(time) * 2;

    const v3 = v1.subtract(v2, "#ff0000");
    drawVector(v3);
}


function script3() {
    // Linear Transformation

    matrix = new Matrix2x2(-1, 0, 0, 1); // Shear Matrix

    const v1 = new Vector2D(3, 4, "#0000ff");
    drawVector(v1);

    const v2 = v1.matrixTransform(matrix.matrix);
    v2.changeColor("#ff0000");
    v2.changeLegend(`Matrix Transform\n(${v2.x.toFixed(2)}, ${v2.y.toFixed(2)})`);
    drawVector(v2);
    
    logMessage(`v1: (${JSON.stringify(v1)})`, "comment");
    logMessage(`v2 (Matrix Transform): (${JSON.stringify(v2)})`, "comment");

    if (matrix.determinant() === 0) {
        logMessage(`The transformation matrix is not invertible.\nM = ${JSON.stringify(matrix.matrix)} - D = ${matrix.determinant()}`, "information");
    } else {
        logMessage(`The transformation matrix is invertible.\nM = ${JSON.stringify(matrix.matrix)} - D = ${matrix.determinant()}`, "information");
    }
    v3 = v1.subtract(v2, "#177517ff");
    v3.changeLegend(`\nv1 - v2\n(${v3.x.toFixed(2)}, ${v3.y.toFixed(2)})`);
    drawVector(v3);
}

function script4() {
    // Range Controlers Example
    if (!window.rangeControler1) {
        window.rangeControler1 = new RangeControler("Vector 1 X", 10, 10, -10, 10, 3, 0.1);
        window.rangeControler1.draw();
    }

    if (!window.rangeControler2) {
        window.rangeControler2 = new RangeControler("Vector 1 Y", 10, 40, -10, 10, 4, 0.1);
        window.rangeControler2.draw();
    }

    const v1 = new Vector2D(window.rangeControler1.getValue(), window.rangeControler2.getValue(), "#0000ff");
    drawVector(v1);

    if (!window.rangeControler3) {
        window.rangeControler3 = new RangeControler("Vector 2 X", 220, 10, -10, 10, 2, 0.1);
        window.rangeControler3.draw();
    }

    if (!window.rangeControler4) {
        window.rangeControler4 = new RangeControler("Vector 2 Y", 220, 40, -10, 10, 4, 0.1);
        window.rangeControler4.draw();
    }

    const v2 = new Vector2D(window.rangeControler3.getValue(), window.rangeControler4.getValue(), "#00ff00");

    drawVector(v2);


    const v3 = v1.subtract(v2, "#ff0000");;
    drawVector(v3);

    logMessage(`v1: (${JSON.stringify(v1)})`, "comment");
    logMessage(`v2: (${JSON.stringify(v2)})`, "comment");
    logMessage(`v1 - v2 = v3: (${JSON.stringify(v3)})`, "comment");
}


function main() {
    animationLoop(script4);
}

document.addEventListener("DOMContentLoaded", main);
document.addEventListener("resize", main);
