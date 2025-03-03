document.getElementById('languageSelect').addEventListener('change', function () {
    var currentPath = window.location.pathname;
    var pathSegments = currentPath.split('/');
    var lastParam = pathSegments[pathSegments.length - 2] + '/';
    var selectedValue = this.value + '/' + lastParam;
    if (selectedValue) {
        window.location.href = selectedValue;
    }
});

function insertValue(value) {
    const polinomInput = document.getElementById('polinomInput');
    polinomInput.value += value;
}

function savePolinom() {
    var polinom = document.getElementById('polinomInput').value;
    document.getElementById('hiddenPolinom').value = polinom;
}

MathJax.Hub.Config({
tex2jax: {
  inlineMath: [['$', '$'], ['\\(', '\\)']],
  displayMath: [['$$', '$$'], ['\\[', '\\]']],
  processEscapes: true
},
TeX: {
  extensions: ["AMSmath.js", "AMSsymbols.js", "noErrors.js", "noUndefined.js"]
}
});


document.getElementById('nextStepButton').addEventListener('click', function() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '{% url "result" %}', true);
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            document.getElementById('stepDisplay').innerText = response.step;
        }
    };
    xhr.send('next_step=true');
});

function sendHistory(id) {
    window.location.href = "{% url 'Result' id=0 %}".replace("0", id);
}

function downloadPDF(id) {
    // Pošalji GET zahtev za generisanje PDF-a
    fetch(`/sr/history/${id}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            // Nakon što je PDF generisan, preuzmi ga
            return fetch('Master/result1.pdf');  // Putanja do PDF-a
        })
        .then(response => {
            if (response.ok) {
                return response.blob(); // Preuzmi blob
            }
            throw new Error('Network response was not ok.');
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'result.pdf'; // Naziv fajla
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url); // Oslobodi blob URL
        })
        .catch(error => console.error('There was a problem with the fetch operation:', error));
}


// ---------------------------------------------------------------------------------------------------------------------

let countdown;
function checkAnswer(button) {
    if (button.getAttribute('data-correct') === 'True') {
        button.style.color = 'green';
    } else {
        button.style.color = 'red';
    }
}




