function calculate() {
    // Get input values
    const eqn1_x = parseFloat(document.getElementById('eqn1_x').value);
    const eqn1_y = parseFloat(document.getElementById('eqn1_y').value);
    const eqn1_z = parseFloat(document.getElementById('eqn1_z').value);
    const eqn1_constant = parseFloat(document.getElementById('eqn1_constant').value);

    const eqn2_x = parseFloat(document.getElementById('eqn2_x').value);
    const eqn2_y = parseFloat(document.getElementById('eqn2_y').value);
    const eqn2_z = parseFloat(document.getElementById('eqn2_z').value);
    const eqn2_constant = parseFloat(document.getElementById('eqn2_constant').value);

    const eqn3_x = parseFloat(document.getElementById('eqn3_x').value);
    const eqn3_y = parseFloat(document.getElementById('eqn3_y').value);
    const eqn3_z = parseFloat(document.getElementById('eqn3_z').value);
    const eqn3_constant = parseFloat(document.getElementById('eqn3_constant').value);

    // Send the data to the server
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            equations: [
                { coefficients: [eqn1_x, eqn1_y, eqn1_z], constant: eqn1_constant },
                { coefficients: [eqn2_x, eqn2_y, eqn2_z], constant: eqn2_constant },
                { coefficients: [eqn3_x, eqn3_y, eqn3_z], constant: eqn3_constant }
            ]
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update the content of the result div
        document.getElementById('result').innerHTML = `Result: [${data.result.join(', ')}]`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}