function generatePDF() {
    const postTitle = document.querySelector('.post-details h1').innerText;
    const postAuthor = document.querySelector('.author-info em').innerText;
    const postContent = document.querySelector('.post-content p').innerText;
    
    const content = `
        <h1>${postTitle}</h1>
        <p><strong>Posted by:</strong> ${postAuthor}</p>
        <p>${postContent}</p>
    `;

    const element = document.createElement('div');
    element.innerHTML = content;

    const opt = {
        margin:       [10, 10, 10, 10],
        filename:     'post.pdf',
        image:        { type: 'jpeg', quality: 1 },
        html2canvas:  { scale: 2 },
        jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    html2pdf().from(element).set(opt).save('post.pdf');
}

document.getElementById('pdf-button').addEventListener('click', generatePDF);
