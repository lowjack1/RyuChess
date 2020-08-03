"use strict";

window.onload = init();

function init() {
    updateCountryDropdown();
}

function updateCountryDropdown() {
    let url = `/api/generic?action=country_record`;
    let html_opt = "";

    $.get(url, function(resp) {
        if(resp.status) {
            let data = resp.result.data;
            html_opt = `<option></option>`;
            $.each(data, function(_, data) {
                html_opt += `<option val="${data['id']}">${data['name']}</option>`;
            });
            $('select[name="country"]').html(html_opt);
            $('select[name="country"]').select2({
                'theme': 'bootstrap',
                placeholder: function(){
                    $(this).data('placeholder');
                }
            });
        }
    });
}