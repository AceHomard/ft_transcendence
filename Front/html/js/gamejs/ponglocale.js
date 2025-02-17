'use strict';

var canvaslocal;
var contextt;
var gamet;

//var PLAYER_HEIGHT = 100;    // var rather than const to make it responsive
//var PLAYER_WIDTH = 5;       // var rather than const to make it responsive
var gameLocalAnimationFrameId;
let debug_game = false;

let game_runningt = true
let max_score_game = 5;

var keysPressedt = {
    player: {},     // Tab to stock if Key are down or not for Player1
    player2: {}     // Tab to stock if Key are down or not for Player2
}

window.addEventListener("resize", (event) => {
    const canvasLocal = document.getElementById("canvas_game");
    if (canvasLocal) {
        canvasLocal.style.width = window.innerWidth * 0.5 + "px";
        canvasLocal.style.height = (window.innerWidth * 0.5) * 0.4923076923 + "px";
    }
});

var local_game_help = false;

function writeTitleNamelocal(context, text, x, y, align, color, size)
{
    context.font = `${size}px Inter, Helvetica, Arial, sans-serif`;
    context.textAlign = "center";
    context.fillStyle = color;
    context.textAlign = align;
    context.fillText(text, x, y);
}

function localgameDrawHelpClear()
{
    local_game_help = false;
}

function localgameDrawHelp()
{
    if (local_game_help == false)
        return ;

    let avatar_size = 150;

    writeTitleNamelocal(contextt, "[W]", 150 * game_resolution + avatar_size / 25, canvaslocal.height / 2 - 15* game_resolution, "center", "white", 20 * game_resolution);
    writeTitleNamelocal(contextt, "[S]", 150 * game_resolution + avatar_size / 25, canvaslocal.height / 2 + 15* game_resolution, "center", "white", 20 * game_resolution);
    writeTitleNamelocal(contextt, "[UP]", canvaslocal.width - 150 * game_resolution + avatar_size / 25, canvaslocal.height / 2 - 15* game_resolution, "center", "white", 20 * game_resolution);
    writeTitleNamelocal(contextt, "[DOWN]", canvaslocal.width - 150 * game_resolution + avatar_size / 25, canvaslocal.height / 2 + 15* game_resolution, "center", "white", 20 * game_resolution);

}

// Function to draw Field, Players and Ball
function drawlocal() {
    
    document.getElementById("canvas_game").style.width = window.innerWidth * 0.5+"px";
    document.getElementById("canvas_game").style.height = (window.innerWidth * 0.5) * 0.4923076923+"px";

    // Draw Field
    contextt.fillStyle = '#18181c';                            // Set Background color
    contextt.fillRect(0, 0, canvaslocal.width, canvaslocal.height);    // Fill Background with a rectangle
    localgameDrawHelp();
    // Draw Score
    contextt.font = 20* game_resolution+"px Arial";                        // Settings Font
    contextt.fillStyle = 'white';                        // Set Font color
    contextt.fillText("" + gamet.player.score, 290* game_resolution, 30* game_resolution);  // Set Text to print with others parameters
    contextt.fillText("" + gamet.player2.score, 340* game_resolution, 30* game_resolution); // Set Text to print with others parameters
    
    
    // Draw Players
    contextt.fillStyle = 'white';                                        // Set color
    contextt.fillRect(0, gamet.player.y * game_resolution, PLAYER_WIDTH * game_resolution, PLAYER_HEIGHT * game_resolution);    // Fill Background (width/height) with a rectangle
    contextt.fillRect(canvaslocal.width - PLAYER_WIDTH * game_resolution, gamet.player2.y * game_resolution, PLAYER_WIDTH * game_resolution, PLAYER_HEIGHT * game_resolution);

    // Draw Ball
    contextt.beginPath(); // Create a new path for a complexe figure (needed to draw Line, circle...)
    contextt.fillStyle = 'white'; // Set color
    contextt.arc(gamet.ball.x * game_resolution, gamet.ball.y * game_resolution, gamet.ball.r * game_resolution, 0, Math.PI * 2, false); // Create a circular center
    contextt.fill(); //  Fill the figure (ball here)
    if (debug_game == true)
    {
        //console.log(gamet.ball);
        //console.log(canvaslocal.width / 2);
        debug_game = false;
    }

}

function initGamelocal(){
    canvaslocal = document.getElementById('canvas_game');
    contextt = canvaslocal.getContext('2d');

    canvaslocal.width = 650 * game_resolution;
    canvaslocal.height = 320 * game_resolution;
    debug_game = true;

    local_game_help = true;
    setTimeout(localgameDrawHelpClear, 4000);
    
    //==============================================Initiating game parameters=====================================================
    gamet = {
        player: {
            id : 'player1',
            y: canvaslocal.height / game_resolution / 2 - PLAYER_HEIGHT / 2,
            score: 0
        },
        player2: {
            id : 'player2',
            y: canvaslocal.height / game_resolution / 2 - PLAYER_HEIGHT / 2,
            score: 0
        },
        ball: {
            x: canvaslocal.width / game_resolution / 2,
            y: canvaslocal.height / game_resolution / 2,
            r: 5,
            speed: {
                x: 2,
                y: 2
            }
        }
    };
	game_runningt = true;
    drawlocal();
    playlocal();

    //===================================================================================================

    document.addEventListener('keydown', function(event) {
        keysPressedt.player[event.keyCode] = true;   // Keydown True for the specified Key for player 1 (see object up there)
        keysPressedt.player2[event.keyCode] = true;  // Keydown True for the specified Key for player 2 (see object up there)
    });

    document.addEventListener('keyup', function(event) {
        keysPressedt.player[event.keyCode] = false;  // Keydown False for the specified Key for player 1 (see object up there)
        keysPressedt.player2[event.keyCode] = false; // Keydown False for the specified Key for player 2 (see object up there)
    })

    document.addEventListener('touchstart', event => {
        let midHeight = screen.height / 2;
        let midWidth = screen.width / 2;
        event.preventDefault();
        if(event.touches[0].pageY >= midHeight && event.touches[0].pageX >= midWidth)
            keysPressedt.player2[40] = true;
        else if(event.touches[0].pageY < midHeight && event.touches[0].pageX >= midWidth)
            keysPressedt.player2[38] = true;
        else if(event.touches[0].pageY >= midHeight && event.touches[0].pageX < midWidth)
            keysPressedt.player[83] = true;
        else
            keysPressedt.player[87] = true;
    })

    document.addEventListener('touchend', event => {
        event.preventDefault();
        keysPressedt.player2[40] = false;
        keysPressedt.player2[38] = false;
        keysPressedt.player[83] = false;
        keysPressedt.player[87] = false;
    })
}

// all Mouvements printing ++ Players mouvements Implementation
function playlocal () {
    if (game_runningt)
    {
        ballMovelocal();
        if (keysPressedt.player[83] && gamet.player.y * game_resolution + PLAYER_HEIGHT * game_resolution < canvaslocal.height) {
            gamet.player.y += 4; // S key Pressed
        }
        if (keysPressedt.player[87] && gamet.player.y > 0) {
            gamet.player.y -= 4; // W Key Pressed
        }
        if (keysPressedt.player2[40] && gamet.player2.y * game_resolution + PLAYER_HEIGHT * game_resolution < canvaslocal.height) {
            gamet.player2.y += 4; // Down Arrow Key Pressed
        }
        if (keysPressedt.player2[38] && gamet.player2.y > 0) {
            gamet.player2.y -= 4; // Up Arrow Key Pressed
        }
            
        drawlocal();
        gameLocalAnimationFrameId = window.requestAnimationFrame(playlocal); // Execute play function before each refresh of the screen
    }
	else
	{
		//console.log("--- END ---");
		setTimeout(redirhome, 5000);
	}
}

function CancelLocalGame()
{
    gameLocalAnimationFrameId = window.cancelAnimationFrame(gameLocalAnimationFrameId);
    game_trigger_stop = true;
}

//=============================================================================================
//  Ball Mouvement
function ballMovelocal() {
    if (gamet.ball.y * game_resolution > canvaslocal.height || gamet.ball.y * game_resolution < 0) {
        gamet.ball.speed.y *= -1;
    }
    if (gamet.ball.x * game_resolution + gamet.ball.r * game_resolution >= canvaslocal.width - PLAYER_WIDTH * game_resolution) {
        collidelocal(gamet.player2);
    } else if (gamet.ball.x * game_resolution - gamet.ball.r * game_resolution <= PLAYER_WIDTH * game_resolution) {
        collidelocal(gamet.player);
    }
    gamet.ball.x += gamet.ball.speed.x;
    gamet.ball.y += gamet.ball.speed.y;
}

//  collision // ICIIII
function collidelocal(player) {
    if (gamet.ball.y * game_resolution < player.y * game_resolution || gamet.ball.y * game_resolution > player.y * game_resolution + PLAYER_HEIGHT * game_resolution)
    {
        debug_game = true;
        gamet.ball.x = canvaslocal.width / game_resolution / 2;
        gamet.ball.y = canvaslocal.height / game_resolution / 2;
        gamet.player.y = canvaslocal.height / game_resolution / 2 - PLAYER_HEIGHT / 2;
        gamet.player2.y = canvaslocal.height / game_resolution / 2 - PLAYER_HEIGHT / 2;

        if (Math.random() >= 0.5)
            gamet.ball.speed.x = Math.random() * (5 - 3) + 3;
        else
            gamet.ball.speed.x = Math.random() * (-3 + 5) - 5;
        if (Math.random() >= 0.5)
            gamet.ball.speed.y = Math.random() * (-3 + 5) - 5;
        else
            gamet.ball.speed.y = Math.random() * (5 - 3) + 3;
        if (player == gamet.player)
            gamet.player2.score++;
        else
            gamet.player.score++;
        if (gamet.player.score == max_score_game || gamet.player2.score == max_score_game)
        {
            if (gamet.player.score == max_score_game)
                EndLocalGame("Player Left");
            else
                EndLocalGame("Player Right");
            game_runningt = false;
        }
           
    } else {
        gamet.ball.speed.x *= -1.2;
        if (gamet.ball.speed.x > 15)
            gamet.ball.speed.x = 15
        else if (gamet.ball.speed.x < -15)
            gamet.ball.speed.x = -15
        changeDirectionlocal(player.y);
    }
}

function EndLocalGame(player_name)
{
    in_game_data = false;
    CancelLocalGame();
    end_status_win = true;
    FireworkInit();
    //end_status_title = "WINNER:";
    end_status_subtitle = player_name
}

// Ball 'Random' collision
function changeDirectionlocal(playerPosition) {
    var impact = gamet.ball.y - playerPosition - PLAYER_HEIGHT / 2;
    var ratio = 1.5

    gamet.ball.speed.y = Math.round(impact * ratio / 10);
    if (gamet.ball.speed.y == 0)
        gamet.ball.speed.y = 1
}
