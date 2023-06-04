
    import Swal from 'sweetalert2';
    import { useToast } from 'vue-toastification';

    export const toast = useToast();

    export const BOOTBOX = {
        
        confirm: (text:string, func:string, params:any[]) => {
            const swalWithBootstrapButtons = Swal.mixin({
                customClass: {
                    confirmButton: 'btn btn-success',
                    cancelButton: 'btn btn-danger'
                },
                buttonsStyling: false
            })
    
            swalWithBootstrapButtons.fire({
                title: 'Are you sure?',
                text: text,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'CONFIRM',
                cancelButtonText: 'CANCEL',
                reverseButtons: true
            })
            .then((result:any) => {
                if (result.isConfirmed) {
                    if (typeof func == 'string') {
                        // @ts-ignore
                        window[func](...[params]);
                    }
                }
            });
        }
    };

    function remove_disabled() {
        setTimeout(()=>{
            $('form input, form select').removeAttr('disabled');
        }, 4000);
    }

    export const confirmed = (message:string) => {
        toast.success(message, {
            timeout:4000
        });
        remove_disabled();
    }

    export const failed = (message:string) => {
        toast.error(message, {
            timeout:4000
        });
        remove_disabled();
    }

    export default BOOTBOX;