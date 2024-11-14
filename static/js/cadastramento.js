document.querySelectorAll('.select-menu').forEach(menu => {
    const selectBtn = menu.querySelector('.select-btn');
    const options = menu.querySelectorAll('.option');
    const sBtnText = menu.querySelector('.sBtn-text');

    selectBtn.addEventListener('click', () => {
        menu.classList.toggle('active');
    });

    options.forEach(option => {
        option.addEventListener('click', () => {
            let selectedOption = option.querySelector('.option-text').innerText;
            sBtnText.innerText = selectedOption;
            menu.classList.remove('active');
        });
    });
});

// Alert de confirmação

document.getElementById('confirmButton').addEventListener('click', function() {
    const steps = document.querySelectorAll('.step');

    steps.forEach(step => {
        step.classList.add('active');
    });
    
    const successMessage = document.getElementById('successMessage');
    successMessage.style.display = 'flex';

    sessionStorage.setItem('showSuccessMessage', 'true');

    setTimeout(() => {
        successMessage.style.display = 'none';
        sessionStorage.removeItem('showSuccessMessage');
    }, 3000);
});


window.addEventListener('load', () => {
    const successMessage = document.getElementById('successMessage');

    if (sessionStorage.getItem('showSuccessMessage') === 'true') {
        successMessage.style.display = 'flex';
        setTimeout(() => {
            successMessage.style.display = 'none';
            sessionStorage.removeItem('showSuccessMessage');
        }, 3000);
    }
});

window.addEventListener('beforeunload', () => {
    const successMessage = document.getElementById('successMessage');
    if (successMessage.style.display === 'flex') {
        sessionStorage.setItem('showSuccessMessage', 'true');
    }
})