var startResults = 5;
var numResults = startResults;
var incResults = 5;

var selected_loc_filters = []
var selected_uni_filters = []
var selected_dept_filters = []
var searchTerm = ''



var docDiv = (doc) => {
    const name = doc[0];
    const prev = doc[1];
    const email = doc[6];
    const uni_dept = doc[3]
    const fac_name = doc[0]
    const fac_url = doc[1]
    const loc = doc[8]
    //More Features
    const expertise = doc[9]
    const dept_url = doc[2]
    const univ_url = doc[4]
    const univ_name = doc[5]
    const fac_phone = doc[7]


    if (email =='None') {
        return (
             `<div class="card">
             <div class="card-header">
       <div style="display: flex;">

        
                 <b style="font-size:14pt">${fac_name}</b>
                 <a style="margin-left:auto;color:black;" href=${fac_url} target="_blank"><i class="material-icons">launch</i></a>
                 </div>
            <div>
                    University - ${univ_name}
                </div>
            <div class="header-item">
            <div class="tag">
            <i class='fas fa-university' ></i>
                  ${uni_dept}
            </div>                
                <div class="tag">
                  <i class="material-icons">location_on</i>
                   ${loc}
                 </div>
                 <div>
                    Phone - ${fac_phone}
                </div>
            </div>            
            </div>
           

              <div class="card-body">
                <span id='docPrev-${name}'><b>Department URL 
                    <a style="margin-left:auto;color:black;" href=${dept_url} target="_blank"><i class="material-icons">launch</i></a>
                </b></span>
                <br>
                <span id='docPrev-${name}'><b>University URL
                    <a style="margin-left:auto;color:black;" href=${univ_url} target="_blank"><i class="material-icons">launch</i></a>
                </b></span>
                <br>
                <span id='docPrev-${name}'><b>Expertise : - </b>${expertise}</span>
                <br>
            </div>
            </div>`
        );
    } else {
        return (
            `<div class="card">
             <div class="card-header">
       <div style="display: flex;">

        
                 <b style="font-size:14pt">${fac_name}</b>
                 <a style="margin-left:auto;color:black;margin-right:20px;" href='mailto:${email}' "><i class="material-icons">email</i></a>
                 <a style="color:black;" href=${fac_url} target="_blank"><i class="material-icons">launch</i></a>
                 </div>
            <div>
                    University - ${univ_name}
                </div>
            <div class="header-item">
            <div class="tag">
            <i class='fas fa-university' ></i>
                  ${uni_dept}
            </div>
                <div class="tag">
                  <i class="material-icons">location_on</i>
                   ${loc}
                 </div>
                 <div>
                    Phone - ${fac_phone}
                </div>
            </div>            
            </div>
         

              <div class="card-body">
                <span id='docPrev-${name}'><b>Department URL 
                    <a style="margin-left:auto;color:black;" href=${dept_url} target="_blank"><i class="material-icons">launch</i></a>
                </b></span>
                <br>
                <span id='docPrev-${name}'><b>University URL
                    <a style="margin-left:auto;color:black;" href=${univ_url} target="_blank"><i class="material-icons">launch</i></a>
                </b></span>
                <br>
                <span id='docPrev-${name}'><b>Expertise : - </b>${expertise}</span>
                <br>                
            </div>
            </div>`
        );
    }
}

var doSearch = function() {
    const data = {
        "query": searchTerm,
        "num_results": numResults,
        "selected_loc_filters" : selected_loc_filters,
        "selected_uni_filters": selected_uni_filters,
        "selected_dept_filters": selected_dept_filters
    }
    if (searchTerm!='')
    {
    var num_fetched_res = 0
    fetch("http://localhost:8095/search", {
    // fetch("http://expertsearch.centralus.cloudapp.azure.com/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    }).then(response => {
        response.json().then(data => {
            const docs = data.docs;
            $("#docs-div").empty();

            docs.forEach(doc => {
            
                $("#docs-div").append(
                    docDiv(doc)
                );
                    num_fetched_res = num_fetched_res+1;

            });
          
            if (num_fetched_res==numResults){

            $("#loadMoreButton").css("display", "block")
        }
        else{
            $("#loadMoreButton").css("display", "none")
        }
        if (num_fetched_res==0){
            $("#docs-div").append(`<h3 style="text-align: center;margin-top:20px;">No Search Results Found</h3>`);
        }
        })

    });
}
}

$(window).on("resize",function() {
    $(document.body).css("margin-top", $(".navbar").height()+5 );
    var width = $(".select2-container").width()
    if ((width == 0)||width===undefined){
        width = 300
    }
    $(".select2-search__field").css('cssText', $(".select2-search__field").attr('style')+'width: ' + width+ 'px !IMPORTANT;');
}
).resize();


$(document).ready(function() {
    $('#loc_filter').select2({placeholder: "e.g. United States, California"});
    $('#uni_filter').select2({placeholder: "e.g. University of Illinois Urbana-Champaign"});
    $('#dept_filter').select2({placeholder: "e.g. Computer Science"});
    $(window).trigger('resize');
});

window.onload=function(){
    console.log("Hello")
    for (var i=0;i<unis.length;i++){
         var newOption = new Option(unis[i], i, false, false);
        // Append it to the select
        $('#uni_filter').append(newOption).trigger('change');
       

    }
    selected_uni_filters = unis.slice()
    for (var i=0;i<locs.length;i++){
         var newOption = new Option(locs[i], i, false, false);
        // Append it to the select
        $('#loc_filter').append(newOption).trigger('change');
    }
    selected_loc_filters = locs.slice()

    selected_dept_filters = depts.slice()
    for (var i=0;i<depts.length;i++){
         var newOption = new Option(depts[i], i, false, false);
        // Append it to the select
        $('#dept_filter').append(newOption).trigger('change');
    }
    selected_dept_filters = depts.slice()

    $(window).trigger('resize');
 
};

function  toggleFilter() {
  filters_div = document.getElementById("search-filters")
  filters_div.style.display = filters_div.style.display=== 'none' ? 'flex' : 'none';
}

$("#submitButton").click(function() {
    numResults = startResults;
    searchTerm = $('#query').val()
    doSearch();
});

$("#filterButton").click(function() {
    toggleFilter();
});

$('#query').keydown(function(e) {
    searchTerm = $('#query').val()
    if (e.keyCode == 13) {
        numResults = startResults;
    
    doSearch();
    }
});

$("#applyFilters").click(function() {
  
    var selected_uni_data = $("#uni_filter").select2("data");
    selected_uni_filters = []
    selected_uni_data.forEach(s => {
            selected_uni_filters.push(s['text']);

});
      
    if (selected_uni_filters.length== 0){
        selected_uni_filters = unis.slice()
    }

    var selected_loc_data = $("#loc_filter").select2("data");
    selected_loc_filters = []
    selected_loc_data.forEach(s => {
            selected_loc_filters.push(s['text']);

});

    if (selected_loc_filters.length == 0){
        selected_loc_filters = locs.slice()
    }

    var selected_dept_data = $("#dept_filter").select2("data");
    selected_dept_filters = []
    selected_dept_data.forEach(s => {
            selected_dept_filters.push(s['text']);

});

    if (selected_dept_filters.length == 0){
        selected_dept_filters = depts.slice()
    }

  filters_div = document.getElementById("search-filters")
  filters_div.style.display = 'none'
        doSearch();
    });

$("#settingsButton").click(function() {
   window.location = "http://localhost:8095/admin"
});

$("#loadMoreButton").click(function() {
    numResults += incResults

    doSearch();
});