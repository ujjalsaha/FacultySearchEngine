
$(document).ready(function() {




$("#crawl_uni").click(function() {
    debugger;
    $("div.spanner").addClass("show");
    $('div.overlay').addClass("show");
    if ($("#searchText").val() === ''){
        $("div.spanner").removeClass("show");
        $("div.overlay").removeClass("show");
        $("#backdrop").modal("show");
        $("#modalBody").text("Please enter a search string");
        $("#backdrop").appendTo("body");
    }
    else{
        const data = {
            "searchText" : $("#searchText").val()
        }
        debugger;
        fetch("http://localhost:8095/admin/crawl", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        }).then(response => {
            response.json().then(data => {
                $("div.spanner").removeClass("show");
        $("div.overlay").removeClass("show");
                $("#backdrop").modal("show");
                $("#modalBody").text(JSON.stringify(data))
                $("#backdrop").appendTo("body");
        })
    });
    }


});

 $("#closeModal").click(function (){
      $("#backdrop").modal("hide");
 });
 $("#closeModalIcon").click(function (){
      $("#backdrop").modal("hide");
 });

});



