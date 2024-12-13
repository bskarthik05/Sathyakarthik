function validateForm() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    // Sample valid credentials (replace with your actual validation logic)
    const validEmail = "user@example.com";
    const validPassword = "password";

    // Validate email and password
    if (email === "" || password === "") {
        alert("Email and password are required!");
        return false; // Prevent form submission
    } else if (password.length < 6) {
        alert("Password must be at least 6 characters long!");
        return false; // Prevent form submission
    }

    // Check for correct credentials
    if (email === validEmail && password === validPassword) {
        // Redirect to upload.html after successful login
        window.location.href = "upload.html";
        return false; // Prevent form submission
    }

    alert("Invalid credentials. Please try again.");
    return false; // Prevent form submission
}
