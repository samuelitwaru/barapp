var notifications = null

function fetchNotifications(){
	fetch("/notifications/count")
    .then(r => r.json())
    .then(data => {
    	count = data.count
    	$("#notifications").html(renderNotificationCount(count))
    })
}

function renderNotificationCount(count){
	if (count != 0){
		return `
				<a href="/notifications" class="btn btn-sm btn-danger border-2 border-light rounded-circle">
		            ${count}
		        </a>
		        `
	}
	return ''
}


window.onload = function windowLoad(event) {	
	fetchNotifications()
	setInterval(fetchNotifications, 30000) 
}

if (window.location.protocol == "https:") {
	var ws_scheme = "wss://";
} else {
	var ws_scheme = "ws://"
};


const barSocket = new WebSocket(
	ws_scheme + window.location.host + '/ws/bar/'
);

barSocket.onopen = function(e){
	console.log("connection opened")
}


barSocket.onclose = function(e){
	console.log("connection closed")
}

barSocket.onmessage = function(e) {
	fetchNotifications()	
};