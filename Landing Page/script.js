document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('career-form');
    const currentRoleInput = document.getElementById('current-role');
    const futureRoleInput = document.getElementById('future-role');
    const skillsInput = document.getElementById('skills');
    const submitButton = document.querySelector('button[type="submit"]');
    const refineButton = document.getElementById('refine-button');

    function checkInputs() {
        if (currentRoleInput.value.trim() !== '' && 
            futureRoleInput.value.trim() !== '' && 
            skillsInput.value.trim() !== '') {
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

    currentRoleInput.addEventListener('input', checkInputs);
    futureRoleInput.addEventListener('input', checkInputs);
    skillsInput.addEventListener('input', checkInputs);

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        console.log('Form submitted:');
        console.log('Current Role:', currentRoleInput.value);
        console.log('Future Role:', futureRoleInput.value);
        console.log('Skills:', skillsInput.value);

        // Here you would typically send this data to a server or process it further
        alert('Thank you for submitting! Check the console for form data.');
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
