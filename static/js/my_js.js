var timeleft = 10;
var downloadTimer = setInterval(function () {
    if (timeleft <= 0) {
        clearInterval(downloadTimer);
        document.getElementById("countdown").innerHTML = "One Time Password is expired";
    } else {
        document.getElementById("countdown").innerHTML = timeleft + " seconds remaining";
    }
    timeleft -= 1;
}, 1000);
