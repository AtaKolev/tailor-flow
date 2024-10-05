document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.getElementById('next-button');
    const form = document.getElementById('survey-form');

    nextButton.addEventListener('click', function(e) {
        const questions = document.querySelectorAll('.question');
        let allAnswered = true;

        questions.forEach(question => {
            const answered = question.querySelector('input[type="radio"]:checked');
            if (!answered) {
                allAnswered = false;
            }
        });

        if (!allAnswered) {
            e.preventDefault();  // Prevent form submission if not all questions answered
            alert("Please answer all questions before proceeding.");
        } else {
            // Do not call preventDefault if everything is okay, the form will be submitted
            console.log("Form is being submitted");
        }
    });
});