from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from PIL import Image
import numpy as np
import os
import cv2
from tensorflow.keras.models import load_model
from django.conf import settings
from django.contrib.auth.models import User

# Load the BiRNN and CNN models
birnn_model_path = os.path.join(settings.BASE_DIR, 'models/bi_rnn_signature_verification_model.h5')
cnn_model_path = os.path.join(settings.BASE_DIR, 'models/cnn_signature_verification_model.keras')

birnn_model = load_model(birnn_model_path)
cnn_model = load_model(cnn_model_path)

# Preprocess image function for BiRNN
def preprocess_image_birnn(image, img_size=(128, 128), patch_size=(128, 128)):
    print("Started preprocessing for BiRNN")  # Debugging statement
    image = image.convert('L')
    image = np.array(image)
    image = cv2.resize(image, img_size)

    patches = []
    for i in range(0, image.shape[0], patch_size[0]):
        for j in range(0, image.shape[1], patch_size[1]):
            patch = image[i:i+patch_size[0], j:j+patch_size[1]].flatten()
            patches.append(patch)

    patches = np.array(patches)
    patches = np.expand_dims(patches, axis=0)
    print("Finished preprocessing for BiRNN")  # Debugging statement
    return patches

# Preprocess image function for CNN
def preprocess_image_cnn(image, img_size=(128, 128)):
    print("Started preprocessing for CNN")  # Debugging statement
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = np.array(image)
    image = cv2.resize(image, img_size)
    image = image / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)
    print("Finished preprocessing for CNN")  # Debugging statement
    return image

# Interpret model prediction
def interpret_prediction(prediction):
    predicted_class = "Real" if prediction[0] > 0.5 else "Forged"
    confidence = prediction[0] if predicted_class == "Real" else 1 - prediction[0]
    return predicted_class, confidence

# Predict signature (for handling AJAX requests)
@csrf_exempt  # CSRF exemption is okay here for testing, but ideally remove this in production
def predict_signature(request):
    if request.method == 'POST' and request.FILES.get('image'):
        response_data = {}
        try:
            uploaded_image = request.FILES['image']
            signature_source = request.POST.get('source')  # Capture the source field
            image = Image.open(uploaded_image)

            # Process and predict with BiRNN
            try:
                processed_image_birnn = preprocess_image_birnn(image)
                birnn_prediction = birnn_model.predict(processed_image_birnn)[0]
                birnn_result, birnn_accuracy = interpret_prediction(birnn_prediction)
                response_data['birnn'] = {'result': birnn_result, 'accuracy': f"{birnn_accuracy:.2%}"}
            except Exception as birnn_error:
                response_data['birnn'] = {'error': 'BiRNN model failed'}

            # Process and predict with CNN
            try:
                processed_image_cnn = preprocess_image_cnn(image)
                cnn_prediction = cnn_model.predict(processed_image_cnn)[0]
                cnn_result, cnn_accuracy = interpret_prediction(cnn_prediction)
                response_data['cnn'] = {'result': cnn_result, 'accuracy': f"{cnn_accuracy:.2%}"}
            except Exception as cnn_error:
                response_data['cnn'] = {'error': 'CNN model failed'}

            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': 'Error processing the image'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# Index page (Login page)
def index(request):
    return render(request, 'index.html')

# Logout view
def logout_view(request):
    logout(request)  # Logs the user out
    return redirect('index')  # Redirect to the index or login page after logout

import re
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# User registration view
def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate inputs
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration.html')

        if not validate_password(password):
            messages.error(request, ("Password must be 6-15 characters long, contain at least one uppercase letter, "
                                     "one lowercase letter, one digit, and one special character."))
            return render(request, 'registration.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return render(request, 'registration.html')

        # Create the user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('index')  # Redirect to login page
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return render(request, 'registration.html')

    return render(request, 'registration.html')


# User login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('upload')  # Redirect to the upload page
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'index.html')  # Stay on the login page

    return render(request, 'index.html')


# Password validation function
def validate_password(password):
    # Regex for password validation
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,15}$'
    return re.match(pattern, password)


# Upload page (requires user to be logged in)
@login_required
def upload_view(request):
    return render(request, 'upload.html')


# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from tensorflow.keras.models import load_model
# from PIL import Image
# import numpy as np
# import os
# from django.conf import settings

# # Define the model file paths
# birnn_model_path = os.path.join(settings.BASE_DIR, 'models/bi_rnn_signature_verification_model.h5')
# cnn_model_path = os.path.join(settings.BASE_DIR, 'models/cnn_signature_verification_model.keras')
# lstm_model_path = os.path.join(settings.BASE_DIR, 'models/my_model.h5')

# # Check if the model files exist before loading
# print(f"BiRNN model path exists: {os.path.exists(birnn_model_path)}")
# print(f"CNN model path exists: {os.path.exists(cnn_model_path)}")
# print(f"LSTM model path exists: {os.path.exists(lstm_model_path)}")

# # Load models from specified files
# birnn_model = load_model(birnn_model_path)
# cnn_model = load_model(cnn_model_path)
# lstm_model = load_model(lstm_model_path)

# # Preprocess image function
# def preprocess_image(image):
#     image = image.convert('L')
#     image = image.resize((128, 128))
#     image = np.array(image) / 255.0
#     image = np.expand_dims(image, axis=0)
#     image = np.expand_dims(image, axis=-1)
#     return image

# # Interpret prediction function
# def interpret_prediction(prediction):
#     predicted_class = "Real" if prediction[0] > 0.5 else "Forged"
#     confidence = prediction[0] if predicted_class == "Real" else 1 - prediction[0]
#     return predicted_class, confidence

# # Simple views
# def index(request):
#     return render(request, 'index.html')

# def registration(request):
#     return render(request, 'registration.html')

# def upload(request):
#     return render(request, 'upload.html')

# # Prediction API view
# @csrf_exempt
# def predict_signature(request):
#     if request.method == 'POST' and request.FILES.get('image'):
#         try:
#             uploaded_image = request.FILES['image']
#             image = Image.open(uploaded_image)
#             processed_image = preprocess_image(image)

#             print("Processing with BiRNN model...")
#             birnn_prediction = birnn_model.predict(processed_image)[0]
#             birnn_result, birnn_accuracy = interpret_prediction(birnn_prediction)

#             print("Processing with CNN model...")
#             cnn_prediction = cnn_model.predict(processed_image)[0]
#             cnn_result, cnn_accuracy = interpret_prediction(cnn_prediction)

#             print("Processing with LSTM model...")
#             lstm_prediction = lstm_model.predict(processed_image)[0]
#             lstm_result, lstm_accuracy = interpret_prediction(lstm_prediction)

#             response_data = {
#                 'birnn': {'result': birnn_result, 'accuracy': f"{birnn_accuracy:.2%}"},
#                 'cnn': {'result': cnn_result, 'accuracy': f"{cnn_accuracy:.2%}"},
#                 'lstm': {'result': lstm_result, 'accuracy': f"{lstm_accuracy:.2%}"},
#             }
#             return JsonResponse(response_data)

#         except Exception as e:
#             print("Error in prediction:", str(e))
#             return JsonResponse({'error': 'Error processing the image'}, status=500)

#     return JsonResponse({'error': 'Invalid request'}, status=400)