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
