document.addEventListener("DOMContentLoaded", function () {
    const editors = document.querySelectorAll('textarea[data-type="ckeditor"]');
    editors.forEach((textarea) => {
        ClassicEditor
            .create(textarea, {
                ckfinder: {
                    uploadUrl: '/ckeditor5/upload/'
                }
            })
            .catch(error => {
                console.error('Erro ao inicializar o CKEditor:', error);
            });
    });
});
