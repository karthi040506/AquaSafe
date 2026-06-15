const form = document.getElementById('predictionForm');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.querySelector('.btn-text');
const loader = document.querySelector('.loader');
const resultCard = document.getElementById('resultCard');
const closeResult = document.getElementById('closeResult');
const globalError = document.getElementById('globalError');

// Result Elements
const predictionResult = document.getElementById('predictionResult');
const riskLevel = document.getElementById('riskLevel');
const statusRing = document.getElementById('statusRing');
const statusIcon = document.getElementById('statusIcon');
const textContent = document.querySelector('.text-content'); // Container for text color

const API_URL = 'http://127.0.0.1:5000/predict';

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Reset UI
    globalError.classList.add('hidden');
    resultCard.classList.add('hidden');

    // Validation
    if (!validateInputs()) return;

    // Loading State
    setLoading(true);

    const formData = new FormData(form);
    const data = {
        criteria: formData.get('criteria'),
        percentage: parseFloat(formData.get('percentage')),
        salt_count: parseFloat(formData.get('salt_count'))
    };

    try {
        // UX Delay to show smooth loading state
        await new Promise(r => setTimeout(r, 600));

        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error('API Error');

        const result = await response.json();
        showResult(result.prediction, result.risk_level);

    } catch (err) {
        console.error(err);
        globalError.innerText = "Connection Failed. Is backend running?";
        globalError.classList.remove('hidden');
    } finally {
        setLoading(false);
    }
});

function validateInputs() {
    // Rely on native form validation as defined in HTML types and min/max
    if (!form.checkValidity()) {
        form.reportValidity();
        return false;
    }
    return true;
}

function setLoading(active) {
    submitBtn.disabled = active;
    if (active) {
        btnText.innerText = "Analyzing...";
        loader.classList.remove('hidden');
    } else {
        btnText.innerText = "Predict Water Safety";
        loader.classList.add('hidden');
    }
}

function showResult(prediction, risk) {
    resultCard.classList.remove('hidden');

    // Update Content
    predictionResult.innerText = prediction;
    riskLevel.innerText = risk;

    // Reset Styles
    statusRing.className = 'status-ring';
    textContent.className = 'text-content';

    if (prediction === 'Safe') {
        statusRing.classList.add('safe-glow');
        textContent.classList.add('text-safe');
        statusIcon.innerText = '🛡️';
    } else {
        statusRing.classList.add('danger-glow');
        textContent.classList.add('text-danger');
        statusIcon.innerText = '☣️';
    }
}

closeResult.addEventListener('click', () => {
    resultCard.classList.add('hidden');
});
