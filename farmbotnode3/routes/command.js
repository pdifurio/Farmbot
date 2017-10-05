var config = require('../config');

exports.get = function () {
	return function (req, res){
		res.render('command');
	};
};
exports.post = function () {
	return function (req, res) {
		console.log('Entered Command POST');
		var mqtt = require('mqtt');
		var client = mqtt.connect(config.mqtt.broker);

		var myTimer = setTimeout(function () {
			client.end();
			callback('Timeout getting command status', null);
		}, config.commandTimeout);

		client.on('connect', function () {
			client.subscribe('/FarmBot/CommandStatus');
			if (typeof req.body.Forward != 'undefined') {
				var command = { 'CommandType': 'StartMotor', 'yAxis': 'Forward' };
				var topic = '/FarmBot/Command/yAxis';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			if (typeof req.body.Backward != 'undefined') {
				var command = { 'CommandType': 'StartMotor', 'yAxis': 'Backward' };
				var topic = '/FarmBot/Command/yAxis';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			//Pro-y-axis action up in here


			if (typeof req.body.Left != 'undefined') {
				var command = { 'CommandType': 'StartMotor', 'xAxis': 'Left' };
				var topic = '/FarmBot/Command/xAxis';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			if (typeof req.body.Right != 'undefined') {
				var command = { 'CommandType': 'StartMotor', 'xAxis': 'Right' };
				var topic = '/FarmBot/Command/xAxis';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			//Pro-x-axis action up in here


			if (typeof req.body.Up != 'undefined') {
				var command = { 'CommandType': 'StartMotor', 'zAxis': 'Up' };
				var topic = '/FarmBot/Command/zAxis';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			if (typeof req.body.Down != 'undefined') {
				var command = { 'CommandType': 'StartMotor', 'zAxis': 'Down' };
				var topic = '/FarmBot/Command/zAxis';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			//Proz-axis action up in here

			//Button for return to Home
			if (typeof req.body.home != 'undefined') {
				var command = { 'CommandType': 'StartMotor', 'Home': 'Home' };
				var topic = '/FarmBot/Command/Home';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			if (typeof req.body.WaterAll != 'undefined') {
				var command = { 'CommandType': 'StartMotor', 'WaterAll': 'Enable' };
				var topic = '/FarmBot/Command/WaterAll';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			//this is the absolute positioning
			if (typeof req.body.absoluteMoveX != 'undefined') {
				//document.write(req.body.absoluteMove);
				var distance = req.body.absPosition;
				var command = { 'CommandType': 'AbsoluteMoveX', 'absolute_position': String(req.body.absPosition) };
				var topic = '/FarmBot/Command/Absolute';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			if (typeof req.body.absoluteMoveY != 'undefined') {
				//document.write(req.body.absoluteMove);
				var distance = req.body.absPosition;
				var command = { 'CommandType': 'AbsoluteMoveY', 'absolute_position': String(req.body.absPosition) };
				var topic = '/FarmBot/Command/Absolute';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			if (typeof req.body.absoluteMoveZ != 'undefined') {
				//document.write(req.body.absoluteMove);
				var distance = req.body.absPosition;
				var command = { 'CommandType': 'AbsoluteMoveZ', 'absolute_position': String(req.body.absPosition) };
				var topic = '/FarmBot/Command/Absolute';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			if (typeof req.body.unalarm != 'undefined') {
				var command = { 'CommandType': 'StartMotor', 'Alarm': 'Disable' };
				var topic = '/FarmBot/Command/unalarm';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
			if (typeof req.body.update != 'undefined') {
				var command = { 'CommandType': 'Request', 'Update': 'Status' };
				var topic = '/FarmBot/Command/update';
				var message = JSON.stringify(command);
				client.publish(topic, message);
				console.log('Command published on topic ' + topic + ', ' + message);
			}
		});

		client.on('message', function (topic, message) {
			client.end();
			clearTimeout(myTimer);

			console.log('Message received on topic ' + topic + ', ' + message);
			callback(null, message);
		});

		function callback(err, data) {
			if (err) {
				console.log(err);
				//res.status(404).send(err);
				res.render('command', {message:err});
			}
			else {
				//res.set('Content-Type', 'text/xml')
				//res.send(data);
				res.render('command', {message:data});
			}
		};
	};
}
