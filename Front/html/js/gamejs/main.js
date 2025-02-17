'use strict';
var i = 0
var player_side = "none";
let in_game_data = false

function getPlayerId()
{
    return (getCookie("uniqid"));
}

var canvas_game;
var game_data;
var gameAnimationFrameId;
let game_trigger_stop = false;
let game_timer_value = "";
let in_tree = false;

let end_status_loose = false;
let end_status_win = false;
let end_status_subtitle = "";

var PLAYER_HEIGHT = 100;    // var rather than const to make it responsive
var PLAYER_WIDTH = 5;       // var rather than const to make it responsive

var game_frameRate = 65;
var game_now;
var game_then = Date.now();
var game_interval = 1000/game_frameRate;
var game_delta;

var game_resolution = 2;
var game_cwidth;
var game_cheight;

var game_type;

var keysPressed = {}// Tab to stock if Key are down or not

var img_a = new Image();
var img_b = new Image();
//img_a.src = '/home/loculy/Desktop/Start/Auth/media/profile_default.png';
//img_b.src = '/home/loculy/Desktop/Start/Auth/media/profile_default.png';
var player_a_name = "Unknown";
var player_b_name = "Unknown";

addEventListener("resize", (event) => {
    if (canvas_game == null)
        return ;
    canvas_game.style.width = window.innerWidth * 0.5+"px";
    canvas_game.style.height = (window.innerWidth * 0.5) * 0.4923076923+"px";
    draw();
});

function drawArrow(ctx, fromx, fromy, tox, toy, arrowWidth, color)
{
    var headlen = 10;
    var angle = Math.atan2(toy-fromy,tox-fromx);
 
    ctx.save();
    ctx.strokeStyle = color;
 
    ctx.beginPath();
    ctx.moveTo(fromx, fromy);
    ctx.lineTo(tox, toy);
    ctx.lineWidth = arrowWidth;
    ctx.stroke();
 
    ctx.beginPath();
    ctx.moveTo(tox, toy);
    ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),
               toy-headlen*Math.sin(angle-Math.PI/7));
 
    ctx.lineTo(tox-headlen*Math.cos(angle+Math.PI/7),
               toy-headlen*Math.sin(angle+Math.PI/7));
 
    ctx.lineTo(tox, toy);
    ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),
               toy-headlen*Math.sin(angle-Math.PI/7));
 
    ctx.stroke();
    ctx.restore();
}

function isImageOk(img)
{
    return img.complete && img.naturalHeight !== 0;
}

function roundedImage(ctx, x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
}

function addRoundedImage(ctx, x, y, width, height, radius, img) {

    if (!isImageOk(img))
    {
        throw new Error('Image is broken or not fully loaded');
    }
    ctx.globalAlpha = 1;
    ctx.save();
    roundedImage(ctx, x, y, width, height, radius);
    ctx.clip();
    ctx.drawImage(img, x, y, width, height);
    ctx.restore();
}

function writeTitleName(context, text, x, y, align, color, size)
{
    context.font = `${size}px Inter, Helvetica, Arial, sans-serif`;
    context.textAlign = "center";
    context.fillStyle = color;
    context.textAlign = align;
    context.fillText(text, x, y);
}

function writeTitle(text, x, y, align, color, size)
{
    var context = canvas_game.getContext('2d');
    context.font = `${size}px Inter, Helvetica, Arial, sans-serif`;
    context.textAlign = "center";
    context.fillStyle = color;
    context.textAlign = align;
    context.fillText(text, x, y);
}

function clearTimerGame()
{
    game_timer_value = "";
}

function displayTime()
{
    if (game_timer_value == "")
        return ;
    writeTitle(game_timer_value, canvas_game.width / 2, 150* game_resolution, "center", "white", 50*game_resolution);
    var ctx = canvas_game.getContext('2d');

    let avatar_size = 150;

    try {
        addRoundedImage(ctx,
            150 * game_resolution - avatar_size / 2,
            canvas_game.height / 2 - avatar_size / 2 - avatar_size / 3,
            avatar_size, avatar_size, avatar_size / 2, img_a);
    } catch (error) {

    }

    try {
        addRoundedImage(ctx,
            canvas_game.width - 150 * game_resolution - avatar_size / 2,
            canvas_game.height / 2 - avatar_size / 2 - avatar_size / 3,
            avatar_size, avatar_size, avatar_size / 2, img_b);
    } catch (error) {

    }

    writeTitleName(ctx, truncateString(player_a_name), 150 * game_resolution + avatar_size / 25, canvas_game.height / 2 + avatar_size - avatar_size / 3, "center", "white", 20 * game_resolution);
    writeTitleName(ctx, truncateString(player_b_name), canvas_game.width - 150 * game_resolution + avatar_size / 25, canvas_game.height / 2 + avatar_size - avatar_size / 3, "center", "white", 20 * game_resolution);

    if (game_timer_value == "GO")
    {
        setTimeout(clearTimerGame, 2000);
    }
}

function endGameDisplay(winner)
{
    var context = canvas_game.getContext('2d');

    canvas_game.style.width = window.innerWidth * 0.5+"px";
    canvas_game.style.height = (window.innerWidth * 0.5) * 0.4923076923+"px";

    context.fillStyle = '#18181c';
    context.textAlign = "center";
    context.fillRect(0, 0, canvas_game.width, canvas_game.height);
    writeTitle("WINNER:", canvas_game.width / 2, 150* game_resolution, "center", "red", 50);
    writeTitle(winner, canvas_game.width / 2, 210* game_resolution, "center", "red", 25);
}

// Function to draw Field, Players and Ball
function draw() {
    if (end_status_win == true)
        return ;
    var context = canvas_game.getContext('2d');
    
    game_cwidth = 650 * game_resolution;
    game_cheight = 320 * game_resolution;

    canvas_game.width = game_cwidth;
    canvas_game.height = game_cheight;

	canvas_game.style.width = window.innerWidth * 0.5+"px";
    canvas_game.style.height = (window.innerWidth * 0.5) * 0.4923076923+"px";


    // Draw Field
    context.fillStyle = '#18181c';                            // Set Background color
    context.fillRect(0, 0, canvas_game.width * game_resolution, canvas_game.height * game_resolution);    // Fill Background with a rectangle

    displayTime();

    context.font = 20 * game_resolution + "px Arial";                        // Settings Font
    context.fillStyle = 'white';                        // Set Font color
    context.textAlign = "center";
    context.fillText("" + game_data.player.score, 290 * game_resolution, 30* game_resolution);  // Set Text to print with others parameters
    context.fillText("" + game_data.player2.score, 340 * game_resolution, 30* game_resolution); // Set Text to print with others parameters
    
    
    // Draw Players
    context.fillStyle = 'white';                                        // Set color
    context.fillRect(0, game_data.player.y * game_resolution, PLAYER_WIDTH * game_resolution, PLAYER_HEIGHT * game_resolution);    // Fill Background (width/height) with a rectangle
    context.fillRect(canvas_game.width - PLAYER_WIDTH * game_resolution, game_data.player2.y * game_resolution, PLAYER_WIDTH * game_resolution, PLAYER_HEIGHT * game_resolution);

    // Draw Ball
    context.beginPath(); // Create a new path for a complexe figure (needed to draw Line, circle...)
	context.strokeStyle = 'white'
    context.lineWidth = 4
    context.fillStyle = 'white'; // Set color
    context.arc(game_data.ball.x * game_resolution, game_data.ball.y * game_resolution, game_data.ball.r * game_resolution, 0, Math.PI * 2); // Create a circular center
    context.fill(); //  Fill the figure (ball here)

}

function sendCommand(command, mouvement) {
    fetch('/cli/command/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ 'command': command, 'mouvement': mouvement })
    })
    .then(response => response.json())
    .then(data => {
    })
    .catch((error) => {
        //console.log('Error:', data);
    });
}

// Fonction CLI
window.up = function() {
    if (getPlayerCoor().y > 0)
        sendCommand('up', -36);
};

window.down = function() {
    if (getPlayerCoor().y * game_resolution + PLAYER_HEIGHT * game_resolution < canvas_game.height)
        sendCommand('down', 36);
};

function initGame()
{
    let btn_Game = document.getElementById('Game');
	let btn_Profil = document.getElementById('Profil');
	let btn_loginButton = document.getElementById('loginButton');
	let btn_signinButton = document.getElementById('signinButton');
    
    btn_Game.style.display = 'none';
	btn_Profil.style.display = 'none';
    btn_loginButton.style.display = 'none';
	btn_signinButton.style.display = 'none';

    
    
    canvas_game = document.getElementById('canvas_game');
    game_data = {
        player: {
            id : 'player1',
            y: canvas_game.height / 2 - PLAYER_HEIGHT / 2,
            score: 0
        },
        player2: {
            id : 'player2',
            y: canvas_game.height / 2 - PLAYER_HEIGHT / 2,
            score: 0
        },
        ball: {
            x: canvas_game.width / 2,
            y: canvas_game.height / 2,
            r: 5,
            speed: {
                x: 0,
                y: 0
            }
        }
    };
    
    draw();

    gameAnimationFrameId = window.requestAnimationFrame(play);

    // Utilisez une fonction de rappel anonyme pour gérer l'événement
    document.addEventListener('keydown', function(event) {
        if (in_game_data === true)
            keysPressed[event.keyCode] = true;   // Keydown True for the specified Key for player (see object up there)
    });

    document.addEventListener('keyup', function(event) {
        if (in_game_data === true)
            keysPressed[event.keyCode] = false;  // Keydown False for the specified Key for player (see object up there)
    })

    document.addEventListener('touchstart', (event) => {
        if (in_game_data === true){
            event.preventDefault();
            if(event.touches[0].pageY >= (screen.height / 2))
                keysPressed[40] = true;
            else
                keysPressed[38] = true;
        }
    })

    document.addEventListener('touchend', (event) => {
        if (in_game_data === true) {
            event.preventDefault();
            keysPressed[40] = false;
            keysPressed[38] = false;
        }
    })


    // CLI command handling
    document.getElementById('cli-input').addEventListener('keydown', function(event) {
        if (event.key == 'Enter') {
            const command = this.value.trim();

            executeCommand(command);
            this.value = '';
        }
    })
}

//CLI Commands Processing
function executeCommand(command) {
    switch (command) {
        case 'start-game_data':
            //console.log('Starting a new game_data...');
            break;
        case 'up':
            if (getPlayerCoor().y > 0)
                movePlayer(-96);
            break;
        case 'down':
            if (getPlayerCoor().y < 380)
                movePlayer(96);
            break;
        default:
            //console.log('Command not found:', command);
            break;
    }
}

function movePlayer(movement) {
    fetch('/api/move_player/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            movement: movement
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('La requête a échoué.');
        }
        return response.json();
    })
    .then(data => {
        if (data.status == true) {
            simulatePlayerMovement(getPlayerId(), data.movement);
            sendPlayerMovement(getPlayerId(), data.movement);
        }
    })
    .catch(error => {
        console.error('Erreur lors de l\'envoi de la requête API:', error);
    });
}

function sendPlayerMovement(playerId, movement) {
    game.sendPlayerMovement(movement);
}

function processMovementCorrection(correction) {
    const playerId = correction.player_id;
    const movementCorrection = correction.movement_correction;
    if ((playerId === getPlayerId() && player_side === "left") || (playerId !== getPlayerId() && player_side !== "left"))
        game_data.player.y = movementCorrection;
    else
        game_data.player2.y = movementCorrection;

    draw();
}

function simulatePlayerMovement(playerId, movement) {
    // Mettre à jour localement la position du joueur
    if ((playerId === getPlayerId() && player_side === "left") || (playerId !== getPlayerId() && player_side !== "left"))
        game_data.player.y += movement;
    else
        game_data.player2.y += movement;
}

function getPlayerCoor()
{
    if (player_side === "left")
        return game_data.player
    return game_data.player2
}

// all Mouvements printing ++ Players mouvements Implementation
function play()
{
    game_now = Date.now();
    game_delta = game_now - game_then;

    if ((game_delta > game_interval))
    {
        game_then = game_now - (game_delta % game_interval);
        if (in_game_data === true)
            ballMove();

        if (keysPressed[40] && getPlayerCoor().y * game_resolution + PLAYER_HEIGHT * game_resolution < canvas_game.height) {
            simulatePlayerMovement(getPlayerId(), 4); // Down Arrow Key Pressed
            sendPlayerMovement(getPlayerId(), 4);
        }
        if (keysPressed[38] && getPlayerCoor().y > 0) {
            simulatePlayerMovement(getPlayerId(), -4); // Up Arrow Key Pressed
            sendPlayerMovement(getPlayerId(), -4);
        }

        draw();
        if (game_trigger_stop == true)
        {
            game_trigger_stop = false;
            return ;
        }
    }
    window.requestAnimationFrame(play); // Execute play function before each refresh of the screen
}

function CancelGame()
{
    gameAnimationFrameId = window.cancelAnimationFrame(gameAnimationFrameId);
    game_trigger_stop = true;
}


//  Ball Mouvement
function ballMove() {
    if (game_data.ball.y > canvas_game.height || game_data.ball.y < 0) {
        game_data.ball.speed.y *= -1;
    }
    if (game_data.ball.x + game_data.ball.r >= canvas_game.width - PLAYER_WIDTH) {
        collide(game_data.player2);
    } else if (game_data.ball.x - game_data.ball.r <= PLAYER_WIDTH) {
        collide(game_data.player);
    }
    game_data.ball.x += game_data.ball.speed.x;
    game_data.ball.y += game_data.ball.speed.y;
}

let lastCollisionTime = 0;
const minCollisionInterval = 100; // Limite à une collision toutes les 100 millisecondes

//  collision // ICIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
function collide(player) {
    if (game_data.ball.y < player.y || game_data.ball.y > player.y + PLAYER_HEIGHT) {
        game_data.ball.x = canvas_game.width / 2;
        game_data.ball.y = canvas_game.height / 2;
        game_data.player.y = canvas_game.height / 2 - PLAYER_HEIGHT / 2;
        game_data.player2.y = canvas_game.height / 2 - PLAYER_HEIGHT / 2;

        game_data.ball.speed.x = 0;
        game_data.ball.speed.y = 0;
    } else {
        game_data.ball.speed.x *= -1.2;
        changeDirection(player);
    }
}

function changeDirection(playerPosition) {
    var impact = game_data.ball.y - playerPosition - PLAYER_HEIGHT / 2;
    var ratio = 1;

    game_data.ball.speed.y = Math.round(impact * ratio / 10);
	if (game_data.ball.speed.y == 0)
        game_data.ball.speed.y = 1
}