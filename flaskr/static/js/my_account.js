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

const send_email_conformation_mail = () =>{
	var ask = window.confirm("Your Email address is in verified with us. \r\nSend a confirmation mail to your registered email address.");
    if (ask) {
        window.location.href = "/my_account/send_mail";
    }
}