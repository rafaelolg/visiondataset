
function makeAutocomplete(sel) {
    sel.autocomplete('/autocomplete-users/', {
        delay: 200,
        formatItem: function(row) {
            return row[1];
        }
    });
}

$(function() {
    makeAutocomplete($('.autocomplete-me'));
})
