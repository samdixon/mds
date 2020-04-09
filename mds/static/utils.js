function saveFile(file) {
    $.ajax({
	type : "POST",
	url : '/mde/save',
	dataType: "json",
	data: JSON.stringify(file),
	contentType: 'application/json;charset=UTF-8',
	success: function (data) {
		console.log(data);
		}
	});
}