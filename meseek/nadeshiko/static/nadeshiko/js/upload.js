var form = document.getElementById("form1")
var loading = document.getElementById("loading")
var content = document.getElementById("upload_scan")

form.addEventListener('submit', function (e) {
    content.style.display = 'none';
    loading.style.display = 'block';
});
     
