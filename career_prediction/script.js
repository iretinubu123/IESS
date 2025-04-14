document.addEventListener('DOMContentLoaded', function() {
    // Experience slider functionality
    const experienceSlider = document.getElementById('experience');
    const expValue = document.getElementById('expValue');
    
   
    // Get all form elements
    const favoriteSubjectsSelect = document.getElementById('Favorite_Subjects');
    const skillsSelect = document.getElementById('Skills');
    const extracurricularSelect = document.getElementById('Extracurricular');
    const workstyleSelect = document.getElementById('Workstyle');
    const genderSelect = document.getElementById('Gender');
    const personalitySelect = document.getElementById('Personality');
   ;
    
    // Get results container
    const resultsContainer = document.getElementById('career-results');
    
    // Get form and submit button
    const careerForm = document.getElementById('career-form');
    const submitButton = document.getElementById('submit-button');
    
    // Form submission handler
    if (careerForm) {
        careerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Finding matches...';
            }
            
            // Collect all form data
            const formData = {
                favorite_subjects: favoriteSubjectsSelect ? favoriteSubjectsSelect.value : '',
                skills: skillsSelect ? skillsSelect.value : '',
                extracurricular: extracurricularSelect ? extracurricularSelect.value : '',
                workstyle: workstyleSelect ? workstyleSelect.value : '',
                gender: genderSelect ? genderSelect.value : '',
                personality: personalitySelect ? personalitySelect.value : '',
                
            };
            
            // Make API call to career advising endpoint
            fetch('http://127.0.0.1:8000/api/career/predict-career/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken() // Function to get CSRF token
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Display the career recommendations
                displayCareerResults(data.careers);
                
                // Reset button state
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Find My Career Match';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                
                // Display error message
                if (resultsContainer) {
                    resultsContainer.innerHTML = `
                        <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
                            <p>Sorry, we couldn't process your request. Please try again later.</p>
                        </div>
                    `;
                }
                
                // Reset button state
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Find My Career Match';
                }
            });
        });
    }
    
    // Function to get CSRF token from cookies (for Django)
    function getCsrfToken() {
        const name = 'csrftoken';
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
    
    // Function to display career results
    function displayCareerResults(careers) {
        if (!resultsContainer) return;
        
        // Clear previous results
        resultsContainer.innerHTML = '';
        
        if (!careers || careers.length === 0) {
            resultsContainer.innerHTML = `
                <div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4">
                    <p>No matching careers found. Try adjusting your preferences.</p>
                </div>
            `;
            return;
        }
        
        // Create HTML for each career
        careers.forEach(career => {
            const careerCard = document.createElement('div');
            careerCard.className = 'bg-white rounded-lg shadow-md p-6 mb-4';
            careerCard.innerHTML = `
                <div class="flex justify-between items-center">
                    <h3 class="text-xl font-bold text-gray-800">${career.title}</h3>
                    <span class="bg-blue-100 text-blue-800 text-sm font-semibold px-3 py-1 rounded-full">
                        ${career.match}% Match
                    </span>
                </div>
                <p class="text-gray-600 mt-2">${career.description}</p>
                <div class="mt-4">
                    <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="bg-blue-600 h-2 rounded-full" style="width: ${career.match}%"></div>
                    </div>
                </div>
                <div class="mt-4">
                    <button class="text-blue-600 hover:text-blue-800 font-medium">
                        Learn more →
                    </button>
                </div>
            `;
            resultsContainer.appendChild(careerCard);
        });
    }
    
    // Optional: Real-time updates when form elements change
    const formElements = [
        favoriteSubjectsSelect, 
        skillsSelect, 
        extracurricularSelect, 
        workstyleSelect, 
        genderSelect, 
        personalitySelect,
        experienceSlider,
        
    ];
    
    formElements.forEach(element => {
        if (element) {
            element.addEventListener('change', function() {
                console.log('Form updated, you could fetch real-time recommendations here');
                // Uncomment this to enable real-time updates
                // careerForm.dispatchEvent(new Event('submit'));
            });
        }
    });
});