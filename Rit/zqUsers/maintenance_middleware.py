# from django.http import HttpResponse
# from django.template import loader

# class MaintenanceMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if maintenance mode is enabled (e.g., using a settings flag)
#         if is_maintenance_mode_enabled():
            
#             context = {}
#             template = loader.get_template('zqUsers/maintenanceMessage.html')
#             response = HttpResponse(template.render(context), status=503)
#             response['Retry-After'] = '3600'  # Optionally, set a Retry-After header
#             return response
#             # # Display maintenance mode message
#             # response = HttpResponse("This site is currently undergoing maintenance. Please try again later.", status=503)
#             # response['Retry-After'] = '3600'  # Optionally, set a Retry-After header
#             # return response

#         # Continue with the request as usual
#         return self.get_response(request)

# def is_maintenance_mode_enabled():
#     # Implement your logic to determine if maintenance mode is enabled
#     # For example, you can check a setting in your Django settings file
#     return False  # Change this to return True or False based on your logic
