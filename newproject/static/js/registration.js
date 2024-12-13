document.getElementById('registrationForm').addEventListener('submit', function(event) {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (!username || !email || !password || !confirmPassword) {
        event.preventDefault();
        alert("All fields are required.");
    } else if (password !== confirmPassword) {
        event.preventDefault();
        alert("Passwords do not match.");
    } else {
        alert("Registration form submitted! Replace this with backend logic.");
    }
});