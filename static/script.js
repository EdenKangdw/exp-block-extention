const API_BASE = '/api';

const fixedExtensionList = document.getElementById('fixed-extension-list');
const customExtensionList = document.getElementById('custom-extension-list');
const customInput = document.getElementById('custom-extension-input');
const addButton = document.getElementById('add-button');
const deleteAllButton = document.getElementById('delete-all-button');
const countDisplay = document.getElementById('count-display');

let currentCustomCount = 0;

// Fetch initial data
async function fetchData() {
    try {
        const response = await fetch(`${API_BASE}/extensions`);
        const data = await response.json();
        renderFixedExtensions(data.fixed);
        renderCustomExtensions(data.custom);
    } catch (error) {
        console.error('Error fetching data:', error);
        alert('데이터를 불러오는데 실패했습니다.');
    }
}

// Render Fixed Extensions
function renderFixedExtensions(extensions) {
    fixedExtensionList.innerHTML = '';
    extensions.forEach(ext => {
        const label = document.createElement('label');
        label.className = 'checkbox-label';

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = ext.is_checked === 1;
        input.addEventListener('change', () => toggleFixedExtension(ext.name, input.checked));

        label.appendChild(input);
        label.appendChild(document.createTextNode(ext.name));
        fixedExtensionList.appendChild(label);
    });
}

// Render Custom Extensions
function renderCustomExtensions(extensions) {
    customExtensionList.innerHTML = '';
    currentCustomCount = extensions.length;
    updateCountDisplay();

    extensions.forEach(ext => {
        const tag = document.createElement('div');
        tag.className = 'tag';

        const text = document.createElement('span');
        text.textContent = ext.name;

        const closeBtn = document.createElement('span');
        closeBtn.className = 'close-btn';
        closeBtn.textContent = '✕';
        closeBtn.addEventListener('click', () => deleteCustomExtension(ext.name));

        tag.appendChild(text);
        tag.appendChild(closeBtn);
        customExtensionList.appendChild(tag);
    });
}

function updateCountDisplay() {
    countDisplay.textContent = `${currentCustomCount}/200`;
}

// API Actions
async function toggleFixedExtension(name, isChecked) {
    try {
        const response = await fetch(`${API_BASE}/fixed-extensions/${name}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_checked: isChecked })
        });
        if (!response.ok) throw new Error('Failed to update');
    } catch (error) {
        console.error('Error updating fixed extension:', error);
        alert('설정 저장에 실패했습니다.');
        fetchData(); // Revert UI on error
    }
}

async function addCustomExtension() {
    const name = customInput.value.trim();
    if (!name) return;

    if (name.length > 20) {
        alert('확장자 이름은 20자 이내여야 합니다.');
        return;
    }

    if (!/^[a-zA-Z0-9]+$/.test(name)) {
        alert('확장자는 영문과 숫자만 입력 가능합니다.');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/custom-extensions`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to add');
        }

        customInput.value = '';
        fetchData(); // Refresh list
    } catch (error) {
        alert(error.message);
    }
}

async function deleteCustomExtension(name) {
    if (!confirm(`'${name}' 확장자를 삭제하시겠습니까?`)) return;

    try {
        const response = await fetch(`${API_BASE}/custom-extensions/${name}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete');

        fetchData(); // Refresh list
    } catch (error) {
        alert('삭제에 실패했습니다.');
    }
}

async function deleteAllCustomExtensions() {
    if (currentCustomCount === 0) return;
    if (!confirm('모든 커스텀 확장자를 삭제하시겠습니까?')) return;

    try {
        const response = await fetch(`${API_BASE}/custom-extensions`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete all');

        fetchData(); // Refresh list
    } catch (error) {
        alert('전체 삭제에 실패했습니다.');
    }
}

// Event Listeners
addButton.addEventListener('click', addCustomExtension);
deleteAllButton.addEventListener('click', deleteAllCustomExtensions);
customInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addCustomExtension();
});
customInput.addEventListener('input', (e) => {
    // Optional: Remove invalid characters in real-time or just let the validation handle it on submit.
    // Requirement says "only English and numbers", so blocking input is a good UX.
    e.target.value = e.target.value.replace(/[^a-zA-Z0-9]/g, '');
});

// Initialize
fetchData();
