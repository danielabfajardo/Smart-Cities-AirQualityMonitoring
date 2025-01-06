# Node-RED enviroment variable reader

Reads enviroment variables from the Node-RED server process using the `process.env` node variable.

## Installation

Type 

```sh
yarn add node-red-contrib-env
```

or

```sh
npm install --save node-red-contrib-env
```

to avoid *yarn*.

## Behavior

There are three ways the node tries to specify the environment variable name which shoud be need in that order

1. Use the `key` specified in the node config.
1. Use the `payload` from the incomming message.
1. Use the `topic` from the incomming message.
