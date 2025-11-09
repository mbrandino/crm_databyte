from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Permitir acesso às rotas públicas
        if (
            path.startswith('/autenticacao/')
            or path.startswith('/static/')
            or path.startswith('/admin/')
        ):
            return self.get_response(request)

        # Exigir sessão para demais páginas
        if not request.session.get('matricula'):
            return redirect('autenticacao')

        return self.get_response(request)