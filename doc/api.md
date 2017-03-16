### Websocket API
#### Endpoint: ws://127.0.0.1:8888/ws

## Error format
```
{"errors": [{"message": "an error message"}]}
```
---

## Users

### Get
Message:
```
{
	"uri": "get/users", 
	"token": "Optional token that identifies this message"
}
```
Response:
```
{
	"users": [{
		"username": "admin", 
		"name": "William Hass", 
		"_id": "58badd550be4444b2ffb6930"
	}, 
	{
		"username": null, 
		"name": "String", 
		"_id": "58c36fab0be4447cdd1bc8d9"
	}]
}
```

### Create/Update

Message:
```
{
	"uri": "post/users", 
	"object": {
		"_id": "xxx", // Send only If updating object
		"name": "Name of the user",
		"username": "Username of the user",
		"password": "Password of the user"
	}
}
```
Response:
```
{
	"user": {
		"_id": "58c9f68b0be444203a5858ea",
		"username": "auser", 
		"password": "Password of the user", 
		"name": "Name of the user"
	}
}
```


### Delete
Message:
```
{
	"uri": "delete/notes", 
	"_id": "58c9f68b0be444203a5858ea"
}
```

Response:
```
{
	"deleted": "58c9f68b0be444203a5858ea"
}
```
---
## Tasks
### GET
Message:

```
{
	"uri": "get/tasks", 
	"arguments": {
		"accessory_id": ""
	}
}
```
- `accessory_id` is optional

Response:

```
{
	"tasks": [{
		"accessory_id": "58bae1f48037ad9994a15986", 
		"name": "My first timer 2", 
		"timer": {
			"hour": "*", 
			"seconds": "*", 
			"month": "*", 
			"year": "_", 
			"timezone": null, 
			"day": "*", 
			"minute": "*"
		}, 
		"creation_date": 1488642588.744635, 
		"action": "turn_off", 
		"_id": "58bae21c0be4444b8a0acc05"
	}]
}
```

### Create/Update
Message
```
{
	"uri": "post/tasks", 
	"object": {
		"_id": "ObjectId",
		"uri": "String",
		"accessory_id": "Int",
		"timer": "Timer model",
		"name": "String",
		"user_id": "ObjectId"
	}
}
```
- Send `_id` if updating an object

Response
```
{
	"_id": "58c937e70be444a541403984",
	"accessory_id": "58c75a7c0be44400b29ce61a",
	"user_id": "58badd550be4444b2ffb6930", 
	"name": "A name", 
	"timer": {
		"hour": "Int", 
		"seconds": "Int", 
		"month": "Int", 
		"year": "Int", 
		"timezone": "1800", 
		"day": "Int", 
		"minute": "Int"
	}, 
	"creation_date": 1489582055.321008, 
	"action": "turn_on"
}
```

### Delete
Message
```
{
	"uri": "delete/tasks", 
	"_id": "58c937e70be444a541403984"
}
```
Response
```
{
	"deleted": "58c937e70be444a541403984"
}
```

## Accessories Log
### GET
Message
```
{
	"uri": "get/accessories_logs", 
	"arguments": {"from_date": "", "to_date": "", "accessory_id": ""}
}
```
- `from_date`, `to_date`, `accessory_id` are optionals

Response
```
{"logs": [
	{
		"accessory": {
			"_id": "5.0", 
			"type": 3.0, 
			"name": "Relay 2", 
			"value": "0"
		},
 		"creation_date": 1487370077.334557
	}, 
	{
		"accessory": {
			"type": 2, 
			"name": "CO2", 
			"value": "450"
		}, 
		"creation_date": 1489459836.427011
	}, 
	{
		"accessory": {
			"type": 3, 
			"name": "Relay 1", 
			"value": "0"
		}, 
		"creation_date": 1489459836.427011
	}
]}
```
---
## Accessories
### GET
Mensagem
```
{
	"uri": "get/accessories_logs", 
	"arguments": {
		"from_date": "", 
		"to_date": "", 
		"accessory_id": ""
	}
}
```

Response

```
{
	"accessories": [{
		"_id": "58c75a7c0be44400b29ce61a", 
		"type": 0, 
		"name": "Humidity", 
		"value": "60"
	}, 
	{
		"_id": "58c75a7c0be44400b29ce61c", 
		"type": 1, 
		"name": "Temperature", 
		"value": "30"
	}
]}

```
---
## Notes
### GET
Mensagem
```
{
	"uri": "get/notes", 
	"arguments": {
		"from_date": "", 
		"to_date": "", 
		"accessory_id": ""
	}
}
```

Response
```
{
	"notes": [{
		"text": "A text", 
		"_id": "58ca06230be444209078f8e4", 
		"user_id": "58badd550be4444b2ffb6930", 
		"creation_date": 1489634851.660841
	}]
}
```


### Create/Update
Mensagem
```
{
	"uri": "post/notes", 
	"object": {
		"_id": "ObjectId", // Include if updating an object
		"user_id": "ObjectId",
		"text": "A text",
		"accessory_log_id": "ObjectId",
		"accessory_id": "ObjectId",
		"creation_date": "Double"
	}
}
```

Response
```
{
	"text": "A text", 
	"_id": "58ca06230be444209078f8e4", 
	"user_id": "58badd550be4444b2ffb6930", 
	"creation_date": 1489634851.660841
}
```

Delete