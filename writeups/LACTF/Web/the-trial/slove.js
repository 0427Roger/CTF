fetch("/getflag", {
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    body: "word=flag"
})
.then(r => r.text())
.then(console.log);