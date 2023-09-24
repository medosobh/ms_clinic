odoo.define('ms_hospital.clinic_tickets', function (require) {
    'use strict';
    console.log('js loaded');
    var FormController = require('web.FormController');

    var ExtendFormController = FormController.include({
        saveRecord: function (recordID) {
            var res = this._super.apply(this, arguments);
            console.log('saveRecord');
            this.do_notify('Success', 'Record Saved');
            return res;
        }
    });

});