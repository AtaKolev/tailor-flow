document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('career-form');
    const futureRoleInput = document.getElementById('future-role');
    const skillsInput = document.getElementById('skills');
    const submitButton = document.querySelector('button[type="submit"]');
    const refineButton = document.getElementById('refine-button');

    function checkInputs() {
        if (futureRoleInput.value.trim() !== '' && skillsInput.value.trim() !== '') {
            submitButton.classList.add('visible');
        } else {
            submitButton.classList.remove('visible');
        }

        if (skillsInput.value.trim() !== '') {
            refineButton.classList.add('visible');
        } else {
            refineButton.classList.remove('visible');
        }
    }

    futureRoleInput.addEventListener('input', checkInputs);
    skillsInput.addEventListener('input', checkInputs);

    // Remove preventDefault to allow form submission
    form.addEventListener('submit', (e) => {
        console.log('Form submitted:');
        console.log('Future Role:', futureRoleInput.value);
        console.log('Skills:', skillsInput.value);

        // Form will be submitted to the Flask backend with the default behavior
        // No need for window.location.href unless you want to prevent the form submission
    });

    refineButton.addEventListener('click', () => {
        // Here you would implement the logic to refine the text
        console.log('Refine button clicked');
        alert('Refining text... (This is where you would implement the refinement logic)');
    });

    // Initially hide the buttons
    submitButton.classList.remove('visible');
    refineButton.classList.remove('visible');
});
