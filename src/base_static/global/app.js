document.addEventListener("DOMContentLoaded", function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie("csrftoken");

    const textareas = document.querySelectorAll('textarea[data-type="ckeditor"]');

    textareas.forEach((textarea) => {
        if (textarea.dataset.ckeInitialized === "1") return;

        ClassicEditor
            .create(textarea, {
                simpleUpload: {
                    uploadUrl: "/ckeditor/upload/",
                    headers: { "X-CSRFToken": csrftoken }
                    }   
            })
            .then(editor => {
                textarea.dataset.ckeInitialized = "1";
                textarea._ckEditorInstance = editor;
                console.log("CKEditor inicializado:", textarea.id);
            })
            .catch(err => {
                console.error("Erro ao inicializar CKEditor:", err);
            });
    });
});