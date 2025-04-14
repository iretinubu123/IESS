document.addEventListener('DOMContentLoaded', function () {
    const signupTab = document.getElementById('signupTab');
    const loginTab = document.getElementById('loginTab');
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');

    // Ensure elements exist before adding event listeners
    if (signupTab && loginTab && signupForm && loginForm) {
        // Tab Switching
        signupTab.addEventListener('click', () => {
            signupTab.classList.add('border-primary', 'text-primary');
            loginTab.classList.remove('border-primary', 'text-primary');
            signupForm.classList.remove('hidden');
            loginForm.classList.add('hidden');
        });

        loginTab.addEventListener('click', () => {
            loginTab.classList.add('border-primary', 'text-primary');
            signupTab.classList.remove('border-primary', 'text-primary');
            loginForm.classList.remove('hidden');
            signupForm.classList.add('hidden');
        });
    }

    // Toggle Password Visibility
    document.querySelectorAll(".toggle-password").forEach(button => {
        button.addEventListener("click", function () {
            const input = this.previousElementSibling;
            const icon = this.querySelector("i");
            if (input.type === "password") {
                input.type = "text";
                icon.classList.replace("ri-eye-line", "ri-eye-off-line");
            } else {
                input.type = "password";
                icon.classList.replace("ri-eye-off-line", "ri-eye-line");
            }
        });
    });

    // Handle Signup Form
    if (signupForm) {
        signupForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            // Show loading indicator
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn ? submitBtn.textContent : null;
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Signing up...';
            }

            let formData = {
                username: document.getElementById("username").value.trim(),
                email: document.getElementById("email").value.trim(),
                password: document.getElementById("password").value.trim(),
            };

            try {
                let response = await fetch("http://127.0.0.1:8000/api/signup/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(formData),
                    credentials: 'include' // Include cookies if using session auth
                });

                let data = await response.json();
                console.log(data);

                if (response.ok) {
                    // Store token if provided
                    if (data.token) {
                        localStorage.setItem("token", data.token);
                        localStorage.setItem("Username", data.user.name);
                    }

                    alert("Signup successful!");
                    loginTab.click(); // Switch to login tab
                } else {
                    alert("Error: " + (data.error || "Unknown error"));
                }
            } catch (error) {
                console.error("Error during signup:", error);
                alert("An error occurred during signup. Please try again.");
            } finally {
                // Reset button state
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }
            }
        });
    }

    // Handle Login Form
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            // Show loading indicator
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn ? submitBtn.textContent : null;
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Logging in...';
            }

            let formData = {
                username: document.getElementById("login_username").value.trim(),
                password: document.getElementById("login_password").value.trim(),
            };

            try {
                let response = await fetch('http://127.0.0.1:8000/api/login/', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(formData), // Use the actual form data
                    credentials: 'include' // Include cookies if using session auth
                });

                    try {
                        let data = await response.json();
    
                        if (response.ok) {
                            localStorage.setItem("token", data.token);
                            localStorage.setItem("Username", data.user.name);
    
                            // Optional: Show success message before redirect
                            alert("Login successful! Redirecting to dashboard...");
                            setTimeout(() => {
                                window.location.href = "dashboard.html";
                            }, 500);
                        } else {
                            console.error("Error: " + (data.error || "Unknown error"));
                        }
                    } catch (error) {
                        console.error("Error during login:", error);
                        alert("An error occurred during login. Please try again.");
                    }
                } finally {
                    // Reset button state
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.textContent = originalText;
                    }
                }
            });
        }
    });
    