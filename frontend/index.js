document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("button");
    const input = document.getElementById("input");
    const textarea = document.getElementById("textarea");

    const editor = CodeMirror.fromTextArea(textarea, {
        mode: "text/x-c++src",
        readOnly: true,
        lineNumbers: true,
    });

    button.addEventListener("click", function () {

        let url = "http://127.0.0.1:5000/" + encodeURIComponent(input.value);
        let xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.responseType = 'json';
        xhr.onload = function () {
            console.log(xhr);
            if (xhr.status == 200) {
                editor.getDoc().setValue(xhr.response['data']);
            } else {
                editor.getDoc().setValue(xhr.response == null ? xhr.status.toString() + " Something Wrong" : xhr.response['error']);
            }
        };
        xhr.send();
    });
});
