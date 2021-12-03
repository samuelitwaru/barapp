window.onload = function windowLoad(event) {
	var notifications = null

	function fetchNotifications(){
		fetch("/notifications")
        .then(r => r.json())
        .then(data => {
        	notifications = data
        	$("#notifications").html(renderNotifications(notifications))
        })
	}
// s,dks
	function renderNotifications(notifications){
		count = 0
		list = ""
		for (var i=0; i < notifications.length; i++) {
			notification = notifications[i]
			itemCount = notification.items.length
			count += itemCount
			if (itemCount){
				el = `
				<li>
					<a class="dropdown-item d-flex justify-content-around text-wrap" href="${notification.url}">
					${notification.message}
					<span class="badge bg-danger p-1 mx-2 my-auto">${itemCount}</span>
					</a>
				</li>
				`
				list += el
			}
		}
		if(count){
			return `
				<button class="btn btn-sm btn-danger border-2 border-light" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false">
		            ${count}
		        </button>
	        	<ul class="dropdown-menu dropdown-menu-end rounded-0 px-0 mt-3 border-dark" aria-labelledby="dropdownMenuButton1" style="z-index: 10000;width:300px">
		        	${list}
		        </ul>`
		}
		return ''
	}
	fetchNotifications()
	setInterval(fetchNotifications, 30000) 
}