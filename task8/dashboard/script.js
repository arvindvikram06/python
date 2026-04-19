const ctx = document.getElementById('chart').getContext('2d');

const data = {
    labels: [],
    datasets: [
        {
            label: 'Temperature',
            data: [],
            borderWidth: 2
        },
        {
            label: 'Moving Avg',
            data: [],
            borderDash: [5, 5],
            borderWidth: 2
        }
    ]
};

const chart = new Chart(ctx, {
    type: 'line',
    data: data
});

const ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onmessage = function (event) {
    const msg = JSON.parse(event.data);

   
    data.labels.push(msg.timestamp);
    data.datasets[0].data.push(msg.temperature);
    data.datasets[1].data.push(msg.moving_avg);

    if (data.labels.length > 20) {
        data.labels.shift();
        data.datasets.forEach(ds => ds.data.shift());
    }

    chart.update();

    document.getElementById("temp").innerText = msg.temperature;
    document.getElementById("avg").innerText = msg.moving_avg;
    document.getElementById("zscore").innerText = msg.z_score;
    document.getElementById("status").innerText = msg.status;

    const alertBox = document.getElementById("alert");

    if (msg.status === "CRITICAL") {
        alertBox.innerText = "CRITICAL ALERT!";
        alertBox.style.color = "red";
    } else if (msg.status === "ANOMALY") {
        alertBox.innerText = "ANOMALY DETECTED!";
        alertBox.style.color = "orange";
    } else {
        alertBox.innerText = "";
    }
};