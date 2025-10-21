const toolInputs = document.querySelectorAll(".ajax-input");

const modeGeneratorResults = document.getElementById("mode-generator-results");
const chordsInKeyGeneratorResults = document.getElementById("chords-in-key-generator-results");

const toolThreeResultOne = document.getElementById("tool-three-result-one");
const toolThreeResultTwo = document.getElementById("tool-three-result-two");
const toolThreeResultThree = document.getElementById("tool-three-result-three");
const toolThreeResultFour = document.getElementById("tool-three-result-four");
const toolThreeResultFive = document.getElementById("tool-three-result-five");
const toolThreeResultSix = document.getElementById("tool-three-result-six");

const messageContainer = document.getElementById("message-container");

toolInputs.forEach(input => {
    input.addEventListener("change", fetchToolResults);
});

window.addEventListener("DOMContentLoaded", fetchToolResults);

/**
 * Fetches tool results from the Django backend using a AJAX request.
 * Then updates the corresponding result display elements.
 *
 * @function
 * @returns {void}
 */
function fetchToolResults() {
    const params = {};

    toolInputs.forEach(i => {
        params[i.dataset.key] = i.value;
    });

    const query = new URLSearchParams(params);

    fetch(`/documentation/tools/?${query.toString()}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' } // AJAX request
    })
    .then(res => res.json())
    .then(data => {
        displayMessages(data);
        displayResults(data);
    })
    .catch(err => console.error(err));
}

/**
 * Displays any messages from Django
 *
 * @param {Object} data - The JSON data returned from the server.
 */
function displayMessages(data) {
    const container = document.getElementById("message-container");
    container.innerHTML = ""; // Clear old messages

    data.messages.forEach(msg => {
        const box = document.createElement("div");
        box.className = `box message message-${msg.tags}`;

        const pre = document.createElement("pre");
        pre.innerHTML = `<strong>${msg.tags.charAt(0).toUpperCase() + msg.tags.slice(1)}</strong> - ${msg.text}`;

        box.appendChild(pre);
        container.appendChild(box);
    });
}

/**
 * Displays the fetched data in the output / results elements.
 *
 * @param {Object} data - The JSON data returned from the server.
 */
function displayResults(data) {
    chordsInKeyGeneratorResults.textContent = data.chords_in_key_generator_results.join('\n');
    modeGeneratorResults.textContent = data.mode_generator_results.join('\n');

    toolThreeResultOne.textContent = data.tool_three_result_one;
    toolThreeResultTwo.textContent = data.tool_three_result_two;
    toolThreeResultThree.textContent = data.tool_three_result_three;
    toolThreeResultFour.textContent = data.tool_three_result_four;
    toolThreeResultFive.textContent = data.tool_three_result_five;
    toolThreeResultSix.textContent = data.tool_three_result_six;
}