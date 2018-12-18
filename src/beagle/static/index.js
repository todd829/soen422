console.log("Hello world")


function send_request(message) {
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready:
            console.log(xhr.responseText);
        }
    };
    xhr.open('GET', message, true);

    xhr.send(null);    
}

document.addEventListener('keydown', function (event) {
    if (event.keyCode == 37) {
        send_request('/press/left');
    }
    else if (event.keyCode == 38) {
        send_request('/press/up');
    }
    else if (event.keyCode == 39) {
        send_request('/press/right');
    }
    else if (event.keyCode == 40) {
        send_request('/press/down');
    }
    else if (event.keyCode == 87) {
        send_request('/press/high');
    }
    else if (event.keyCode == 83) {
        send_request('/press/low');
    }
});

document.addEventListener('keyup', function (event) {
    if (event.keyCode == 37) {
        send_request('/release/left');
    }
    else if (event.keyCode == 38) {
        send_request('/release/up');
    }
    else if (event.keyCode == 39) {
        send_request('/release/right');
    }
    else if (event.keyCode == 40) {
        send_request('/release/down');
    }
    else if(event.keyCode == 87) {
        send_request('/release/high');
    }
    else if(event.keyCode == 83) {
        send_request('/release/low');
    }
});