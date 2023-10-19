const clockSpeed = 60 * 1000;

document.addEventListener('DOMContentLoaded', function () {
    const needs = document.querySelectorAll('.need-card');

    navLinksConfig();
    addNeedConfig();
    addActionConfig();

    needs.forEach(need => {
        setNeedColor(need);
        deleteNeedConfig(need);
    });

    setInterval(() => {
        needs.forEach(need => incrementNeedLevel(need))
    }, clockSpeed);
})

function incrementNeedLevel(need) {
    const maxLevel = need.dataset.maxLevel;
    const currentLevelPercent = need.dataset.currentLevel / 100;
    let updatedLevel;

    if (need.dataset.negativeNeed === 'True') {
        updatedLevel = Math.min((((maxLevel * currentLevelPercent) + 1) / maxLevel) * 100, 100);
    } else {
        updatedLevel = Math.max((((maxLevel * currentLevelPercent) - 1) / maxLevel) * 100, 0);
    }

    need.dataset.currentLevel = updatedLevel;
    need.querySelector('.progress').ariaValueNow = updatedLevel;
    need.querySelector('.progress-bar').style.width = `${updatedLevel}%`

    setNeedColor(need);
}

function setNeedColor(need) {
    const levelVal = need.dataset.currentLevel;
    let levelBarColor, levelBarBgColor;

    switch (true) {
        case (levelVal < 25):
            levelBarColor = 'Red';
            levelBarBgColor = 'DarkRed';
            break;
        case (levelVal < 50):
            levelBarColor = 'Orange';
            levelBarBgColor = 'DarkOrange';
            break;
        case (levelVal < 75):
            levelBarColor = 'Yellow';
            levelBarBgColor = 'Gold';
            break;
        default:
            levelBarColor = 'LimeGreen';
            levelBarBgColor = 'Green';
    }

    need.querySelector('.progress-bar').style.backgroundColor = levelBarColor;
    need.querySelector('.progress').style.backgroundColor = levelBarBgColor;
}

function navLinksConfig() {
    const addNeedLink = document.querySelector('#add-need-link');
    const deleteNeedLink = document.querySelector('#delete-need-link');
    const addActionLink = document.querySelector('#add-action-link');
    const addNeedForm = document.querySelector('#add-need-form');
    const addActionForm = document.querySelector('#add-action-form')
    const deleteNeedButtons = document.querySelectorAll('.delete-need-btn');

    addNeedLink.addEventListener('click', () => {
        addNeedForm.style.display = 'block';
        addActionForm.style.display = 'none';
    })

    addActionLink.addEventListener('click', () => {
        addActionForm.style.display = 'block';
        addNeedForm.style.display = 'none';
    })

    deleteNeedLink.addEventListener('click', () => {
        deleteNeedButtons.forEach(button => {
            button.style.display = 'block';
        })
    })
}

function addNeedConfig() {
    const normalNeedButton = document.querySelector('#normal-need-btn');
    const negativeNeedButton = document.querySelector('#negative-need-btn');
    const cancelAddNeedButton = document.querySelector('#cancel-add-need-btn');

    const addNeedForm = document.querySelector('#add-need-form');
    const normalNeedText = document.querySelector('#normal-need-text');
    const negativeNeedText = document.querySelector('#negative-need-text');
    const normalDecayText = document.querySelector('#normal-decay-text');
    const negativeDecayText = document.querySelector('#negative-decay-text');

    normalNeedButton.addEventListener('click', () => {
        negativeNeedText.style.display = 'none';
        negativeDecayText.style.display = 'none';
        normalNeedText.style.display = 'block';
        normalDecayText.style.display = 'block';
    })

    negativeNeedButton.addEventListener('click', () => {
        normalNeedText.style.display = 'none';
        normalDecayText.style.display = 'none';
        negativeNeedText.style.display = 'block';
        negativeDecayText.style.display = 'block';
    })

    cancelAddNeedButton.addEventListener('click', () => {
        addNeedForm.style.display = 'none';
    })
}

function addActionConfig() {
    const cancelAddActionButton = document.querySelector('#cancel-add-action-btn');
    const addActionDropdownLinks = document.querySelectorAll('.add-action-dropdown');
    const relatedNeedSelect = document.querySelector('#related-need-select');

    const addActionForm = document.querySelector('#add-action-form');

    cancelAddActionButton.addEventListener('click', () => {
        addActionForm.style.display = 'none';
    })

    addActionDropdownLinks.forEach(link => {
        link.addEventListener('click', () => {
            addActionForm.style.display = 'block';
            relatedNeedSelect.value = link.dataset.needId;
        })
    })
}

function deleteNeedConfig(need) {
    const deleteNeedButton = need.querySelector('.delete-need-btn');
    const needId = need.dataset.id;

    deleteNeedButton.addEventListener('click', () => {
        if (confirm('Are you sure you want to delete this need?')) {
            fetch(`/delete-need/${needId}/`, {
                method: 'POST',
            })
                .then(response => {
                    if (response.ok) {
                        need.remove();
                        hideDeleteButtons();
                    } else {
                        console.error('Error deleting need');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    })
}

function hideDeleteButtons() {
    const deleteNeedButtons = document.querySelectorAll('.delete-need-btn');

    deleteNeedButtons.forEach(button => {
        button.style.display = 'none';
    })
}