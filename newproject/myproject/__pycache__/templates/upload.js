// Function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to handle the image prediction
async function predictImage() {
    const imageInput = document.getElementById('imageUpload'); // Make sure ID matches
    // Retrieve result elements
    const birnnAccuracy = document.getElementById('birnn-accuracy');
    const birnnStatus = document.getElementById('birnn-status');
    const lstmAccuracy = document.getElementById('lstm-accuracy');
    const lstmStatus = document.getElementById('lstm-status');
    const cnnAccuracy = document.getElementById('cnn-accuracy');
    const cnnStatus = document.getElementById('cnn-status');

    // Check if an image file is selected
    if (imageInput.files.length === 0) {
        alert("Please select an image to upload.");
        return;
    }

    const file = imageInput.files[0];
    const formData = new FormData();
    formData.append('image', file); // Make sure this key matches what your Django view expects

    try {
        const response = await fetch('/predict/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // Include CSRF token in request
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Display the results
        birnnAccuracy.innerText = data.birnn.accuracy;
        birnnStatus.innerText = data.birnn.result;
        lstmAccuracy.innerText = data.lstm.accuracy;
        lstmStatus.innerText = data.lstm.result;
        cnnAccuracy.innerText = data.cnn.accuracy;
        cnnStatus.innerText = data.cnn.result;
    } catch (error) {
        console.error("Error predicting image:", error);
        alert("There was an error processing your request. Please try again.");
    }
}