document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const emotionInput = document.getElementById('emotionInput');
    const charCount = document.getElementById('charCount');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultsSection = document.getElementById('resultsSection');
    
    // Character counter
    if (emotionInput && charCount) {
        emotionInput.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = count + (count === 1 ? ' character' : ' characters');
            
            // Optional: Add visual indication if minimum character count is met
            if (count >= 100) {
                charCount.classList.add('text-green-600');
            } else {
                charCount.classList.remove('text-green-600');
            }
        });
    }
    
    // Analyze button functionality
    if (analyzeBtn && resultsSection) {
        analyzeBtn.addEventListener('click', function() {
            const text = emotionInput.value.trim();
            
            if (text.length < 20) {
                alert('Please enter more text for a more accurate analysis.');
                return;
            }
            
            // Show loading state
            analyzeBtn.disabled = true;
            analyzeBtn.textContent = 'Analyzing...';
            
            // Fetch data from your sentiment analysis API
            fetch('/sentiment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken() // Function to get CSRF token (defined below)
                },
                body: JSON.stringify({ text: text })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Show results section
                resultsSection.classList.remove('hidden');
                resultsSection.classList.add('show');
                
                // Create chart with the received data
                createEmotionChart(data);
                
                // Reset button state
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = 'Analyze';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while analyzing the text. Please try again.');
                
                // Reset button state
                analyzeBtn.disabled = false;
                analyzeBtn.textContent = 'Analyze';
            });
        });
    }
    
    // Function to get CSRF token from cookies
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
    
    // Create the emotion chart
    function createEmotionChart(apiData) {
        const ctx = document.getElementById('emotionChart').getContext('2d');
        
        // Process the API data
        // Assuming the API returns data in this format: 
        // { emotions: { Joy: 40, Confidence: 20, Anxiety: 15, Neutral: 25 } }
        
        const emotionLabels = Object.keys(apiData.emotions);
        const emotionValues = Object.values(apiData.emotions);
        
        // Colors for different emotions
        const backgroundColors = [
            'rgba(66, 99, 235, 0.8)',   // Blue
            'rgba(111, 207, 151, 0.8)', // Green
            'rgba(251, 191, 36, 0.8)',  // Yellow
            'rgba(239, 100, 97, 0.8)',  // Red
            'rgba(161, 98, 247, 0.8)',  // Purple
            'rgba(45, 212, 191, 0.8)',  // Teal
            'rgba(249, 115, 22, 0.8)'   // Orange
        ];
        
        // Prepare data for chart
        const data = {
            labels: emotionLabels,
            datasets: [{
                data: emotionValues,
                backgroundColor: backgroundColors.slice(0, emotionLabels.length),
                borderWidth: 1
            }]
        };
        
        // Check if chart already exists and destroy it
        if (window.emotionPieChart) {
            window.emotionPieChart.destroy();
        }
        
        // Create new chart
        window.emotionPieChart = new Chart(ctx, {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            font: {
                                size: 12
                            }
                        }
                    }
                }
            }
        });
    }
});