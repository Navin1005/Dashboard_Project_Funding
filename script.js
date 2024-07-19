// script.js

document.addEventListener('DOMContentLoaded', () => {
    fetch('categories.json')
        .then(response => response.json())
        .then(data => initializeDashboard(data));

    function initializeDashboard(data) {
        const categoryGroups = document.getElementById('category-groups');
        const subcategoryContainer = document.getElementById('subcategories');

        Object.keys(data).forEach(category => {
            const li = document.createElement('li');
            li.textContent = category;
            li.addEventListener('click', () => showSubcategories(category, data[category]));
            li.setAttribute('data-category', category);
            categoryGroups.appendChild(li);
        });

        Object.values(data).flat().forEach(subcategory => {
            const div = document.createElement('div');
            div.textContent = subcategory;
            div.classList.add('subcategory');
            div.setAttribute('draggable', true);
            div.addEventListener('dragstart', dragStart);
            div.addEventListener('dragend', dragEnd);
            subcategoryContainer.appendChild(div);
        });

        categoryGroups.addEventListener('dragover', dragOver);
        categoryGroups.addEventListener('drop', drop);
    }

    let draggedItem = null;

    function dragStart(e) {
        draggedItem = e.target;
        setTimeout(() => {
            e.target.style.display = 'none';
        }, 0);
    }

    function dragEnd(e) {
        setTimeout(() => {
            if (draggedItem) {
                draggedItem.style.display = 'block';
                draggedItem = null;
            }
        }, 0);
    }

    function dragOver(e) {
        e.preventDefault();
    }

    function drop(e) {
        e.preventDefault();
        if (draggedItem && e.target.tagName === 'LI') {
            const category = e.target.getAttribute('data-category');
            const subcategoryText = draggedItem.textContent;
            draggedItem.remove();

            // Update JSON data structure (optional)
            if (data[category]) {
                data[category].push(subcategoryText);
            } else {
                data[category] = [subcategoryText];
            }

            // Optionally show updated subcategories
            showSubcategories(category, data[category]);

            draggedItem = null;
        }
    }

    function showSubcategories(category, subcategories) {
        const subcategoryContainer = document.getElementById('subcategories');
        subcategoryContainer.innerHTML = '';
        subcategories.forEach(sub => {
            const div = document.createElement('div');
            div.textContent = sub;
            div.classList.add('subcategory');
            subcategoryContainer.appendChild(div);
        });
    }
});
