    import Swal from 'sweetalert2';
    import {useToast} from 'vue-toastification'
    import BOOTBOX from '../js/bootbox';
    import { confirmed, failed } from '../js/bootbox';

    export function confirm_submit(event:MouseEvent, message:string="") {
        let text:string = message==""?`Are you sure you want to submit this form?`:message;
        let func:string = "submit";
        let params:[] = [];

        $('form input, form select').attr('disabled','disabled');

        if (form_validated()) {
            BOOTBOX.confirm(text, func, params);
        } else {
            $('input, select').removeAttr('disabled');
            failed("Some form fields are invalid. Check the form and try again.");
        }

    }

    export function form_validated() {
        // @ts-ignore
        return document.querySelector('form').checkValidity();
    }

    export function clear() {
        $('form').trigger('reset');
    }
    
    export function close() {
        $("[data-dismiss=modal]").trigger("click");
    }

    export {BOOTBOX, confirmed, failed};