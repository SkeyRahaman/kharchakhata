const load_more_table = () => {
	let table = document.getElementById("main_table")
	let id = table.lastElementChild.lastElementChild.id;
	
	let current_url = window.location.href.split("/");
	let year = current_url[current_url.length-1];
	let month = current_url[current_url.length-2];
	hit_url = ("/add_table/" + month + "/" + year + "/" + id);




	fetch(hit_url)
	.then(function(responce){
		responce.json().then(function(data) {
			if(data != false){
				console.log(data);
				for (i=0;i<data.length;i++){
					row = table.insertRow();
					row.setAttribute("id", data[i]['id']);
					cell = row.insertCell();
					cell.innerHTML = ('<th><input type="checkbox" name="edit" id="check_'+ data[i][data[i].length-1] + '"></th>');
					cell = row.insertCell();
					cell.innerHTML = ("<strong>"+data[i]['name']+"</strong>");
					cell = row.insertCell();
					cell.innerHTML = ("<strong>"+data[i]['date']+"</strong>");
					cell = row.insertCell();
					cell.innerHTML = ("<strong>"+data[i]['time']+"</strong>");
					cell = row.insertCell();
					cell.innerHTML = ("<strong>"+data[i]['type']+"</strong>");
					cell = row.insertCell();
					cell.innerHTML = ("<strong>"+data[i]['subtype']+"</strong>");
					cell = row.insertCell();
					cell.innerHTML = ("<strong>"+data[i]['frequency']+"</strong>");

					if (data[i]['debit'] === 0) {
						cell = row.insertCell();
						cell.innerHTML = ("<strong>"+"</strong>");
					} else {
						cell = row.insertCell();
						cell.innerHTML = ("<strong>"+data[i]['debit']+"</strong>");
					}
					if (data[i]['credit'] === 0) {
						cell = row.insertCell();
						cell.innerHTML = ("<strong>"+"</strong>");
					} else {
						cell = row.insertCell();
						cell.innerHTML = ("<strong>"+data[i]['credit']+"</strong>");
					}
					
					cell = row.insertCell();
					cell.innerHTML = ("<strong>"+data[i]['payment_method']+"</strong>");
					cell = row.insertCell();
					cell.innerHTML = ("<strong>"+data[i]['comment']+"</strong>");
				}
			}
			else{
				alert("All Transactions For Selected Month Is Shown.");
			}
		})
	});

}
