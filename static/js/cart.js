const total = document.querySelector("#cart_form #total");
const inputs = document.querySelectorAll("#cart_form input");


document.querySelectorAll("#cart_form img").forEach((img) => {
    img.addEventListener("click", (e) => {
        const action = e.currentTarget.dataset.action;
        const tr = e.currentTarget.closest('tr');
        const input = tr.querySelector("input");

        switch (action) {
            case "cart_form_plus":
                input.value++;
                send();
                calculateSumItem(tr, input)
                break;
            case "cart_form_minus":
                if (Number(input.value) > 0) {
                    input.value--;
                    send();
                    calculateSumItem(tr, input)
                }
                if (Number(input.value) === 0) {
                    removeElement(tr);
                }
                break;
            default:
                break;
        }
    });
});

function send() {

    const form = document.querySelector("#cart_form");
    const body = new FormData(form);
    const elementQuantity = document.querySelector("#cart_quantity");
    const elementTotalSum = document.getElementsByClassName("cart_total_price");


    debug(body); // just for log, you can remove this line and function declaration
    fetch("cart_update/", {
        method: "POST",
        body,

    })
        .then(response => {
            console.log(response);
            return response.json()
        })  // convert to json
        .then(json => {
            let result = JSON.parse(json);
            for (let i = 0; i < elementTotalSum.length; i++) {
                elementTotalSum[i].textContent = (result[0].toFixed(2));
            }
            elementQuantity.textContent = result[1]
        })  //print data to console
        .catch(err => console.log('Request Failed', err)); // Catch errors
}

function removeElement(element) {
    element.parentNode.removeChild(element);
}

function calculateSumItem(tr, input) {
    const sumElement = tr.querySelector('[data-sum]')
    const itemPrice = Number(input.dataset.price)
    const itemAmount = Number(input.value)
    const itemSum = itemPrice * itemAmount
    sumElement.textContent = itemSum.toFixed(2)

}

function debug(formData) {
    for (const pair of formData.entries()) {
        console.log(pair[0] + ", " + pair[1]);
    }
}
