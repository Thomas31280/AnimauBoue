//Show or hide new form for a reservation, with update of the "required" parameters of the fields concerned

function toggleForm(id){
    var form = document.getElementById(id);
    var dog_name = document.getElementById('name_'+id);
    var dog_arrival = document.getElementById('arrival_date_'+id);
    var dog_departure = document.getElementById('departure_date_'+id);
    var dog_commentaries = document.getElementById('commentaries_'+id);
    
    const html_elements = [dog_name, dog_arrival, dog_departure]
    
    if (form.style.display === "none") {
        form.style.display = "block";
        
        //Set required parameter at 'True' for all these elements
        for (const element of html_elements){
            element.required = true
        }
        
    } else {
        form.style.display = "none";
        //Set required parameter at 'False' for all these elements, and remove the fields content
        for (var element of html_elements){
            element.required = false
            element.value = null
        }
        
        dog_commentaries.value = null

    }
}


//When user has selected a client, the following forms are displayed

function toggleParkSelection(id, client_name){
    document.getElementById('client_id').value = id;
    document.getElementById('clientName').innerHTML = "Vous avez sélectionné le client : " + client_name;
    document.getElementById('selectedClient').style.display = "block";
}
