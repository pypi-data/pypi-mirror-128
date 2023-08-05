/* ****************************************************************************
 * Listens for a change of selected project and gets
 * all categories of it.
 *
 * @author Francisco Sanz  (frasanz@bifi.es)
 * ***************************************************************************/

$(function() {
    'use strict';
    var projectOriginSelect = $('select[name=project_origin]');
    var categorySelect = $('#category_origin');
    var projectId, categoryId;

    projectOriginSelect.on('change', function() {
        projectId = $(this).val();

        categorySelect.find('option').each(function() {
            if ($(this).val() !== '') {
                $(this).remove();
            }
        });

        if (projectId) {
            $.get('/admin/duplicate_categories/projects/' + projectId + '/categories/', function(categories) {
                if (categories) {
                    for (var key in categories) {
                        if (categories.hasOwnProperty(key)) {
                            categorySelect.append($('<option value="' + key + '">' + categories[key] + '</option>'));
                        }
                    }
                }
            });
        }
    });
	 
	 $('#download_format').on('change', function(){
					 $('#options_for_download_xlsx').hide();
 					 if ($(this).val() == 'xlsx')
					 		$('#options_for_download_xlsx').show();



	 });
	$("#log_tab").click(function(){
		$('#which_log').trigger('change');
	});
	$("#which_log").change(function(){
		if (this.value == 'Categories'){
			var url_dest = '/admin/duplicate/getallcategoryduplications/'
			$.ajax({
				type: 'GET',
				url : url_dest
			}).done(function(data){
				$('#tb_log').html(
					"<thread>"+
					"<tr>"+
					"<th scope='col'>#</th>"+
					"<th scope='col'>When</th>"+
      					"<th scope='col'>Category Source</th>"+
      					"<th scope='col'>Category Destination</th>"+
					"<th scope='col'>Done by</th>"+
    					"</tr>"+
    					"<tbody>");
				$.each(JSON.parse(data.category_duplications), function(i,category){
					$("#tb_log").append(
					"<tr>"+
					"<th>"+category.pk+"</th>"+
					"<td>"+(category.fields.created_at).replace(/T/," at ").slice(0,-5)+"</td>"+
					"<td>"+category.fields.category_source+"</td>"+
					"<td>"+category.fields.category_destination+"</td>"+
					"<td>"+category.fields.creator+"</td>"+
					"</tr>");
				});
				$('#tb_log').append('</tbody></thread>');
			});
		}else{
			$.ajax({
				type: 'GET',
				url : '/admin/duplicate/getallprojectduplications/'
			}).done(function(data){
				$('#tb_log').html(
					"<thread>"+
					"<tr>"+
					"<th scope='col'>#</th>"+
					"<th scope='col'>When</th>"+
      					"<th scope='col'>Project Source</th>"+
      					"<th scope='col'>Project Destination</th>"+
					"<th scope='col'>Done by</th>"+
    					"</tr>"+
    					"<tbody>");
				$.each(JSON.parse(data.project_duplications), function(i,project){
					$('#tb_log').append(
					"<tr>"+
					"<th>"+project.pk+"</th>"+
					"<td>"+(project.fields.created_at).replace(/T/," at ").slice(0,-5)+"</td>"+
					"<td>"+project.fields.project_source+"</td>"+
					"<td>"+project.fields.project_destination+"</td>"+
					"<td>"+project.fields.creator+"</td>"+
					"</tr>");
				});
				$('#tb_log').append('</tbody></thread>');
			});

		}
	});

$("#form_project").submit(function (event) {
    $("button").attr('disabled','disabled');

    $("#statusproject").attr('class','alert alert-warning')
    $("#statusproject").html("<span class='sr-only'>Loading...</span>We are duplicating a project for you, plase wait")

    event.preventDefault();
    var formData = {
      csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
      pproject_origin: $("#pproject_origin").val(),
      pproject_destination_name: $("#pproject_destination_name").val(),
    };
    $.ajax({
      type: 'POST',
      url: '/admin/duplicate_project/',
      data: formData,
    }).done(function (data) {
      const obj = JSON.parse(data['project'])
      $("button").removeAttr('disabled');
      $("#statusproject").attr('class','alert alert-success')
      $("#statusproject").html("The project <b>"+$('#pproject_origin').find('option:selected').text()+"</b> has been duplicated into <a href='/admin/projects/"+obj[0]['pk']+"/'>"+obj[0]['fields']['name']+"</a>")
      $("#pproject_origin").append("<option value='"+obj[0]['pk']+"' selected>"+obj[0]['fields']['name']+"</option>")
      // Re-sort 
      var options = $("#pproject_origin option");                    // Collect options         
      options.detach().sort(function(a,b) {               // Detach from select, then Sort
        var at = $(a).text();
        var bt = $(b).text();         
        return (at > bt)?1:((at < bt)?-1:0);            // Tell the sort function how to order
      });
      options.appendTo("#pproject_origin"); 
         }).fail(function (jqXHR, textStatus){
   }).error(function(xhr){
	const obj = JSON.parse(xhr.responseText)
	$("button").removeAttr('disabled')
   	$("#statusproject").attr('class','alert alert-danger')
	$("#statusproject").html("Unable to duplicate project. The reason is<b>: "+obj['error']+"</b>")

   });
  });

$("#form_category").submit(function (event) {
    $("button").attr('disabled','disabled');

    $("#statuscategory").attr('class','alert alert-warning')
    $("#statuscategory").html("We are duplicating a category for you, plase wait")


    event.preventDefault();
    var formData = {
      csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
      project_origin: $("#project_origin").val(),
      project_destination: $("#project_destination").val(),
      category_origin: $("#category_origin").val(),
      destcategoryname: $("#destcategoryname").val(),
    };

    $.ajax({
      type: 'POST',
      url: '/admin/duplicate_category/',
      data: formData,
    }).done(function (data) {
      $("button").removeAttr('disabled');
      $("#statuscategory").html("A new category has been created")
  	  $("#statuscategory").attr('class','alert alert-success')
	    $("#project_origin").change()
    }).fail(function (jqXHR, textStatus){
   }).error(function(xhr){
        const obj = JSON.parse(xhr.responseText)
        $("button").removeAttr('disabled')
        $("#statuscategory").attr('class','alert alert-danger')
        $("#statuscategory").html("Unable to duplicate category. The reason is<b>: "+obj['error']+"</b>")

   });;
  });

    $("#form_observations").submit(function (event) {

	event.preventDefault(); 

	let data = 'project_id='+$("#project_name_download").val()+'&format='+$("#download_format").val();

	/* Check if we want to include media or comments */
	if ($('#comments_json').is(':checked'))
	    data += "&comments_json=true"
	if ($('#media_json').is(':checked'))
	    data += "&media_json=true"
	if ($('#comments_xlsx').is(':checked'))
	    data += "&comments_xlsx=true"
	if ($('#media_xlsx').is(':checked'))
	    data += "&media_xlsx=true"
	$("button").attr('disabled','disabled');	
	
	$("#statusdownload").attr('class','alert alert-warning')
        $("#statusdownload").html("We are preparing the data for you. It might take several minutes for big projects, plase wait.")	
	    
	var req = new XMLHttpRequest();
	var csrftoken = $("[name='csrfmiddlewaretoken']").val() 
	var url_dest = "/admin/duplicate/getallproject/";
	if ($("#download_format").val() == 'xlsx')
		url_dest="/admin/duplicate/getallprojectxlsx/"
	req.open("POST", url_dest, true);
	req.setRequestHeader('X-CSRFToken', csrftoken)
	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
	if ($("#download_format").val() == 'xlsx')
		req.responseType = "blob";
	else
		req.responseType = "json";

	req.onload = function (event) {
		if(req.status == 200){
			if ($("#download_format").val() == 'xlsx')
				var blob = req.response;
			else
				var blob = new Blob([req.response])
			var url =  URL.createObjectURL(blob);
			var a = document.createElement('a');
			a.href = url;
			a.download = $( "#project_name_download option:selected" ).text()+'-'+new Date().toISOString().split('T')[0]+"."+$( "#download_format option:selected" ).text();
			a.click()
			URL.revokeObjectURL(url);
			$("button").removeAttr('disabled')
			$("#statusdownload").attr('class','alert alert-success')
			$("#statusdownload").html("Done!")	
		}
		else{
			$("button").removeAttr('disabled')
			$("#statusdownload").attr('class','alert alert-danger')
			$("#statusdownload").html("Error "+req.status+": Maybe you do not have access to the project")

		}
	
	}
	req.send(data);
	});
});
