$(document).ready(function() {
    $('#importForm').submit(function(event) {
    
        var $submitButton = $('#importBtn');
        var $spinner = $submitButton.siblings('.input-group-append').find('.spinner-border');

        // Show spinner and disable button
        $spinner.removeClass('d-none');
        //$submitButton.prop('disabled', true);
    });
});

$(document).ready(function() {
    $('#loadForm').submit(function(event) {
    
        var $submitButton = $('#openBtn');
        var $spinner = $submitButton.siblings('.input-group-append').find('.spinner-border');

        // Show spinner and disable button
        $spinner.removeClass('d-none');
        //$submitButton.prop('disabled', true);
    });
});

$(document).ready(function() {
    $('#generateForm').submit(function(event) {
    
        var $submitButton = $('#generateBtn');
        var $spinner = $submitButton.siblings('.input-group-append').find('.spinner-border');

        // Show spinner and disable button
        $spinner.removeClass('d-none');
        //$submitButton.prop('disabled', true);
    });
});