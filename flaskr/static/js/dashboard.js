document.getElementById("add_transsetion_up").addEventListener("click" , function(){
	document.getElementById("new_entry_form").style.display = "block";
});

document.getElementById("add_transsetion_down").addEventListener("click" , function(){
	document.getElementById("new_entry_form").style.display = "block";
});
document.getElementById("close_new_entry_form").addEventListener("click" , function(){
	document.getElementById("new_entry_form").style.display = "none";
});


const get_subtype = () => {
	type = document.getElementById('type')

	fetch('/get_subtype_of_type/'  + type.value)
	.then(function(responce){
		responce.json().then(function(data) {
			var sel = document.getElementById('sub_type');
			var length = sel.options.length;
			for (i = length-1; i >= 0; i--) {
			  sel.options[i] = null;
			}
			length = data.length
			
			for (i = 0;i<length;i++) {
				var opt = document.createElement('option');
				opt.appendChild( document.createTextNode(data[i].subtype) );
				opt.value = data[i].id;
				sel.appendChild(opt);
			}
		})
	});
};

document.getElementById('date_today').onchange = function() {
	document.getElementById('transaction_date').disabled  = this.checked;
};

document.getElementById('time_now').onchange = function() {
	document.getElementById('transaction_time').disabled  = this.checked;
};
const check_new_transaction = () =>{
	expence_name = document.getElementById("expence_name_first").value;
	amount = document.getElementById("amount_first").value;
	if(expence_name.length > 0 && amount.length >0) {
		sel = document.getElementById("c_d_first");
		c_d = sel.options[sel.selectedIndex].text;
		sel = document.getElementById("type");
		type = sel.options[sel.selectedIndex].text;
		sel = document.getElementById("sub_type");
		sub_type = sel.options[sel.selectedIndex].text;
		sel = document.getElementById("frequency");
		frequency = sel.options[sel.selectedIndex].text;
		sel = document.getElementById("sel1");
		payment_medium = sel.options[sel.selectedIndex].text;
		comment = document.getElementById("comment_first").value;
		if(document.getElementById("date_today").checked === true){
			
			date = "Current Date";
		}
		else{
			date = document.getElementById("transaction_date").value;
		}
		if(document.getElementById("time_now").checked === true){
			
			time = "Current Date";
		}
		else{
			time = document.getElementById("transaction_time").value;
		}
		





		document.getElementById("expence_name_con").innerHTML = expence_name;
		document.getElementById("date_con").innerHTML = date;
		document.getElementById("time_con").innerHTML = time;
		document.getElementById("c_d_con").innerHTML = c_d;
		document.getElementById("type_con").innerHTML = type;
		document.getElementById("sub_type_con").innerHTML = sub_type;
		document.getElementById("frequency_con").innerHTML = frequency;
		document.getElementById("pay_method_con").innerHTML = payment_medium;
		document.getElementById("amount_con").innerHTML = amount;
		document.getElementById("comment_con").innerHTML = comment;
		document.getElementById("entry_conformation").style.display = "block";
		document.getElementById("new_entry_form").style.display = "none";
	}
	else{
		alert("Please Fill All The Required Entry.");
	}
	
};

const go_back_to_edit = () => {
	document.getElementById("entry_conformation").style.display = "none";
	document.getElementById("new_entry_form").style.display = "block";
};

const load_more_table = () => {
	let table = document.getElementById("main_table")
	let date = table.lastElementChild.lastElementChild.children[2].innerHTML.replace(/-/g,"_");
	let time = table.lastElementChild.lastElementChild.children[3].innerHTML.replace(/:/g,"_");
	if(date.slice(0,8) === "<strong>"){
        date = date.replace("<strong>","")
        date = date.replace("</strong>","" )
        time = time.replace("<strong>", "")
        time = time.replace("</strong>", "")
    };
	let current_url = window.location.href.split("/");
	let year = current_url[current_url.length-1];
	let month = current_url[current_url.length-2];
	hit_url = ("/add_table/" + month + "/" + year + "/" + date + "/" +time);





	fetch(hit_url)
	.then(function(responce){
		responce.json().then(function(data) {
			if(data != false){
				for (i=0;i<data.length;i++){
					row = table.insertRow();
					row.setAttribute("id", data[i][data[i].length-1]);
					cell = row.insertCell();
					cell.innerHTML = ('<th><input type="checkbox" name="edit" id="check_'+ data[i][data[i].length-1] + '"></th>');
					for(j=0;j<data[i].length-1;j++){
						cell = row.insertCell();
						cell.innerHTML = ("<strong>"+data[i][j]+"</strong>");
					};
				}
			}
			else{
				alert("All Transactions For Selected Month Is Shown.");
			}
		})
	});

}
