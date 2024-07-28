document.addEventListener('DOMContentLoaded', () => {
    let allSubcategories = [];
    let currentCategory = 'home';
    let userCategories = {};

    fetch('/data')
        .then(response => response.json())
        .then(data => {
            initializeDashboard(data.categories);
            if (data.user_data) {
                userCategories = data.user_data;
                populateUserCategories(userCategories);
            }
        });

    function initializeDashboard(categories) {
        const categoryGroups = document.getElementById('category-groups');
        const subcategoryContainer = document.getElementById('subcategories');

        const categoriesList = [
            { name: 'Home', id: 'home' },
            { name: 'Uncategorized', id: 'uncategorized' }
        ];

        categoriesList.forEach(cat => {
            const li = document.createElement('li');
            li.textContent = cat.name;
            li.addEventListener('click', () => showSubcategories(cat.id));
            li.setAttribute('data-category', cat.id);
            categoryGroups.appendChild(li);
        });

        Object.keys(categories).forEach(category => {
            const li = document.createElement('li');
            li.textContent = category;
            li.addEventListener('click', () => showSubcategories(category));
            li.setAttribute('data-category', category);
            categoryGroups.appendChild(li);
        });

        allSubcategories = Object.values(categories).flat();
        showSubcategories('home');

        categoryGroups.addEventListener('dragover', dragOver);
        categoryGroups.addEventListener('drop', drop);

        document.getElementById('submit-button').addEventListener('click', submitData);
    }

    function showSubcategories(category) {
        currentCategory = category;
        const subcategoryContainer = document.getElementById('subcategories');
        subcategoryContainer.innerHTML = '';

        let subcategoriesToShow = [];
        if (category === 'home') {
            subcategoriesToShow = allSubcategories.filter(sub => !Object.values(userCategories).flat().includes(sub));
        } else {
            subcategoriesToShow = userCategories[category] || [];
        }

        subcategoriesToShow.forEach(subcategory => {
            const div = document.createElement('div');
            div.textContent = subcategory;
            div.classList.add('subcategory');
            div.setAttribute('draggable', true);
            div.addEventListener('dragstart', dragStart);
            div.addEventListener('dragend', dragEnd);
            subcategoryContainer.appendChild(div);
        });

        const categoryItems = document.querySelectorAll('#category-groups li');
        categoryItems.forEach(item => {
            if (item.getAttribute('data-category') === category) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
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

            if (!userCategories[category]) {
                userCategories[category] = [];
            }
            userCategories[category].push(subcategoryText);

            for (const cat in userCategories) {
                if (cat !== category) {
                    userCategories[cat] = userCategories[cat].filter(sub => sub !== subcategoryText);
                }
            }

            showSubcategories(currentCategory);

            draggedItem = null;
        }
    }

    function submitData() {
        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userCategories),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Data submitted successfully!');
            } else {
                alert('Failed to submit data.');
            }
        });
    }

    function populateUserCategories(userCategories) {
        Object.keys(userCategories).forEach(category => {
            if (category !== 'home' && category !== 'uncategorized') {
                const categoryElement = document.querySelector(`li[data-category="${category}"]`);
                if (categoryElement) {
                    categoryElement.classList.add('has-items');
                }
            }
        });
    }
});
