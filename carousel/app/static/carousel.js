var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
    showDivs(slideIndex += n);
}

function showDivs(n) {
    var i;
    var x = document.getElementsByClassName("slide");
    if (n > x.length) { slideIndex = 1 }//window.location = "/next" + window.location.search} 
    if (n < 1) {slideIndex = x.length} ;
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none"; 
    }
    x[slideIndex-1].style.display = "block"; 
}

function onPress(c) {
    if(c.key == "ArrowRight")
    {
        plusDivs(1);
    }
    else if(c.key == "ArrowLeft")
    {
        plusDivs(-1);
    }
    else if(c.key == "ArrowDown")
    {
		document.getElementById("cycleTime").value--;
    }
	else if(c.key == "ArrowUp")
    {
		document.getElementById("cycleTime").value++;
    }
	else if(c.key == " ")
	{
		document.getElementById("cycleCheck").checked = !document.getElementById("cycleCheck").checked;
		cycle();
	}
}

function cycle() {
	if(document.getElementById("cycleCheck").checked === true){
		var time = document.getElementById("cycleTime").value;
      	t = setTimeout(cycle_loop(true), time*1000);
    } else {
		cycle_loop(false);
    } 
}

function cycle_loop(start) {
	var t;
	if(start){
		var time = document.getElementById("cycleTime").value;
		clearTimeout(t);
		plusDivs(1);
      	t = setTimeout(cycle,time*1000);
	}
	else {
		clearTimeout(t);
	}
}
