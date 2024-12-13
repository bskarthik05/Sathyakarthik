function predictImage() {
    console.log("Predict button clicked!"); // Debug log
    // Get the form and the image file
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);

    // Perform the AJAX request to the backend
    fetch('/predict/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Prediction response received:", data); // Debug log
        // Handle the prediction result and update the UI
        const resultsDiv = document.getElementById('prediction-results');
        
        // Clear previous results if any
        resultsDiv.innerHTML = '';

        if (data.error) {
            resultsDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
        } else {
            let resultHTML = `<h2>Prediction Results:</h2><table>
                                <thead>
                                    <tr>
                                        <th>Model</th>
                                        <th>Label</th>
                                        <th>Confidence</th>
                                    </tr>
                                </thead>
                                <tbody>`;
            
            // Add prediction results for BiRNN and CNN models
            if (data.birnn) {
                resultHTML += `<tr>
                                    <td>BiRNN</td>
                                    <td>${data.birnn.result}</td>
                                    <td>${data.birnn.accuracy}</td>
                                </tr>`;
            }

            if (data.cnn) {
                resultHTML += `<tr>
                                    <td>CNN</td>
                                    <td>${data.cnn.result}</td>
                                    <td>${data.cnn.accuracy}</td>
                                </tr>`;
            }

            resultHTML += `</tbody></table>`;

            resultsDiv.innerHTML = resultHTML;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const resultsDiv = document.getElementById('prediction-results');
        resultsDiv.innerHTML = `<p style="color: red;">An error occurred. Please try again.</p>`;
    });
}