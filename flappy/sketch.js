let bird;
let pipes = [];
let score = 0;
let gameOver = false;

function setup() {
  createCanvas(800, 600);
  bird = new Bird();
  pipes.push(new Pipe());
}

function draw() {
  background(0);
  
  bird.update();
  bird.show();
  
  if (frameCount % 90 == 0) {
    pipes.push(new Pipe());
  }

  for (let i = pipes.length - 1; i >= 0; i--) {
    pipes[i].show();
    pipes[i].update();
    
    if (pipes[i].hits(bird)) {
      gameOver = true;
      fill(255, 0, 0);
      textSize(32);
      text("Game Over", width/2-100, height/2);
    }

    if (pipes[i].offscreen()) {
      pipes.splice(i, 1);
      if(!gameOver) {
        score++;
      }
    }
  }
  
  fill(255);
  textSize(32);
  text("Score: " + score, 10, 50);
  
  if (gameOver) {
    noLoop(); // Stop drawing / updating the game
  }
}

function mousePressed() {
  if (!gameOver) {
    bird.flap();
  }
}

class Bird {
  constructor() {
    this.y = height / 2;
    this.x = 64;
    
    this.gravity = 0.7;
    this.lift = -12;
    this.velocity = 0;
  }
  
  update() {
    this.velocity += this.gravity;
    this.y += this.velocity;
    
    if (this.y > height) {
      this.y = height;
      this.velocity = 0;
    }
    
    if (this.y < 0) {
      this.y = 0;
      this.velocity = 0;
    }
  }
  
  show() {
    fill(255, 204, 0); // Yellow color
    ellipse(this.x, this.y, 32, 32);
  }
  
  flap() {
    this.velocity += this.lift;
  }
}

class Pipe {
  constructor() {
    this.top = random(height / 2);
    this.bottom = random(height / 2);
    this.x = width;
    this.w = 20;
    this.speed = 2;
  }
  
  show() {
    fill(0, 255, 0); // Green color
    rect(this.x, 0, this.w, this.top);
    rect(this.x, height - this.bottom, this.w, this.bottom);
  }
  
  update() {
    this.x -= this.speed;
  }
  
  offscreen() {
    return (this.x < -this.w);
  }
  
  hits(bird) {
    if (bird.y < this.top || bird.y > height - this.bottom) {
      if (bird.x > this.x && bird.x < this.x + this.w) {
        return true;
      }
    }
    return false;
  }
}
