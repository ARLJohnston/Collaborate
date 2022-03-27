function setCookie(cookieName, cookieValue){
 	document.cookie = cookieName + "=" + cookieValue;
}

function getCookie(cookieName){
	let name = cookieName + "=";
	let cookies = document.cookie.split(';');

	for(let i = 0; i < cookies.length; i++){
		let cookie = cookies[i];

		while (cookie.charAt(0) == ' '){
			cookie = cookie.substring(1);
		}

		if (cookie.indexOf(name) == 0){
			return cookie.substring(name.length, cookie.length);
		}

	}

	return "";
}

function validateCookie(cookieName, defaultVal = true){
	let cookie = getCookie(cookieName);
	if(cookie == ""){
		setCookie(cookieName, defaultVal);
	}
}

function changeTheme(){
	validateCookie("theme");
	let theme = getCookie("theme");
	let element = document.body;

	element.classList.toggle("dark-theme");

	if(theme == "true"){
		setCookie("theme", "false");
	}
	else{
		setCookie("theme", "true");
	}
}

function loadTheme(){
	validateCookie("theme");
	let theme = getCookie("theme");
	let element = document.body;
	
	if(theme == "false"){
		element.classList.toggle("dark-theme");
	}
}

function addPageToRecent(page = "collab_app:index"){
	if(page != " not found. "){
		validateCookie("recent", page);
		let recent = getCookie("recent");

		let recentPages = recent.split(",");

		if(!recentPages.includes(page)){
			setCookie("recent", recent + "," + page);
		}
		if(recentPages.length > 6){
			let recentLatest = recentPages.slice(-6, -0);
			let newCookie = recentLatest[0];
			for(let i = 1; i < 5; i++){
				newCookie = newCookie + "," + recentLatest[i];
			}
			setCookie("recent", newCookie);
		}
	}
}

function onLoad(page){
	//Scripts that run when the page loads
	loadTheme();
	if(page.includes("collab_app:")){
		addPageToRecent(page);
	}
}
