/* ;(function($){
    $(function(){
        var $form = $('form');
        if ($form.length === 0) return;

        // Ensure there's a place to show messages
        var $alerts = $('.login-alerts');
        if ($alerts.length === 0) {
            $alerts = $('<div class="login-alerts mb-3"></div>');
            $form.before($alerts);
        }

        var $submit = $form.find('button[type="submit"]');

        function showAlert(message, type){
            var cls = 'alert-' + (type || 'danger');
            var $a = $('<div class="alert ' + cls + '" role="alert"></div>').text(message);
            $alerts.empty().append($a);
        }

        function clearAlerts(){ $alerts.empty(); }

        function validate(){
            clearAlerts();
            var email = $.trim($form.find('#email').val() || '');
            var pass = $.trim($form.find('input[type="password"]').val() || '');
            if (!email){ showAlert('Por favor ingrese su correo electrónico.'); $form.find('#email').focus(); return false; }
            // simple email regex
            var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!re.test(email)){ showAlert('Por favor ingrese un correo válido.'); $form.find('#email').focus(); return false; }
            if (!pass){ showAlert('Por favor ingrese su contraseña.'); $form.find('input[type="password"]').focus(); return false; }
            return true;
        }

        $form.on('submit', function(e){
            e.preventDefault();
            if (!validate()) return;

            var action = $form.attr('action') || window.location.href;
            var data = $form.serialize();

            // Disable submit
            $submit.prop('disabled', true).addClass('disabled');

            $.ajax({
                url: action,
                method: 'POST',
                data: data,
                dataType: 'json',
                success: function(resp){
                    // Expecting JSON like { success: true, redirect: '/path' } or { success: false, errors: 'msg' }
                    if (resp && resp.success){
                        // redirect if provided, otherwise reload
                        if (resp.redirect){ window.location.href = resp.redirect; }
                        else { window.location.reload(); }
                    } else {
                        var msg = 'Credenciales incorrectas. Por favor intente de nuevo.';
                        if (resp && resp.errors){ msg = resp.errors; }
                        showAlert(msg, 'danger');
                        $submit.prop('disabled', false).removeClass('disabled');
                    }
                },
                error: function(xhr, status, err){
                    // Si el servidor responde con HTML (redirect), hacemos el submit tradicional
                    if (xhr && xhr.status === 200 && xhr.responseText && xhr.responseText.indexOf('<!DOCTYPE') === 0){
                        // Fallback: submit the form normally
                        $form.off('submit');
                        $form.submit();
                        return;
                    }
                    // Mostrar mensaje genérico
                    showAlert('Ocurrió un error al intentar iniciar sesión. Intente nuevamente.');
                    $submit.prop('disabled', false).removeClass('disabled');
                }
            });
        });

        // Optional: toggle password visibility (if the template uses .toggle-password)
        $(document).on('click', '.toggle-password', function(){
            var $t = $(this);
            var $input = $form.find('.pass-input');
            if ($input.attr('type') === 'password') { $input.attr('type', 'text'); $t.removeClass('fa-eye-slash').addClass('fa-eye'); }
            else { $input.attr('type', 'password'); $t.removeClass('fa-eye').addClass('fa-eye-slash'); }
        });

    });
})(jQuery);
 */
    $(document).ready(function() {
        // Validación del formulario
        $('#login-form').on('submit', function(e) {
            var username = $('#id_username').val().trim();
            var password = $('#id_password').val().trim();
            
            if (!username) {
                e.preventDefault();
                alert('Por favor ingresa tu usuario');
                $('#id_username').focus();
                return false;
            }
            
            if (!password) {
                e.preventDefault();
                alert('Por favor ingresa tu contraseña');
                $('#id_password').focus();
                return false;
            }
        });
    });
    