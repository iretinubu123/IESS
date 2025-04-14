document.getElementById('advisingForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    // Get form values
    const gpa = parseFloat(document.getElementById('gpa').value);
    const studyHours = parseInt(document.getElementById('study_Hours').value);
    const preferredSubject = document.getElementById('Preferred_Subject').value;

    // Validate inputs
    if (gpa < 0 || gpa > 4) {
        alert('GPA must be between 0 and 4');
        return;
    }

    if (studyHours < 1 || studyHours > 40) {
        alert('Study hours must be between 1 and 40');
        return;
    }

    try {
        // In a real application, this would be an API call
        const response = await fetch('http://127.0.0.1:8000/api/academic-advising/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gpa,
                study_hours: studyHours,
                preferred_subject: preferredSubject
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Show results
        document.getElementById('results').classList.remove('hidden');
        document.getElementById('recommendationText').textContent = 
            `Based on your academic profile, we recommend: ${data.recommended_course}`;

    } catch (error) {
        console.error('Error:', error);
        alert('There was an error getting your recommendation. Please try again.');
    }
});

// Input validation
document.getElementById('gpa').addEventListener('input', function(e) {
    if (this.value > 4) this.value = 4;
    if (this.value < 0) this.value = 0;
});

document.getElementById('studyHours').addEventListener('input', function(e) {
    if (this.value > 40) this.value = 40;
    if (this.value < 1) this.value = 1;
});