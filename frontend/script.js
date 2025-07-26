document.addEventListener("DOMContentLoaded", () => {
    const checkButton = document.getElementById('checkButton');
    if (checkButton) {
        checkButton.addEventListener('click', checkPasswordStrength);
    }
});

async function checkPasswordStrength() {
    const passwordInput = document.getElementById('password');
    const resultDiv = document.getElementById('result');
    const strengthMeter = document.getElementById('strengthMeter');
    const tipsDiv = document.getElementById('tips');

    const password = passwordInput?.value?.trim();

    if (!password) {
        displayResult("Please enter a password", "", "0%", "#ccc", "");
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const strengthLabel = data.strength?.toLowerCase(); // "weak", "medium", "strong"

        const strengthStyles = {
            weak: {
                label: "Weak Password",
                color: "#dc3545",
                width: "33%",
                tips: "Tips: Tambahkan huruf besar, angka, simbol, dan hindari pola umum."
            },
            medium: {
                label: "Medium Password",
                color: "#ffc107",
                width: "66%",
                tips: "Tips: Sudah lumayan, coba tambah panjang & variasi karakter."
            },
            strong: {
                label: "Strong Password",
                color: "#28a745",
                width: "100%",
                tips: "Tips: Bagus! Password kamu sudah cukup kuat."
            }
        };

        const style = strengthStyles[strengthLabel] || {
            label: "Unknown Strength",
            color: "#ccc",
            width: "0%",
            tips: ""
        };

        displayResult(`${data.message} (${style.label})`, style.label.toLowerCase(), style.width, style.color, style.tips);

    } catch (error) {
        console.error('Error:', error);
        displayResult(`Error: ${error.message}`, "", "0%", "#ccc", "");
    }

    function displayResult(text, resultClass, width, color, tips) {
        resultDiv.textContent = text;
        resultDiv.className = `result ${resultClass}`;
        strengthMeter.style.width = width;
        strengthMeter.style.backgroundColor = color;
        tipsDiv.textContent = tips;
    }
}
