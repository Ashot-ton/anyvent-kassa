#!/usr/bin/env node
const amqp = require("amqplib/callback_api");

//Kassa specific vars
const exchange = "heartbeat-exchange";

//create connection with RMQ server
amqp.connect('amqp://10.3.56.9', (errConnection, connection) => {
    if (errConnection) {
        throw errConnection;
    }
    connection.createChannel((errChannel, channel) => {
        if (errChannel) {
            throw errChannel;
        }
//heartbeat interval
setInterval(() => {
//function to format timestamp
function checkTime(i) {
    if (i < 10) {
      i = "0" + i;
    }
    return i;
}
// timestamp vars
let dag = new Date();
let h = checkTime(dag.getHours());
let m = checkTime(dag.getMinutes());
let s = checkTime(dag.getSeconds());

let currtime = `${h}:${m}:${s}`;

//message to send
const msg = `<?xml version="1.0" encoding="UTF-8"?>
<Heartbeat>
<Sender>Kassa</Sender>
<Timestamp>${currtime}</Timestamp>
</Heartbeat>`;

//sending message to exchange
console.log(`Heartbeat sent.`);
channel.assertExchange(exchange, 'direct', { durable: false }, () => {
    channel.publish(exchange, "heartbeat", Buffer.from(msg))
});
}, 1000);
});
})
