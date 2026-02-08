/* ;(function($){
    $(function(){
        var $form = $('form');
        if ($form.length === 0) return;

        // Ensure there's a place to show messages
        var $alerts = $('.register-alerts');
        if ($alerts.length === 0) {
            $alerts = $('<div class="register-alerts mb-3"></div>');
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
            var nombre = $.trim($form.find('#nombre').val() || '');
            var email = $.trim($form.find('#email').val() || '');
            var pass = $.trim($form.find('#contraseña').val() || '');
            if (!nombre){ showAlert('Por favor ingrese su nombre.'); $form.find('#nombre').focus(); return false; }
            if (!email){ showAlert('Por favor ingrese su correo electrónico.'); $form.find('#email').focus(); return false; }
            var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!re.test(email)){ showAlert('Por favor ingrese un correo válido.'); $form.find('#email').focus(); return false; }
            if (!pass){ showAlert('Por favor ingrese su contraseña.'); $form.find('#contraseña').focus(); return false; }
            if (pass.length < 6){ showAlert('La contraseña debe tener al menos 6 caracteres.'); $form.find('#contraseña').focus(); return false; }
            return true;
        }

        $form.on('submit', function(e){
            e.preventDefault();
            if (!validate()) return;

            var action = $form.attr('action') || window.location.href;
            var data = $form.serialize();

            $submit.prop('disabled', true).addClass('disabled');

            $.ajax({
                url: action,
                method: 'POST',
                data: data,
                dataType: 'json',
                success: function(resp){
                    if (resp && resp.success){
                        if (resp.redirect){ window.location.href = resp.redirect; }
                        else { window.location.href = '/signin/'; }
                    } else {
                        var msg = 'No se pudo completar el registro.';
                        if (resp && resp.errors){ msg = resp.errors; }
                        showAlert(msg, 'danger');
                        $submit.prop('disabled', false).removeClass('disabled');
                    }
                },
                error: function(xhr, status, err){
                    // Fallback: si llega HTML, submit tradicional
                    if (xhr && xhr.status === 200 && xhr.responseText && xhr.responseText.indexOf('<!DOCTYPE') === 0){
                        $form.off('submit');
                        $form.submit();
                        return;
                    }
                    showAlert('Ocurrió un error al intentar registrarse. Intente nuevamente.');
                    $submit.prop('disabled', false).removeClass('disabled');
                }
            });
        });

        // Optional: toggle password visibility
        $(document).on('click', '.toggle-password', function(){
            var $t = $(this);
            var $input = $form.find('.pass-input, #contraseña');
            if ($input.attr('type') === 'password') { $input.attr('type', 'text'); $t.removeClass('fa-eye-slash').addClass('fa-eye'); }
            else { $input.attr('type', 'password'); $t.removeClass('fa-eye').addClass('fa-eye-slash'); }
        });

    });
})(jQuery);
 */