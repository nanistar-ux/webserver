document.addEventListener('DOMContentLoaded', () => {
    const pdfFile = document.getElementById('pdfFile');
    const fileNameDisplay = document.getElementById('fileName');
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');
    const initialApiResponse = document.getElementById('initialApiResponse');
    
    // Show selected file name
    pdfFile.addEventListener('change', () => {
        if (pdfFile.files.length > 0) {
            fileNameDisplay.textContent = pdfFile.files[0].name;
        } else {
            fileNameDisplay.textContent = 'No file chosen';
        }
    });

    // Show spinner on form submit
    uploadForm.addEventListener('submit', () => {
        submitBtn.disabled = true;
        loading.style.display = 'inline-block';
    });
});