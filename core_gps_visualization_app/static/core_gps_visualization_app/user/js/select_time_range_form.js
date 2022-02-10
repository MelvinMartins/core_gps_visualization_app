
/**
 * on change of dropdown
 * Update selected time range
 */
var onTimeRangeChanged = function(event){
    document.getElementById("visualization").style.visibility = "hidden";
    showVisuLoadingSpinner();
    time_range_selected = $("#select-time-range-dropdown-form :selected").attr("value");
    console.log(time_range_selected);
    $.ajax({
        url : 'select-time-range-dropdown-form',
        type : "POST",
        data : {
            time_range_selected,
        },
        success: function(data){
            hideVisuLoadingSpinner();
            // Refresh plots after they were updated
            if (data.script === '404') {
                document.getElementById("charts404").style.visibility = "visible";
                document.getElementById('charts404').style.height = "200px";
                }
            else {
                $("#visualization").html(data.script);
                document.getElementById('charts404').style.height = "0px";
                }
            document.getElementById("visualization").style.visibility = "visible";
        },
        error: function(data){
            console.log("Error");
        }
    });
}

// .ready() called.
$(function() {
    // bind change event to dropdown box
    $("#select-time-range-dropdown-form").on("change", onTimeRangeChanged);
});