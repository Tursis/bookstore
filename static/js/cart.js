const total = document.querySelector("#card_form #total");
const inputs = document.querySelectorAll("#card_form input");

totalUpdate();
document.querySelectorAll("#card_form img").forEach((img) => {
    img.addEventListener("click", (e) => {
        const action = e.currentTarget.dataset.action;
        const tr = e.currentTarget.closest('tr');
        const input = tr.querySelector("input");

        switch (action) {
            case "card_form_plus":
                input.value++;
                send();
                calculateSumItem(tr, input)
                break;
            case "card_form_minus":
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
        totalUpdate();
    });
});

function send() {
    const form = document.querySelector("#card_form");
    const element = document.querySelector(".card_total_price")
    const body = new FormData(form);
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
            element.textContent = json;
            console.log(json);

        })  //print data to console
        .catch(err => console.log('Request Failed', err)); // Catch errors
}

function removeElement(element) {
    element.parentNode.removeChild(element);
}

function totalUpdate() {
    let sum = 0;
    inputs.forEach((input) => {
        sum += input.value * input.dataset.price;
    });
    total.textContent = sum;

}

function calculateSumItem(tr, input) {
    const sumElement = tr.querySelector('[data-sum]')
    const itemPrice = Number(input.dataset.price)
    const itemAmount = Number(input.value)
    const itemSum = itemPrice * itemAmount
    sumElement.textContent = itemSum

}

function debug(formData) {
    for (const pair of formData.entries()) {
        console.log(pair[0] + ", " + pair[1]);
    }
}
