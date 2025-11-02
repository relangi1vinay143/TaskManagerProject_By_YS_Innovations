from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from TaskManagerApp.models import TaskModel
from TaskManagerApp.serializers import TaskSerializer

@csrf_exempt
def TaskManagerRequest(request, id=0):
    if request.method == 'GET':
        if id != 0:
            try:
                task = TaskModel.objects.get(id=id)
                serializer = TaskSerializer(task)
                return JsonResponse(serializer.data, safe=False)
            except TaskModel.DoesNotExist:
                return JsonResponse({'error': 'Task not found'}, status=404)
        else:
            tasks = TaskModel.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except Exception:
            return JsonResponse({'error': 'Invalid or empty JSON body'}, status=400)

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'success', 'message': 'Task added successfully'}, status=201)

        # Debug: show which fields are invalid
        print("POST serializer errors:", serializer.errors)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'PUT':
        try:
            data = JSONParser().parse(request)
        except Exception:
            return JsonResponse({'error': 'Invalid or empty JSON body'}, status=400)

        try:
            task = TaskModel.objects.get(id=id)
        except TaskModel.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)

        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'status': 'success', 'message': 'Task updated successfully'}, status=200)

        # Debug: show which fields are invalid
        print("PUT serializer errors:", serializer.errors)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        try:
            task = TaskModel.objects.get(id=id)
        except TaskModel.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)

        task.delete()
        return JsonResponse({'status': 'success', 'message': 'Task deleted successfully'}, status=200)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
