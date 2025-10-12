const toolInputs = document.querySelectorAll(".ajax-input");

const modeGeneratorResults = document.getElementById("mode-generator-results");
const chordsInKeyGeneratorResults = document.getElementById("chords-in-key-generator-results");

toolInputs.forEach(input => {
    input.addEventListener("change", fetchToolResults);
});

// Run on page load to show correct reults
window.addEventListener("DOMContentLoaded", fetchToolResults);
window.addEventListener("DOMContentLoaded", animateAccordianPanels);






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
        displayResults(data)
    })
    .catch(err => console.error(err));
}

/**
 * Displays the fetched data in the output / results elements.
 *
 * @param {Object} data - The JSON data returned from the server.
 */
function displayResults(data) {
    document.getElementById('output').textContent = data.result;
    document.getElementById("list-result").textContent = data.my_list.join('\n');

    chordsInKeyGeneratorResults.textContent = data.chords_in_key_generator_results.join('\n');
    modeGeneratorResults.textContent = data.mode_generator_results.join('\n');
}

function animateAccordianPanels() {
    const accordionHeaders = document.getElementsByClassName("accordion-header");

    for (let ah of accordionHeaders) {
        const panel = ah.nextElementSibling;

        if(panel != null) {
            // temporarily disable transition
            panel.classList.add("no-transition");

            // open all panels by default
            panel.style.maxHeight = panel.scrollHeight + "px";
            ah.classList.add("active");

            // allow browser to paint, then re-enable transition
            requestAnimationFrame(() => {
                panel.classList.remove("no-transition");
            });

            // click toggle
            ah.addEventListener("click", function() {
                this.classList.toggle("active");
                
                if (panel.style.maxHeight && panel.style.maxHeight !== "0px") {
                    panel.style.maxHeight = "0px"; // collapse
                } 
                else {
                    panel.style.maxHeight = panel.scrollHeight + "px"; // expand
                }
            });
        }
    }
}