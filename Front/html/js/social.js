class Social {
    #trigger;

    constructor(id)
    {
        this.#trigger = true;
        document.getElementById("social_main_btn").addEventListener("click", (e) => {
            if (this.#trigger == true)
                this.Open()
            else
                this.Close()
        });
    }

    addFriend(player_id)
    {
        matchmaking.addFriend(player_id);
    }

    removeFriend(player_id)
    {
        matchmaking.removeFriend(player_id);
    }

    updateStatus(player_id, status)
    {
        this.updatePlayer(true, player_id, player_id, status);
    }


    updatePlayer(is_friend, player_id, name, status)
    {
        let element = document.getElementById('social_'+player_id);
        ////console.log(element, element.parentElement.id, is_friend);
        if (element == null)
            return ;
        //console.log(element.parentElement.id, is_friend);
        if ((element.parentElement.id == "social_list_player" && is_friend == true)
            || (element.parentElement.id == "social_list_friends" && is_friend == false))
        {
            element.remove();
            this.addPlayer(is_friend, player_id, name, status);
            return ;
        }

        if (status)
            document.getElementById('social_status_'+player_id).className = 'social-status-player social-status-player-on';
        else
            document.getElementById('social_status_'+player_id).className = 'social-status-player social-status-player-off';
    }

    addPlayer(is_friend, player_id, name, status)
    {
        let element = document.getElementById('social_'+player_id);

        if (element != null)
        {
            if (status)
                document.getElementById('social_status_'+player_id).className = 'social-status-player social-status-player-on';
            else
                document.getElementById('social_status_'+player_id).className = 'social-status-player social-status-player-off';
            return ;
        }
        let parent_id = "social_list_player";
        let action_type = "img/star_line.svg";

        if (is_friend)
        {
            parent_id = "social_list_friends";
            action_type = "img/star_fill.svg";
        }
        const socialPlayer = document.createElement('div');
        socialPlayer.className = 'social-player';
        socialPlayer.id = 'social_'+player_id;

        const socialPlayerBox = document.createElement('div');
        socialPlayerBox.className = 'social-player-box';

        const socialStatusPlayer = document.createElement('div');
        socialStatusPlayer.id = 'social_status_'+player_id;
        if (status)
            socialStatusPlayer.className = 'social-status-player social-status-player-on';
        else
            socialStatusPlayer.className = 'social-status-player social-status-player-off';

        const socialPlayerName = document.createElement('span');
        socialPlayerName.className = 'social-player-name';
        socialPlayerName.textContent = name;
		socialPlayerName.setAttribute("onclick", "loadHistory('" + `https://${raw_url}/front/history/` + player_id + "')");
        socialPlayerBox.appendChild(socialStatusPlayer);
        socialPlayerBox.appendChild(socialPlayerName);

        const img = document.createElement('img');
        img.src = action_type;
        img.className = 'social-player-action';
        if (is_friend)
            img.setAttribute("onclick", "social.removeFriend(\""+player_id+"\")");
        else
            img.setAttribute("onclick", "social.addFriend(\""+player_id+"\")");
        socialPlayer.appendChild(socialPlayerBox);
        socialPlayer.appendChild(img);

        //document.getElementById(parent_id).appendChild(socialPlayer);
        this.appendPlayer(parent_id, socialPlayer);
    }

    appendPlayer(parent_id, social_player)
    {
        const parentElement = document.getElementById(parent_id);
        
        if (parentElement)
            parentElement.appendChild(social_player);
        else
            setTimeout(() => this.appendPlayer(parent_id, social_player), 500);
    }
    

    leavePlayer(player_id)
    {
        let element = document.getElementById('social_'+player_id);

        if (element == null)
            return ;

        element.remove();
    }

    clear()
    {
        var element_friends = document.getElementById("social_list_friends");
        element_friends.innerHTML= "";

        var element_player = document.getElementById("social_list_player");
        element_player.innerHTML= "";
    }

    updateFriends(player_id, status)
    {
        if (status)
            document.getElementById('social_status_'+player_id).className = 'social-status-player social-status-player-on';
        else
            document.getElementById('social_status_'+player_id).className = 'social-status-player social-status-player-off';
    }

    changeRelation(is_friend, player_id, name, status)
    {
        let type_status;
        let element = document.getElementById('social_'+player_id);

        if (element == null)
            return ;

        let element_status = document.getElementById('social_status_'+player_id);
        if (element_status == null)
            return ;

        type_status = element_status.className;

        element.remove();

       
        if (type_status == "social-status-player social-status-player-on")
            this.addPlayer(is_friend, player_id, name, status);
    }


    Show()
    {
        document.getElementById("social_main").style.display = "flex";
    }

    Hide()
    {
        document.getElementById("social_main").style.display = "none";
        this.Close();
    }

    Open()
    {
        document.getElementById("social_main").style.height = "300px";
        document.getElementById("social_main_arrow").style.transform = "rotateX(0deg)";
        this.#trigger = false;
    }

    Close()
    {
        document.getElementById("social_main").style.height = "32px";
        document.getElementById("social_main_arrow").style.transform = "rotateX(180deg)";
        this.#trigger = true;
    }

}