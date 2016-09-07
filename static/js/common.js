var hasClass = function(el, cls) {
	if (el.nodeName == '#text')
		return false; // ignore text nodes
	return el.className.match(new RegExp('(\\s|^)' + cls + '(\\s|$)')) ? true
			: false;
};

var addClass = function(el, cls) {
	if (!this.hasClass(el, cls))
		el.className = el.className.trim() + " " + cls;
};

var getContentItems = function(id, tag) {
	var itemEl = document.getElementById(id);
	// IE does not support the getElementsByClassName method
	// return menuEl.getElementsByClassName('menu-item');
	return itemEl.getElementsByTagName(tag);
};

var removeClass = function(el, cls) {
	if (hasClass(el, cls)) {
		var reg = new RegExp('(\\s|^)' + cls + '(\\s|$)');
		el.className = el.className.replace(reg, ' ');
	}
};

var radioClass = function(el, cls) {
	var siblingEl = el.parentNode.firstChild;
	while (siblingEl) {
		siblingEl == el ? addClass(siblingEl, cls) : removeClass(siblingEl, cls);
		siblingEl = siblingEl.nextSibling;
	}
};

var ajaxRequest = function(method, url, headers, body, success, error, scope) {
	var xhr;
	if (window.XMLHttpRequest) {
		xhr = new XMLHttpRequest();
	} else { // for IE6
		xhr = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xhr.open(method, url, true);
	for(var h in headers) {
		xhr.setRequestHeader(h, headers[h]);
	}
	xhr.onreadystatechange = function() {
		if(xhr.readyState == 4) {
			if(xhr.status >= 200 && xhr.status < 300) {
				success.call(scope, xhr.status, xhr.getAllResponseHeaders, xhr.responseText);
			} else {
				error.call(scope, xhr.status, xhr.getAllResponseHeaders, xhr.responseText);
			}
		}
	}
	xhr.send(body);
};

var escapeHtml = function(html) {
	return html.replace(/&/g, '&amp;')
			.replace(/>/g, '&gt;')
			.replace(/</g, '&lt;')
			.replace(/"/g, '&quot;');
};
