Presentable Exceptions
======================

This is a module for django restframework, in which modules can specifiy exceptions in an
extra file with an key an description. At some place in the code, they can be fetched by 
the package and key and bubble up to the view. Here a mixin detects them and creates a 
proper response for an fat-client, which can show them then to to user - thus the exceptions
are presentable.

Getting started
---------------

Say, you have a module, like `auth_api` which is registered in `INSTALLED_APPS` in the Django
`settings.py`. Create a new file `auth_api/presentable_exceptions.py` with this content

```python
presentable_exceptions = {
    'client': [
        ('not-enough-data-to-delete-user', 'You did not provide enough data, that we can delete the user {username}')
    ],
    'server': [
        ('backend-connection-lost', 'We lost the connection to the backend'),
    ]
}
```

This file can be in every module and consists of two parts: The exceptions, that are the clients 
fault and the exceptions that are our fault. The first will cause a 4xx error, the latter a 5xx.

Say, you have now an View somewhere, like that:

```python
class MeView(WithPresentableException, APIView):

    def get(self, request):
        data = some_function_with_a_deep_call_stack()
        return Response(data)
```

This will call multiple function and somewhere there is the function `boom()` called:

```python
def boom():
    raise PresentableException.of('auth_api', 'backend-connection-lost')


def some_function_with_a_deep_call_stack():
    # ...
    boom()
    # ...
```

This `PresentableException` will be an `PresentableServerException` and bubble up into 
the Mixing `WithPresentableException` specified in the view above, which generates 
a proper response (with a 5xx code in this case).



