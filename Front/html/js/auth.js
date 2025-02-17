var player_id = ""
var matchmaking;
var game;
var notificationWS;
var leaderboard;
var social;
var isBotGame = false;
function setCookie(cname, cvalue, exdays)
{
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/;SameSite=Lax";
}

function getCookie(cname)
{
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function eraseCookie(name)
{
  document.cookie = name + '=; Max-Age=0'
}


window.addEventListener('DOMContentLoaded', () => {
  if (getCookie("notif_id") == "")
    setCookie("notif_id", Uniqid.generate(), 365)
  matchmaking = new Matchmaking();
  notificationWS = new NotificationWS();
  notificationWS.sendAuth() 
  game = new GameWebSocket();
  leaderboard = new Leaderboard();
  social = new Social();
});

function updatePlayerId()
{
    player_id = getCookie("uniqid");
    matchmaking.sendAuth();
    game.sendAuth();
}

function truncateString(str)
{
    maxLength = 10;
    
    if (str.length > maxLength)
      return str.substring(0, maxLength - 3) + '...';

    return str;
}
