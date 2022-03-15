function setThemeCookie(cookieName, cookieValue, expiry){
	const d = new Date();
	d.setTime(d.getTime() + (expiry * 24 * 60 * 60 * 1000));
 	let expires = "expires="+d.toUTCString();
 	document.cookie = cookieName + "=" + cookieValue + ";" + expires + ";path=/";
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

function validateCookie(defaultVal = true){
	let cookie = getCookie("theme");
	if(cookie == ""){
		setThemeCookie("theme", defaultVal, 365);
	}
}

function changeTheme(){
	validateCookie();
	let theme = getCookie("theme");
	let element = document.body;

	element.classList.toggle("dark-theme");

	if(theme == "true"){
		setThemeCookie("theme", "false", 365);
	}
	else{
		setThemeCookie("theme", "true", 365);
	}
}

function loadTheme(){
	validateCookie();
	let theme = getCookie("theme");
	let element = document.body;
	
	if(theme == "false"){
		element.classList.toggle("dark-theme");
	}
}
