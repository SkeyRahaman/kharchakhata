document.getElementById("dob_edit").addEventListener("click",function(){
	document.getElementById("dob_date").style.display = "block";
	document.getElementById("dob_cancel").style.display = "block";
	document.getElementById("dob_edit").style.display = "none";
});

document.getElementById("dob_cancel").addEventListener("click",function(){
	document.getElementById("dob_date").style.display = "none";
	document.getElementById("dob_cancel").style.display = "none";
	document.getElementById("dob_edit").style.display = "block";
});

document.getElementById("sex_edit").addEventListener("click",function(){
	document.getElementById("sex_edit_div").style.display = "block";
	document.getElementById("sex_edit").style.display = "none";
});

document.getElementById("sex_cancel").addEventListener("click",function(){
	document.getElementById("sex_edit_div").style.display = "none";
	document.getElementById("sex_edit").style.display = "block";
});

document.getElementById("reset_btn").addEventListener("click" , function(){
	window.location.reload();
});

// document.getElementById("save_btn").addEventListener("click" , function(){
// 	window.location.href = "/edit_profile";
// });