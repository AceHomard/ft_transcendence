//ratio 2.03125
// 0.4923076923
//1300 -> 650

//console.log("test");

let resolution = 2;
let width = 650;
let height = 320;

document.getElementById("play_page_canvas").style.width = window.innerWidth * 0.5+"px";
document.getElementById("play_page_canvas").style.height = (window.innerWidth * 0.5) * 0.4923076923+"px";

addEventListener("resize", (event) => {
    document.getElementById("play_page_canvas").style.width = window.innerWidth * 0.5+"px";
    document.getElementById("play_page_canvas").style.height = (window.innerWidth * 0.5) * 0.4923076923+"px";
});



let play_pong_animation = true;

let pose_a = 100;
let pose_b = 420;
let paddle_height = 65 * resolution;
let ball_pose = {x:0, y: 0, direction: 0, velocity: 0};

function degreesToRadians(degrees)
{
    return degrees * Math.PI / 180;
}

function moveProtection(input, height_line)
{
    if (input <= 0)
        return (0);
    if (input + height_line >= height * 2)
        return (height * 2 - height_line);
    return (input);
}

function reverseDirection(direction)
{
    let reversedDirection = direction - 180;

    reversedDirection += Math.random() * 20 - 10;

    if (reversedDirection < 0)
        reversedDirection += 360;
    else if (reversedDirection >= 360)
        reversedDirection -= 360;
    return reversedDirection;
}

function handleVerticalCollision(direction)
{
    return 360 - direction;
}


function checkCollisions()
{
    let ball_radius = 4;

    if (ball_pose.y <= 0)
    {
        ball_pose.direction = handleVerticalCollision(ball_pose.direction);
    }

    if (ball_pose.y >= height * resolution)
    {
        ball_pose.direction = handleVerticalCollision(ball_pose.direction);
    }

    if (ball_pose.x - ball_radius < 58 && ball_pose.y > pose_a && ball_pose.y < pose_a + paddle_height)
    {
        ball_pose.direction = reverseDirection(ball_pose.direction);
        ball_pose.velocity += 1;
    }

    if (ball_pose.x + ball_radius > width * resolution - 58 && ball_pose.y > pose_b && ball_pose.y < pose_b + paddle_height)
    {
       ball_pose.direction = reverseDirection(ball_pose.direction);
       ball_pose.velocity += 1;
    }
}

function movePadle(pose, height_line, excepeted)
{
    let speed = 4;

    if (excepeted >= pose + 20 && excepeted <= (pose + height_line) - 20)
        return (0);
    pose = pose + (paddle_height / 2);
    if (pose < excepeted)
        return (speed);
    if (pose > excepeted)
        return (-speed);
}

function playPongAnimation()
{
    if (ball_pose.x < 20 || ball_pose.x  > cwidth - 20)
    {
        centerPong();
    }
    ctx.clearRect(0, 0, width * resolution, height * resolution);

    if (ball_pose.direction >= 90 && ball_pose.direction <= 270)
    {
        pose_a += movePadle(pose_a, paddle_height, ball_pose.y);
        pose_a = moveProtection(pose_a, paddle_height);
    }
    else
    {

        pose_b += movePadle(pose_b, paddle_height, ball_pose.y);
        pose_b = moveProtection(pose_b, paddle_height);
    }
    checkCollisions();
    ball_pose.x += ball_pose.velocity * Math.cos(degreesToRadians(ball_pose.direction));
    ball_pose.y += ball_pose.velocity * Math.sin(degreesToRadians(ball_pose.direction));


    Drawarc(ctx, ball_pose.x, ball_pose.y, 10, 0, Math.PI * 2, 4, "white", true);
    Drawrect(ctx, 50, pose_a, 8, paddle_height, 9, "white");
    Drawrect(ctx, cwidth - 50, pose_b, 8, paddle_height, 9, "white");
    if (play_pong_animation)
        window.requestAnimationFrame(playPongAnimation);
}



function generateRandomStartAngle() {
    const random = Math.random();

    let angle;
    if (random < 0.5) {
        angle = Math.random() < 0.5 ? Math.floor(Math.random() * 26) : Math.floor(Math.random() * 26) + 335;
    } else {
        angle = Math.floor(Math.random() * 51) + 155;
    }

    return angle;
}

function centerPong()
{
    let start_angle = generateRandomStartAngle();

    ball_pose = {x:width, y:height, direction: start_angle, velocity: 10};
    pose_a = (height * resolution) / 2 - (paddle_height / 2);
    pose_b = (height * resolution) / 2 - (paddle_height / 2);
}


centerPong();

window.requestAnimationFrame(playPongAnimation);


let canvas = document.getElementById("play_page_canvas");
let ctx = canvas.getContext("2d");

let cwidth = width * resolution;
let cheight = height * resolution;

canvas.width = cwidth;
canvas.height = cheight;
/* ==================== CANVAS ==================== */

function Drawline(ctx, x1, y1, x2, y2, width, color)
{
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
}

function Drawarc(ctx, x, y, diametre, start, end, width, color, fill=false)
{
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.arc(x, y, diametre, start, end);
    if (fill) {
        ctx.fillStyle = color;
        ctx.fill();
    } else {
        ctx.stroke();
    }
}

function Drawrect(ctx, x, y, width, height, width_line, color)
{
    ctx.strokeStyle = color;
    ctx.lineWidth = width_line;
    ctx.beginPath();
    ctx.rect(x, y, width, height);
    ctx.stroke();
}

function WriteText(ctx, text, x, y, align, color)
{
    ctx.font = "65px Inter, Helvetica, Arial, sans-serif";
    ctx.fillStyle = color;
    ctx.textAlign = align;

    ctx.fillText(text, x, y);
}

function WriteTitle(ctx, text, x, y, align, color, size)
{
    ctx.font = size+"px Inter, Helvetica, Arial, sans-serif";
    ctx.fillStyle = color;
    ctx.textAlign = align;

    ctx.fillText(text, x, y);
}