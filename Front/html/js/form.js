class FormInputTitle {
    #id;

    constructor(id)
    {
        this.#id = id;
        document.getElementById(this.#id).addEventListener("focus", (e) => {
            document.getElementById(this.#id+"_box").style.border = "1.5px solid #bdbdbd";
            this.#upTitle();
        });

        document.getElementById(this.#id).addEventListener("blur", (e) => {
            document.getElementById(this.#id+"_box").style.border = "1.5px solid transparent";
            if (document.getElementById(this.#id).value == "")
                this.#downTitle();
        });
    }

    #upTitle()
    {
        //document.getElementById(this.#id+"_title").style.color = "#bdbdbd";
        document.getElementById(this.#id+"_title").style.fontSize = "12px";
        document.getElementById(this.#id+"_title").style.top = "0px";
    }

    #downTitle()
    {
        //document.getElementById(this.#id+"_title").style.color = "#757575";
        document.getElementById(this.#id+"_title").style.fontSize = "15px";
        document.getElementById(this.#id+"_title").style.top = "12px";
    }
}