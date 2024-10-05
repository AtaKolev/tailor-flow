document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.getElementById('next-button');
    
    nextButton.addEventListener('click', function() {
        // Check if all questions are answered
        const questions = document.querySelectorAll('.question');
        let allAnswered = true;
        
        questions.forEach(question => {
            const answered = question.querySelector('input[type="radio"]:checked');
            if (!answered) {
                allAnswered = false;
            }
        });
        
        if (allAnswered) {
            alert('Thank you for completing the survey! Proceeding to the next page...');
            // Here you would typically navigate to the next page or submit the form
        } else {
            alert('Please answer all questions before proceeding.');
        }
    });
});
