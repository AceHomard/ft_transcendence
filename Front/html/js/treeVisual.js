class TreeVisual {
    constructor ()
    {
        this.width = 570;
        this.height = 570;
        this.resolution = 2;

        this.canvas = document.getElementById("tree_array");
        this.ctx = this.canvas.getContext("2d");

        this.cwidth = this.width * this.resolution;
        this.cheight = this.height * this.resolution;

        this.canvas.width = this.cwidth;
    	this.canvas.height = this.cheight;

        this.prct = 0;
        this.state_match = 0;
        this.state_final = 0;
        this.state_left = 0;
        this.state_right = 0;

        this.match_obj = "{}";
        this.tour_obj = "{}";
        
        this.middle = this.cwidth / 2;
        this.vs_line_width = 40 * this.resolution;
        this.vs_side_line_width = 50 * this.resolution;
        this.border = 150;
    }

    setMatchObj(obj)
    {
        this.match_obj = obj;
        if (isBotGame === true) {
            this.match_obj.player2_name = "BOT";
            this.match_obj.player2_avatar = "/media/bot.png";
        }
        //console.log(obj);
    }

    seTourObj(obj)
    {
        this.tour_obj = obj;
        //console.log(obj);
    }

    drawLine(x1, y1, x2, y2, width, color)
    {
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = width;
        this.ctx.beginPath();
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();
    }

    drawArc(x, y, diameter, start, end, width, color)
    {
        this.ctx.beginPath();
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = width;
        this.ctx.arc(x, y, diameter, start, end);
        this.ctx.stroke();
    }

    drawRect(x, y, width, height, lineWidth, color)
    {
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = lineWidth;
        this.ctx.beginPath();
        this.ctx.rect(x, y, width, height);
        this.ctx.stroke();
    }

    writeText(text, x, y, align, color)
    {
        this.ctx.font = "65px Inter, Helvetica, Arial, sans-serif";
        this.ctx.fillStyle = color;
        this.ctx.textAlign = align;
        this.ctx.fillText(text, x, y);
    }

    writeTitle(text, x, y, align, color, size)
    {
        this.ctx.font = `${size}px Inter, Helvetica, Arial, sans-serif`;
        this.ctx.fillStyle = color;
        this.ctx.textAlign = align;
        this.ctx.fillText(text, x, y);
    }

    writeName(text, x, y, align, color, size)
    {
        this.ctx.font = "bold "+size+"px sans-serif";
        this.ctx.fillStyle = color;
        this.ctx.textAlign = align;
        this.ctx.fillText(text, x, y);
    }


    drawArcFill(x, y, diameter, start, end, width, colorIn, colorOut)
    {
        this.ctx.beginPath();
        this.ctx.strokeStyle = colorOut;
        this.ctx.lineWidth = width;
        this.ctx.fillStyle = colorIn;
        this.ctx.arc(x, y, diameter, start, end);
        this.ctx.fill();
        this.ctx.stroke();
    }

    lineRounded(x1, y1, x2, y2, thickness, colorIn, colorOut)
    {
        const angle = Math.atan2(y2 - y1, x2 - x1);
        const perpAngle = angle + Math.PI / 2;

        const offset = thickness / 2;
        const dx = offset * Math.cos(perpAngle);
        const dy = offset * Math.sin(perpAngle);

        this.ctx.beginPath();
        this.ctx.arc(x2, y2, thickness / 2, angle - Math.PI / 2, angle + Math.PI / 2, false);
        this.ctx.lineTo(x2 + dx, y2 + dy);
        this.ctx.arc(x1, y1, thickness / 2, angle + Math.PI / 2, angle - Math.PI / 2, false);
        this.ctx.lineTo(x1 - dx, y1 - dy);
        this.ctx.closePath();

        this.ctx.fillStyle = colorIn;
        this.ctx.fill();
        this.ctx.lineWidth = 3;
        this.ctx.strokeStyle = colorOut;
        this.ctx.stroke();
    }

    onIMG_Loose(x, y) {
        this.drawArcFill(
            x + 60 * this.resolution / 2,
            y + 60 * this.resolution / 2,
            60 * this.resolution / 2,
            0, Math.PI * 2, 1, "rgb(255 56 86 / 70%)", "rgb(255 56 86 / 70%)"
        );

        this.writeTitle(
            "X", x + 60 * this.resolution / 2, y + 60 * this.resolution / 1.25, "center",
            "rgb(139 29 45 / 100%)", 100
        );
    }

    onIMG_Unknown(x, y) {
        this.drawArcFill(
            x + 60 * this.resolution / 2,
            y + 60 * this.resolution / 2,
            60 * this.resolution / 2,
            0, Math.PI * 2, 1, "rgb(56 56 56 / 70%)", "rgb(56 56 56 / 70%)"
        );

        this.writeTitle(
            "?", x + 60 * this.resolution / 2, y + 60 * this.resolution / 1.25, "center",
            "#e7eced", 100
        );
    }

    addRoundedImage(x, y, width, height, radius, src, type) {
        var img = new Image();
        img.onload = () => {
            this.ctx.globalAlpha = 1;
            this.ctx.save();
            this.roundedImage(x, y, width, height, radius);
            this.ctx.clip();
            this.ctx.drawImage(img, x, y, width, height);
            this.ctx.restore();
            ////console.log(type, parseInt(type), parseInt(type) === 1, parseInt(type) === 2);
            if (parseInt(type) === 1) {
                this.onIMG_Unknown(x, y);
            } else if (parseInt(type) === 2) {
                this.onIMG_Loose(x, y);
            }
        };
        img.src = src;
    }

    roundedImage(x, y, width, height, radius) {
        this.ctx.beginPath();
        this.ctx.moveTo(x + radius, y);
        this.ctx.lineTo(x + width - radius, y);
        this.ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
        this.ctx.lineTo(x + width, y + height - radius);
        this.ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
        this.ctx.lineTo(x + radius, y + height);
        this.ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
        this.ctx.lineTo(x, y + radius);
        this.ctx.quadraticCurveTo(x, y, x + radius, y);
        this.ctx.closePath();
    }

    progressionAnimation(percentage, min_value, max_value)
    {
        return min_value + (max_value - min_value) * (percentage / 100);
    }

    titleTree(text) {
        this.ctx.clearRect(0, 0, this.cwidth, 150);
        this.ctx.font = "bold 95px 'Press Start 2P'";
        this.ctx.fillStyle = "rgb(255, 56, 86)";
        this.ctx.textAlign = "center";
        this.ctx.fillText(text, this.middle, 60 * this.resolution);
    }

    matchArrayInit() {
        let obj = this.match_obj

        this.titleTree(title_match);
        this.addRoundedImage(
            this.middle - 60 * this.resolution / 2 - this.vs_line_width * 2.5,
            this.border * this.resolution - 60 * this.resolution / 2,
            60 * this.resolution,
            60 * this.resolution,
            33 * this.resolution, obj.player1_avatar, this.state_final === 0 || this.state_final === 1 ? 0 : 1);
        this.writeName(truncateString(obj.player1_name),
            this.middle - 60 * this.resolution / 2 - this.vs_line_width * 2.5 + 30* this.resolution,
            this.border * this.resolution - 60 * this.resolution / 2 + 85* this.resolution,
            "center", "#e7eced", 35);

        this.addRoundedImage(
            this.middle - 60 * this.resolution / 2 + this.vs_line_width * 2.5,
            this.border * this.resolution - 60 * this.resolution / 2,
            60 * this.resolution,
            60 * this.resolution,
            33 * this.resolution, obj.player2_avatar, this.state_final === 0 ? 0 : 1);
       	this.writeName(truncateString(obj.player2_name),
            this.middle - 60 * this.resolution / 2 + this.vs_line_width * 2.5 + 30* this.resolution,
            this.border * this.resolution - 60 * this.resolution / 2 + 85* this.resolution,
            "center", "#e7eced", 35);
    }

    matchArray() {
        
        this.titleTree(title_match);
        this.lineRounded(
            this.progressionAnimation(this.prct, this.middle, (this.middle - this.vs_line_width / 0.75)),
            this.border * this.resolution,
            this.progressionAnimation(this.prct, this.middle, (this.middle + this.vs_line_width / 0.75)),
            this.border * this.resolution,
            4 * this.resolution, "#e7eced", "#e7eced");
    }

    matchArrayAnimation() {
        this.matchArray();
        if (this.prct < 100) {
            this.prct += 3.5;
            window.requestAnimationFrame(() => this.matchArrayAnimation());
        }
    }

    titleTour(text) {
        this.ctx.clearRect(0, 0, this.cwidth, 150);
        this.ctx.font = "bold 95px 'Press Start 2P'";
        this.ctx.fillStyle = "rgb(255, 56, 86)";
        this.ctx.textAlign = "center";
        this.ctx.fillText(text, this.middle, 60 * this.resolution);
    }

    tournamentArrayInit() {
        let obj = this.tour_obj

        this.titleTour(title_tournament);
        this.addRoundedImage(
            this.middle - 60 * this.resolution / 2 - this.vs_line_width * 1.5,
            this.border * this.resolution - 60 * this.resolution / 2,
            60 * this.resolution,
            60 * this.resolution,
            33 * this.resolution, obj.final_game[0].avatar, obj.final_game[0].unknown);
        this.writeName(truncateString(obj.final_game[0].name),
            this.middle - 60 * this.resolution / 2 - this.vs_line_width * 1.5 + 30* this.resolution,
            this.border * this.resolution - 60 * this.resolution / 2 + 85* this.resolution,
            "center", "#e7eced", 35);
        
        this.addRoundedImage(
            this.middle - 60 * this.resolution / 2 + this.vs_line_width * 1.5,
            this.border * this.resolution - 60 * this.resolution / 2,
            60 * this.resolution,
            60 * this.resolution,
            33 * this.resolution, obj.final_game[1].avatar, obj.final_game[1].unknown);
        this.writeName(truncateString(obj.final_game[1].name),
            this.middle - 60 * this.resolution / 2 + this.vs_line_width * 1.5 + 30* this.resolution,
            this.border * this.resolution - 60 * this.resolution / 2 + 85* this.resolution,
            "center", "#e7eced", 35);
        
        this.addRoundedImage(
            this.middle / 2.5 - 60 * this.resolution / 2 - this.vs_side_line_width * 1.5,
            (this.height - this.border) * this.resolution - 60 * this.resolution / 2,
            60 * this.resolution,
            60 * this.resolution,
            33 * this.resolution, obj.left_game[0].avatar, obj.left_game[0].win);
        this.writeName(truncateString(obj.left_game[0].name),
            this.middle / 2.5 - 60 * this.resolution / 2 - this.vs_side_line_width * 1.5 + 30* this.resolution,
            (this.height - this.border) * this.resolution - 60 * this.resolution / 2 + 85* this.resolution,
            "center", "#e7eced", 35);
    
        this.addRoundedImage(
            this.middle / 2.5 - 60 * this.resolution / 2 + this.vs_side_line_width * 1.5,
            (this.height - this.border) * this.resolution - 60 * this.resolution / 2,
            60 * this.resolution,
            60 * this.resolution,
            33 * this.resolution, obj.left_game[1].avatar, obj.left_game[1].win);
        this.writeName(truncateString(obj.left_game[1].name),
            this.middle / 2.5 - 60 * this.resolution / 2 + this.vs_side_line_width * 1.5 + 30* this.resolution,
            (this.height - this.border) * this.resolution - 60 * this.resolution / 2 + 85* this.resolution,
            "center", "#e7eced", 35);
    
        this.addRoundedImage(
            this.cwidth - this.middle / 2.5 - 60 * this.resolution / 2 - this.vs_side_line_width * 1.5,
            (this.height - this.border) * this.resolution - 60 * this.resolution / 2,
            60 * this.resolution,
            60 * this.resolution,
            33 * this.resolution, obj.right_game[0].avatar, obj.right_game[0].win);
        this.writeName(truncateString(obj.right_game[0].name),
            this.cwidth - this.middle / 2.5 - 60 * this.resolution / 2 - this.vs_side_line_width * 1.5 + 30* this.resolution,
            (this.height - this.border) * this.resolution - 60 * this.resolution / 2 + 85* this.resolution,
            "center", "#e7eced", 35);
        
        this.addRoundedImage(
            this.cwidth - this.middle / 2.5 - 60 * this.resolution / 2 + this.vs_side_line_width * 1.5,
            (this.height - this.border) * this.resolution - 60 * this.resolution / 2,
            60 * this.resolution,
            60 * this.resolution,
            33 * this.resolution, obj.right_game[1].avatar, obj.right_game[1].win);
        this.writeName(truncateString(obj.right_game[1].name),
            this.cwidth - this.middle / 2.5 - 60 * this.resolution / 2 + this.vs_side_line_width * 1.5 + 30* this.resolution,
            (this.height - this.border) * this.resolution - 60 * this.resolution / 2 + 85* this.resolution,
            "center", "#e7eced", 35);
        
    }

    tournamentArray() {
        // Clear the entire canvas before drawing
        //this.ctx.clearRect(0, 0, this.cwidth, this.cheight);
    
        // Call the function to display the title for the tournament
        this.titleTour(title_tournament);
    
        // Draw lines for the final match
        this.lineRounded(
            this.progressionAnimation(this.prct, this.middle, (this.middle - this.vs_line_width / 2)),
            this.border * this.resolution,
            this.progressionAnimation(this.prct, this.middle, (this.middle + this.vs_line_width / 2)),
            this.border * this.resolution,
            4 * this.resolution, "#e7eced", "#e7eced");
    
        // Draw lines for the left side
        this.lineRounded(
            this.progressionAnimation(this.prct, (this.middle / 2.5), (this.middle / 2.5 - this.vs_side_line_width / 1.5)),
            (this.height - this.border) * this.resolution,
            this.progressionAnimation(this.prct, (this.middle / 2.5), (this.middle / 2.5 + this.vs_side_line_width / 1.5)),
            (this.height - this.border) * this.resolution,
            4 * this.resolution, "#e7eced", "#e7eced");
    
        this.lineRounded(
            (this.middle / 2.5 - this.vs_line_width / 4 + 9 * this.resolution),
            this.progressionAnimation(this.prct, this.border * this.resolution, (this.height - this.border) * this.resolution),
            (this.middle / 2.5 - this.vs_line_width / 4 + 9 * this.resolution),
            this.border * this.resolution,
            4 * this.resolution, "#e7eced", "#e7eced");
    
        this.lineRounded(
            (this.middle / 2.5 - this.vs_line_width / 4 + 9 * this.resolution),
            this.border * this.resolution,
            this.progressionAnimation(this.prct, (this.middle / 2.5 - this.vs_line_width / 4 + 9 * this.resolution), (this.middle / 2.5 + this.vs_line_width * 1.75)),
            this.border * this.resolution,
            4 * this.resolution, "#e7eced", "#e7eced");
    
        // Draw lines for the right side
        this.lineRounded(
            this.progressionAnimation(this.prct, (this.cwidth - this.middle / 2.5), (this.cwidth - this.middle / 2.5 - this.vs_side_line_width / 1.5)),
            (this.height - this.border) * this.resolution,
            this.progressionAnimation(this.prct, (this.cwidth - this.middle / 2.5), (this.cwidth - this.middle / 2.5 + this.vs_side_line_width / 1.5)),
            (this.height - this.border) * this.resolution,
            4 * this.resolution, "#e7eced", "#e7eced");
    
        this.lineRounded(
            (this.cwidth - this.middle / 2.5 - this.vs_line_width / 4 + 9 * this.resolution),
            this.progressionAnimation(this.prct, this.border * this.resolution, (this.height - this.border) * this.resolution),
            (this.cwidth - this.middle / 2.5 - this.vs_line_width / 4 + 9 * this.resolution),
            this.border * this.resolution,
            4 * this.resolution, "#e7eced", "#e7eced");
    
        this.lineRounded(
            (this.cwidth - this.middle / 2.5 - this.vs_line_width / 4 + 9 * this.resolution),
            this.border * this.resolution,
            this.progressionAnimation(this.prct, (this.cwidth - this.middle / 2.5 - this.vs_line_width / 4 + 9 * this.resolution), (this.cwidth - this.middle / 2.5 - this.vs_line_width * 1.75)),
            this.border * this.resolution,
            4 * this.resolution, "#e7eced", "#e7eced");
    }
    
    tournamentArrayAnimation() {
        this.tournamentArray();
        if (this.prct < 100) {
            this.prct += 2;
            window.requestAnimationFrame(() => this.tournamentArrayAnimation());
        }
    }
}