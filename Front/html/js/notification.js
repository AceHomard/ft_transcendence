/* ==================== Notification ==================== */
//duree des notifs info ou si il faut les fermer
//duree des notifs error ou si il faut les fermer


class Notification {


    #duration_info = 4;
    #duration_error = 4;
    #notifications_list_max_size = 3;

    #notifications_id;
    #notifications_list = [];

    constructor() {
        this.#notifications_id = document.getElementById("notifications");
        setInterval(() => this.update(), 1000);
    }

    update()
    {
        for (let i = 0; i < this.#notifications_list.length; i++)
		{
			if (this.#notifications_list[i].expire <= this.#time())
			{
                this.#remove(this.#notifications_list[0].id);
                this.#notifications_list.splice(i, 1);
				i--;
			}
		}
    }

    #push(id)
    {
        if (this.#notifications_list.length + 1 > this.#notifications_list_max_size)
        {
            this.#remove(this.#notifications_list[0].id);
            this.#notifications_list.shift();
        }
         this.#notifications_list.push(id);
    }

    #add(title, message, type, expire)
    {
        const id = "notif_id" + Math.random().toString(16).slice(2)
        const notificationDiv = document.createElement("div");
        notificationDiv.setAttribute("id", id);
        notificationDiv.setAttribute("class", "notification reveal reveal-r notification-"+type);

        const iconSpan = document.createElement("img");
        iconSpan.setAttribute("class", "material-symbols-outlined notification-icon");
        if (type == "error")
            iconSpan.src = "img/info_error.svg";
        else if (type == "info")
            iconSpan.src = "img/info_info.svg";
        notificationDiv.appendChild(iconSpan);

        const innerDiv = document.createElement("div");
        const titleDiv = document.createElement("div");
        const titleSpan = document.createElement("span");
        titleSpan.setAttribute("class", "notification-title");
        titleSpan.textContent = title;
        titleDiv.appendChild(titleSpan);

        const messageSpan = document.createElement("span");
        messageSpan.setAttribute("class", "notification-message");
        messageSpan.textContent = message;

        innerDiv.appendChild(titleDiv);
        innerDiv.appendChild(messageSpan);

        notificationDiv.appendChild(innerDiv);

        this.#push({'id': id, 'expire': this.#time() + expire});
        this.#notifications_id.appendChild(notificationDiv);
        setTimeout(function() {
            notificationDiv.classList.add("active");
        }, 100);
    }

    #remove(id)
    {
        let element = document.getElementById(id);
        if (element)
        {
            element.classList.remove("active");
            setTimeout(function() {
                element.parentNode.removeChild(element);
            }, 500);
        }

    }

    info(title, message)
    {
        this.#add(title, message, "info", this.#duration_info);
    }

    error(title, message)
    {
        this.#add(title, message, "error", this.#duration_error);
    }

    #time()
	{
		return (parseInt(Date.now() / 1000));
	}

}