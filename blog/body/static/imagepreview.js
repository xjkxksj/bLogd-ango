function handleFileInputChange(event) {
    const fileInput = event.target;
    const previewContainer = document.getElementById('image-preview');
    const previewImage = previewContainer.querySelector('img');
    const previewPlaceholder = previewContainer.querySelector('.image-placeholder');

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            previewImage.src = e.target.result;
            previewContainer.classList.add('has-image');
            previewPlaceholder.style.display = 'none';
        };

        reader.readAsDataURL(fileInput.files[0]);
    } else {
        previewImage.src = '';
        previewContainer.classList.remove('has-image');
        previewPlaceholder.style.display = 'block';
    }
}

const fileInput = document.getElementById('image');
fileInput.addEventListener('change', handleFileInputChange);
