const canvas = document.getElementById('canvas1');
const ctx = canvas.getContext('2d');

width = window.innerWidth;
height = window.innerHeight;

canvas.width = width;
canvas.height = height;

const cellSize = 20;


class Ball{
    constructor (color, radius, init_position) {
        this.position = init_position
        this.radius = radius
        this.color = color
    }
    draw(ctx) {


    }
}