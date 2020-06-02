setTimeout(function(){

const button = document.getElementById("navbar-button")
button.setAttribute("data-toggle", "collapse");
button.setAttribute("data-target", "#navbarNav");
button.setAttribute("aria-controls", "navbarNav");
button.setAttribute("aria-expanded", "false");


button.setAttribute("aria-label", "Toggle navigation");
const toggle_button = document.getElementById("fig1_togel")
toggle_button.setAttribute("data-toggle", "buttons");


document.getElementById("graph1_1").style.display = "block";
document.getElementById("graph1_2").style.display = "none";


document.getElementById("graph1_btn1").addEventListener("click", function(){
	document.getElementById("graph1_1").style.display = "block";
	document.getElementById("graph1_2").style.display = "none";
});
document.getElementById("graph1_btn2").addEventListener("click", function(){
	document.getElementById("graph1_1").style.display = "none";
	document.getElementById("graph1_2").style.display = "block";
});







}, 3000);