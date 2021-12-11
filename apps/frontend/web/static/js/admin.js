
$(document).ready(function() {

$("#crawl_uni").click(function() {
    debugger;
    $("#spinner2").addClass("show-spinner");
    if ($("#searchText").val() === ''){
       $("#spinner2").removeClass("show-spinner");
        $("#backdrop").modal("show");
        $("#modalBody").text("Please enter a search string");
        $("#backdrop").appendTo("body");
    }
    else{
        const data = {
            "searchText" : $("#searchText").val()
        }
        debugger;
        fetch("/admin/crawl", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        }).then(response => {
            response.json().then(data => {
                $("#spinner2").removeClass("show-spinner");
                $("#backdrop").modal("show");
                $("#modalBody").text(data["msg"])
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



