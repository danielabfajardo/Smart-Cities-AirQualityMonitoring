
module.exports = function (RED) {
    function EnvNode(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        this.on('input', function (msg) {
            var key = config.key || msg.topic || msg.payload;
            msg.payload = process.env[key];
            msg.topic = msg.topic || config.topic;
            node.send(msg);
        });
    }
    RED.nodes.registerType('process-env', EnvNode);
};